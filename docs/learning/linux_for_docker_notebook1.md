# Nền tảng Linux cốt lõi cho tối ưu hoá Docker Image và Best Practices

## 1. Cơ sở lý luận: Kiến trúc Linux Kernal trong bối cảnh Container hoá

Sự chuyển dịch mô hình từ ảo hoá phần cứng (Hardware Virtualization) sang ảo hoá cấp hệ điều hành
(OS-level Virtualization) thông qua Docker đã định hình lại hoàn toàn cách thức phát triển và vận hành
phần mềm hiện đại. Để làm chủ Docker và xây dựng các Docker Image tối ưu, bảo mật, điều kiện tiên quyết
không phải là học thuộc lòng các lệnh Docker, mà là thấu hiểu sâu sắc cơ chế hoạt động của hệ điều hành Linux.

> Docker, về bản chất, không phải là một "máy ảo nhẹ" như nhiều lầm tưởng phổ biến, mà là một phương thức đóng gói và cách ly các tiến trình (processes) dựa trên các tính năng cốt lõi của Linux Kernel như Namespaces và Control Groups (cgroups). 

Báo cáo này cung cấp một phân tích toàn diện, chi tiết và chuyên sâu về các khía cạnh nền tảng của Linux cần thiết để tuân thủ các "Best Practices" của Docker. 
Từ cơ chế quản lý hệ thống tệp, quyền hạn người dùng, đến quản lý tiến trình và tự động hoá bằng script, mọi khía cạnh sẽ được mổ xẻ dưới góc độ tối ưu hoá cho môi trường Container. 


### 1.1. Sự chia sẻ kernel và tính bất biến (Immutability)

Khác với máy ảo (VM) nơi mỗi instacne chạy một kernel riêng biệt, tất cả các container trên một host đều chia sẻ chung kernel. Điều này mang lại hiệu suất vượt trội nhưng cũng đặt ra 
các yêu cầu khắt khe về việc quản lý tài khuyên và bảo mật. Khi một lệnh như `rm` hay `chmod` được thực thi trong Dockerfile, nó đang tương tác với system call của kernel host, 
nhưng thông qua lớp trừu tượng của hệ thống tệp phân lớp (layered filesystem). 

Hiểu biết về tính bất biến (immutability) là chìa khoá. Docker Image là các mẫu (templates) chỉ đọc (read-only). Khi container chạy, một lớp ghi (writable layer) mỏng được đặt lên trên cùng. 
Mọi thay đổi dữ liệu (như ghi log, tạo file tạm) nếu không được quản lý đúng cách (ví dụ: ghi vào `/var` thay vì `stdout` hoặc volume) sẽ làm phình to container và giảm hiệu năng I/O do cơ chế Copy-on-Write (CoW).
Do đó, kiến thức về phân cấp thư mục Linux (FHS) trở thành nền tảng để xác định đâu là dữ liệu tĩnh (thuộc image) và đâu là dữ liệu động (thuộc volume). 


## 2. Terminal và Giao diện dòng lệnh (CLI): Tương tác cốt lõi

Trong môi trường Docker, đặc biệt là khi viết `Dockerfile` hoặc debug container, giao diện đồ hoạ (GUI) hoàn toàn vắng mặt.
Terminal và CLI là phương tiện giao tiếp duy nhất. Việc sử dụng thành thạo các lệnh cơ bản không chỉ giúp thao tác nhanh hơn mà còn giúp hiểu rõ cách Docker thực thi các chỉ thị `RUN`. 


### 2.1. Cơ chế hoạt động của Shell và Lệnh `RUN`

Mỗi chỉ thị `RUN` trong Dockerfile mặc định được thực thi bằng `/bin/sh -c`. Điều này có nghĩa là các lệnh CLI được shell phân tích cú pháp (parsing), 
mở rộng biến (expansion), và xử lý wildcard (globbing) trước khi gửi system call tới Kernel.  


### 2.2. Phân tích chi tiết các lệnh quản lý tệp tin

Các lệnh `ls`, `cd`, `pwd`, `cp`, `mv`, `rm` tương chừng đơn giản nhưng ẩn chứa nhiều sắc thái kỹ thuật quan trọng trong bối cảnh Docker Layer.

#### 2.2.1. `ls` (List) và `pwd` (Print Working Directory)

