# Xây dựng Notification Service với Websocket

## Sự chuyển dịch kiến trúc - Tại sao lại là WebSocket? 

Để hiểu sâu sắc về WebSocket, trước tiên chúng ta cần giải phẫu những hạn chế của các giao thức tiền nhiệm trong bối cảnh ứng dụng web thời gian thực.

### 1.1. Hạn chế của mô hinh Request-Response (HTTP)

Giao thức HTTP (Hypertext Transfer Protocol), nền tảng của WWW, được thiết kế theo mô hình request-response. 
Trong mô hình này, máy khách (client) luon là bên khởi xướng hội thoại. Máy chủ (server) là thụ động, nó không thể
tự động gửi dữ liệu cho client nếu không được hỏi trước. Đối với một hệ thống đi chợ tiện lợi, 
việc thông báo "sản phẩm hết hạn" hay "thành viên mới vào nhóm" đòi hỏi độ trễ thấp và tính kịp thời cao.


Điều này tạo ra một rào cản lớn cho các tính năng thông báo. Nếu server biết một sản phẩm vừa hết hạn, nó không có cách nào
để đẩy thông tin xuống cho user ngay lập tức. Trong quá khứ, các LTV đã phải sử dụng các kỹ thuật giả lập thời gian thực, 
nhưng chúng đều tồn tại những chúng đều tồn tại những nhược điểm chí mạng về hiệu năng. 

### 1.2. Phân tích các kỹ thuật giả lập thời gian thực

Trước khi WebSocket trở thành tiêu chuẩn, ba kỹ thuật chính được sử dụng: Short Polling, Long Polling và Server-Sent Events (SSE). 
Dưới dây là bảng so sánh chi tiết về các đặc tính kỹ thuật và hiệu năng của chúng so với WebSocket.


| Đặc tính | Short Polling | Long Polling | Server-Sent Events (SSE) | WebSocket |
|----------|---------------|--------------|--------------------------|-----------|
| **Cơ chế hoạt động** | Client gửi request định kỳ (vd: 5s/lần) | Client gửi request, Server giữ kết nối cho đến khi có dữ liệu | Kết nối HTTP đơn chiều, Server đẩy dữ liệu liên tục | Kết nối TCP hai chiều (Full-duplex), dữ liệu truyền qua lại tự do |
| **Độ trễ (Latency)** | Cao (phụ thuộc vào chu kỳ poll) | Trung bình (cần thiết lập lại kết nối sau mỗi msg) | Thấp (nhưng chỉ một chiều) | Cực thấp (Real-time) |
| **Tải Server (Load)** | Cực cao (xử lý headers liên tục) | Cao (giữ connections, reconnect liên tục) | Thấp | Thấp nhất (1 kết nối duy nhất) |
| **Băng thông (Bandwidth)** | Lãng phí (HTTP Header overhead lớn) | Lãng phí (Header gửi lại mỗi lần reconnect) | Hiệu quả | Rất hiệu quả (Header frame chỉ 2-14 bytes) |
| **Hướng dữ liệu** | Đơn chiều (Client pull) | Giả lập hai chiều | Đơn chiều (Server to Client) | Hai chiều (Bidirectional) |
| **Hỗ trợ Binary** | Có (thông qua HTTP) | Có | Không (chỉ text/UTF-8) | Có (hỗ trợ Binary frames) |

#### 1.2.1. Short Polling (Hỏi liên tục)

Kỹ thuật này giống như việc người dùng liên tục nhất F5. Client gửi Request: "Có thông báo mới không?". Server trả lời: "Không". 5 giây sau, quy trình lặp lại:
* **Vấn đề:** Nếu header HTTP request là 1KB (chứ Cookie, User-Agent), và bạn có 10.000 user online polling mỗi 5 giây, server phải xử lý 2MB dữ liệu rác mỗi giây chỉ để
trả lời "Không có gì mới". Điều này gây lãng phí băng thông và tài nguyên CPU khủng khiếp. 

#### 1.2.2. Long Polling (Hỏi và chờ)

Client gửi request. Server không trả lời ngay mà "treo" kết nối đó cho đến khi có dữ liệu (hoặc timeout). 
Ngay khi nhận được dữ liệu, client đóng kết nối và mở ngay một kết nối mới. 
* **Vấn đề:** Mặc dù giảm độ trễ, nhưung việc thiết lập và huỷ bỏ kết nối TCP/TLS liên tục vẫn tiêu tốn tài nguyên. Hơn nữa, việc quản lý thứ tự tin nhắn (message ordering) trong Long Polling rất phức tạp. 


#### 1.2.3. Server-Sent Events (SSE)

SSE cho phép server đẩy dữ liệu xuống client qua một kết nối HTTP dài hạn. 
* **Vấn đề:** SSE chỉ là đơn chiều (Server->Client). Nếu ứng dụng của bạn cần tính năng "Chat nhóm" hoặc user cần gửi xác nhận 
"Đã xem thông báo" (ACK) lại cho server, SSE buộc client phải dùng một request HTTP riêng biệt (AJAX) để gửi dữ liệu lên, làm phức tạp hoá kiến trúc ứng dụng. 


#### 1.2.4. WebSocket: giải pháp tối ưu cho Notification Service. 

