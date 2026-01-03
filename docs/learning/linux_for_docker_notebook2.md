# Kiến trúc Container Linux và tối ưu hoá Docker Image

Báo cáo này bao quát toàn diện hai trụ cột chính của việc build docker image ở cấp độ trung cấp (intermediate):
**Linux Networking & Security** và **Package Management & Software Installation.** Chúng ta sẽ phân tích cách các
namespaces mạng hoạt động, luồng đi của gói tin qua `iptables`, sự khác biệt tinh tế giữa `glibc` và `musl` trong phân giải DNS,
và chiến lược quản lý gói tin tối ưu cho các hệ sinh thái Debian và RedHat, cũng như lý giải kỹ thuật tại sao Snap và Flatpak lại thất bại trong môi trường Docker. 

# Phần I: Linux Networking và Bảo mật trong Container

Để làm chủ mạng Docker, người kỹ sư phải ngừng coi Docker là một "hộp đen" mạng và bắt đầu nhìn nhận nó như một trình điều phối (orchestrator) các tính năng mạng tiêu chuẩn 
của Linux Kernel. Docker không tạo ra ngăn xếp mạng mới; nó tận dụng Linux namespaces (`netns`), cặp ethernet ảo (`veth`), cầu nối (`bridge`), và khung lọc gói tin Netfilter (`iptables`)
để tạo ra sự cô lập và định tuyến. 

## 1.1. Network Namespace: Đơn vị nguyên tử của sự cô lập

Tại trái tim của mạng container là Linux Namespace. Một namespace là một bản sao của ngăn xếp mạng hệ thống - bao gồm các giao diện mạng (interfaces), bảng định tuyến (routing tables),
quy tắc tường lửa và sockets - được cô lập hoàn toàn với các namespace khác với máy chủ (host). 

### 1.1.1. Cơ chế của `CLONE_NEWNET` và sự hình thành "Mạng ảo"

Khi Docker Deamon khởi tạo một container, nó thực hiện lời gọi hệ thống (system call) `clone()` với cờ `CLONE_NEWNET`. 
Hành động này yêu cầu hạt nhân Linux tạo ra một không gian mạng hoàn toàn mới, nguyên sơ cho tiến trình con. Khác với máy ảo (VM)
vốn ảo hoá phần cứng mạng (như card mạng ảo PCI), container chia sẻ kernel của máy chủ nhưng nhìn thấy một tập hợp các giao diện mạng
hoàn toàn khác biệt. Trong namespace mới này, ban đầu chỉ tồn tại giao diện loopback (`lo`), và nó hoàn toàn bị ngắt kết nối với thế giới
bên ngoài cho đến khi Docker can thiệp để thiết lập hệ thống dây cáp ảo. 

Một điểm quan trọng trong tư duy là hiểu cách truy cập và gỡ lỗi các namespace này. Theo mặc định, Docker không hiển thị các namespace này trong
đường dẫn chuẩn của Linux (`/var/run/netns`), khiến lệnh `ip netns list` của người dùng thường trả về rỗng. Docker ẩn chúng đi để quản lý nội bộ. 
Tuy nhiên, một kiến trúc sư hệ thống cần biết rằng mọi namespace đều gắn liền với tiến trình ID (PID). Thông tin về namespace của một container có thể
tìm thấy tại `/proc/<PID>/ns/net`. Bằng cách tạo một liên kết mềm (symlink) từ đường dẫn này sang `/var/run/netns`, quản trị viên có thể sử dụng các công cụ
mạng tiêu chuẩn của Linux như `ip netns` để thao tác trực tiếp trên ngăn xếp mạng của container mà không cần phải "chui vào" container đó.


## 1.1.2. Cặp Veth (Veth Pair): Cặp mạng ảo xuyên không gian

Sau khi namespace được tạo ra, nó giống như một hòn đảo cô lập. Để kết nối hòn đoả này với đất liền (máy chủ host), Linux sử dụng khái niệm `Veth Pair` (Virtual Ethernet Pair). 
Hãy hình dung đây là một sọi cáp mạng ảo với hai đầu nối. 