Lệnh `ls` dùng để liệt kê nội dung thư mục. Trong quá trình build Docker (để debug) hoặc trong script entrypoint, `ls` giúp xác minh cấu trúc tệp.
* **Debug Layer:** Một kỹ thuật debug Dockerfile phổ biến là chèn chèn `RUN ls -la /path` để kiểm tra xem lệnh COPY trước đó có hoạt động đúng như mong đợi hay không, 
hoặc để xem quyền sở hữu tệp tin (`-l` hiển thị permissions và owner).
* **`pwd` và Ngữ cảnh:** Lệnh `pwd` in ra thư mục làm việc hiện tại. Trong Dockerfile, điều này liên quan mật thiết đến chỉ thị `WORKDIR`. 
Nếu không xác định `WORKDIR`, `pwd` mặc định thường là `/`. Việc hiểu `pwd` giúp tránh các lỗi "file not found" khi sử dụng đường dẫn tương đối. 


#### 2.2.2. `cd` (Change Directory) vs `WORKDIR`

Đây là điểm khác biệt lớn nhất giữa môi trường Linux tương tác và Dockerfile. 
* **Trong Shell:** `cd /app` thay đổi thư mục hiện tại của shell session đó. 
* **Trong Dockerfile:** Lệnh `RUN cd /app` chỉ thay đổi thư mục cho layer hiện tại (Lệnh `RUN` đó). Ngay khi lệnh kết thúc, trạng thái thư mục bị reset. 
Lệnh `RUN` tiếp theo sẽ quay về thư mục gốc hoặc thư mục được định nghĩa bởi `WORKDIR` gần nhất. 
* **Best Practices:** Tuyệt đối không dùng `RUN cd` để điều hướng lâu dài. Luôn sử dụng `WORKDIR` để thiết lập trạng thái thư mục nhất quán cho các chỉ thị tiếp theo
(`RUN`, `CMD`, `ENTRYPOINT`, `COPY`, `ADD`). `WORKDIR` còn tự động tạo thư mục nếu nó chưa tồn tại, loại bỏ nhu cầu `mkdir`. 


#### 2.2.3 `cp` (Copy) và `mv` (Move)

* `cp`: Sao chép tệp, Trong Dockerfile, `COPY` là lệnh ưu tiên để đưa file từ host và image. Tuy nhiên, `cp` thường được dùng trong `RUN` script để sao chép file cấu hình mẫu
(ví dụ: `cp config.sample.ini config.ini`) hoặc trong Multi-stage builds để lấy artifact. 

* `mv`: Di chuyển tệp. Một đặc điểm kỹ thuật quan trọng của `mv` là tính nguyên tử (atomicity) khi di chuyển trong cùng một phân vùng (filesystem). 
Nó chỉ đơn giản là thay đổi con trỏ inode. Tuy nhiên, nếu di chuyển giữa các phân vùng (ví dụ từ image layer vào volume count), `mv` thực chất là sao chép (`cp`) rồi xoá (`rm`),
tốn kém tài nguyên I/O hơn. Trong entrypoint script, `mv` thường dùng để đưa file cấu hình vào đúng vị trí trước khi app khởi chạy. 

#### 2.2.4. `rm` (Remove) và hiệu ứng Layer

Lệnh `rm` là con dao hai lưỡi trong Docker. 

* **Cơ chế UnionFS:** Docker sử dụng hệ thống tệp Union (như Overlay2). Khi bạn xoá một tệp tin tồn tại ở layer dưới bằng lệnh `rm` ở layer trên, tệp tin đó không thực sự bị xoá khỏi đĩa.
Thay vào đó, Docker tạo ra một tệp đặc biệt gọi là "whiteout file" để che khuất tệp gốc. Tệp gốc vẫn nằm ở layer dưới và chiếm dung lượng. 

* **Hậu quả:** Nếu bạn `COPY` một file lớn (1GB) ở Layer 1, rồi `RUN rm file` ở Layer 2, kích thước image cuối cùng vẫn tăng thêm 1GB (file gốc) + kích thước whiteout (nhỏ). 

* **Best Practice:** Luôn thực hiện cài đặt và dọn dẹp (cleanup) trong **cùng một dòng lệnh** `RUN`. Ví dụ: `apt-get install -y package && rm -rf /var/lib/apt/lists/*`. 
Việc nối lệnh bằng `&&` đảm bảo các tệp tạm bị xoá trước khi layer được commit, giúp giảm kích thước image thực tế.


## 3. Hệ thống tệp và phân cấp thư mục (Filesystem Hierarchy Standard - FHS)

