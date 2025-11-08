# Nginx - Reverse Proxy và góc nhìn phát triển lên API GATEWAY

[Phần 1. Giới thiệu về Nginx](#phần-1-giới-thiệu-về-nginx)
  * [Chương 1.1. Giải mã Nginx: Không chỉ là máy chủ Web](#chương-11-giải-mã-nginx-không-chỉ-là-máy-chủ-web)
  * [Chương 1.2. Kiến trúc hướng sự kiện (Event-Driven)](#chương-12-kiến-trúc-hướng-sự-kiện-event-driven)
  * [Chương 1.3. Các khái niệm cấu hình cốt lõi (ngữ pháp của Nginx)](#chương-13-các-khái-niệm-cấu-hình-cốt-lõi-ngữ-pháp-của-nginx)

[Phần 2. Tích hợp Nginx vào dự án Sanic của bạn](#phần-2-tích-hợp-nginx-vào-dự-án-sanic-của-bạn)
  * [Chương 2.1. Tại sao không nên để Sanic/Gunicorn "ra gió"?](#chương-21-tại-sao-không-nên-để-sanicgunicorn-ra-gió-)
  * [Chương 2.2: Cập nhật `docker-compose.yml` cho dự án `backend-training`](#chương-22-cập-nhật-docker-composeyml-cho-dự-án-backend-training)
  * [Chương 2.3. Tệp Nginx đầu tiên (Reverse Proxy cho Monolith)](#chương-23-tệp-nginx-đầu-tiên-reverse-proxy-cho-monolith)

[Phần 3. Cấu hình Nginx chuyên sâu (bảo mật và hiệu suất)](#phần-3-cấu-hình-nginx-chuyên-sâu-bảo-mật-và-hiệu-suất)
  * [Chương 3.1. Giải mã `proxy_set_header` (tại sao Sanic cần biết sự thật?)](#chương-31-giải-mã-proxy_set_header-tại-sao-sanic-cần-biết-sự-thật)
  * [Chương 3.2. Chấm dứt SSL (SSL Termination)](#chương-32-chấm-dứt-ssl-ssl-termination)
  * [Chương 3.3. Thực tế: Tự động hoá SSL với Let's Encrypt và Certbot](#chương-33-thực-tế-tự-động-hoá-ssl-với-lets-encrypt-và-certbot)

[Phần 4. Từ Monolith đến Nginx Microservices: Nginx trong vai trò API Gateway.](#phần-4-từ-monolith-đến-nginx-microservices-nginx-trong-vai-trò-api-gateway-)
  * [Chương 4.1. Tại sao Microservices cần một "cổng vào"?](#chương-41-tại-sao-microservices-cần-một-cổng-vào)
  * [Chương 4.2. Reverse Proxy vs. API Gateway (Bảng so sánh)](#chương-42-reverse-proxy-vs-api-gateway-bảng-so-sánh)
  * [Chương 4.3. Triển khai (Định tuyến dựa trên đường dẫn - Path-based Routing)](#chương-43-triển-khai-định-tuyến-dựa-trên-đường-dẫn---path-based-routing)
  * [Chương 4.4. Mở rộng quy mô (cân bằng tải - load balancing)](#chương-44-mở-rộng-quy-mô-cân-bằng-tải---load-balancing)

[Phần 5: Các tính năng API Gateway nâng cao và Tương lai](#phần-5-các-tính-năng-api-gateway-nâng-cao-và-tương-lai)
  * [Chương 5.1: Kiểm soát Truy cập (Rate Limiting)](#chương-51-kiểm-soát-truy-cập-rate-limiting)
  * [Chương 5.2: Xác thực (Authentication)](#chương-52-xác-thực-authentication)
  * [Chương 5.3. Nhìn ra ngoài Nginx: Kong và Traefik](#chương-53-nhìn-ra-ngoài-nginx-kong-và-traefik)

[Kết luận](#kết-luận)






## Phần 1. Giới thiệu về Nginx

Phần này đặt nền móng lý thuyết. Chúng ta sẽ không chỉ định nghĩa Nginx là gì, 
mà còn giải thích tại sao nó trở thành tiêu chuẩn vàng cho các ứng dụng web hiệu suất cao. 

### Chương 1.1. Giải mã Nginx: Không chỉ là máy chủ Web

NGINX là một phần mềm mã nguồn mở, hiệu suất cao. Mặc dù ban đầu nó được tạo như một máy chủ web, vai trò của nó trong 
các kiến trúc ứng dụng hiện đại đã vượt xa điều đó. Đối với một nhà phát triển backend, Nginx nên được xem là một công 
cụ đa năng, một con dao "thuỵ sĩ" cho việc xử lý lưu lượng truy cập mạng. 

Các vai trò chính của Nginx bao gồm: 
* **Reverse Proxy (Proxy ngược):** Nginx đứng trước ứng dụng backend, nhận tất cả các yêu cầu của người dùng và chuyển tiếp
(proxy) chúng đến các ứng dụng của bạn. 
* **Load Balancer (Bộ cân bằng tải):** Khi ứng dụng của bạn mở rộng và chạy nhiều bản sao (instances), Nginx có thể phân phối lưu 
lượng truy cập một cách thông minh giữa các bản sao đó để đảm bảo hiệu suất và khả năng chịu lỗi. 
* **HTTP Cache (bộ đệm):** Nginx có thể lưu trữ (cache) các phản hồi từ backend. Nếu một yêu cầu tương tự được thực hiện lại, 
Nginx sẽ trả về phản hồi từ bộ đệm mà không cần làm phiền đến ứng dụng Backend, giúp giảm tải đáng kể. 
* **API Gateway:** Trong bối cảnh microservices, Nginx hoạt động như một điểm vào duy nhất, định tuyến các yêu cầu API đến nhiều 
dịch vụ Backend khác nhau. 

Lịch sử của Nginx giải thích lý do tại sao nó lại quan trọng đến vậy. Nó được Igor Sysoev tạo ra vào năm 2002 với một mục tiêu cụ thể:
giải quyết **Vấn đề C10k** (xử lý 10.000 kết nối đồng thời). Các máy chủ web truyền thống tại thời điểm đó (như Apache) gặp khó khăn lớn 
về hiệu suất khi số lượng kết nối đồng thời tăng lên. Nginx được thiết kế ngay từ đầu để giải quyết vấn đề cốt lõi về hiệu suất và khả 
năng mở rộng này, đó là lý do tại sao nó trở thành lựa chọn hàng đầu cho các ứng dụng web có lưu lượng truy cập cao. 

### Chương 1.2. Kiến trúc hướng sự kiện (Event-Driven)

Câu hỏi quan trọng nhất là: Tại sao Nginx lại nhanh đến vậy?. Câu trả lời không nằm ở "tốc độ" của mã, mà ở cách nó xử lý các kết nối.

**Mô hình truyền thống (ví dụ: Apache với `mpm_prefork`):** Mô hình này thường sử dụng kiến trúc Process-per-connection (mỗi kết nối một tiến trình)
hoặc Thread-per-connection (mỗi kết nối một luồng). Khi một client mới kết nối, máy chủ sẽ tạo ra một process hoặc thread để xử lý toàn bộ kết nối đó. 
Nếu client đó chậm (ví dụ: mạng di động yếu), process/thread đó sẽ bị "treo" (blocked) trong khi chờ đợi client gửi dữ liệu. Với 10.000 kết nối chậm, 
bạn sẽ cần 10.000 process/thread, điều này cực kỳ lãng phí tài nguyên (CPU, RAM) và gây ra chi phí chuyển đổi ngữ cảnh (context-switching) khổng lồ. 

**Mô hình Nginx (Event-Driven, Asynchronous):** Nginx sử dụng một kiến trúc hoàn toàn khác: 
1. **Master Process:** Khi bạn khởi động Nginx, một tiến trình chủ (master process) sẽ chạy. Nó đọc tệp cấu hình (ví dụ: `nginx.conf`) và 
khởi chạy một số lượng nhỏ tiến trình thợ (worker process).
2. **Worker Process:** Đây là nơi điều kỳ diệu xảy ra. Thông thường, bạn sẽ cấu hình Nginx để chạy một worker cho mỗi lõi CPU. Mỗi worker 
process này chạy như một tiến trình đơn luồng (single-threaded) và không chặn (non-blocking).
3. **Vòng lặp sự kiện (Event Loop) & Máy trạng thái (State Machine):** Thay vì tạo một luồng cho mỗi kết nối, mỗi worker process chạy một "vòng lặp sự kiện" (event loop) 
hiệu quả cao. Nó lăng nghe các "sự kiện" trên tất cả các socket (kết nối) mà nó quản lý. Các sự kiện này có thể là "một kết nối vừa đến", "dữ liệu sẵn sàng để đọc từ client A", 
"backend Sanic đã trả về phản hồi cho client B".
4. **Hoạt động không chặn (Non-blocking I/O):** Khi một worker process xử lý một yêu cầu (ví dụ: đọc HTTP Header từ client A), nó sử dụng một máy trạng thái (state machine). 
Nếu nó phải chờ đợi một thao tác I/O (ví dụ: chờ backend Sanic xử lý nghiệp vụ), nó **không bị chặn**. Nó ngay lập tức lưu trạng thái của yêu cầu A và chuyển sang xử lý một sự kiện 
khác (ví dụ: gửi dữ liệu cho client C). Khi backend Sanic phản hồi, một sự kiện được tạo ra (ví dụ như "dữ liệu từ backend đã sẵn sàng"), và worker sẽ quay lại xử lý yêu cầu của A. 

Mô hình này cho phép một worker process duy nhất xử lý _hàng nghìn kết nối_ đồng thời. Chi phí tài nguyên cho mỗi kết nối là cực kỳ nhỏ (chỉ là một bộ mô tả tệp (file descriptor) 
và một chút bộ nhớ cho máy trạng thái). Đây là nguyên nhân trực tiếp dẫn đến việc Nginx sử dụng tài nguyên (RAM/CPU) cực kỳ thấp nhưng lại đạt được hiệu suất và khả năng mở rộng vượt trội.

### Chương 1.3. Các khái niệm cấu hình cốt lõi (ngữ pháp của Nginx)

Để làm việc với Nginx, bạn cần hiểu "ngữ pháp" của nó. Nginx bao gồm các "mô đun" (modules) được điều khiển bởi các chỉ thị (directives) mà bạn viết trong tệp cấu hình (thường là `nginx.conf`).

Các chỉ thị này được tổ chức trong các "khối" (block) hoặc "ngữ cảnh" (context) lồng nhau. Dưới đây là 4 khối quan trọng nhất bạn cần biết:
1. `http {...}`: Khối này định nghĩa bối cảnh cho tất cả các máy chủ HTTP. Hầu hết các cấu hình của bạn sẽ nằm trong khối này. Đây là nơi bạn định nghĩa các thứ toàn cục như `log_format` 
(định dạng log) hoặc `limit_req_zone` (vùng giới hạn yêu cầu).
2. `server {...}`: Mỗi khối `server` định nghĩa một máy chủ ảo (virtual server). Bạn có thể có nhiều khối `server` (ví dụ: một cho `api.yourdomain.com`), một cho `www.yourdomain.com`. 
Đây là nơi bạn định nghĩa Nginx nên `listen` (lắng nghe) trên cổng nào (ví dụ: 80 cho HTTP, 443 cho HTTPS) và `server_name` (tên miền) là gì.
3. `location {...}`: Đây là khối quan trọng nhất và được sử dụng nhiều nhất. Nó nằm bên trong một khối `server` và định nghĩa cách Nginx xử lý các yêu cầu cho các URI (đường dẫn) khác nhau. 
Ví dụ, `location/api/v1/` sẽ được xử lý khác với `location /static/`.
4. `upstream {...}`: Khối này định nghĩa một "nhóm" (pool) các máy chủ backend. Thay vì trỏ `proxy_pass` đến một IP:Port cố định, bạn trỏ nó đến một khối `upstream`. 
Điều này là chìa khoá cho việc cân bằng tải và khả năng chịu lỗi. 

Hiểu được hệ thống phân cấp `http` -> `server` -> `location` là chìa khoá để viết và gỡ lỗi cấu hình Nginx. Một chỉ thị được đặt trong `location` sẽ ghi đè lên chỉ thị tương tự  trong `server`.

## Phần 2. Tích hợp Nginx vào dự án Sanic của bạn

Đây là phần thực hành cốt lõi. Chúng ta sẽ áp dụng các khái niệm lý thuyết ở Phần 1 để tích hợp Nginx vào dự án `backend-training`, 
sử dụng `docker-compose.yml` đã được định nghĩa sẵn trong thư mục dự án.

### Chương 2.1. Tại sao không nên để Sanic/Gunicorn "ra gió"? 
Ứng dụng Sanic của bạn có thể tự chạy (app.run), và trong môi trường sản xuất, bạn có thể chạy nó thông qua một máy chủ ứng dụng WSGI/ASGI như Gunicorn. 
Vậy tại sao phải thêm một lớp Nginx phức tạp ở phía trước?

Câu trả lời nằm ở hiệu suất và bảo mật:

**Lý do 1: Hiệu suất phục vụ tệp tĩnh (tối ưu hoá cốt lõi):** Dự án của bạn có thể sẽ có các tệp tĩnh (static files) như CSS, Javascript, hình ảnh, hoặc tệp tài liệu (ví dụ: Swagger UI).
* Sanic (và hầu hết các framework Python khác) có thể phục vụ các tệp tĩnh, nhưng chúng làm điều đó **không hiệu quả.** Mỗi yêu cầu tệp tĩnh sẽ chiếm dụng một worker Python. 
Khi 1000 người dùng tải trang, họ có thể tạo ra 5000 yêu cầu tệp tĩnh, làm tê liệt khả năng xử lý nghiệp vụ của ứng dụng. 
* Nginx được sinh ra để làm việc này, nó sử dụng các cơ chế I/O cấp hệ điều hành (như `sendfile`) để gửi tệp trực tiếp từ đĩa cứng ra mạng mà không cần tải tệp vào không gian người dùng 
(user-space) của ứng dụng. Điều này mang lại hiệu suất tối đa và giải phóng hoàn toàn Sanic khỏi gánh nặng này. 

**Lý do 2: Bảo vệ Backend (tấm khiên "Buffering"):** Đây là một lý do quan trọng mà Gunicorn _khuyến nghị mạnh mẽ_ việc sử dụng một proxy server như Nginx ở phía trước. 
Lý do chính là để **"đệm cho các máy khách chậm" (buffer slow clients).** 
* **Kịch bản tấn công (ví dụ: Tấn công Slowloris):** Hãy tưởng tượng một kẻ tấn công mở 1000 kết nối đến Gunicorn/Sanic. Thay vì gửi một yêu cầu HTTP hoàn chỉnh, chúng gửi từng byte một, _cực kỳ chậm_.
* **Vấn đề:** Các worker của Gunicorn/Sanic sẽ bị "treo" (blocked) khi chờ đợi phần còn lại của yêu cầu đến. Nếu tất cả các worker của bạn đều bị treo, ứng dụng của bạn sẽ ngừng phục vụ người dùng hợp lệ. 
Đây là một hình thức tấn công Từ chối dịch vụ (DoS) hiệu quả. 
* **Giải pháp Nginx:** Nginx đứng ở phía trước như một "tấm khiên". Nó sẽ nhận toàn bộ yêu cầu từ client, dù client đó có chậm đến đâu. Nginx sẽ kiên nhẫn "đệm" (buffer) yêu cầu đó. **Chỉ khi** Nginx 
nhận được yêu cầu HTTP hoàn chỉnh, nó mới quay lại và chuyển tiếp (proxy) yêu cầu hoàn chỉnh đó đến Gunicorn/Sanic thông qua kết nối mạng nội bộ cực nhanh của Docker. 
* **Kết quả:** Worker của Sanic chỉ bận rộn trong vài mili giây để xử lý yêu cầu và trả về phản hồi, sau đó được giải phóng ngay lập tức. Nginx đã hấp thụ toàn bộ "sự chậm chạp" và "sự độc hại" của Internet. 

**Lý do 3: Tách biệt trách nhiệm (Seperation of Concerns):** Đây là một nguyên tắc thiết kế hệ thống tốt:
* **Sanic/Gunicorn:** Chỉ tập trung vào một việc: thực thi logic nghiệp vụ (business logic) của bạn. 
* **Nginx:** Xử lý tất cả các công việc của hạ tầng: Chấm dứt SSL (HTTPS), nén Gzip, ghi log truy cập, giới hạn tốc độ (rate limiting), phục vụ tệp tĩnh,...

### Chương 2.2: Cập nhật `docker-compose.yml` cho dự án `backend-training`

Bây giờ, hãy chỉnh sửa tệp `docker-compose.yml` ở gốc dự án của bạn:

```YAML
version: '3.8' # Sử dụng phiên bản mới

services:
  app: # Đây là service Sanic của bạn
    build:. # Dockerfile của bạn ở gốc
    # QUAN TRỌNG: Gỡ bỏ 'ports'
    # Chúng ta không muốn thế giới bên ngoài truy cập Sanic trực tiếp
    # ports:
    #   - "8000:8000"
    expose:
      - "8000" # Chỉ 'expose' (phơi bày) cổng cho các service khác trong mạng Docker
    env_file:
      -.env
    volumes:
      # Chúng ta cần một volume cho tệp tĩnh để Nginx có thể đọc
      -./app/static:/app/static # Giả sử tệp tĩnh của bạn nằm ở 'app/static'
    restart: unless-stopped
    # Thêm 'depends_on' nếu bạn có CSDL, ví dụ:
    # depends_on:
    #   - db

  nginx: # Đây là service Nginx mới của chúng ta
    image: nginx:1.25-alpine # Dùng bản 'alpine' cho nhẹ
    ports:
      - "80:80"   # Ánh xạ cổng 80 của máy chủ host vào cổng 80 của container Nginx
      - "443:443" # Ánh xạ cổng 443 (cho HTTPS sau này)
    volumes:
      # Mount tệp cấu hình tùy chỉnh của chúng ta vào container Nginx
      # :ro có nghĩa là 'read-only' (chỉ đọc)
      -./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      # Mount volume tệp tĩnh
      -./app/static:/var/www/static:ro # Nginx sẽ đọc tệp tĩnh từ đây
    depends_on:
      - app # Khởi động Nginx SAU KHI khởi động app
    restart: unless-stopped

# networks: # Không bắt buộc nếu dùng mạng 'default'
#   default:
#     driver: bridge
```
**Phân tích cấu hình `docker-compose.yml` mới:**
1. **Thêm service `nginx`:** Chúng ta đã định nghĩa một service mới tên là nginx sử dụng image chính thức nginx:alpine.

2. **Quản lý Cổng (Ports):** Chúng ta đã gỡ bỏ ports khỏi service app. Đây là một **best practice** về bảo mật. 
3. Chỉ có Nginx nên được tiếp xúc với mạng bên ngoài. Service `app` chỉ cần `expose` cổng `8000` để các service khác trong cùng một mạng Docker (cụ thể là nginx) có thể "nhìn thấy" nó.

4. **Volumes:** Chúng ta mount (gắn) hai thứ vào container nginx:
   * Tệp cấu hình `nginx/nginx.conf` của chúng ta, ghi đè lên cấu hình mặc định.
   * Thư mục tệp tĩnh `./app/static` vào một đường dẫn bên trong container Nginx (`/var/www/static`) để Nginx có thể đọc và phục vụ chúng.

5. **Networking:** Khi `nginx` và `app` được định nghĩa trong cùng một tệp `docker-compose.yml`, Docker Compose sẽ tự động đặt chúng vào một mạng ảo chung (thường tên là `backend-training_default`). 
Điều này cho phép `nginx` truy cập `app` bằng chính **tên dịch vụ (service name)**. Docker cung cấp một DNS nội bộ để phân giải app thành địa chỉ IP nội bộ của container app.

6. **`depends_on:`** Bằng cách thêm `depends_on: - app`, chúng ta ra lệnh cho Docker Compose khởi động service `app` trước khi khởi động service `nginx`. 
Tuy nhiên, cần lưu ý rằng `depends_on` chỉ đảm bảo container `app` đã khởi động, chứ không đảm bảo ứng dụng Sanic bên trong nó đã sẵn sàng nhận yêu cầu. 
Đối với môi trường production, bạn sẽ cần một cơ chế "health check" hoặc "wait-for-it" phức tạp hơn.


### Chương 2.3. Tệp Nginx đầu tiên (Reverse Proxy cho Monolith)

Bây giờ, hãy tạo nội dung cho tệp `nginx/nginx.conf` mà chúng ta đã tham chiếu ở trên. Đây là một cấu hình reverse proxy cơ bản nhất.

```Nginx
# 1. Định nghĩa một 'upstream' trỏ đến service 'app' của chúng ta
# Đây là một best practice, ngay cả khi chỉ có một máy chủ
upstream sanic_backend {
    # 'app' là tên service trong tệp docker-compose.yml
    # 8000 là cổng mà Sanic đang 'expose' bên trong mạng Docker
    server app:8000; 
}

# 2. Cấu hình máy chủ HTTP chính
server {
    listen 80; # Lắng nghe trên cổng 80 (HTTP)
    server_name localhost; # Chấp nhận yêu cầu đến 'localhost'
    
    # Cấu hình ghi log (tùy chọn nhưng nên có)
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;

    # 3. Khối location chính cho Reverse Proxy
    # Dấu '/' có nghĩa là khớp với MỌI yêu cầu
    location / {
        # Chuyển tiếp tất cả yêu cầu đến upstream đã định nghĩa ở trên
        proxy_pass http://sanic_backend; 
        
        # Các header quan trọng sẽ được giải thích ở Phần 3
        # Chúng báo cho Sanic biết thông tin về client gốc
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Phân tích cấu hình `nginx.conf`:

1. `upstream sanic_backend {... }`: Chúng ta định nghĩa một nhóm các máy chủ backend tên là `sanic_backend`. 
Hiện tại, nó chỉ có một máy chủ: `app:8000` (đây chính là tên service và cổng đã `expose` trong `docker-compose.yml`). 
Sử dụng `upstream` là một thói quen tốt, vì nếu sau này bạn muốn chạy 3 bản sao của app (cân bằng tải), 
bạn chỉ cần thêm chúng vào khối `upstream` này mà không cần thay đổi `location`.

2. `location / {... }:` Khối này khớp với mọi URI yêu cầu.

3. `proxy_pass http://sanic_backend;:` Đây là chỉ thị "ma thuật". Nó nói Nginx: "Lấy yêu cầu này và gửi nó đến một trong các máy chủ trong nhóm `sanic_backend`". 
Nginx sẽ xử lý tất cả các chi tiết kết nối.

Với hai tệp này (`docker-compose.yml` và `nginx.conf`), bạn có thể chạy `docker-compose up -d --build` từ thư mục gốc. 
Bây giờ, khi bạn truy cập `http://localhost` trên trình duyệt, Nginx sẽ nhận yêu cầu, chuyển tiếp nó đến service `app`, 
nhận phản hồi từ Sanic và trả về cho bạn.

## Phần 3. Cấu hình Nginx chuyên sâu (bảo mật và hiệu suất)

Bạn đã có một hệ thống chạy. Bây giờ, chúng ta sẽ làm cho nó hoạt động đúng và an toàn cho môi trường sản xuất (production).

### Chương 3.1. Giải mã `proxy_set_header` (tại sao Sanic cần biết sự thật?)
Khi Nginx làm proxy, ứng dụng Sanic của bạn sẽ bị "mù". Từ góc nhìn của Sanic, tất cả các yêu cầu đều đến từ một client duy nhất: 
container Nginx (ví dụ: từ một địa chỉ IP nội bộ như `172.20.0.5`).

Điều này phá vỡ nhiều thứ:
* **Ghi Log:** Log truy cập của Sanic sẽ chi ghi lại IP của Nginx, vô dụng cho việc phân tích. 
* **Bảo mật:** Bạn không thể cấm IP của kẻ tấn công ở tầng ứng dụng. 
* **Logic ứng dụng:** Các hàm tạo URL tuyệt đối (absolute URLs) có thể bị sai

Để khắc phục điều này, chúng ta phải "nói dối" Sanic một cách có chủ đích bằng cách sử dụng `proxy_set_header` 
để chuyển tiếp các header của client gốc. 

Đây là giải thích chi tiết về các dòng bạn đã thêm trong `nginx.conf`:
* `proxy_set_header Host $host`
  * **$host:** Là biến Nginx chứa tên miền (ví dụ: `yourdomain.com`) mà client đã gõ trên trình duyệt. 
  * **Tại sao:** Nếu không có header này, Nginx sẽ gửi header `Host` là tên của `upstream` (ví dụ: `sanic_backend`). 
  Sanic sẽ không biết client thực sự muốn truy cập tên miền nào. 

* `proxy_set_header X-Forwarded-Proto $scheme;`
  * **$scheme:** Là biến Nginx chứa giao thức mà client đã sử dụng (`http` hoặc `https` sau này).
  * **Tại sao:** Khi chúng ta triển khai SSL (HTTPS) ở Nginx, kết nối giữa Nginx và Sanic vẫn là HTTP. 
Header này báo cho Sanic biết rằng: "Mặc dù tôi (Nginx) đang nói chuyện với bạn bằng HTTP, nhưng client thực sự đang kết nối qua HTTPS".
Điều này rất quan trọng để Sanic tạo các URL chuyển hướng (redirect) hoặc URL tuyệt đối đúng giao thức `https://`

* `pxoxy_set_header X-Real-IP $remote_addr;`
  * **$remote_addr:** Là biến Nginx chứa địa chỉ IP của thứ kết nối trực tiếp đến Nginx (trong trường hợp này, đó là IP thật của người dùng).
  * **Tại sao:** Header `X-real-IP` (một header không chính thức nhưng phổ biến) cung cấp cho Sanic một cách đơn giản để biết IP của người dùng. 

* `proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;`
  * `X-Forwarded-For` **(XFF)** là một header tiêu chuẩn chứa một danh sách các địa chỉ IP mà yêu cầu đã đi qua: `client_ip`, `proxy1_ip`, `proxy2_ip`.
  * Biến **$proxy_add_x_forwarded_for:** là một biến Nginx thông minh. Nó sẽ lấy header `X-Forwareded-For` hiện có (nếu có) và nối (append) `$remote_addr` vào cuối danh sách. 
  * **So sánh X-Real-IP và X-Forwarded-For:** `X-Real-IP` thường chỉ chứa IP của client. `X-Forwarded-For` chứa toàn bộ "chuỗi proxy". 
Trong ứng dụng, bạn thường sẽ tin cậy IP đầu tiên (ngoài cùng bên trái) trong danh sách `X-Forwarded-For` (sau khi đã cấu hình `set_real_ip_from` để loại bỏ các IP của proxy đáng tin cậy). 
Gửi cả hai là một best practices. 

### Chương 3.2. Chấm dứt SSL (SSL Termination)

Trong môi trường production, bạn không bao giờ nên chạy ứng dụng trên HTTP. Bạn cần HTTPS. Tuy nhiên, bạn cũng **không bao giờ** nên cấu hình SSL (chứng chỉ HTTPS) bên trong ứng dụng Sanic/ Python. 
Đó là cơn ác mộng về quản lý và hiệu suất. 

Thay vào đó, chúng ta sử dụng một mẫu hình gọi là **"SSL Termination" (Chấm dứt SSL)**
* **Khái niệm:** Nginx sẽ là "thiết bị đầu cuối" (endpoint) cho kết nối SSL/HTTPS. 
* **Luồng hoạt động:**
  * Client (trình duyệt) <--- (kết nối **HTTPS**, đã mã hoá) ---> Nginx. 
  * Nginx giải mã yêu cầu (tiêu tốn CPU).
  * Nginx <--- (kết nối HTTP, không mã hoá) ---> Sanic (bên trong mạng Docker nội bộ)
* **Lợi ích:**
  * **Hiệu suất:** Giải mã SSL là một tác vụ nặng, tiêu tốn nhiều CPU. Hãy để Nginx (được viết bằng C, tối ưu cho I/O) làm việc này. Điều này giải phóng các worker Python của Sanic để tập trung 100% vào logic nghiệp vụ. 
  * **Quản lý tập trung:** Bạn chỉ cần cài đặt, cấu hình và gia hạn chứng chỉ SSL ở một nơi duy nhất (Nginx), thay vì phải cài đặt chúng trên mỗi service backend.

Để cấu hình SSL, bạn sẽ cần một tệp chứng chỉ (ví dụ: `fullchain.pem`) và một tệp khoá riêng (ví dụ: `privkey.pem`). Chúng ta sẽ tìm hiểu cách lấy chúng ở chương sau: 

Cập nhật `nginx/nginx.conf` để xử lý HTTPS:

```Nginx
upstream sanic_backend {... } # Giữ nguyên

# 1. Server block MỚI cho HTTP, chỉ để CHUYỂN HƯỚNG
server {
    listen 80;
    server_name yourdomain.com; # Thay 'localhost' bằng tên miền thật của bạn
    
    # Chuyển hướng vĩnh viễn (301) tất cả lưu lượng HTTP sang HTTPS
    return 301 https://$host$request_uri; 
}

# 2. Server block chính cho HTTPS
server {
    listen 443 ssl http2; # Lắng nghe trên cổng 443 (HTTPS) và bật 'ssl' và 'http2'
    server_name yourdomain.com;

    # 3. Chỉ định đường dẫn đến chứng chỉ SSL của bạn
    # Chúng ta sẽ lấy các tệp này từ Certbot ở chương sau
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # 4. Các cấu hình SSL bảo mật (Best Practice)
    ssl_protocols TLSv1.2 TLSv1.3; # Chỉ cho phép các giao thức bảo mật
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:ECDHE-RSA-AES128-GCM-SHA256';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m; # Bật cache phiên SSL để tăng tốc
    ssl_session_timeout 10m; #

    # 5. Các khối location (giữ nguyên như trước)
    location /static/ {
        alias /var/www/static/;
        expires 1d;
    }

    location / {
        try_files $uri $uri/ @proxy_to_app;
    }

    location @proxy_to_app {
        proxy_pass http://sanic_backend;
        
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        # Bây giờ $scheme sẽ tự động là 'https' cho các yêu cầu đến server block này
        proxy_set_header X-Forwarded-Proto $scheme; 
    }
}
```

### Chương 3.3. Thực tế: Tự động hoá SSL với Let's Encrypt và Certbot

Làm thế nào để có được các tệm `.pem` và `.key` ở trên? Dịch vụ miễn phí `Let's Encrypt` cung cấp chúng, 
và công cụ `Certbot` giúp tự động hoá quá trình này. 

Cách tốt nhất trong môi trường Docker là chạy Certbot trong một Container riêng. 

**Kế hoạch phối hợp (Orchestration):**
1. Certbot cần chứng bạn sở hữu tên miền. Nó sử dụng phương thức "HTTP-01 Challange", tức là nó sẽ tạo ra một tệp ngẫu nhiên và yêu cầu máy chủ Let's Encrypt truy cập tệp đó tại
`http://yourdomain.com/.well-known/acme-challange/<file_name>`.
2. Container Nginx của chúng ta phải có khả năng phục vụ tệp "challange" đó từ một thư mục chia sẻ. 
3. Container Certbot sẽ ghi tệp "challange" vào thư mục chia sẻ đó. 
4. Sau khi xác thực, Certbot sẽ tạo ra các tệp chứng chỉ (`.pem`, `.key`) và lưu chúng vào thư mục chia sẻ khác. 
5. Container Nginx phải đọc được các tệp chứng chỉ từ thư mục chia sẻ đó. 
6. Certbot cần chạy định kỳ để gia hạn (renew) chứng chỉ (chúng hết hạn sau 90 ngày).
7. Nginx cần tải lại (reload) cấu hính au khi chứng chỉ được gia hạn để sử dụng chứng chỉ mới. 

Đây là cách chúng ta thực hiện điều đó:

**Cập nhật `docker-compose.yml` (Phiên bản cuối cùng)**

```YAML
version: '3.8'
services:
  app:
    build:.
    expose: [ "8000" ]
    env_file: [ ".env" ]
    volumes:
      -./app/static:/app/static
    restart: unless-stopped

  nginx:
    image: nginx:1.25-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      -./nginx/nginx.conf:/etc/nginx/conf.d/default.conf:ro
      -./app/static:/var/www/static:ro
      # 1. Volume chia sẻ cho chứng chỉ (read-only)
      -./data/certbot/conf:/etc/letsencrypt:ro
      # 2. Volume chia sẻ cho tệp challenge (read-only)
      -./data/certbot/www:/var/www/certbot:ro
    depends_on:
      - app
    restart: unless-stopped
    # 3. Thêm lệnh này để Nginx tự động reload cấu hình 
    # mỗi 6 giờ, giúp nhận chứng chỉ mới
    command: /bin/sh -c 'while :; do sleep 6h & wait $${!}; nginx -s reload; done & nginx -g "daemon off;"'

  certbot: # 4. Service Certbot mới
    image: certbot/certbot
    volumes:
      # 5. Certbot cần ghi vào các volume này
      -./data/certbot/conf:/etc/letsencrypt
      -./data/certbot/www:/var/www/certbot
    # 6. Lệnh để chạy và tự động gia hạn mỗi 12 giờ
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

**Cập nhật `nginx/nginx.conf` (thêm xử lý challenge)**

Bạn cần sửa đổi khối `server { listen 80;... }` (khối HTTP) của mình:

```Nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Thêm khối location này TRƯỚC khi chuyển hướng
    # Để xử lý challenge của Certbot
    location /.well-known/acme-challenge/ {
        root /var/www/certbot; # Phục vụ tệp từ thư mục challenge đã chia sẻ
    }

    # Chuyển hướng tất cả các yêu cầu HTTP khác sang HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;
    
    # Mọi thứ khác giữ nguyên...
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    location /static/ {... }
    location / {... }
    location @proxy_to_app {... }
}
```
**Lần chạy đầu tiên (Lấy chứng chỉ):** Trước khi chạy `docker-compose up`, bạn cần lấy chứng chỉ lần đầu tiên. Chạy lệnh sau (thay `yourdomain.com` và `email` của bạn):

```bash
sudo docker-compose run --rm certbot certonly --webroot -w /var/www/certbot -d yourdomain.com --email your@email.com --agree-tos --no-eff-email
```

Lệnh này sẽ tạm thời khởi động service `nginx` (vì `certbot` cần nó để xác thực), chạy Certbot để lấy chứng chỉ, và lưu chúng vào thư mục `./data/certbot/conf`

Sau khi thành công, bạn có thể chạy `sudo docker-compose up -d --build`. Hệ thống của bạn hiện đã chạy trên HTTPS với chứng chỉ tự động gia hạn.

## Phần 4. Từ Monolith đến Nginx Microservices: Nginx trong vai trò API Gateway. 

Bây giờ, chúng ta thay đổi tư duy. Dự án `backend-training` của bạn phát triển thành công. Thay vì một ứng dụng `app` monolith, 
bạn quyết định tách nó thành nhiều dịch vụ nhỏ hơn (microservices), ví dụ: `user-service`, `courses-service`, và `subject-service`.

### Chương 4.1. Tại sao Microservices cần một "cổng vào"?
Bạn đã biết Nginx là một "reverse proxy". Khi một reverse proxy được đặt ở phía trước một hệ thống các microservices, thì nó được gọi là một **API Gateway.**

**Vấn đề khi không có Gateway:** Nếu bạn để ứng dụng di động hoặc ứng dụng web (client) gọi trực tiếp đến từng Microservices, bạn sẽ gặp phải các vấn đề nghiêm trọng:
1. **Client "quá thông minh":** Client phải biết địa chỉ 10 services khác nhau (ví dụ: `user.api.yourdomain.com`, `courses.api.yourdomain.com`,...). Điều này làm client trở nên phức tạp. 
2. **Quá "nói nhiều" (Chattiness):** Để tải một trang chi tiết về khoá học, ứng dụng di động của bạn có thể phải thực hiện 3 cuộc gọi API riêng biệt: `GET /courses/123` (lấy thông tin khoá học),
`GET /users/456` (lấy thông tin sinh viên), `GET /reviews/123` (lấy đánh giá). Ba cuộc gọi mạng riêng biệt là một thảm hoạ về độ trễ, đặc biệt là trên mạng di động. 
3. **Tái cấu trúc là không thể:** Giả sử bạn gộp `reviews-service` vào chung với `courses-service`. Điều này sẽ phá vỡ tất cả các client đang gọi đến `reviews.api.yourdomain.com`. 
Bạn không thể thay đổi kiến trúc backend mà không buộc tất cả client phải cập nhật. 

**Giải pháp (Mô hình API Gateway):**
* Tạo ra một "cổng vào" duy nhất (ví dụ: `api.yourdomain.com`). Client chỉ cần biết và nói chuyện với một địa chỉ này.
* Gateway **đóng gói (encapsulates)** kiến trúc nội bộ. Client không biết (và không cần biết) liệu có 1 hay 100 microservices ở phía sau. 
* Gateway có thể **tổng hợp (aggregates)** các cuộc gọi. Client chỉ cần `GET /api/course-details/123` một lần duy nhất. Gateway sẽ thay mặt client, gọi 3 services nội bộ (courses, users, reviews), 
tổng hợp dữ liệu lại và trả về một phản hồi JSON duy nhất. 

### Chương 4.2. Reverse Proxy vs. API Gateway (Bảng so sánh)

Một câu hỏi phổ biến là: "Sự khác biệt giữa Reverse Proxy và API Gateway là gì?"

Câu trả lời: **Một API Gateway là một Reverse Proxy, nhưng với các tính năng bổ sung.** Không phải mọi Reverse Proxy đều là API Gateway. 

Sự khác biệt nằm ở múc độ thông minh và các tính năng ở _Lớp 7 (Lớp ứng dụng)._ Nginx (Open Source) là một Reverse Proxy tuyệt vời và có thể hoạt động như một API Gateway cơ bản. 
Các công cụ như Nginx Plus (trả phí), Kong, hoặc Traefik là các API Gateway đầy đủ tính năng.

<table>
  <thead>
    <tr>
      <th>Tính năng</th>
      <th>Reverse Proxy (Nginx cơ bản)</th>
      <th>API Gateway (Nginx nâng cao, Kong)</th>
      <th>Mục đích</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Chuyển tiếp Yêu cầu (L7)</td>
      <td>✅</td>
      <td>✅</td>
      <td>Định tuyến lưu lượng đến backend.</td>
    </tr>
    <tr>
      <td>Chấm dứt SSL</td>
      <td>✅</td>
      <td>✅</td>
      <td>Xử lý HTTPS cho backend.</td>
    </tr>
    <tr>
      <td>Cân bằng tải</td>
      <td>✅</td>
      <td>✅</td>
      <td>Phân phối tải cho các bản sao.</td>
    </tr>
    <tr>
      <td>Phục vụ Tệp tĩnh</td>
      <td>✅</td>
      <td>⚠️ (Ít phổ biến)</td>
      <td>Giảm tải cho backend.</td>
    </tr>
    <tr>
      <td>Định tuyến (Path-Based)</td>
      <td>✅</td>
      <td>✅</td>
      <td><code>location /users/ &rarr; user-service</code>.</td>
    </tr>
    <tr>
      <td>Giới hạn Tốc độ (Rate Limiting)</td>
      <td>✅</td>
      <td>✅✅ (Nâng cao)</td>
      <td>"Bảo vệ API. Gateway có thể giới hạn theo user, theo API key."</td>
    </tr>
    <tr>
      <td>Xác thực &amp; Ủy quyền</td>
      <td>❌ (Cơ bản)</td>
      <td>✅✅✅ (Cốt lõi)</td>
      <td>"Xác thực JWT, API Key, OAuth."</td>
    </tr>
    <tr>
      <td>Chuyển đổi Yêu cầu/Phản hồi</td>
      <td>❌</td>
      <td>✅</td>
      <td>Thay đổi request/response (ví dụ: JSON sang XML).</td>
    </tr>
    <tr>
      <td>Khám phá Dịch vụ (Service Discovery)</td>
      <td>❌ (Tĩnh)</td>
      <td>✅ (Động)</td>
      <td>Tự động tìm backend mới khi chúng khởi động.</td>
    </tr>
    <tr>
      <td>Giám sát &amp; Phân tích</td>
      <td>❌ (Chỉ logs)</td>
      <td>✅✅</td>
      <td>Cung cấp dashboard, theo dõi độ trễ, tỷ lệ lỗi của từng API.</td>
    </tr>
    <tr>
      <td>Cấu hình Động qua API</td>
      <td>❌ (Tệp tĩnh)</td>
      <td>✅</td>
      <td>Thêm/thay đổi route mà không cần reload Nginx.</td>
    </tr>
  </tbody>
</table>

Bảng này trực quan háo "sự tiến hoá" từ Reverse Proxy thành API Gateway. Nó cho thấy Nginx Open Source có thể đưa bạn đi rất xa (đến tận "Rate Limiting"). 
Nhưng khi bạn cần các tính năng "động" (Service Discovery, Cấu hình API) hoặc "thông minh" (Xác thực JWT), bạn sẽ gặp phải giới hạn và cần xem xét các công cụ chuyên dụng hơn.

### Chương 4.3. Triển khai (Định tuyến dựa trên đường dẫn - Path-based Routing)

Đây là tính năng API Gateway cơ bản nhất mà bạn có thể làm với Nginx Open Source.

Giả sử `docker-compose.yml` của bạn bây giờ trông như sau (loại bỏ app monolith, thêm 2 microservices):

```YAML
services:
  user_service: # Service quản lý người dùng
    build:./user-service
    expose: [ "8001" ] # Chạy trên cổng 8001
    restart: unless-stopped
    
  course_service: # Service quản lý đơn hàng
    build:./course-service
    expose: [ "8002" ] # Chạy trên cổng 8002
    restart: unless-stopped
    
  nginx:
   ... # Cấu hình Nginx vẫn như cũ
    depends_on:
      - user_service
      - course_service
```

Bây giờ, chúng ta cập nhật `nginx/nginx.conf` để định tuyến yêu cầu đến đúng service dựa trên đường dẫn (path):

```Nginx
# Chúng ta không cần 'upstream sanic_backend' nữa

server {
    listen 443 ssl http2;
    server_name api.yourdomain.com; # Đổi sang tên miền API
    
    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;
    
    #... Các cấu hình SSL khác...

    # 1. Định tuyến cho User Service
    # Khớp với bất kỳ URI nào bắt đầu bằng /api/v1/users/
    location /api/v1/users/ {
        # 'proxy_pass' đến service 'user_service' trên cổng đã expose
        proxy_pass http://user_service:8001/;
        
        # Luôn gửi các header proxy quan trọng
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 2. Định tuyến cho Course Service
    # Khớp với bất kỳ URI nào bắt đầu bằng /api/v1/courses/
    location /api/v1/courses/ {
        proxy_pass http://course_service:8002/;
        
        # Gửi các header proxy
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 3. (Tùy chọn) Xử lý các yêu cầu không khớp
    location / {
        return 404; # Trả về lỗi 404 cho các đường dẫn không xác định
    }
}
```

**Một cạm bẫy phổ biến (Dấu `/` trong `proxy_pass`):** Cú pháp của `proxy_pass` rất "kỳ quặc" và là lỗi phổ biến nhất.

* `location /api/v1/users/ { proxy_pass http://host:port; }` (Không có `/` ở cuối):
  * Yêu cầu `GET /api/v1/users/1` sẽ được chuyển tiếp thành `GET /api/v1/users/1.`

* `location /api/v1/users/ { proxy_pass http://host:port/; }` (Có `/` ở cuối):
  * Yêu cầu `GET /api/v1/users/1` sẽ được chuyển tiếp thành `GET /1`. Nginx sẽ "cắt" phần URI khớp với location (tức là `/api/v1/users/`) và thay thế bằng `/`.

Hiểu rõ điều này là rất quan trọng để đảm bảo microservice của bạn nhận được đúng đường dẫn mà nó mong đợi. 

### Chương 4.4. Mở rộng quy mô (cân bằng tải - load balancing)

`course_service` của bạn đang trở nên phổ biến và bị quá tải. Bạn quyết định chạy 3 bản sao (instances) của nó để xử lý tải.

Trong một môi trường Docker thực tế, bạn sẽ dùng `docker-compose up --scale course_service=3` (trong development) hoặc Docker Swarm/Kubernetes (trong production).

Làm thế nào để Nginx biết về 3 bản sao này và phân phối tải? Đây là lúc khối `upstream` (đã giới thiệu ở 2.3) phát huy sức mạnh thực sự của nó.

Cập nhật `nginx/nginx.conf`

```Nginx
# 1. Định nghĩa một 'upstream' (nhóm cân bằng tải) cho course_service
upstream course_service_cluster {
    # Nginx sẽ phân giải tên 'course_service' thành TẤT CẢ các IP
    # của các container 'course_service' đang chạy (trong Docker Swarm/K8s)
    # Với Docker Compose cơ bản, Docker DNS sẽ trả về nhiều IP
    # hoặc bạn có thể phải liệt kê rõ ràng nếu tên không cố định
    server course_service:8002;
    
    # Nếu dùng docker-compose scale, tên container sẽ là 
    # backend-training_course_service_1,..._2,..._3
    # server backend-training_course_service_1:8002;
    # server backend-training_course_service_2:8002;
    # server backend-training_course_service_3:8002;
}

server {
   ... # Mọi thứ khác giữ nguyên

    location /api/v1/users/ {
        proxy_pass http://user_service:8001/;
       ...
    }

    # 2. Cập nhật location của Course Service
    location /api/v1/courses/ {
        # 3. Proxy đến NHÓM, thay vì một máy chủ duy nhất
        proxy_pass http://course_service_cluster/;
        
        # Các header proxy...
    }
}
```

Phân tích:

1. `upstream course_service_cluster:` Chúng ta đã định nghĩa một nhóm các máy chủ.

2. **Cân bằng tải:** Theo mặc định, Nginx sẽ sử dụng phương thức round-robin (lần lượt) để phân phối yêu cầu. 
Yêu cầu 1 đến server 1, yêu cầu 2 đến server 2, yêu cầu 3 đến server 3, yêu cầu 4 quay lại server 1.

3. **Các phương thức khác:** Nginx cũng hỗ trợ các phương thức cân bằng tải khác như `least_conn` (chuyển yêu cầu đến máy chủ có ít kết nối nhất) hoặc `ip_hash` (giữ một client luôn "dính" vào một máy chủ nhất định, 
hữu ích nếu bạn lưu session trên máy chủ đó).

4. **Khả năng chịu lỗi:** Bạn vừa đạt được khả năng mở rộng ngang (horizontal scaling) và khả năng chịu lỗi (fault tolerance). 
Nếu một trong 3 container `course_service` bị sập, Nginx sẽ phát hiện ra (sau một thời gian `timeout`) và tự động ngừng gửi lưu lượng đến nó, chỉ phân phối tải cho 2 container còn lại.

## Phần 5: Các tính năng API Gateway nâng cao và Tương lai
Bạn đã có một API Gateway cơ bản nhưng mạnh mẽ. Đây là những gì Nginx có thể làm tiếp theo, và khi nào bạn nên xem xét các công cụ khác.

### Chương 5.1: Kiểm soát Truy cập (Rate Limiting)
Một tính năng cốt lõi của API Gateway là bảo vệ các dịch vụ backend của bạn khỏi bị lạm dụng (ví dụ: một script spam API của bạn) hoặc tấn công DoS. 
Nginx thực hiện điều này rất hiệu quả bằng thuật toán "leaky bucket" (xô rò rỉ).

Cấu hình: Cần 2 chỉ thị:

1. `limit_req_zone`: (Đặt trong khối `http`) Định nghĩa một "vùng" (zone) bộ nhớ chia sẻ để theo dõi các client (thường là dựa trên IP).

2. `limit_req`: (Đặt trong `location`) Áp dụng "vùng" đó cho một `location` cụ thể.

Ví dụ (đặt trong `nginx/nginx.conf`):

```Nginx
http { # Thêm vào bên trong khối http, bên ngoài khối server
    # Định nghĩa 1 zone tên 'api_limit', dùng IP client làm key
    # Kích thước 10MB, tốc độ 10 yêu cầu/giây (10r/s)
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=10r/s;

    server {
        listen 443 ssl http2;
        server_name api.yourdomain.com;
       ...

        # Áp dụng cho một API cụ thể
        location /api/v1/courses/ {
            # Áp dụng zone 'api_limit'
            # burst=20: Cho phép 20 yêu cầu "vượt mức" vào hàng đợi
            # nodelay: Xử lý 20 yêu cầu burst ngay lập tức, không delay
            limit_req zone=api_limit burst=20 nodelay;
            
            proxy_pass http://course_service_cluster/;
           ...
        }

        # Hoặc áp dụng cho TOÀN BỘ API
        # location /api/v1/ {
        #    limit_req zone=api_limit burst=20 nodelay;
        #   ... (Cần cấu hình proxy phức tạp hơn ở đây)
        # }
    }
}
```
**Giá trị:** Với cấu hình này, bạn đã bảo vệ API `courses` của mình chỉ với vài dòng cấu hình ở Gateway. 
Bạn không cần phải viết bất kỳ logic giới hạn tốc độ nào trong code Python của `course-service`. Đây là một 
lợi ích lớn của API Gateway: tập trung hoá các mối quan tâm chung (cross-cutting concerns).

### Chương 5.2: Xác thực (Authentication)
Đây là một điểm quan trọng phân định rõ ràng Nginx Open Source và các giải pháp API Gateway chuyên dụng.
* **Kịch bản lý tưởng:** Một client gửi yêu cầu với header `Authorization: Bearer <jwt_token>`. API Gateway (Nginx) nên: 
  1. Tự mình kiểm tra chữ ký (signature) của JWT (sử dụng một khóa bí mật).

  2. Kiểm tra ngày hết hạn (expiration) và các "claims" khác.

  3. Nếu JWT hợp lệ, chuyển tiếp yêu cầu đến microservice.

  4. Nếu JWT không hợp lệ, trả về lỗi 401 Unauthorized ngay lập tức và không làm phiền đến microservice.

* **Thực tế:** Nginx Open Source **không thể** làm điều này một cách nguyên bản (natively).

* Khả năng `auth_jwt` (xác thực JSON Web Tokens) là một tính năng thương mại của **Nginx Plus** (phiên bản trả phí).

Đây thường là lý do chính khiến các tổ chức chuyển từ Nginx Open Source sang một API Gateway chuyên dụng (như Kong) 
hoặc trả tiền cho Nginx Plus. Việc để mọi microservice (user, course, subject...) tự xác thực JWT là một sự lặp lại code, 
lãng phí tài nguyên và rủi ro bảo mật.

### Chương 5.3. Nhìn ra ngoài Nginx: Kong và Traefik

Khi bạn đã thành thạo Nginx, bạn sẽ nhận thấy 2 nhược điểm lớn của nó trong bối cảnh Microservices/Docker: 
1. **Cấu hình tĩnh (static configuration):** Mỗi khi bạn thêm / thay đổi một `location` (ví dụ: thêm `subject-service`),
bạn phải sửa tệp `nginx.conf` và chạy lệnh `nginx -s reload`.
2. **Không có khám phá dịch vụ (no service discorvery):** Khi bạn chạy `docker-compose up --scale course_service=4`, 
Nginx không tự biết về container thứ 4. Bạn phải thủ công cập nhật khối `upstream`.

Hai công cụ sau đây được sinh ra để giải quyết chính xác các vấn đề này: 
1. **Kong: "Nginx với một API"** 
* **Phép ẩn dụ:** Nếu Nginx là một "chiếc xe thể thao" (nhanh, hiệu quả, nhưng phải lái thủ công), 
thì Kong là một "chiếc xe buýt du lịch" (được xây dựng trên nền tảng xe thể thao) - Kong sử dụng Nginx bên trong - nhưng có
tài xế, lịch trình, và hệ thống bán vé. 
* **Cách hoạt động:** Kong chạy Nginx bên trong, nhưng bạn không bao giờ chạm vào tệp `nginx.conf`. Thay vào đó, bạn cấu hình 
Kong thông qua một **Management API**. Ví dụ, để thêm một route mới, bạn gọi: `POST /routes` với một JSON định nghĩa route. 
Kong lưu cấu hình này vào cơ sở dữ liệu (PostgreSQL/Cassandra) và tự động tạo ra tệp `nginx.conf` tương ứng và reload Nginx. 

2. **Traefik: "API Gateway cho Docker"**
* **Cách hoạt động:** Traefik là một "Edge Router" hiện đại được thiết kế cho cloud-native. Nó không dùng tệp `.conf` tĩnh. 
Thay vào đó, nó lắng nghe các sự kiện của Docker (hoặc Kubernetes).
* Bạn cấu hình Traefik bằng cách thêm **"nhãn" (labels)** vào tệp `docker-compose.yml` của bạn. 

```YAML
services:
  user_service:
    image:...
    expose: [ "8001" ]
    labels:
      # Báo cho Traefik: "Tạo một route tên là 'users'"
      - "traefik.http.routers.users.rule=Host(`api.yourdomain.com`) && PathPrefix(`/api/v1/users`)"
      # Báo cho Traefik: "Route này trỏ đến service 'user_service' trên cổng 8001"
      - "traefik.http.services.users.loadbalancer.server.port=8001"
```

* **Lợi ích:** Khi bạn chạy `docker-compose up`, Traefik thấy label này và tự động tạo route. Khi bạn `scale` service `user-service`
lên 3 bản sao. Traefik tự động phát hiện ra 2 container mới và thêm chúng vào nhóm cân bằng tải. Nó cũng tích hợp Let's Encrypt tự động 
mà không cần service `certbot` riêng. 
* **Khi nào dùng:** Khi bạn ở trong một môi trường rất động (dynamic) như Docker/Kubernetes và muốn cấu hình được "gắn liền" với service (config-as-code), 
thay vì quản lý một tệp `nginx.conf` trung tâm.

**Bảng 2: So sánh Nginx vs. Kong vs. Traefik (Trong bối cảnh Docker/Microservices)**

<table>
  <thead>
    <tr>
      <th>Đặc điểm</th>
      <th>Nginx (Open Source)</th>
      <th>Kong (Open Source)</th>
      <th>Traefik</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Core Engine</td>
      <td>Nginx (Viết bằng C)</td>
      <td>Nginx (C) + Plugin Lua</td>
      <td>Tự viết bằng Go</td>
    </tr>
    <tr>
      <td>Phương thức Cấu hình</td>
      <td>Tệp tĩnh (.conf)</td>
      <td>Động (Dynamic) qua API / CSDL</td>
      <td>Động (Dynamic) qua Docker Labels / K8s CRD</td>
    </tr>
    <tr>
      <td>Service Discovery</td>
      <td>Thủ công (Phải sửa tệp upstream)</td>
      <td>Thủ công (Qua API) / Tích hợp Consul</td>
      <td>Tự động (Lắng nghe Docker/K8s)</td>
    </tr>
    <tr>
      <td>Tự động hóa SSL</td>
      <td>Thủ công (Cần Certbot/Script)</td>
      <td>Plugin (Cần cấu hình)</td>
      <td>Tích hợp sẵn (Rất dễ)</td>
    </tr>
    <tr>
      <td>Tính năng API Gateway</td>
      <td>Cơ bản (Routing, Rate Limit)</td>
      <td>Đầy đủ (Auth, Plugins, v.v.)</td>
      <td>Đầy đủ (Middleware, v.v.)</td>
    </tr>
    <tr>
      <td>Trường hợp dùng tốt nhất</td>
      <td>Reverse proxy, Load balancer, Gateway tĩnh.</td>
      <td>API Gateway tập trung, quản lý qua API.</td>
      <td>Gateway tự động cho Docker/Kubernetes.</td>
    </tr>
  </tbody>
</table>

## Kết luận
Báo cáo này đã đưa bạn đi từ con số không đến một cấu hình Nginx hoàn chỉnh, sẵn sàng cho sản xuất (production-ready) cho dự án Sanic của bạn. 
Chúng ta đã bắt đầu bằng cách hiểu tại sao Nginx nhanh (kiến trúc event-driven), sau đó áp dụng nó làm một "tấm khiên" (reverse proxy) cho ứng dụng monolith, 
tối ưu hóa tệp tĩnh và tự động hóa SSL.

Quan trọng nhất, chúng ta đã vạch ra con đường "tiến hóa" từ một reverse proxy đơn giản thành một API Gateway phức tạp. 
Bạn đã học cách sử dụng Nginx (Open Source) để thực hiện các chức năng API Gateway cơ bản nhưng mạnh mẽ, 
như định tuyến dựa trên đường dẫn (path-based routing) và cân bằng tải (load balancing) cho kiến trúc microservices.

Bạn cũng đã thấy được "vách đá" của Nginx Open Source—những giới hạn của nó, đặc biệt là trong việc xác thực JWT và cấu hình động. 
Bảng so sánh cuối cùng với Kong và Traefik cung cấp cho bạn một lộ trình rõ ràng cho tương lai khi hệ thống của bạn phát triển về quy mô và độ phức tạp.

Dự án backend-training của bạn là một nền tảng hoàn hảo. Bằng cách làm theo các bước trong sổ tay này, bạn không chỉ "thêm" Nginx vào dự án, 
mà bạn đang xây dựng một nền tảng hạ tầng mạnh mẽ, an toàn và có khả năng mở rộng—một kỹ năng thiết yếu cho bất kỳ kỹ sư backend nào.