* **Đầu A (Container End):** Được đưa vào bên trong namespace của container. Để đảm bảo sự nhất quán cho các ứng dụng, Docker thường đổi tên giao diện này thành `eth0` bên trong container. e

* **Đầu B (Host End):** Nằm tại namespace gốc (root namespace) của máy chủ. Nó thường có tên ngẫu nhiên như `veth3b14a2` hoặc gắn với ID của container. 

Sự hiểu biết này giải thích hiện tượng khi chạy lệnh `ip link` hoặc `ifconfig` trên máy chủ Docker, ta thấy hàng loạt giao diện `veth...` xuất hiện. 
Đây chỉnh là các đầu nối vật lý (ảo) tương ứng với từng container đang chạy. Mọi gói tin đi vào `eth0` của container sẽ ngay lập tức xuất hiện tại đầu `veth` tương ứng trên máy chủ và ngược lại. 

## 1.2. Chiến lược gỡ lỗi

Một trong những thói quen khó bỏ nhất của người quản trị hệ thống khi chuyển từ VM sang Docker là việc cài đặt `openssh-server` vào bên trong container để phục vụ việc gỡ lỗi hoặc quản trị. Đây là một mô hình sai lầm (anti-pattern) nghiêm trọng.

### 1.2.1. Tại sao SSH trong Docker là một ý tưởng tồi? 

Việc cài đặt SSH vi phạm nguyên tắc "Mỗi container một tiến trình" (One Process Per Container). Container được thiết kế để vòng đời của nó gắn liền với ứng dụng chính (PID 1).
Nếu cài đặt SSH, bạn buộc phải sử dụng một trình quản lý tiến trình (như Supervisord hoặc s6-overlay) để chạy song song cả ứng dụng và SSH daemon. Điều này làm phức tạp hoá việc quản lý log (log của ai xuất ra stdout?),
xử lý tín hiệu (SIGTERM sẽ tắt ai trước?), và tăng bề mặt tấn công bảo mật khi phải quản lý key và mật khẩu SSH trong môi trường container động. Hơn nữa, việc duy trì một server SSH tiêu tốn tài nguyên không cần thiết, 
đi ngược lại triết lý tối gian của container. 


### 1.2.2. Giải pháp kiến trúc: `nsenter` và Debugging từ Host

Thay vì cài đặt công cụ vào container (làm phình to kích thước image và rủi ro bảo mật), phương pháp tận dụng kiến trúc namespace của Linux. 
Công cụ `nsenter` (Namespace Enter) cho phép một tiến trình từ máy chủ "nhập" vào namespace của một tiến trình khác. 

Quy trình gỡ lỗi mạng chuyên nghiệp diễn ra như sau:
1. **Xác định PID:** Tìm PID của tiến trình container trên máy chủ host: `PID=$(docker.inspect -f '{{.State.Pid}}' <container_id>)`.
2. **Xâm nhập Namespace:** Sử dụng `nsenter` để chạy các công cụ gỡ lỗi có sẵn trên máy chủ (như `ping`, `curl`, `tcpdump`, `ip`) nhưng trong bối cảnh mạng của container. 

```bash
sudo nsenter -t $PID -n ip addr show
sudo nsenter -t $PID -n curl -v http://google.com
```

Lệnh trên hướng dẫn kernel chuyển ngữ cảnh mạng sang namespace của PID đích (`-n`) nhưng vẫn sử dụng nhị phân `curl` nằm trên máy chủ. Điều này cho phép chúng ta gỡ lỗi ngay cả những container siêu nhỏ (như Distroless hoặc Scratch) vốn không hề có shell hay công cụ mạng nào bên trong. 
Đây là minh chứng rõ ràng nhất cho việc hiểu sâu về cơ chế Linux giúp giải quyết vấn đề một cách thanh lịch và an toàn hơn. 

## 1.3. Cơ chế định tuyến IP và cầu nối (Bridge)

Chế độ mạng mặc định của Docker là `bridge`. Hiểu rõ đường đi của gói tin qua cầu nối là chìa khoá để xử lý các sự cố kết nối. 