Linux không lưu trữ tệp lộn xộn, nó tuân theo chuẩn FHS. Việc tuân thủ FHS trong Dockerfile không chỉ là vấn đề thẩm mỹ mà còn ảnh hưởng đến tính bảo mật, khả năng bảo trì và khả năng tương thích với các công cụ quản trị. 

### 3.1. `/etc`: Cấu hình hệ thống (System Configuration)

* **Chức năng:** Chứa các tệp cấu hình tĩnh của hệ thống và ứng dụng (ví dụ: `/etc/nginx/nginx.conf`, `/etc/hosts`, `/etc/resolv.conf`). 
* **Trong Docker:** Đây là nơi bạn thường xuyên `COPY` các file config tuỳ chỉnh vào. 
  * _Config Management:_ Một mẫu thiết kế (pattern) phổ biến là sử dụng `envsubst` trong entrypoint script để thay thế các biến môi trường các file template trong `/etc/` tại thời điểm runtime, 
giúp image trở nên linh hoạt trên các môi trường (Dev/Test/Prod). 
  * _Lưu ý:_ `/etc` thường là read-only trong tư duy immutable infrastructure, trừ khi cần thiết lập runtime. 


### 3.2. `/usr`: Tài nguyên người dùng (User System Resources)

Khác với tên gọi dễ gây hiểu nhầm, `/usr` không phải là "user home". Nó chứa các phần mềm, thư viện, tài liệu dùng chung cho tất cả user. 
* `/usr/bin`: Nơi chứa các lệnh thực thi phổ biến (như `python`, `node`, `java`).
* `/usr/local`: Đây là thư mục quan trọng nhất trong các Docker Image tự build. 
Theo chuẩn FHS, `/usr/local` dành cho phần mềm được cài đặt thủ công bởi administrator (trong trường hợp này là người viết Dockerfile) 
để không xung đột với phần mềm do hệ thống quản lý gói (`apt`, `apk`) cài đặt vào `/usr`. 
* **Best Practices:** Khi biên dịch phần mềm từ source hoặc tải binary về, hãy đặt chúng vào `/usr/local/bin`. 
Biến môi trường `$PATH` mặc định của Linux luôn ưu tiên `/usr/local/bin` trước `/usr/bin`, đảm bảo phiên bản tuỳ chỉnh của bạn được ưu tiên chạy. 

### 3.3. `/var` Dữ liệu biến đổi (Variable Data)

Chứa các tệp tin có kích thước thay đổi theo thời gian như logs, caches, spool files. 
* `/var/log`: Nơi truyền thống để ghi log. Trong Docker, ghi log vào file trong container là một "anti-pattern" vì khó thu thập và quản lý vòng đời (log rotation). 
  * _Best Practice:_ Redirect logs ra `stdout` và `stderr`. Nginx Docker Image chính thức thực hiện điều này bằng cách tạo symlink: `ln -sf /dev/stdout/var/log/nginx/access.log`. 
Điều này đánh lừa ứng dụng nghĩ rằng nó đang ghi vào file, nhưng thực tế dữ liệu được Docker Daemon bắt lấy.
* `/var/lib`: Chứa dữ liệu trạng thái của ứng dụng (ví dụ: `/var/lib/mysql` cho database). Đây là các ứng cử viên hàng đầu để gắn kết (mount) volume. 
Dữ liệu trong `/var/lib` nên được coi là dữ liệu bền vững (persistent data) và phải tồn tại độc lập với vòng đời container. 

  
### 3.4. `/home`: Thư mục người dùng (User Home Directories)

* **Chức năng:** Nơi chứa dữ liệu cá nhân và cấu hình của từng user. 
* **Trong Docker:** Mặc định container chạy user `root` (với home là `/root`). Tuy nhiên, để bảo mật, ta nên chuyển sang user thường. 
Khi tạo user mới (ví dụ `appuser`), thư mục `/home/appuser` được tạo ra.
* **Best Practices:** Đặt mã ứng dụng vào `WORKDIR /home/appuser/app`. Điều này cô lập ứng dụng trong không gian người dùng, hạn chế quyền ghi vào các thư mục hệ thống. 

## 4. Đường dẫn: Tuyệt đối và Tương đối (Absolute vs Relative Path)

Sự mơ hồ trong đường dẫn là nguyên nhân của nhiều lỗi build khó phán hiện. 

