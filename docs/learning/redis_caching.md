# Redis Caching

## Mục lục

[Phần I. Nền tảng về Caching](#phần-i-nền-tảng-về-caching)
  * [1.1. Tầm quan trọng của Caching trong ứng duyệt Web](#11-tầm-quan-trọng-của-caching-trong-ứng-duyệt-web)
    * [Lợi ích 1: Cải thiện hiệu năng vượt trội & Giảm độ trễ](#lợi-ích-1-cải-thiện-hiệu-năng-vượt-trội--giảm-độ-trễ)
    * [Lợi ích 2: Giảm tải cho cơ sở dữ liệu & Chi phí vận hành](#lợi-ích-2-giảm-tải-cho-cơ-sở-dữ-liệu--chi-phí-vận-hành)
    * [Lợi ích 3: Giảm thiểu "điểm nóng" và đảm bảo hiệu năng ổn định](#lợi-ích-3-giảm-thiểu-điểm-nóng-và-đảm-bảo-hiệu-năng-ổn-định)
    * [Lợi ích 4: Tăng thông lượng & khả năng mở rộng:](#lợi-ích-4-tăng-thông-lượng--khả-năng-mở-rộng)
  * [1.2. Khám phá thế giới Caching: Phía Client và Phía Server](#12-khám-phá-thế-giới-caching-phía-client-và-phía-server)
    * [Bảng 1: So sánh Caching phía Cient và phía Server](#bảng-1-so-sánh-caching-phía-cient-và-phía-server)
  * [1.3. Giải mã HTTP Caching](#13-giải-mã-http-caching)

[Phần II. Giới thiệu về Redis - "Con dao đa năng" cho Backend](#phần-ii-giới-thiệu-về-redis---con-dao-đa-năng-cho-backend)
  * [2.1. Redis là gì?](#21-redis-là-gì-)
  * [2.2. Bí mật tốc độ của Redis](#22-bí-mật-tốc-độ-của-redis)
    * [Yếu tố 1: Lưu trữ trong bộ nhớ (In-Memory Storage)](#yếu-tố-1-lưu-trữ-trong-bộ-nhớ-in-memory-storage)
    * [Yếu tố 2: Kiến trúc đơn luồng, hướng sự kiện (Single-Threaded, Event-Driven)](#yếu-tố-2-kiến-trúc-đơn-luồng-hướng-sự-kiện-single-threaded-event-driven)
    * [Yếu tố 3: I/O không chặn (Non-Blocking I/O)](#yếu-tố-3-io-không-chặn-non-blocking-io)
    * [Yếu tố 4: Các cấu trúc dữ liệu được tối ưu hoá](#yếu-tố-4-các-cấu-trúc-dữ-liệu-được-tối-ưu-hoá)
  * [2.3. Các cấu trúc dữ liệu cốt lõi trong Redis](#23-các-cấu-trúc-dữ-liệu-cốt-lõi-trong-redis)
    * [Bảng 2. Các cấu trúc dữ liệu Redis và trường hợp sử dụng](#bảng-2-các-cấu-trúc-dữ-liệu-redis-và-trường-hợp-sử-dụng)
  * [2.4. Vòng đời của dữ liệu và tính nguyên tử](#24-vòng-đời-của-dữ-liệu-và-tính-nguyên-tử)

[Phần III. Tích hợp Redis vào Sanic - Hướng dẫn thực chiến](#phần-iii-tích-hợp-redis-vào-sanic---hướng-dẫn-thực-chiến)
  * [3.1. Thiết lập môi trường](#31-thiết-lập-môi-trường)
  * [3.2. Quản lý kết nối chuyên nghiệp: Connection Pool](#32-quản-lý-kết-nối-chuyên-nghiệp-connection-pool)

[Phần IV. Triển khai 3 trường hợp điển hình với Sanic và Redis](#phần-iv-triển-khai-3-trường-hợp-điển-hình-với-sanic-và-redis)
  * [4.1. Trường hợp 1: Caching phản hồi API](#41-trường-hợp-1-caching-phản-hồi-api)
  * [4.2. Trường hợp 2: Vô hiệu hoá JWT với Backlist](#42-trường-hợp-2-vô-hiệu-hoá-jwt-với-backlist)
  * [4.3. Trường hợp 3: Giới hạn tần suất truy cập (Rate Limiting)](#43-trường-hợp-3-giới-hạn-tần-suất-truy-cập-rate-limiting)

[Phần V. Thao tác với Redis qua CLI](#phần-v-thao-tác-với-redis-qua-cli)
  * [5.1. Cài đặt & Chạy Redis (qua Docker)](#51-cài-đặt--chạy-redis-qua-docker)
  * [5.2. Kết nối và thao tác với Redis CLI](#52-kết-nối-và-thao-tác-với-redis-cli)
  * [5.3. Atomic Operations: MULTI / EXEC](#53-atomic-operations-multi--exec)
  * [5.4. Monitoring cơ bản](#54-monitoring-cơ-bản)

## Phần I. Nền tảng về Caching
### 1.1. Tầm quan trọng của Caching trong ứng duyệt Web
Về cơ bản, caching là một chiến lược kỹ thuật nhằm cải thiện hiệu năng bằng 
cách lưu trữ các bản sao của dữ liệu ở một vị trí tạm thời có tốc độ truy cập cao 
(gọi là "bộ đệm" hay "cache") để phục vụ các yêu cầu trong tương lai một cách nhanh 
chóng hơn. Tầm quan trọng của nó được thể hiện qua nhiều lợi ích cốt lõi.

#### Lợi ích 1: Cải thiện hiệu năng vượt trội & Giảm độ trễ
Nguyên nhân chính là do bộ nhớ truy cập ngẫu nhiên (RAM) nhanh hơn nhiều bậc so với ổ đĩa
(cả SSD và HDD). Việc đọc dữ liệu từ một bộ đệm trong bộ nhớ (in-memory cache) có thể chỉ mất chưa đến một mili giây, 
điều này trực tiếp chuyển thành trải nghiệm người dùng nhanh hơn và mượt mà hơn. Một trang web tải nhanh không chỉ là sự tiện lợi; 
nó còn ảnh hưởng trực tiếp đến tỷ lệ giữ chân người dùng và thậm chí cả thứ hạng SEO.   

#### Lợi ích 2: Giảm tải cho cơ sở dữ liệu & Chi phí vận hành
Việc lưu vào bộ đệm các dữ liệu được truy cập thường xuyên giúp giảm đáng kể số lượng truy vấn đến cơ sở dữ liệu chính. 
Một thực thể cache duy nhất có thể xử lý hàng trăm nghìn thao tác mỗi giây (IOPS), có khả năng thay thế nhiều thực thể cơ sở dữ liệu, 
từ đó giảm chi phí cơ sở hạ tầng. Điều này đặc biệt quan trọng đối với các ứng dụng có lượng đọc lớn (read-heavy). 

#### Lợi ích 3: Giảm thiểu "điểm nóng" và đảm bảo hiệu năng ổn định
Trong nhiều ứng dụng, một tập hợp nhỏ dữ liệu thường nhận được một lượng truy cập không tương xứng so với phần còn lại 
(ví dụ: một trang sản phẩm đang lan truyền, thông tin của một người nổi tiếng). Hiện tượng này tạo ra các "điểm nóng" (hotspots) 
có thể khiến cơ sở dữ liệu trở thành nút thắt cổ chai khi lưu lượng truy cập tăng đột biến. Bằng cách lưu trữ các dữ liệu "nóng" này trong cache, 
hệ thống có thể tránh được tình trạng quá tải cơ sở dữ liệu, đảm bảo hiệu năng ổn định và có thể dự đoán được ngay cả trong những thời điểm cao điểm.

#### Lợi ích 4: Tăng thông lượng & khả năng mở rộng:
Bằng cách giảm tải các yêu cầu đọc, toàn bộ hệ thống có thể xử lý một khối lượng lớn truy cập lớn hơn, cải thiện thông lượng
tổng thể (IOPS) và giúp ứng dụng dễ dàng mở rộng hơn khi nhu cầu tăng lên. 

Những lợi ích này cho thấy caching không chỉ là một kỹ thuật tối ưu hóa hiệu năng đơn thuần, mà là một trụ cột kiến trúc. 
Việc quyết định cái gì, ở đâu và làm thế nào để cache nên được xem xét ngay từ giai đoạn đầu của quá trình thiết kế hệ thống. 
Một chiến lược caching hiệu quả không chỉ giúp ứng dụng nhanh hơn mà còn đơn giản hóa các yêu cầu đối với cơ sở dữ liệu chính, 
cho phép nó được cấu hình cho tải trung bình thay vì tải cao điểm, giúp tiết kiệm đáng kể chi phí và độ phức tạp trong vận hành.

### 1.2. Khám phá thế giới Caching: Phía Client và Phía Server
**Caching phía Client (Client-Side Caching hay Browser Caching):** Dữ liệu được lưu trữ ngay trên thiết bị của người dùng, 
cụ thể là trong trình duyệt web. Đây là giải pháp lý tưởng cho các tài nguyên tĩnh (static assets) như file CSS, JavaScript, 
hình ảnh, và các dữ liệu dành riêng cho người dùng ít thay đổi. Nó mang lại độ trễ thấp nhất có thể cho các lần truy cập lặp lại, 
vì trình duyệt thậm chí không cần gửi yêu cầu qua mạng. Tuy nhiên, nhà phát triển có quyền kiểm soát hạn chế; người dùng có thể xóa bộ đệm của họ bất cứ lúc nào, 
và có nguy cơ phục vụ dữ liệu cũ (stale data) nếu không được quản lý đúng cách.

**Caching phía Server (Server-Side Caching):** Dữ liệu được lưu trữ trên hạ tầng máy chủ, nằm giữa logic ứng dụng và nguồn dữ liệu chính (ví dụ: trong Redis). 
Với phương pháp này, nhà phát triển toàn quyền kiểm soát nội dung, kích thước và các chính sách vô hiệu hoá của bộ đệm. Nó mang lại lợi ích cho tất cả người dùng, 
không chỉ một người duy nhất, và là lựa chọn lý tưởng để cache kết quả truy vấn cơ sở dữ liệu, phản hồi API, và các đoạn HTML được render sẵn. 

Để có cái nhìn tổng quan, bảng dưới đây so sánh hai phương pháp caching này. 

#### Bảng 1: So sánh Caching phía Cient và phía Server

<table>
  <thead>
    <tr>
      <th>Tiêu chí</th>
      <th>Caching Phía Server</th>
      <th>Caching Phía Client</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Vị trí lưu trữ</td>
      <td>Trên máy chủ hoặc hạ tầng trung gian (ví dụ: Redis, Memcached, CDN).</td>
      <td>Trên thiết bị của người dùng cuối (ví dụ: trình duyệt web).</td>
    </tr>
    <tr>
      <td>Quyền kiểm soát</td>
      <td>Toàn quyền kiểm soát bởi nhà phát triển/quản trị viên hệ thống.</td>
      <td>Hạn chế, bị ảnh hưởng bởi cài đặt của trình duyệt và hành động của người dùng.</td>
    </tr>
    <tr>
      <td>Độ tươi mới của dữ liệu</td>
      <td>Dễ dàng đảm bảo tính nhất quán và tươi mới thông qua kiểm soát tập trung.</td>
      <td>Có nguy cơ phục vụ dữ liệu cũ nếu không có chiến lược vô hiệu hóa hoặc cập nhật hiệu quả.</td>
    </tr>
    <tr>
      <td>Bảo mật</td>
      <td>An toàn hơn vì dữ liệu được lưu trữ trên máy chủ, giảm tiếp xúc với các lỗ hổng phía client.</td>
      <td>Tiềm ẩn rủi ro bảo mật cao hơn vì dữ liệu được lưu trên thiết bị của người dùng, có thể bị truy cập hoặc giả mạo.</td>
    </tr>
    <tr>
      <td>Tác động hiệu năng</td>
      <td>Giảm tải cho cơ sở dữ liệu và các hệ thống backend.</td>
      <td>Giảm số lượng yêu cầu mạng, giảm độ trễ và tăng tốc độ tải trang cho người dùng cá nhân.</td>
    </tr>
    <tr>
      <td>Trường hợp sử dụng</td>
      <td>Nội dung động, kết quả truy vấn CSDL, phản hồi API, dữ liệu được chia sẻ giữa nhiều người dùng.</td>
      <td>Tài nguyên tĩnh (CSS, JS, ảnh), dữ liệu dành riêng cho người dùng, ứng dụng trang đơn (SPA).</td>
    </tr>
    <tr>
      <td>Khả dụng ngoại tuyến</td>
      <td>Không hỗ trợ, yêu cầu kết nối đến máy chủ.</td>
      <td>Có thể hỗ trợ, cho phép truy cập vào các tài nguyên đã được cache mà không cần kết nối mạng.</td>
    </tr>
  </tbody>
</table>

### 1.3. Giải mã HTTP Caching
HTTP, ngôn ngữ của web, có cơ chế caching được tích hợp sẵn ngay trong giao thức thông qua header. 
Các header này là những chỉ thị từ máy chủ gửi đến client (trình duyệt, proxy, CDN) về cách xử ly một phản hồi. 
Đây chính là "API" mà máy chủ sử dụng để điều khiển lớp caching phía client. 

Kiểm soát độ tươi mới với `Cache-Control`. Đây là chỉ thị quan trọng nhất và phổ biến nhất:
- `max-age=<second>`: Chỉ thị phổ biến nhất, cho client biết một phản hồi được coi là "tươi mới" (fresh) trong 
bao nhiêu giây. Trong thời gian này, client có thể sử dụng lại phản hồi từ cache của mình mà không cần phản hồi 
lại máy chủ. 
- `public` vs. `private`: `pubic` cho phép các bộ đệm chia sẻ (shared caches) như CDN lưu trữ phản hồi. 
`private` chỉ cho phép bộ đệm cá nhân của người dùng cuối (trình duyệt) lưu trữ nó.
- `no-cache` vs `no-store`: Đây là một điểm thường gây nhầm lẫn. `no-cache` không có nghĩa là "đừng cache".
Nó có nghĩa là client có thể lưu trữ phản hồi (response), nhưng phải xác thực lại với máy chủ (revalidate) trước mỗi lần 
sử dụng. Ngược lại, `no-store` mới thực sự là chỉ thị "không được lưu trữ dưới bất kfy hình thức nào", 
thường dùng cho dữ liệu nhạy cảm. 

Xác thực với yêu cầu có điều kiện (`ETag` và `Last-Modified`): Khi một tài nguyên trong cache hết hạn `max-age`,
nó trở thành "cũ" (stale). Thay vì phải tải lại toàn bộ tài nguyên, client có thể thực hiện một yêu cầu có điều kiện
(conditional request).
- Client gửi một yêu cầu kèm theo header `If-None-Match` với giá trị `ETag` của phiên bản tài nguyên mà nó đang giữ. 
`ETag` (entity tag) là một chuỗi định danh duy nhất cho một phiên bản cụ thể của tài nguyên, thường là một giá trị hash nội dung. 
- Ngoài ra, client có thể dùng header `If-Modified-Since` với giá trị là ngày `Last-Modified` của tài nguyên trong cache. 
- Nếu tài nguyên trên máy chủ không có gì thay đổi, máy chủ sẽ trả về một phản hồi `304 Not Modified` với phần thân trống. 
Đây là một tín hiệu cực kỳ nhẹ, cho client biết rằng phiên bản trong cache của nó vẫn còn tốt và có thể tiếp tục sử dụng. 
Cơ chế này giúp tiết kiệm băng thông một cách đáng kể. `ETag` thường được ưu tiên hơn vì nó mạnh mẽ và linh hoạt hơn so với 
việc so sánh dấu thời gian (timestamp).

Việc hiểu và sử dụng đúng các header HTTP này là một phần không thể thiếu của việc phát triển backend. 
Khi bạn triển khai caching phía server cho một endpoint API, bạn cũng nên trả về header `Cache-Control` và `ETag` phù hợp. 
Điều này cho phép bạn tận dung lớp caching miễn phí và mạnh mẽ ngay trên trình duyệt của người dùng, 
giảm tải cho máy chủ của bạn một cách tối đa. 

## Phần II. Giới thiệu về Redis - "Con dao đa năng" cho Backend
### 2.1. Redis là gì? 
Redis (viết tắt của **RE**mote **DI**ctionary **S**erver) là một cơ sở dữ liệu NoSQL, mã nguồn mở, 
lưu trữ dữ liệu trong bộ nhớ (in-memory) theo mô hình key-value. 

Tuy nhiên, việc gọi Redis đơn thuần là "bộ đệm" hay một "kho lưu trữ key-value" là chưa đầy đủ.
Chính xác hơn, Redis nên được mô tả là một **máy chủ cấu trúc dữ liệu (data structure server).** 
Điểm khác biệt cốt lõi này nằm ở chỗ phần "value" trong cặp key-value của Redis không chỉ là một chuỗi đơn giản. 
Thay vào đó, nó có thể là các cấu trúc dữ liệu phức tạp như Lists, Sets, Hashes, Sorted Sets, mỗi loại đi kèm với một bộ lệnh chuyên biệt, 
có tính nguyên tử (atomic) để thao tác trên chúng. Sự linh hoạt này cho phép Redis đảm nhận nhiều vai trò khác nhau trong một kiến trúc hệ thống, 
từ cơ sở dữ liệu, bộ đệm, message broker, cho đến hàng đợi (queue)

### 2.2. Bí mật tốc độ của Redis
Hiệu năng cực cao của Redis không đến từ một yếu tố duy nhất, mà là sự kết hợp của nhiều quyết định thiết kế kiến trúc thông minh. 
#### Yếu tố 1: Lưu trữ trong bộ nhớ (In-Memory Storage)
Đây là lý do cơ bản và quan trọng nhất. Bằng cách lưu trữ toàn bộ tập dữ liệu trong RAM, Redis loại bỏ hoàn toàn các thao tác I/O trên 
đĩa vốn rất chậm chạp. Điều này làm cho các hoạt động và ghi trở nên cực kỳ nhanh chóng.

#### Yếu tố 2: Kiến trúc đơn luồng, hướng sự kiện (Single-Threaded, Event-Driven)
Redis sử dụng một luồng duy nhất để xử lý tất cả các lệnh từ client. Điều này nghe có vẻ phản trực giác trong thế giới đa lõi ngày nay, 
nhưng nó lại là một ưu điểm lớn. Kiến trúc đơn luồng giúp loại bỏ hoàn toàn chi phí chuyển đổi ngữ cảnh (context switching) và 
sự phức tạp của cơ chế khoá (locking) cần thiết trong môi trường đa luồng. Điều này giúp ngăn chặn các điều kiện tranh chấp (race condition) 
và làm cho hệ thống đơn giản, dễ dự đoán hơn. 

#### Yếu tố 3: I/O không chặn (Non-Blocking I/O)
Luồng đơn của Redis được kết hợp với mô hình I/O ghép kênh (I/O Multiplexing) hiệu quả cao (như `epoll` của Linux). Điều này cho phép luồng đơn xử 
lý hàng nghìn request đồng thời. Thay vì bị chặn lại để chờ một kết nối hoàn tất thao tác I/O, nó có thể chuyển sang phục vụ các kết nối khác đã sẵn sàng, 
tối đa hoá việc sử dụng tài nguyên. 

#### Yếu tố 4: Các cấu trúc dữ liệu được tối ưu hoá
Việc triển khai nội bộ các cấu trúc dữ liệu của Redis được tối ưu hóa cao cho các hoạt động cụ thể. 
Ví dụ, Hashes sử dụng bảng băm cho phép tra cứu với độ phức tạp thời gian trung bình là $O(1)$, 
trong khi Lists được triển khai dưới dạng danh sách liên kết đôi, cho phép thêm/xóa phần tử ở hai đầu một cách cực kỳ nhanh chóng.

Sự kết hợp của các yếu tố này tạo nên một triết lý thiết kế nhất quán: hiệu năng thông qua sự đơn giản và chuyên môn hóa. 
Mô hình đơn luồng chỉ thực sự hiệu quả bởi vì các thao tác được thực hiện trong bộ nhớ và do đó cực kỳ nhanh. 
Nếu các thao tác này yêu cầu I/O đĩa, luồng đơn sẽ bị chặn liên tục và mô hình sẽ thất bại. 
Điều này cho thấy một mối liên hệ nhân quả: **lưu trữ trong bộ nhớ cho phép mô hình đơn luồng phát huy hiệu quả.** 
Thiết kế này cũng ngụ ý rằng Redis được tối ưu hóa cho các tác vụ nhanh và không tốn nhiều CPU. 
Đối với các tác vụ tính toán nặng, kéo dài, Redis sẽ không phải là công cụ phù hợp.   

### 2.3. Các cấu trúc dữ liệu cốt lõi trong Redis
Sức mạnh thực sự của Redis nằm ở khả năng ánh xạ các key đơn giản tới các cấu trúc dữ liệu mạnh mẽ này. 
Dưới đây là các loại phổ biến nhất. 

#### Bảng 2. Các cấu trúc dữ liệu Redis và trường hợp sử dụng

<table>
  <thead>
    <tr>
      <th>Cấu trúc dữ liệu</th>
      <th>Mô tả</th>
      <th>Lệnh chính</th>
      <th>Trường hợp sử dụng phổ biến</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>String</td>
      <td>Chuỗi nhị phân an toàn (binary-safe), có thể lưu trữ bất cứ thứ gì từ văn bản đến đối tượng đã được serialize. Kích thước tối đa 512 MB.</td>
      <td><code>SET</code>, <code>GET</code>, <code>INCR</code>, <code>DECR</code></td>
      <td>Caching các đoạn HTML, JSON; lưu trữ đối tượng đã serialize; bộ đếm (counters) cho lượt xem, lượt thích.</td>
    </tr>
    <tr>
      <td>Hash</td>
      <td>Một bản đồ (map) chứa các cặp field-value. Rất hiệu quả về bộ nhớ để lưu trữ các đối tượng có cấu trúc.</td>
      <td><code>HSET</code>, <code>HGET</code>, <code>HGETALL</code></td>
      <td>Lưu trữ thông tin đối tượng như hồ sơ người dùng (tên, email, tuổi), thông tin sản phẩm.</td>
    </tr>
    <tr>
      <td>List</td>
      <td>Một danh sách các chuỗi được sắp xếp theo thứ tự chèn, được triển khai dưới dạng danh sách liên kết đôi (doubly linked list).</td>
      <td><code>LPUSH</code>, <code>RPUSH</code>, <code>LPOP</code>, <code>RPOP</code>, <code>LRANGE</code></td>
      <td>Triển khai hàng đợi (queues) cho các tác vụ nền; lưu trữ nhật ký hoạt động (activity feeds); capped collections.</td>
    </tr>
    <tr>
      <td>Set</td>
      <td>Một tập hợp không có thứ tự của các chuỗi duy nhất. Các thao tác thêm, xóa, kiểm tra tồn tại rất nhanh ($O(1)$).</td>
      <td><code>SADD</code>, <code>SREM</code>, <code>SISMEMBER</code>, <code>SMEMBERS</code></td>
      <td>Lưu trữ các tag cho một bài viết; theo dõi các lượt truy cập duy nhất; quản lý danh sách bạn bè, người theo dõi.</td>
    </tr>
    <tr>
      <td>Sorted Set (ZSET)</td>
      <td>Tương tự như Set nhưng mỗi thành viên được liên kết với một điểm số (score). Các thành viên được sắp xếp theo điểm số này.</td>
      <td><code>ZADD</code>, <code>ZRANGE</code>, <code>ZREVRANGE</code>, <code>ZRANK</code></td>
      <td>Bảng xếp hạng (leaderboards); hàng đợi ưu tiên (priority queues); rate limiting sử dụng cửa sổ thời gian.</td>
    </tr>
  </tbody>
</table>

### 2.4. Vòng đời của dữ liệu và tính nguyên tử
- **Tính nguyên tử (Atomicity):** Trong Computer Science, "nguyên tử" có nghĩa là một hoạt động không thể bị chia nhỏ 
và không thể bị gián đoạn. Do bản chất đơn luồng của Redis, mỗi lệnh riêng lẻ được thực thi một cách nguyên tử. 
Ví dụ, khi lệnh `INCR` (tăng giá trị) được thực thi trên một key, không có lệnh nào khác có thể xen vào giữa quá trình đọc giá trị cũ, 
tăng nó lên và ghi lại giá trị mới. Điều này đảm bảo rằng các hoạt động như bộ đếm sẽ luôn chính xác, 
ngay cả khi có hàng nghìn client cùng lúc thực hiện. Đây là nền tảng cho các ứng dụng như rate limiting.

- **Quản lý vòng đời dữ liệu (TTL):** Time-To-Live (TTL) là một tính năng cơ bản nhưng cực kỳ quan trọng của Redis. 
Các key trong Redis có thể được thiết lập để tự động bị xoá sau một khoảng thời gian nhất định. 
Điều này rất quan trọng cho việc quản lý bộ nhớ đệm, giúp ngặn chặn dữ liệu cũ và tự động giải phóng bộ nhớ.
  * `EXPIRE <key> <seconds>:` Lệnh để đặt TTL (tính bằng giây) cho một key đã tồn tại. 
  * `TTL <key>:` Lệnh để kiểm tra thời gian sống còn lại của một key. Giá trị trả về `-1` nếu key không có TTL, và `-2` nếu key không tồn tại. 
  * Nhiều lệnh ghi, như `SET`, cũng hỗ trợ tùy chọn `EX` để thiết lập giá trị và thời gian hết hạn trong cùng một thao tác nguyên tử.

TTL không chỉ là một công cụ quản lý bộ nhớ. Nó là một cơ chế tự phục hồi (self-healing) cho các hệ thống cache. 
Khi bạn cache một phản hồi API và TTL là 60 giây, bạn đang tạo ra một hợp đồng rõ ràng: "Dữ liệu này được coi là hợp lệ trong 60 giây".
Sau thời gian đó mục cache tự động biến mất. Điều này ngăn hệ thống phục vụ dữ liệu cũ vô thời hạn. 
Cơ chế vô hiệu hóa thụ động, tự động này đơn giản và ít bị lỗi hơn nhiều so với việc vô hiệu hóa chủ động (nơi bạn phải `DEL` một key một cách tường minh mỗi khi dữ liệu nguồn thay đổi). 
Đối với nhiều kịch bản caching, việc chọn một giá trị TTL phù hợp là chiến lược đơn giản và mạnh mẽ nhất để duy trì tính nhất quán của dữ liệu.

## Phần III. Tích hợp Redis vào Sanic - Hướng dẫn thực chiến
### 3.1. Thiết lập môi trường
Trước khi bắt đầu, hãy đảm bảo bạn đã cài đặt Python 3.7+ và có một máy chủ Redis đang chạy (có thể cài đặt cục bộ hoặc sử dụng Docker).

Tiếp theo, chúng ta cần cài đặt các thư viện cần thiết. Chúng ta sẽ sử dụng `aioredis`, 
thư viện tiêu chuẩn và hiện đại để giao tiếp với Redis một cách bất đồng bộ trong Python, cùng với Sanic.

```Bash
pip install "sanic[ext]"
pip install "aioredis[hiredis]"
```

Lưu ý: `[hiredis]` là một phần phụ thuộc tùy chọn giúp tăng tốc độ phân tích cú pháp giao thức Redis, được khuyến nghị cho môi trường sản xuất.

### 3.2. Quản lý kết nối chuyên nghiệp: Connection Pool
**Vấn đề với kết nối thông thường:** Việc tạo một kết nối mới đến Redis cho mỗi yêu cầu API là một cách làm cực kỳ kém hiệu quả. 
Mỗi lần kết nối mới đều phải trải qua quá trình bắt tay TCP (TCP handshake) và xác thực với Redis, tạo ra một lượng lớn chi phí và độ trễ không cần thiết, 
đi ngược lại mục tiêu sử dụng một cơ sở dữ liệu hiệu năng cao.   

**Giải pháp: Connection Pooling:** Connection pool là một "bộ đệm" chứa các kết nối cơ sở dữ liệu. 
Nó duy trì một tập hợp các kết nối được mở sẵn sàng để ứng dụng tái sử dụng. Khi một yêu cầu kết nối, 
nó sẽ mượn một kết nối từ pool và trả lại sau khi sử dụng xong. 
Điều này giúp giảm đáng kể độ trễ và mức tiêu thụ tài nguyên hệ thống. 

**Best Practices trong Sanic - Sử dụng Listeners vòng đời:** Cách tiếp cận mạnh mẽ và đúng đắn nhất để quản lý connection pool trong Sanic là sử dụng các trình lắng nghe sự kiện (event listeners)`before_server_start` và `after_server_stop`. 
* `@app.listener('before_server_start')`: Coroutine này chỉ chạy một lần duy nhất khi ứng dụng khởi động, trước khi nó bắt đầu nhận yêu cầu.
Đây là nơi hoàn hảo để khởi tạo `aioredis` connection pool và gắn nó vào ngữ cảnh ứng dụng (`app.ctx`) để có thể dễ dàng truy cập từ bất kỳ đâu trong ứng dụng.   

* `@app.listener('before_server_start')`: Coroutine này chạy một lần khi ứng dụng tắt. Đây là nơi chúng ta đóng connection pool một cách an toàn để giải phóng tất cả các kết nối và tài nguyên. 

Việc sử dụng các listener này thể hiện một nguyên tắc thiết kế quan trọng: vòng đời của một tài nguyên dùng chung và đắt đỏ (như connection pool)
nên được gắn chặt với vòng đời của chính ứng dụng. Pool nên tồn tại miễn là ứng dụng đang chạy và được dọn dẹp sạch sẽ khi ứng dụng dừng lại. 
Gắn pool vào `app.ctx` biến nó thành một đối tượng `singleton` được quản lý bởi framework, ngăn chặn tình trạng tạo ra các kết nối rải rác, không được quản lý. 

**Mã nguồn thiết lập:** Dưới đây là đoạn mã hoàn chỉnh để thiết lập connection pool trong ứng dụng Sanic của bạn.

```python
# file: server.py
import aioredis
from sanic import Sanic
from sanic.log import logger

# Khởi tạo ứng dụng Sanic
app = Sanic("MyRedisApp")

# Cấu hình thông tin kết nối Redis
REDIS_URL = "redis://localhost:6379/0"

@app.listener('before_server_start')
async def setup_redis(app, loop):
    """
    Khởi tạo connection pool trước khi server bắt đầu.
    Gắn pool vào app.ctx để truy cập toàn cục.
    """
    try:
        # aioredis.from_url tạo ra một client sử dụng connection pool bên trong
        app.ctx.redis = aioredis.from_url(
            REDIS_URL, 
            encoding="utf-8", 
            decode_responses=True # Tự động giải mã phản hồi từ bytes sang string
        )
        await app.ctx.redis.ping()
        logger.info("Redis connection pool established.")
    except Exception as e:
        logger.error(f"Could not connect to Redis: {e}")
        # Có thể dừng ứng dụng ở đây nếu Redis là bắt buộc
        # raise Exception("Failed to connect to Redis")

@app.listener('after_server_stop')
async def close_redis(app, loop):
    """
    Đóng connection pool sau khi server dừng.
    """
    if hasattr(app.ctx, 'redis') and app.ctx.redis:
        await app.ctx.redis.close()
        logger.info("Redis connection pool closed.")

# Các route và logic khác của ứng dụng sẽ ở đây...
```
Mô hình này đảm bảo rằng ứng dụng của bạn quản lý các kết nối Redis một cách hiệu quả, 
có khả năng phục hồi và sẵn sàng cho môi trường sản xuất.

## Phần IV. Triển khai 3 trường hợp điển hình với Sanic và Redis
Bây giờ, chúng ta sẽ áp dụng những kiến thức đã học để triển khai ba trường hợp sử dụng thực tế mà bạn đã đề cập.

### 4.1. Trường hợp 1: Caching phản hồi API
**Kịch bản:** Chúng ta có một endpoint `GET /products` thực hiện một truy vấn tốn kém đến cơ sở dữ liệu để lấy danh sách sản phẩm. 
Dữ liệu này được đọc rất thường xuyên nhưng ít khi thay đổi. Đây là một ứng cử viên hoàn hảo cho việc caching để giảm tải cho CSDL và cải thiện đáng kể thời gian phản hồi.

**Chiến lược đặt tên Key:** Một quy ước đặt tên key tốt là rất quan trọng để tránh xung đột và dễ dàng gỡ lỗi. 
Chúng ta sẽ áp dụng mẫu từ hình ảnh của bạn: `cache:{endpoint}:{params}`. Ví dụ, một yêu cầu đến `/products?page=1&sort=price` 
sẽ có key là `cache:/products:page=1&sort=price`.

**Logic triển khai (Mô hình Cache-Aside):** Đây là mô hình caching phổ biến và hiệu quả. 
1. Khi nhận được yêu cầu, trước tiên, tạo ra cache key dựa trên đường dẫn và các tham số truy vấn. 
2. Thử lấy (`GET`) dữ liệu từ Redis bằng cache key này. 
3. **Cache Hit (Tìm thấy trong cache):** Nếu dữ liệu tồn tại trong Redis, giải mã nó (ví dụ: từ chuỗi JSON) 
và trả về ngay lập tức cho client. 
4. **Cache Miss (Không tìm thấy trong cache):** Nếu dữ liệu không có trong Redis, 
tiếp tục thực hiện logic thông thường (truy vấn cơ sở dữ liệu).
5. Trước khi trả về phản hồi cho client, hãy mã hóa dữ liệu (ví dụ: thành chuỗi JSON) 
và lưu (`SET`) nó vào Redis với cache key đã tạo, kèm theo một thời gian hết hạn (`EX`) phù hợp (ví dụ: 60 giây).

**Mã nguồn ví dụ:** Dưới đây là một ví dụ hoàn chỉnh cho một route Sanic, triển khai mô hình Cache-Aside 
và đồng thời trả về các header HTTP Caching để tận dụng cả caching phía client.

```Python
# file: server.py (tiếp theo)
import json
import hashlib
from sanic.response import json as json_response

# Giả lập một hàm truy vấn CSDL chậm
async def fetch_products_from_db(page: int, sort: str):
    import asyncio
    await asyncio.sleep(1) # Giả lập độ trễ của CSDL
    return [{"id": i, "name": f"Product {i}", "price": i * 10} for i in range((page-1)*10, page*10)]

@app.get("/products")
async def get_products(request):
    # 1. Tạo cache key
    page = request.args.get("page", "1")
    sort = request.args.get("sort", "name")
    cache_key = f"cache:/products:page={page}&sort={sort}"
    
    redis_client = request.app.ctx.redis
    
    try:
        # 2. Thử lấy dữ liệu từ cache
        cached_data = await redis_client.get(cache_key)
        
        if cached_data:
            # 3. Cache Hit
            logger.info(f"Cache HIT for key: {cache_key}")
            products = json.loads(cached_data)
            
            # Tạo ETag từ hash của dữ liệu cache
            etag = hashlib.sha1(cached_data.encode()).hexdigest()
            
            # Kiểm tra header If-None-Match từ client
            if request.headers.get("if-none-match") == etag:
                return response.empty(status=304)
            
            headers = {
                "Cache-Control": "public, max-age=60",
                "ETag": etag
            }
            return json_response(products, headers=headers)

        # 4. Cache Miss
        logger.info(f"Cache MISS for key: {cache_key}")
        products = await fetch_products_from_db(int(page), sort)
        
        # 5. Lưu vào cache trước khi trả về
        products_json = json.dumps(products)
        await redis_client.set(cache_key, products_json, ex=60) # Cache trong 60 giây
        
        etag = hashlib.sha1(products_json.encode()).hexdigest()
        headers = {
            "Cache-Control": "public, max-age=60",
            "ETag": etag
        }
        return json_response(products, headers=headers)

    except Exception as e:
        logger.error(f"Error in /products endpoint: {e}")
        return json_response({"error": "An internal error occurred"}, status=500)
```

### 4.2. Trường hợp 2: Vô hiệu hoá JWT với Backlist
Vấn đề với JWT không trạng thái (Stateless): Một trong những ưu điểm chính của Json Web Tokens (JWT) 
là chúng không trạng thái. Máy chủ không cần lưu trữ thông tin phiên, chỉ cần xác thực chữ kỳ của token. 
Tuy nhiên, điều này tạo ra một nhược điểm: Khi người dùng đăng xuất, token vẫn hợp lệ cho đến khi nó hết hạn. 
Nếu token này bị đánh cắp, kẻ tấn công có thể sử dụng nó để truy cập hệ thống. 

**Giải pháp: Backlist sử dụng Redis:** Chúng ta có thể giải quyết vấn đề này bằng cách thêm vào một lượng trạng thái tối thiểu. 
Khi người dùng đăng xuất, chúng ta sẽ lưu trữ một định danh duy nhất của token (ví dụ: claim `jti` - JWT ID) vào một "danh sách đen"
(backlist) trong Redis. 

**Logic triển khai**
1. Tạo một middleware để bảo vệ các endpoint yêu cầu xác thực. 
2. Trong middleware, sau khi giải mã và xác thực token, trích xuất `jti` và thời gian hết hạn `exp`.
3. Kiểm tra xem `jti` này tồn tại trong backlist của Redis hay không. 
4. Nếu có, token sẽ bị thu hồi. Từ chối yêu cầu với lỗi `401 Unauthorized`
5. Nếu không, cho phép yêu cầu tiếp tục. 
6. Trong endpoint `/logout`
   * Trích xuất `jti` và `exp` từ token.
   * Tính toán thời gian sống còn lại của token. 
   * Lưu `jti` vào Redis với TTL bằng đúng thời gian sống còn lại đó. Điều này đảm bảo backlist không bị phình to vô hạn với các token đã hết hạn. 

```Python
# file: server.py (tiếp theo)
# Giả sử bạn có các hàm để tạo và giải mã token
# from my_jwt_utils import create_token, decode_token, JWT_SECRET
import jwt
import uuid
from datetime import datetime, timedelta, timezone

JWT_SECRET = "your-super-secret-key"
JWT_ALGORITHM = "HS256"

# Middleware để kiểm tra blacklist
@app.middleware("request")
async def check_jwt_blacklist(request):
    # Bỏ qua các endpoint không cần xác thực
    if request.path in ["/login", "/logout"]:
        return

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return # Hoặc trả về lỗi 401 nếu endpoint này là bắt buộc

    token = auth_header.split(" ")
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=)
        jti = payload.get("jti")
        if not jti:
            return json_response({"error": "Token is missing JTI"}, status=401)
        
        # Kiểm tra blacklist
        is_blacklisted = await request.app.ctx.redis.get(f"blacklist:{jti}")
        if is_blacklisted:
            return json_response({"error": "Token has been revoked"}, status=401)

    except jwt.ExpiredSignatureError:
        return json_response({"error": "Token has expired"}, status=401)
    except jwt.InvalidTokenError:
        return json_response({"error": "Invalid token"}, status=401)

@app.post("/login")
async def login(request):
    # Logic xác thực người dùng (username/password) ở đây
    #...
    
    # Nếu thành công, tạo token
    user_id = 123
    jti = str(uuid.uuid4())
    exp = datetime.now(timezone.utc) + timedelta(hours=1)
    
    payload = {
        "user_id": user_id,
        "exp": exp,
        "iat": datetime.now(timezone.utc),
        "jti": jti
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return json_response({"token": token})

@app.post("/logout")
async def logout(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return json_response({"error": "Missing token"}, status=400)

    token = auth_header.split(" ")
    redis_client = request.app.ctx.redis
    
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=)
        jti = payload.get("jti")
        exp = payload.get("exp")
        
        if not jti or not exp:
            return json_response({"error": "Invalid token payload"}, status=400)
            
        # Tính thời gian sống còn lại
        remaining_ttl = int(exp - datetime.now(timezone.utc).timestamp())
        
        if remaining_ttl > 0:
            # Thêm vào blacklist với TTL tương ứng
            await redis_client.set(f"blacklist:{jti}", "revoked", ex=remaining_ttl)
            
        return json_response({"message": "Successfully logged out"})

    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        # Token đã hết hạn hoặc không hợp lệ, không cần làm gì
        return json_response({"message": "Token is invalid or expired"})
```

### 4.3. Trường hợp 3: Giới hạn tần suất truy cập (Rate Limiting)
**Mục đích:** Bảo vệ API khỏi các hành vi lạm dụng, tấn công brute-force, 
và đảm bảo việc sử dụng tài nguyên một cách công bằng cho tất cả các client. 

**Thuật toán: Fixed Window Counter (Bộ đếm cửa sổ cố định):** Đây là một thuật toán đơn giản nhưng hiệu quả. 
Chúng ta sẽ đếm số lượng yêu cầu từ một IP hoặc người dùng cụ thể trong một khoảng thời gian cố định (ví dụ: 100 yêu cầu mỗi phút)

**Tại sao Redis là lựa chọn hoàn hảo:** Việc này đòi hỏi một bộ đếm dùng chung có tốc độ truy cập cực nhanh. 
Lệnh `INCR` nguyên tử của Redis được sinh ra để giải quyết chính xác bài toán này.

**Logic triển khai:** 
1. Tạo một middleware để xử lý logic rate limiting. 
2. Xác định một định danh cho client (ví dụ: địa chỉ IP của họ).
3. Tạo một key trong Redis cho client (ví dụ: địa chỉ IP của họ).
4. Sử dụng một pipeline (giao dịch) của Redis để đảm bảo tính nguyên tử cho hai thao tác: 
tăng bộ đếm và thiết lập thời gian hết hạn. 
5. Với mỗi yêu cầu, chúng ta sẽ `INCR` giá trị của key. 
6. Nếu giá trị trả về là 1 (tức là đây là yêu cầu đầu tiên trong cửa sổ thời gian), chúng ta sẽ đặt `EXPIRE` cho key đó (ví dụ: 60 giây).
7. Nếu giá trị bộ đếm vượt quá giới hạn cho phép (ví dụ: > 100), từ chối yêu cầu với mã trạng thái. `429 Too Many Requests`.

**Mã nguồn ví dụ:**

```Python
# file: server.py (tiếp theo)
from sanic.exceptions import SanicException

# Cấu hình Rate Limiting
RATE_LIMIT = 100  # 100 yêu cầu
RATE_LIMIT_WINDOW = 60  # trong 60 giây

class RateLimitExceeded(SanicException):
    status_code = 429
    quiet = True

@app.middleware("request")
async def rate_limiter(request):
    # Bỏ qua cho các route không cần rate limit nếu muốn
    # if request.path == "/healthcheck":
    #     return

    redis_client = request.app.ctx.redis
    ip = request.ip
    
    key = f"rate_limit:{ip}"
    
    try:
        # Sử dụng pipeline để đảm bảo tính nguyên tử
        pipe = redis_client.pipeline()
        pipe.incr(key)
        pipe.ttl(key)
        
        count, ttl = await pipe.execute()

        if ttl == -1:
            # Nếu key vừa được tạo (ttl = -1), đặt thời gian hết hạn
            await redis_client.expire(key, RATE_LIMIT_WINDOW)
            
        if count > RATE_LIMIT:
            raise RateLimitExceeded("Too many requests")
            
    except RateLimitExceeded as e:
        raise e
    except Exception as e:
        logger.error(f"Rate limiting error: {e}")
        # Trong trường hợp Redis lỗi, có thể cho phép yêu cầu đi qua
        # hoặc chặn tất cả tùy thuộc vào chính sách bảo mật
        pass
```

_Lưu ý: Đoạn mã trên sử dụng hai lệnh riêng biệt (`INCR` và `TTL` trong pipeline) và sau đó là `EXPIRE`. 
Một cách tiếp cận khác, đơn giản hơn nhưng có một race condition nhỏ, là `INCR` trước, 
sau đó kiểm tra nếu kết quả là 1 thì `EXPIRE`. Với `aioredis`, pipeline đảm bảo các lệnh được gửi cùng nhau, giảm độ trễ mạng._

## Phần V. Thao tác với Redis qua CLI

Báo cáo tập trung vào việc tích hợp Redis vào code, nhưng việc hiểu cách thao tác trực tiếp với Redis qua giao diện dòng lệnh (CLI) là một kỹ năng cực kỳ quan trọng để gỡ lỗi và kiểm tra dữ liệu.

### 5.1. Cài đặt & Chạy Redis (qua Docker)

Cách đơn giản và phổ biến nhất để chạy Redis cho môi trường phát triển là sử dụng Docker.
```bash
# Tải image Redis mới nhất từ Docker Hub
docker pull redis

# Chạy một container Redis, đặt tên là "my-redis-instance"
# -d: chạy ở chế độ detached (chạy nền)
# -p 6379:6379: ánh xạ cổng 6379 của máy bạn vào cổng 6379 của container
docker run --name my-redis-instance -d -p 6379:6379 redis
```

### 5.2. Kết nối và thao tác với Redis CLI

Sau khi container đang chạy, bạn có thể kết nối vào Redis CLI:
```bash
# Kết nối vào Redis CLI bên trong container đang chạy
docker exec -it my-redis-instance redis-cli
```

Bây giờ bạn đang ở trong giao diện dòng lệnh của Redis. Hãy thử các lệnh cơ bản:
```
# Kiểm tra kết nối, server sẽ trả về "PONG"
127.0.0.1:6379> PING
PONG

# Lưu một key-value. "OK" có nghĩa là thành công.
127.0.0.1:6379> SET user:100:name "John Doe"
OK

# Lấy giá trị của một key
127.0.0.1:6379> GET user:100:name
"John Doe"

# Đặt thời gian hết hạn cho key là 30 giây
127.0.0.1:6379> EXPIRE user:100:name 30
(integer) 1

# Kiểm tra thời gian sống còn lại (Time To Live) của key
127.0.0.1:6379> TTL user:100:name
(integer) 25  # (sẽ giảm dần)

# Xóa một key
127.0.0.1:6379> DEL user:100:name
(integer) 1

# Thử lấy lại key đã xóa, kết quả là (nil) - không tồn tại
127.0.0.1:6379> GET user:100:name
(nil)
```

### 5.3. Atomic Operations: MULTI / EXEC

Khi bạn cần thực hiện một chuỗi các lệnh và đảm bảo rằng không có client nào khác có thể xen vào giữa chừng, bạn cần một giao dịch (transaction). Trong Redis, giao dịch được thực hiện bằng cặp lệnh MULTI và EXEC.

- **MULTI:** Bắt đầu một khối giao dịch. Tất cả các lệnh tiếp theo sẽ được xếp vào hàng đợi (queued) thay vì thực thi ngay lập tức.
- **EXEC:** Thực thi tất cả các lệnh trong hàng đợi một cách nguyên tử.
- **DISCARD:** Hủy bỏ giao dịch, xóa sạch hàng đợi lệnh.

**Ví dụ với CLI:** Giả sử chúng ta muốn tăng số dư của một người dùng và đồng thời ghi lại một log giao dịch. Chúng ta muốn đảm bảo cả hai việc này đều xảy ra hoặc không có việc nào xảy ra.
```
127.0.0.1:6379> SET user:1:balance 1000
OK

# Bắt đầu giao dịch
127.0.0.1:6379> MULTI
OK

# Các lệnh này chỉ được xếp hàng, chưa thực thi
127.0.0.1:6379> DECRBY user:1:balance 200
QUEUED
127.0.0.1:6379> LPUSH user:1:transactions "DEBIT 200"
QUEUED

# Thực thi tất cả các lệnh trong hàng đợi
127.0.0.1:6379> EXEC
1) (integer) 800      # Kết quả của lệnh DECRBY
2) (integer) 1        # Kết quả của lệnh LPUSH (độ dài mới của list)
```

Trong `aioredis`, khi bạn sử dụng `pipeline(transaction=True)` (mặc định là True cho hầu hết các phiên bản), nó sẽ tự động bọc các lệnh của bạn trong MULTI và EXEC.

### 5.4. Monitoring cơ bản

Đây là các lệnh bạn thường dùng trong CLI để kiểm tra "sức khỏe" và trạng thái của server Redis.

**INFO:** Cung cấp một lượng lớn thông tin và số liệu thống kê về server. Rất hữu ích để kiểm tra mức sử dụng bộ nhớ, số lượng kết nối, số lệnh đã thực thi, v.v.
```
127.0.0.1:6379> INFO memory
# Memory
used_memory:1034048
used_memory_human:1010.00K
...
```

**MONITOR:** Đây là một lệnh gỡ lỗi mạnh mẽ, nó sẽ stream trực tiếp tất cả các lệnh mà server Redis nhận được.
```
127.0.0.1:6379> MONITOR
OK
1667528600.123456 [0 127.0.0.1:54321] "SET" "mykey" "hello"
1667528605.654321 [0 127.0.0.1:54321] "GET" "mykey"
```

**Cảnh báo:** Lệnh MONITOR rất tốn tài nguyên và có thể làm giảm hiệu năng của server. Tuyệt đối không sử dụng trên môi trường production trừ khi bạn đang thực sự cần gỡ một lỗi nghiêm trọng.

**FLUSHDB / FLUSHALL:** Các lệnh này dùng để xóa dữ liệu.

- **FLUSHDB:** Xóa tất cả các key trong cơ sở dữ liệu hiện tại bạn đang chọn.
- **FLUSHALL:** Xóa tất cả các key trong tất cả các cơ sở dữ liệu trên server Redis.

Đây là những lệnh có tính phá hủy cao, thường chỉ được sử dụng trong môi trường phát triển (development) hoặc kiểm thử (testing) để reset trạng thái.