### 1.3.1. Cầu nối `docker0`: Switch ảo Layer 2

Khi Docker Service khởi chạy, nó tạo ra một cầu nối ảo tên là `docker0`. Về mặt kỹ thuật, `docker0` hoạt động như một switch Layer 2. Tất cả các giao diện `veth` từ các container được cắm vào `switch` này. 

* **Giao tiếp nội bộ (East-West Traffic):** Khi Container A (172.17.0.2) muốn gửi tin đến Container B (172.17.0.3), gói tin đi từ `eth0` của A, qua cặp veth đến `docker0`. Tại đây, cầu nối `docker0` tra cứu
bảng MAC (ARP table) và chuyển tiếp khung tin (frame) đến nhánh veth của B, và cuối cùng đến `eth0` của B. Toàn bộ quá trình này diễn ra trong kernel, không đi ra ngoài giao diện vật lý máy chủ.

### 1.3.2. Giao tiếp ra ngoài (North-South Traffic) và IP Masquerading

Khi container cần truy cập internet (ví dụ: tải gói tin từ `8.8.8.8`), gói tin sẽ đi đến `docker0`. Vì địa chỉ đích không nằm trong mạng cục bộ của bridge, gói tin được chuyển lên ngăn xếp IP của máy chủ để định tuyến.
Máy chủ thấy đích đến là Internet nên đẩy gói tin ra giao diện vật lý `eth0` (hoặc `wlan0`). 

Tuy nhiên, địa chỉ IP nguồn của gói tin là `172.17.0.2` (IP private của container). Nếu gói tin này đi ra Internet, các server của Google sẽ không thể phản hồi vì `172.17.0.2` là địa chỉ không định tuyến được trên Internet. 
Để giải quyết vấn đề này, Docker sử dụng kỹ thuật **IP Masquerading** (một dạng của Source NAT - SNAT) thông quan `iptables`. 

Cụ thể, Docker thêm một quy tắc vào bảng `nat` trong chuỗi `POSTROUTING`:

```bash
-A POSTROUTING -s 172.17.0.0/16! -o docker0 -j MASQUERADE
```

Quy tắc này có nghĩa là: "Nếu gói tin xuất phát từ subnet của Docker và không đi ngược lại vào bridge" (tức là đang đi ra ngoài thế giới), hãy thay thế địa chỉ IP nguồn bằng địa chỉ IP chính của máy chủ. Nhờ đó, thế giới 
bên ngoài chỉ nhìn thấy giao tiếp đến từ máy chủ host, và kernel Linux sẽ tự động theo dõi kết nối (connection tracking) để chuyển gói tin phản hồi về đúng container ban đầu. Nếu người dùng vô tình tắt tính năng masquerade hoặc
can thiệp sai vào iptables, container sẽ mất khả năng truy cập internet, một lỗi phổ biến của người mới. 

## 1.4. Phân giải DNS: `glibc` và `musl` và bẫy `ndots`

Một trong những chủ đề phức tạp và thường gây lỗi nhất trong container là DNS. 
Docker xử lý DNS khác nhau tuỳ thuộc vào loại mạng và bản phân phối Linux cơ sở (Base Image). 


### 1.4.1. Cơ chế `resolv.conf` động

Trong một máy chủ Linux thông thường, `/etc/resolv.conf` là file tĩnh hoặc được quản lý bởi systemd.
Trong Docker, file này được quản lý động. 

* **Default Bridge:** Docker sao chép `/etc/resolv.conf` từ máy chủ vào container. Tuy nhiên, nếu máy chủ
sử dụng local resolver (như `127.0.0.53` của Ubuntu), Docker sẽ tự động lọc bỏ vì container không thể truy cập loopback của máy chủ, 
thay vào đó nó sử dụng Google DNS (8.8.8.8) làm fallback. 