### 4.1. Định nghĩa và Cơ chế
* **Đường dẫn tuyệt đối:** Bắt đầu bằng dấu gạch chéo `/` (root). Ví dụ: `/usr/local/bin/script.sh`. Nó tham chiếu đến cùng một vị trí bất kể thư mục hiện tại đang ở đâu. 
* **Đường dẫn tương đối:** Không bắt đầu bằng `/`. Ví dụ: `script.sh` hoặc `./script.sh` hoặc `../config/`. Nó phụ thuộc hoàn toàn vào ngữ cảnh của `PWD` (Present Working Directory).


### 4.2. Ứng dụng trong Docker Best Practices
Việc sử dụng đường dẫn tương đối trong Dockerfile được coi là rủi ro và thiếu chuyên nghiệp. 

* **Sự phụ thuộc vào Base Image:** Nếu bạn dùng `WORKDIR app` (tương đối), Base Image thay đổi `WORKDIR` mặc định từ `/` sang `/opt`, thì ứng dụng của bạn sẽ vô tình chuyển từ `/app` sang `/opt/app`.
Sự thay đổi ngầm định này có thể phá vỡ logic ứng dụng. 
* **Độ minh bạch (Clarity):** `COPY ...` là một lệnh phổ biến nhưng tối nghĩa. `COPY ./app` (đích tuyệt đối) rõ ràng hơn nhiều. 
* **Quy tắc:** Luôn sử dụng đường dẫn tuyệt đối cho `WORKDIR`. Các công cụ phân tích tĩnh (linter) như Hadolint hay Datadog Security Rules đều cảnh bảo nếu phát hiện `WORKDIR` tương đối. 
  * _Khuyến nghị:_ `WORKDIR /usr/src/app`
  * _Tránh:_ `WORKDIR app`


## 5. Quản lý người dùng và phân quyền (Users, Groups & Permissions)

Bảo mật container bắt đầu từ việc hiểu mô hình phân cấp của Linux. Docker Daemon chạy với quyền root, và mặc định container cũng vậy. Đây là rủi ro bảo mật lớn nhất. 

### 5.1. UID (User ID) và GID (Group ID)
Kernel Linux không quan tâm đến người dùng ("alice", "bob"), nó chỉ quan tâm đến UID (số). 

* **Mapping giữa Host và Container:** Khi bạn chạy container, UID bên trong và bên ngoài chia sẻ chung không gian kernel. Tiến trình có UID 0 trong container chính là UID 0 (root) trên host (trừ khi dùng User Namespaces).

* **Vấn đề Volume Permission:** Khi mount một thư mục từ host vào container, nếu thư mục trên host thuộc sở hữu của UID 1000, nhưng container chạy với UID 0 (root), container có thể ghi đè file. 
Ngược lại, nếu container chạy user `nobody` (UID 65534) mà file trên host thuộc UID 1000 (mode 700), container sẽ bị lỗi "Permission Denied".

* **Best Practices:** Tạo user và group cụ thể trong Dockerfile với UID/GID cố định để đồng bộ quyền hạn. 
```Dockerfile
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -m appuser
USER appuser
```

Việc này đảm bảo tính nhất quán và nguyên tắc đặc quyền tối thiểu (Least Privilege). 


### 5.2. Quyền sở hữu (Ownership) và `chown`
Lệnh `chown` thay đổi chủ sở hữu tệp. 

* **Vấn đề Layer Size:** Một lỗi kinh điển là `COPY` file vào (mặc định owner là root), sau đó chạy `RUN chown -R appuser /app`. 
Điều này tạo ra một layer mới sao chép, toàn bộ dữ liệu với metadata mới, làm tăng gấp đôi kích thước image. 

* **Giải pháp:** Sử dụng cờ `--chown` có sẵn trong lệnh `COPY` và `ADD`.
  * `COPY --chown=appusser:appgroup /app` Lệnh này thực hiện copy và chown trong cùng một atomic operation, không tạo layer dư thừa. 


### 5.3. Phân quyền (Permissions) và `chmod`

Lệnh `chmod` thay đổi chế độ đọc (r), ghi (w), thực thi (x).