WebSocket (được chuẩn hoá trong RFC 6455) giải quyết triệt để các vấn đề trên bằng cách cung cấp một kênh giao tiếp (full-duplex) (song công toàn phần) trên một kết nối TCP duy nhất. 
* **Kết nối bền vững (Persistent Connection):** Kết nối được thiết lập một lần và duy trì mãi mãi (cho đến khi một bên ngắt). Không còn gánh nặng của việc bắt tay (handshake) lại liên tục. 
* **Overhead cực thấp:** Sau khi kết nối được thiết lập, mỗi tin nhắn (frame) chỉ tốn thêm khoảng 2 đến 14 bytes cho phần header, so với hàng trăm bytes của HTTP Header. 
* **Hai chiều thực sự:** Server có thể đẩy thông báo sản phẩm hết hạn xuống client, và client có thể gửi ngay lập tức tín hiệu "Đã xem thông báo" lên server trên cùng một đường truyền. 

Đối với hệ thống "Convenient Shopping System", WebSocket là lựa chọn kiến trúc duy nhất đảm bảo được trải nghiệm người dùng mượt mà khi quy mô người dùng tăng lên, đặc biệt là với các tính năng tương tác nhóm và thông báo tức thời.   

## Chương 2: Giải phẫu giao thức WebSocket (Từ A-Z)

Để triển khai thành công, bạn không chỉ cần biết cách dùng thư viện, mà cần hiểu cơ chế bên dưới để xử lý lỗi (debugging) và bảo mật. 

### 2.1. Quá trình bắt tay (The Handshake)

Mọi kết nối WebSocket đều bắt đầu cuộc đời của nó như một HTTP Request bình thường. Đây gọi là quá trình "nâng cấp giao thức" (Protocol Upgrade). 

**Bước 1: Client xin nâng cấp**

```HTTP
GET /feed HTTP/1.1
Host: server.example.com
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ==
Sec-WebSocket-Version: 13
```

* `Upgrade: websocket`: Báo hiệu cho server biết client muốn chuyển sang giao thức WebSocket.
* `Connection: Upgrade`: Yêu cầu giữ kết nối này để nâng cấp.
* `Sec-WebSocket-Key`: Một chuỗi ngâu nhiên 16-byte được mã hoá Base64. Đây không phải là key bảo mật hay token xác thực user. Nó dung để đảm bảo server thực sự hiểu giao thức WebSocket chứ không phải là một HTTP server ngở ngẩn nào đó. 


**Bước 2: Server chấp nhận (Switching Protocols)**

Nếu server (Sanic) đồng ý, nó sẽ thực hiện một phép ma thuật: lấy `Sec-WebSocket-Key` của client, cộng thêm một chuỗi GUID cố định (`258EAFA5-E914-47DA-95CA-C5AB0DC85B11`), băm bằng SHA-1 rồi mã hoá Base64 kết quá đó. Server gửi trả về response 101: 

```HTTP
HTTP/1.1 101 Switching Protocols
Upgrade: websocket
Connection: Upgrade
Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo=
```

Sau dòng response này, kết nối HTPT chấm dứt về mặt logic, và kết nối TCP bên dưới được tái sử dụng để truyền dữ liệu WebSocket dạng binary (nhị phân). 

#### 2.2. Cấu trúc Frame (Khung dữ liệu)

Không giống HTTP gửi text thuần tuý, WebSocket gửi dữ liệu dưới dạng các "Frame". Hiểu về Frame giúp bạn hiểu tại sao WebSocket lại nhẹ và nhanh. 

Cấu trúc cơ bản của một WebSocket Frame (theo RFC 6455):

1. **FIN bit (1 bit):** Đánh dấu đây có phải là mảnh cuối cùng của tin nhắn không. WebSocket hỗ trợ gửi tìn nhắn lớn bằng cách chia nhỏ thành nhiều frame (Fragmentation). 
2. **OpCode (4 bits):** Định nghĩa loại dữ liệu của frame: 
   * `0x1`: Text Frame (Dữ liệu dạng chuỗi JSON/Text).
   * `0x2`: Binary Frame (Dữ liệu nhị phân, vd: ảnh, file). 
   * `0x8`: Connection Close (Yêu cầu đóng kết nối). 
   * `0x9`: Ping (Kiểm tra kết nối).
   * `0xA`: Pong (Trả lời kiểm tra kết nối).
3. **Mask bit (1bit):** Quy định dữ liệu có được mã hoá (mask) hay không. Theo chuẩn, tất cả frame từ Client gửi lên server bắt buộc phải được Mask để tránh lỗi cache proxy. Frame từ Server gửi xuống client thì không cần. 
4. **Payload Length:** Độ dài dữ liệu. 
5. **Payload Data:** Nội dung thực sự (ví dụ: chuỗi JSON thông báo). 

#### 2.3. Cơ chế Ping/Pong (Heartbeat)

Trong môi trường mạng thực tế, các thiết bị trung gian (Load Balancer, Router, Firewall) thường tự động cắt các kết nối TCP nhàn rỗi (idle)
sau một khoảng thời gian (thường là 60 giây). Để duy trì kết nối bền vững:
* **Ping:** Server hoặc Client gửi một frame có OpCode là `0x9`. 
* **Pong:** Bên nhận bắt buộc phải trả lời ngay lập tức bằng frame `0xA` kém theo nội dung của gói Ping. 

Việc này giúp hai bên biết đối phương còn sống và giữ cho đường truyền TCP luôn active, tránh bị Router cắt. 