* **User-Defined Network:** Đây là mô hình "Best Practice". Khi sử dụng mạng tuỳ chỉnh (ví dụ qua Docker Compose), Docker gắn kết một file
`resolv.conf` trỏ tới `127.0.0.11`. Đây là **Embedded DNS Server** của Docker. Server DNS nhúng này có khả năng "Service Discovery" - nó có thể phân giải
tên container thành IP nội bộ. Các yêu cầu tên miền ngoại mạng (như `google.com`) sẽ được proxy ra DNS của máy chủ. 

### 1.4.2. Vấn đề `ndots:5` và Hiệu năng

Mặc định, cấu hình DNS trong container (đặc biệt là Kubernetes hoặc một số Docker setup) thường có tuỳ chọn `options ndots:5`. 
Điều này có nghĩa là nếu ứng dụng phân giải một tên miền không có dấu chấm ở cuối (như `google.com`), trình phân giải (resolver)
sẽ cố gắng thêm các hậu tố tìm kiếm (search domains) trước. Ví dụ: nó sẽ thử `google.com.default.svc.cluster.local`, `google.com.svc.cluster.local`...trước khi thử `google.com`.
Điều này tạo ra một lượng lớn lưu lượng DNS rác và làm chậm ứng dụng. Best Practices là luôn sử dụng tên miền đầy đủ (FQDN) có dấu chấm ở cuối trong cấu hình ứng dụng critical để bỏ
qua quy trình tìm kiếm thừa thãi này. 

### 1.4.3. Cuộc chiến `glibc` và `musl`

Sự lựa chọn Base Image (Debian vs Alpine) ảnh hưởng trực tiếp đến hành vi DNS:
* **Debian/RedHat (glibc):** Sử dụng thư viện `glibc` với trình phân giải DNS tuần tự, hỗ trợ tốt TCP fallback và các plugin NSS. Hành vi của nó giống với hầu hết các máy chủ Linux tiêu chuẩn. 
* **Alpine (musl):** Sử dụng thư viện `musl libc`. Trình phân giải của `musl` hoạt động song song (gửi truy vấn A và AAAA cùng lúc) và không hỗ trợ đầy đủ EDNS0 trong các phiên bản cũ. 
Trong một số môi trường mạng có firewall cũ hoặc cấu hình VPN phức tạp, các gói tin UDP gửi song song có thể bị drop, dẫn đến lỗi phân giải DNS chập chờn (intermittent failures). 
**Insight:** Nếu ứng dụng của bạn gặp lỗi DNS "Unknown Host" ngẫu nhiên trên Alpine, thay vì cố gắng "patch" Alpine (Think Harder), hãy chuyển sang Debian-slim (Think Smarter) để tận dụng sự ổn định của `glibc`.   

  
## 1.5. Tường lửa: Xung đột UFW và `iptables`

Một lỗ hổng bảo mật phổ biến mà người quản trị Docker trung cấp hay mắc phải là tin tưởng tuyệt đối vào UFW (Uncomplicated Firewall) trên Ubuntu khi chạy Docker.

### 1.5.1. Cơ chế "vượt rào" của Docker

Người quản trị thường cấu hình UFW để `deny all incoming` và chỉ mở cổng 22 (SSH). Sau đó, họ chạy một container với `-p 8080:80`. 
Họ kỳ vọng UFW sẽ chặn cổng 8080 vì chưa cho phép. Tuy nhiên, thực tế cổng 8080 vẫn mở toang cho cả thế giới.


Nguyên nhân nằm ở thứ tự xử lý gói tin trong kernel. Để thực hiện Port Forwarding, Docker chèn các quy tắc vào bảng `nat` chuỗi `PREROUTING`. 
Trong sơ đồ luồng dữ liệu của Netfilter, `NAT PREROUTING` diễn ra trước bảng `filter` chuỗi `INPUT` (nơi UFW thường đặt quy tắc chặn). 
Do đó, gói tin đi vào cổng 8080 được Docker "bắt" và chuyển hướng (DNAT) thẳng vào địa chỉ IP của container trước khi UFW kịp nhìn thấy nó để chặn.   


### 1.5.2. Giải pháp `DOCKER-USER`: Quyền lực tối thượng