* **Octal Mode (số):** `chmod 755` (rwxr-xr-x). Chủ sở hữu có toàn quyền, người khác chỉ đọc và thực thi. 
* **Symbolic Mode (Ký tự):** `chmod +x script.sh`: Thêm quyền thực thi. 
* **Best Practices:** Các entrypoint script phải có quyền thực thi (`chmod +x`). Các file chứa secrets (nếu copy vào image - dù không khuyến khích) phải được set `chmod 600` (chỉ owner đọc được) hoặc `400` (read-only).
* `SGID` (Set Group ID): Đối với các thư mục chia sẻ dữ liệu (ví dụ volume chia sẻ) giữa 2 container trong 1 Pod), lệnh `chmod g+s <directory>` giúp đảm bảo mọi file mới tạo ra trong thư mục đó đều kế thừa Group ID của thư mục cha, giải quyết vấn đề chia sẻ quyền truy cập nhóm. 

## 6. Liên kết tệp tin: Symbolic vs Hard Links

Docker Image là tập hợp của nhiều layer file system. Hiểu cách liên kết hoạt động giúp tối ưu hoá không gian và cấu hình.

### 6.1. Hard Links
* **Cơ chế:**  Hard Link là một tên file khác trỏ cùng một inode (cấu trúc dữ liệu trên đĩa chứa thông tin file). 
Hai hard link hoàn toàn bình đẳng; không có cái nào là "gốc". Dữ liệu chỉ bị xoá khi link cuối cùng tới inode đó bị xoá. 

* **Giới hạn:** Không thể tạo hard link cho thư mục (để tránh vòng lặp vô hạn). Không thể tạo hard link giữa các phân vùng (filesystem) khác nhau. 

* **Ứng dụng:** Ít dùng trong Dockerfile thông thường nhưng được dùng nhiều trong công cụ backup hoặc tối ưu hoá lưu trữ (deduplication) trên host. 


### 6.2. Symbolic Links (Symlinks)

* **Cơ chế:** Symlink là một file nhỏ chứa đường dẫn của file khác. Nó hoạt động như shortcut. Nếu file đích bị xoá, symlink trở nên "gãy" (dangling).

* **Ưu điểm:** Có thể trỏ tới thư mục và vượt qua ranh giới filesystem. 

* **Ứng dụng thiết yếu trong Docker:**
1. **Quản lý Log:** Chuyển hướng ghi log sang `stdout` như đã bàn ở phần `/var`.
2. **Cấu hình linh hoạt:** Tạo symlink `app.conf` trỏ tới `app-prod.conf` hoặc `app-dev.conf` tuỳ thuộc vào script khởi chạy.
3. **Tương thích ngược:** Giả sử ứng dụng hardcode đường dẫn `/user/lib/old-lib`, nhưng thư viện mới nằm ở `/usr/local/lib/new-lib`. Tạo symlink giúp ứng dụng chạy mà không cần sửa code. 
4. **Lưu ý với `COPY`:** Mặc định `COPY` sẽ sao chép nội dung file mà symlink trỏ tới (dereference). Nếu muốn copy chính symlink đó, cần kiểm tra kỹ tài liệu của phiên bản Docker đang dùng. 


## 7. Biến môi trường (Environment Variables)
Trong phương phpas 12-Factor App, cấu hình được lưu trong môi trường.

### 7.1. `$PATH`
Biến danh sách các thư mục mà shell sẽ tìm kiếm tệp thực thi.
* **Tuỳ biến:** Nếu bạn cài đặt ứng dụng vào `/opt/myapp/bin`, bạn phải thêm nó vào PATH: `ENV PATH="/opt/myapp/bin:${PATH}"`. Nếu không, người dùng phải gõ đường dẫn đầy đủ mỗi khi chạy lệnh. 

* **Thự tự ưu tiên:** Đường dẫn đứng trước có độ ưu tiên cao hơn. Đặt `/usr/local/bin` trước `/usr/bin` đảm bảo các phiên bản custom đè lên phiên bản hệ thống. 

### 7.2. `$HOME`

Thư mục chủ của user hiện tại. 
* **Pitfall:** Nhiều ứng dụng (npm, pip, maven) ghi cache vào `$HOME`. 
Nếu bạn đổi user bằng `USER appuser` nhưng không thiết lập đúng biến `HOME` (hoặc `/etc/password` chưa cập nhật), ứng dụng có thể cố ghi vào `/root` và bị lỗi permission denied. 


### 7.3. `ENV` vs `ARG`

Sự phân biệt này rất quan trọng để bảo mật và tối ưu build. 
* `ARG` **(Build-time variables):** Chỉ tồn tại trong lúc `docker build`. Dùng để truyền phiên bản (`ARG VERSION=1.0`), tuỳ chọn biên dịch. 
Không lưu lại trong image cuối cùng (tuy nhiên vẫn có thể xem được qua `docker history`), nên không dùng cho secret. 