Để khắc phục điều này mà không phá vỡ chức năng của Docker, ta không nên tắt tính năng iptables của Docker (`--iptables=false` là một giải pháp tồi vì nó làm hỏng NAT). 
Thay vào đó, Docker cung cấp một chuỗi đặc biệt tên là `DOCKER-USER`. Docker cam kết rằng các quy tắc trong chuỗi này sẽ luôn được đánh giá trước các quy tắc của chính Docker.

Cấu hình bảo mật để giới hạn truy cập vào container:

```Bash
# Cho phép các kết nối đã thiết lập (để traffic trả về hoạt động)
iptables -I DOCKER-USER -m state --state RELATED,ESTABLISHED -j ACCEPT
# Cho phép truy cập từ mạng nội bộ (ví dụ VPN)
iptables -I DOCKER-USER -s 10.0.0.0/8 -j ACCEPT
# Chặn tất cả truy cập khác từ giao diện ngoài vào container
iptables -I DOCKER-USER -i eth0 -j DROP
```

Việc sử dụng `DOCKER-USER` cho phép bạn kiểm soát mịn màng (granular control) ai được phép nói chuyện với container mà không cần can thiệp vào logic NAT phức tạp của Docker.

## Phần II. Quản lý gói tin & cài đặt phần mềm nâng cao

Xây dựng Docker Image khác xa với việc quản trị một máy chủ truyền thống. Trên máy chủ, bạn cài đặt phần mềm
để tồn tại lâu dài và cập nhật liên tục. Trong Docker, tính bất biến (immutability) và cơ chế layer (lớp) đòi
hỏi một chiến lược quản lý gói tin hoàn toàn khác. 

## 2.1. Cơ chế Copy-on-Write (CoW) và nghệ thuật tối ưu Layer

Hệ thống tệp của Docker được xây dựng dựa trên UnionFS (như OverlayFS). Một chỉ thị trong Dockerfile (`RUN`, `COPY`) tạo ra một lớp mới chỉ đọc (read-only layer).
Khi bạn sửa đổi một tệp ở lớp trên, Docker thực hiện chiến lược "Copy-on-Write": nó sao chép tệp từ dưới lên lớp hiện tại để chỉnh sửa. 

Hệ quả của kiến trúc này là **dữ liệu không bao giờ thực sự bị xoá.** Nếu bạn cài đặt một gói 100MB ở lớp 1, và xoá nó ở lớp 2, kích thước cuối cùng của image vẫn bao gồm 100MB đó
(nó chỉ bị ẩn đi đối vứoi người dùng cuối). **Nguyên tắc vàng:** Cài đặt, cấu hình, và dọn dẹp phải diễn ra trong **cùng một lớp** (cùng một lệnh `RUN`). Việc tách chúng ra nhiều dòng
lệnh `RUN` là sai lầm cơ bản dẫn đến image phình to. 

## 2.2. Hệ sinh thái Debian/Ubuntu (APT)

Debian và Ubuntu là nền tảng phổ biến nhất cho Docker Image. `apt` mạnh mẽ nhưng mặc định rất "hao" dung lượng. 

### 2.2.1. Bẫy `apt-get update` và Caching

Một lỗi phổ biến là viết:

```Dockerfile
RUN apt-get update
RUN apt-get install -y python3
```

Điều này nguy hiểm vì Docker cache các lớp riêng biệt. Nếu bạn sửa dòng dưới thành `install -y python3 python3-pip`. Docker có thể tái sử dụng lớp `apt-get udpate` cũ (đã được cache từ tuần trước). 
Kết quả là `apt-get install` sẽ cố tải các phiên bản gói tin cũ từ danh sách cache, nhưng các phiên bản này có thể đã bị xoá khỏi mirror repository, dẫn đến lỗi build (404 Not Found). **Giải pháp:** 
Luôn kết hợp update và install trong một câu lệnh: `RUN apt-get update & apt-get install...`.


### 2.2.2. Tối ưu hoá dung lượng với APT

Để giảm kích thước image Debian/Ubuntu:
1. `--no-install-recommends`: Mặc định, APT cài đặt các gói "recommended" (được đề xuất). Trong môi trường server/container, các gói này thường là tài liệu, công cụ hỗ trợ giao diện, hoặc thư viện không
thiết yếu. Sử dụng cờ này để loại bỏ chúng. 

2. **Dọn dẹp danh sách gói (`lists`):** Lệnh `apt-get update` tải về danh sách gói tin (metadata) vào `/var/lib/apt/lists/`. Dữ liệu này có thể lên tới 30-50 MB. Sau khi cài đặt xong, chúng trở nên vô dụng runtime image. Hãy xoá chúng ngay lập tức. 
Lưu ý: `apt-get clean` chỉ xoá cache của file `.deb` đã tải (trong `/var/cache/apt/archives`), nó không xoá danh sách metadata. Bạn phải `rm -rf /var/lib/apt/lists/*` thủ công. 

**Mẫu Dockerfile chuẩn cho Debian:**

```Dockerfile
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*
```


## 2.3. Hệ sinh thái RedHat (RPM/DNF/Microdnf)

Trong môi trường doanh nghiệp (Enterprise), Red Hat Enterprise Linux (RHEL) và các bản sao (AlmaLinux, Rocky Linux) là tiêu chuẩn.

### 2.3.1. Universal Base Image (UBI)

Red Hat cung cấp UBI để giải quyết vấn đề phân phối. Image UBI cho phép bạn xây dựng ứng dụng trên nền tảng RHEL và phân phối tự do mà không cần subscription cho người dùng cuối (trừ khi họ muốn hỗ trợ).

* **UBI Standard:** Đầy đủ công cụ, dùng `dnf`.

* **UBI Minimal:** : Phiên bản rút gọn tối đa, sử dụng `microdnf`. `microdnf` là phiên bản viết lại bằng C của DNF, không phụ thuộc vào Python, giúp giảm kích thước image đáng kể.

### 2.3.2. Tối ưu hoá DNF

Tương tự APT, DNF/YUM cũng cần tối ưu:

* `--nodocs`: Đây là cờ quan trọng nhất. Gói RPM thường kèm theo tài liệu hướng dẫn (man pages, html) rất lớn. Cờ này loại bỏ chúng ngay từ khi cài đặt.   

* `clean all`: Xoá toàn bộ metadata và cache. 

Mẫu Dockerfile chuẩn cho UBI Minimal: 

```bash
FROM registry.access.redhat.com/ubi9/ubi-minimal
RUN microdnf install -y --nodocs \
    python3 \
    && microdnf clean all
```

## 2.4. Snap và Flatpak: Sự khập khiễng trong kiến trúc container

Một câu hỏi thường gặp ở mức intermediate: "Tại sao tôi không thể dùng Snap hay Flatpak trong Docker để cài ứng dụng cho tiện?" Câu trả lời nằm sâu trong kiến trúc hệ điều hành.

### 2.4.1. Sự phụ thuộc vào Systemd và PID 1

Snap (`snapd`) được thiết kế dựa trên giả định rằng nó đang chạy trên một hệ điều hành đầy đủ, nơi `systemd` là tiến trình khởi tạo (PID 1). Snap dựa vào `systemd` để quản lý các unit file, mount point và các dịch vụ nền. 
Trong Docker container, PID 1 thường là ứng dụng của bạn (ví dụ: python app.py) hoặc một shell script đơn giản, không phải `systemd`. Nếu không có `systemd`, `snapd` không thể khởi động.

### 2.4.2. Vấn đề Mount Namespace và Privileged

Cả Snap và Flatpak bản thân chúng là các công nghệ đóng gói và cô lập (sandbox). Chúng sử dụng mount namespaces và squashfs để gắn kết các gói ứng dụng vào hệ thống tập tin.

* **SquashFS:** Để mount một file .snap (định dạng SquashFS), kernel cần quyền mount loop device. Container thường không có quyền này trừ khi chạy với cờ `--privileged`.

* **Nested Sandboxing:** Chạy Snap trong Docker là cố gắng chạy một công nghệ container bên trong một công nghệ container khác. Việc yêu cầu quyền `--privileged` để làm điều này sẽ phá vỡ hoàn toàn mô hình bảo mật của Docker, trao cho container quyền truy cập root vào máy chủ.   