* `ENV` **(Runtime variables):** Tồn tại trong container khi chạy (`docker run`). Dùng cho cấu hình database, debug flag. 
Các lệnh `RUN` tiếp theo trong Dockerfile cũng nhìn thấy `ENV`. 

* **Chiến lược:** Sử dụng `ARG` để parameterize Dockerfile (làm cho nó tái sử dụng được), và dùng `ENV` để cấu hình ứng dụng mặc định. 


## 8. Quản lý tiến trình (Process Management)

Container không phải là máy ảo đầy đủ, nó thường chỉ chạy một tiến trình duy nhất. Sự khác biệt này dẫn đến nhiều vấn đề quản lý tiến trình độc đáo. 

### 8.1. Vấn đề PID 1 và Tín hiệu (Signals)

Trong Linux, tiến trình PID 1 (init) có nhiệm vụ đặc biệt: thu dọn tiến trình con mồ côi (zombie reaping) và xử lý tín hiệu. 

* **Vấn đề Zombie:** Khi một tiến trình con kết thúc, nó trở thành zombie cho đến khi tiến trình cha đọc exit code của nó.
Nếu tiến trình cha chết, zombie được gán cho PID 1. Nếu PID 1 (ứng dụng của bạn) không được lập trình để thu dọn zombie, chúng sẽ
tích tụ và làm đầy bảng tiến trình kernel, khiến container bị treo. 

* **Vấn đề tín hiệu (Graceful Shutdown):** Khi `docker stop` chạy, nó gửi `SIGTERM` tới PID 1. 
Kernel Linux đối xử đặc biệt với PID 1: nó chặn các tín hiệu mặc định trừ khi tiến trình chủ động lắng nghe (handle) chúng. 
Nếu ứng dụng (ví dụ Java hay Python script) không bắt `SIGTERM`, nó sẽ lờ đi. Docker sẽ đợi 10s (mặc định) rồi gửi `SIGKILL` để diệt container. 
Điều àny gây tắt đột ngột, có thể làm hỏng dữ liệu đang ghi dở. 

  
### 8.2. Giải pháp: Tini và `exec`

* **Tini:** Một init process cực nhỏ, đóng vai trò PID 1, chuyển tiếp tin hiệu cho ứng dụng và thu dọn zombie. 
  * Sử dụng: `ENTRYPOINT ["/tini", "--", "/docker-entrypoint.sh"]`

* Lệnh `exec`: Trong các shell scipt entrypoint, dòng cuối cùng khởi chạy ứng dụng phải dùng `exec`.
  * Không dùng `exec`: Ứng dụng chạy như tiến trình con của shell (PID 2+). Shell (PID 1) nhận `SIGTERM` nhưng thường không chuyển tiếp cho con.
  * Dùng `exec`: `exec app` thay thế tiến trình shell bằng tiến trình app. App nhận lại PID 1 (hoặc PID hiện tại của shell) và nhận được tín hiệu trực tiếp từ Docker. 

    
### 8.3. Các công cụ giám sát: `ps`, `top`, `nice`

* `ps aux`: Liệt kê toàn bộ tiến trình. Cần thiết để debug xem có bao nhiêu tiến trình đang chạy, ai là cha của ai (PPID).
* `top` / `htop`: Xem mức tiêu thụ CPU/RAM realtime. Giúp phát hiện memory leak hoặc CPU spike. 
* `nice`: Điều chỉnh độ ưu tiên của tiến trình (niceness). Giá trị từ -20 (ưu tiên cao nhất) đến 19 (thấp nhất). 
Trong Docker, mặc dù ta ít dùng lệnh `nice` trực tiếp nhưng khái niệm này tương đương với cờ `--cpu-shares` khi chạy container, giúp kernel điều phối CPU giữa các container.

  
## 9. Bash Scripting: Tự động hoá và Entrypoints

Scripting là keo dính kết nối hệ điều hành và ứng dụng. Một entrypoint script tốt phải mạnh mẽ (robust) và xử lý lỗi tốt. 

### 9.1. Bash Basics: Biến, Vòng lặp, Điều kiện

* **Shebang:** Luôn bắt dầu bằng `#!bin/bash` (hoặc `#!/bin/sh` nếu dùng Alpine)
* **Biến:** ` ${VAR:-default}` (dùng giá trị mặc định nếu biến chưa set) rất hữu ích để cấu hình container linh hoạt. 
* **Vòng lặp (Loops):** Thường dùng để chờ dịch vụ phụ thuộc (Wait-for-it-patterm)
  * Ví dụ: `while! nc -z db 5432; do sleep 1; done` (chờ database mở cổng 5432).
* **Điều kiện (Conditions):** Kiểm tra xem user có muốn chạy lệnh mặc định hay lệnh tuỳ chỉnh. 
  * `if [ "$1" = 'npm']; then... fi`

  
### 9.2. Shell I/O: Redirects và Pipes

* **Redirects:**
  * `>`: Ghi đè. Dùng để tạo file config từ biến môi trường: `echo "host=$DB_HOST" > /etc/app.conf`.
  * `>>`: Ghi nối (Append).
  * `2>&1`: Hợp nhất `stderr` vào `stdout`. Quan trọng để đảm bảo mọi log lỗi đều được đẩy ra luồng log của Docker.  

* **Pipes (`|`):** Kết nối lânhj
  * `curl url | tar xz`
  * **Rủi ro:** Nếu `curl` lỗi (ví dụ 404) nhưng trả về text rác, `tar` có thể vẫn chạy và báo lỗi, nhưng exit code của cả dòng lệnh (pipeline) là của `tar`. 
Nếu tar không coi đó là lỗi nghiêm trọng, pipeline trả về 0 (thành công). Docker build sẽ tiếp tục với file rác.
  * **Giải pháp:** `set -o pipefail`. Tùy chọn này bắt buộc pipeline trả về lỗi nếu bất kỳ thành phần nào lỗi.

    
### 9.3. Job Control (Foreground/Background)

Docker Container được thiết kế để chạy một tiến trình foreground. 
Nếu entrypoint script chạy ứng dụng bằng `app &` (background) rồi kết thúc script, container sẽ nghĩ rằng nhiệm vụ đã xong và tự tắt (`Exited`)

* **Quy tắc:** Tiến trình chính phải luôn chạy ở foreground. 

* **Multi-process:** Nếu bắt buộc chạy 2 dịch vụ (ví dụ: cron + web server) trong 1 container, không nên dùng `&` đơn thuần. 
Hãy dùng một process manager như `supervisord` hoặc `s6-overlay`. Chúng sẽ quản lý các tiến trình con và giữ container sống. 

  
## 10. Dịch vụ và tự động hoá: Systemctl vs Cron

### 10.1. Services (Systemd/Systemctl)

Đây là điểm gây bối rối nhất cho người mới chuyển từ VM sang Docker. 