**Kết luận:** Sử dụng Snap/Flatpak trong Docker là sai lầm về mặt kiến trúc. Hãy cài đặt phần mềm trực tiếp từ nguồn (source), từ kho gói (apt/dnf), hoặc sử dụng các image Docker đã được đóng gói sẵn cho ứng dụng đó. 


## 2.5. Multi-Stage Builds: Đỉnh cao của tối ưu hoá

Multi-Stage Builds là công cụ mạnh mẽ nhất trong cài đặt phần mềm. Nó giải quyết mâu thuẫn giữa việc cần công cụ để build (compiler, header files) và nhu cầu giữ image nhỏ gọn để chạy (runtime).

### 2.5.1. Nguyên lý hoạt động

Thay vì nén tất cả vào một image, ta chia nhiều giai đoạn:
1. **Stage Builder:** Sử dụng image "béo" (đầy đủ SDK, ví dụ `golang:1.21` hoặc `maven`). Tại đây ta cài đặt mọi thứ cần thiết để biên dịch mã nguồn. Kết quả đầu ra là một file nhị phân (binary) hoặc file JAR. 

2. **Stage Runtime:** Sử dụng image "siêu nhỏ" (ví dụ: `alpine` hoặc `distroless`). Ta chỉ **COPY** duy nhất file nhị phân từ Stage Builder sang. Tất cả mã nguồn, trình biên dịch GCC, thư viện header bị bỏ lại ở 
Stage 1 và không bao giờ xuất hiện trong image cuối cùng. 

### 2.5.2. Phân tích so sánh: Alpine vs. Distroless cho Production

Đây là bảng so sánh:

| Đặc điểm | Alpine Linux (`alpine`) | Distroless (`gcr.io/distroless/static`) |
|----------|------------------------|------------------------------------------|
| **Kích thước** | Rất nhỏ (~5MB) | Cực nhỏ (~2MB cho static) |
| **Thư viện C** | `musl libc` | `glibc` (hoặc không có cho static) |
| **Shell** | Có (`/bin/sh`) | Không |
| **Package Mgr** | `apk` | Không |
| **Bảo mật** | Tốt, nhưng có bề mặt tấn công từ shell/apk | Tuyệt đối, tối thiểu bề mặt tấn công |
| **Gỡ lỗi** | Dễ (docker exec) | Khó (phải dùng `nsenter` hoặc ephemeral containers) |
| **Tương thích** | Kém hơn (do `musl`), đặc biệt với Python/Node C-extensions | Tốt (tương thích Debian/glibc) |


**Phân tích chuyên sâu:** 
* **Alpine:** Dù nhỏ gọn, việc sử dụng `musl libc` đôi khi gây đau đầu về hiẹu năng (như đã bàn ở phần DNS) và tương thích nhị phân. Nhiều thư viện Python (numpy, pandas) hoặc Nodejs cần biên dịch lại để chạy trên Alpine.

* **Distroless:** Đây là xu hướng hiện đại cho bảo mật cao (DevSecOps). Distroless loại bỏ hoàn toàn Shell. Điều này có nghĩa là nếu hacker khai thác được lỗ hổng RCE (Remote Code Execution) trong ứng dụng của bạn, hắn cũng không thể mở shell (/bin/bash) để chạy lệnh, tải malware hay quét mạng, vì shell đơn giản là không tồn tại.
  * _Thách thức:_ Debugging Distroless rất khó. Bạn không thể `docker exec` vào nó. Bạn buộc phải sử dụng kỹ thuật `nsenter` (đã đề cập ở phần 1.1.2) để gỡ lỗi từ bên ngoài. Đây là sự đánh đổi giữa tiện lợi và bảo mật mà một kiến trúc sư cần chấp nhận.

### 2.6. Tối ưu hoá Image với Docker-Slim (Mint)