* **Xung đột:** Systemd yêu cầu đặc quyền cao và quản lý toàn bộ hệ thống (cgroups, logging journald). Docker container chỉ là một phần nhỏ. Chạy systemd trong Docker rất phức tạp và thường không cần thiết ("fat container). 

* **Thay thế:** Thay vì `systemctl start nginx`, hãy chạy trực tiếp lệnh binary `nginx -g "daemon off;"`. Lệnh này chạy ngin ở foreground, phù hợp hoàn hảo vứoi mô hình Docker.  

### 10.2. Cron Jobs

* **Cron truyền thống:** Được thiết kế cho môi trường server đầy đủ. 
Nó gửi log qua email (cần postfix), chạy background, và quan trọng nhất: cron session thường không kế thừa biến môi trường của container (`ENV` trong Dockerfile). Do đó các job chạy bởi cron thường fail vì thiếu config DB, API Key. 

* **Supercronic:** Một giải pháp thay thế cron viết bằng Go, dành riêng cho container. 
  * Ưu điểm: Kế thừa toàn bộ biến môi trường, log trực tiếp ra stdout/stderr (dễ debug qua `docker logs`), xử lý tín hiệu SIGTERM đúng cách.
  * Bảng so sánh: 

| Tính năng | Cron Truyền thống | Supercronic |
|-----------|-------------------|-------------|
| **Log output** | Email / Syslog / Logfile | Stdout / Stderr |
| **Env Vars** | Không kế thừa (phải tự source) | Tự động kế thừa |
| **Signal Handling** | Kém (khó dừng graceful) | Tốt (hỗ trợ SIGTERM) |
| **Kiến trúc** | Background Daemon | Foreground Process |

Sử dụng `supercronic` là Best Practice cho các container chạy tác vụ định kỳ. 

## 11. Tập thực hành tổng hợp (Hands-on Scenarios)
Để củng cố kiến thức, dưới đây là các bài tập tích hợp tất cả các khái niệm trên.

**Bài tập 1: Script "Service Checker" và Entrypoint an toàn**

**Mục tiêu:** Viết entrypoint cho một web app, đảm bảo DB sẵn sàng, cấu hình được tạo từ ENV, và chạy app với PID 1.

```bash
#!/bin/bash
# Sử dụng chế độ an toàn: Exit ngay nếu lỗi, lỗi pipeline, hoặc biến chưa định nghĩa
set -euo pipefail

# 1. Kiểm tra biến môi trường (Environment Variables)
: "${DB_HOST:?Biến DB_HOST chưa được thiết lập}"
: "${DB_PORT:=5432}" # Giá trị mặc định

echo "Đang khởi tạo container..."

# 2. Vòng lặp kiểm tra dịch vụ (Loop & Conditions & Netcat)
echo "Đang chờ Database tại $DB_HOST:$DB_PORT..."
# Thử kết nối mỗi giây, tối đa 30s
timeout=30
while! nc -z "$DB_HOST" "$DB_PORT"; do
  timeout=$((timeout - 1))
  if [ $timeout -le 0 ]; then
    echo "Lỗi: Không thể kết nối tới Database sau 30s" >&2 # Redirect stderr
    exit 1
  fi
  sleep 1
done
echo "Database đã sẵn sàng!"

# 3. Tạo file cấu hình từ template (I/O Redirection & Sed)
# Thay thế placeholder {{DB_HOST}} trong file config bằng giá trị thực
sed "s/{{DB_HOST}}/$DB_HOST/g" /etc/app/config.tpl > /etc/app/config.ini
chmod 600 /etc/app/config.ini # Phân quyền bảo mật

# 4. Chuyển quyền điều khiển (Process Management)
# Dùng exec để app nhận PID 1
echo "Khởi chạy ứng dụng..."
exec "$@"
```

**Bài tập 2: Tự động Sao lưu với Supercronic**

**Mục tiêu:** Tạo image chạy backup mỗi ngày lúc 3h sáng, upload lên S3 (giả lập), chạy non-root.

```bash
FROM alpine:3.18

# Cài đặt curl và supercronic (Process Management)
# Dùng && và rm để tối ưu layer (Filesystem)
ENV SUPERCRONIC_URL=https://github.com/aptible/supercronic/releases/download/v0.2.1/supercronic-linux-amd64 \
    SUPERCRONIC=supercronic-linux-amd64 \
    SUPERCRONIC_SHA1SUM=d7f4c0886eb85249ad05ed592902fa6865bb9d70

RUN apk add --no-cache curl tar \
 && curl -fsSLO "$SUPERCRONIC_URL" \
 && echo "${SUPERCRONIC_SHA1SUM}  ${SUPERCRONIC}" | sha1sum -c - \
 && chmod +x "$SUPERCRONIC" \
 && mv "$SUPERCRONIC" /usr/local/bin/supercronic \
 && ln -s /usr/local/bin/supercronic /usr/local/bin/crond # Symlink

# Thiết lập User (Security)
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -D appuser
WORKDIR /home/appuser

# Script backup
COPY --chown=appuser:appgroup backup.sh.
RUN chmod +x backup.sh

# Crontab file
RUN echo "0 3 * * * /home/appuser/backup.sh" > crontab

USER appuser

# Chạy supercronic ở foreground
CMD ["supercronic", "crontab"]
```

**backup.sh**

```bash
#!/bin/sh
set -e
echo "[$(date)] Bắt đầu backup..."
# Giả lập nén data (CLI tar)
tar -czf /tmp/backup.tar.gz /data
# Giả lập upload
echo "Uploading to S3..."
#... lệnh upload...
echo "[$(date)] Backup hoàn tất!"
```


## Kết luận
Kiến thức về Linux không chỉ là nền tảng mà yếu tố sống còn để vận hành Docker hiệu quả. 
Từ việc tối ưu hoá từng byte trong layer image bằng cách hiểu rõ hệ thống tệp và lệnh `rm`,
đến việc đảm bảo an toàn vận hành (graceful shutdown) thông qua hiểu biết về tín hiệu và quản lý
tiến trình. Việc tuân thủ các Best Practices này không chỉ giúp bạn tạo ra các image nhỏ hơn mà còn
an toàn và chuyên nghiệp hơn, đáp ứng tiêu chuẩn khắt khe của môi trường Production doanh nghiệp. 