Ngoài multi-stage, cộng đồng còn sử dụng các công cụ tự động như **Docker-Slim** (hiện nay là Mint) để "ép cân" image. Docker-Slim hoạt động bằng cách chạy container tạm thời, theo dõi (trace) xem ứng dụng thực sự chạm vào những file nào trong quá trình hoạt động, sau đó tạo ra một image mới chỉ chứa những file đó và vứt bỏ phần còn lại.

* **Ưu điểm:** Có thể giảm kích thước image gấp 30 lần (ví dụ từ 800 MB xuống 20MB) mà không cần viết lại Dockerfile phức tạp. 

* **Nhược điểm:** Cơ chế "dò tìm" động này có rủi ro. Nếu trong quá trình trace, ứng dụng không chạy vào một chức năng hiếm gặp (edge case), Docker-Slim có thể vô tình xóa mất thư viện cần thiết cho chức năng đó, gây lỗi runtime trong tương lai. 
**Lời khuyên:** Sử dụng Multi-stage build và Distroless là phương pháp chính thống và an toàn nhất. Docker-Slim nên được sử dụng cẩn trọng với quy trình test hồi quy (regression testing) kỹ lưỡng.   


## Phần III. Bảo mật tập tin và phân quyền (File Security)

Bảo mật không chỉ là firewall, mà còn là cách container tương tác với hệ thống tập tin và quyền hạn người dùng.


### 3.1. Chạy dưới quyền Non-root (Rootless)

Mặc định, Docker Container chạy với `UID 0` (root). Dù đây là "root trong container", nhưng nếu kernel có lỗ hổng, tiến trình này có thể thoát ra (breakout) và chiếm quyền root của máy chủ. 

**Best Practices:**
1. Tạo user/group cụ thể trong Dockerfile
2. Sử dụng chỉ thị `USER` để chuyển đổi context. 
3. Lưu ý về quyền ghi: User thường không thể ghi vào các thư mục hệ thống. Bạn cần `chown` thư mục logs hoặc data cho user này trước khi chuyển đổi `USER`.

Trong các image Distroless, Google tạo ra sẵn user tên là `nonroot` (UID 65532). Sử dụng user này giúp chuẩn hoá bảo mật. 

### 3.2. Hiểm hoạ SUID/SGID

Các file có bit SUID (Set User ID) cho phép người dùng thường thực thi file với quyền của chủ sở hữu file (thường là root). Các lệnh như `passwd`, `su`, `ping` đều có SUID. 
Trong container microservices, chúng ta hiếm khi cần đổi mật khẩu và switch user. Sự tồn tại của file SUID là một vector tấn công tiềm tàng. 

**Giải pháp:**

* Xoá bit SUID trong quá tình build:
```Dockerfile
RUN find / -perm /6000 -type f -exec chmod a-s {} \; | true
```

* Sử dụng tùy chọn bảo mật của Docker khi chạy: `--security-opt=no-new-privileges`. Cờ này ngăn chặn kernel cấp thêm quyền mới cho tiến trình con, vô hiệu hóa hoàn toàn tác dụng của SUID, ngay cả khi file SUID vẫn còn trong image.

## Kết luận

Việc xây dựng Docker Image ở mức intermediate đòi hỏi sự chuyển dịch từ việc "biết lệnh" sang "hiểu hệ thống".

* Trong **Networking**, cần hiểu luồng gói tin qua iptables để cấu hình bảo mật chính xác thay vì tắt firewall, và sử dụng nsenter để gỡ lỗi thay vì cài SSH.
* Trong **Package Management**, cần tận dụng Multi-Stage Builds và Distroless để loại bỏ hoàn toàn bloatware, thay vì cố gắng dọn dẹp thủ công.
* Về **Bảo mật**, đó là việc chủ động tước bỏ quyền root và SUID để giảm thiểu rủi ro ngay cả khi ứng dụng bị khai thác.

Báo cáo này cung cấp nền tảng kiến trúc để bạn không chỉ tạo ra các container "chạy được", mà là các container chuẩn mực: nhỏ gọn, an toàn và hiệu năng cao, sẵn sàng cho môi trường production khắt khe nhất.

