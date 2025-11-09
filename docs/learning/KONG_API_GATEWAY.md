# Xây dựng Kong API Gateway cho hệ thống Microservices

## Mục lục

[Phần 1: Nền tảng và kiến trúc của KONG GATEWAY](#phần-1-nền-tảng-và-kiến-trúc-của-kong-gateway)
 * [1.1. Từ Nginx đến Kong: Phân tích chuyển đổi cho kiến trúc sư](#11-từ-nginx-đến-kong-phân-tích-chuyển-đổi-cho-kiến-trúc-sư)
 * [1.2. Giải phẫu Kong: Mô hình Control Plane / Data Plane (CP/DP)](#12-giải-phẫu-kong-mô-hình-control-plane--data-plane-cpdp)
 * [1.3. Vai trò của OpenResty và Lua: "Bộ não" vận hành trên "Cỗ máy" Nginx](#13-vai-trò-của-openresty-và-lua-bộ-não-vận-hành-trên-cỗ-máy-nginx)

[Phần 2. Mô hình dữ liệu lõi (Core Entities) của Kong](#phần-2-mô-hình-dữ-liệu-lõi-core-entities-của-kong)
 * [2.1. Services: Ánh xạ đến Upstream Microservices](#21-services-ánh-xạ-đến-upstream-microservices)
 * [2.2. Routes: Định nghĩa điểm truy cập và quy tắc khớp (matching rules)](#22-routes-định-nghĩa-điểm-truy-cập-và-quy-tắc-khớp-matching-rules)
 * [2.3. Upstreams và Targets: Tối ưu hoá Load Balancing và Health Checks](#23-upstreams-và-targets-tối-ưu-hoá-load-balancing-và-health-checks)
 * [2.4. Consumers và Credentials: Quản lý danh tính client](#24-consumers-và-credentials-quản-lý-danh-tính-client)

[Phần 3. Lựa chọn mô hình triển khai (Topology) chiến lược](#phần-3-lựa-chọn-mô-hình-triển-khai-topology-chiến-lược)
 * [3.1. Phân tích chuyên sâu: DB-backed (truyền thống) vs. DB-less (khai báo)](#31-phân-tích-chuyên-sâu-db-backed-truyền-thống-vs-db-less-khai-báo)
 * [3.2. Best Practice: Mô hình DB-less cho tự động hoá và GitOps](#32-best-practice-mô-hình-db-less-cho-tự-động-hoá-và-gitops)
 * [3.3. Mô hình Hybrid (Hybrid Mode): Tách biệt Control Plane và Data Plane](#33-mô-hình-hybrid-hybrid-mode-tách-biệt-control-plane-và-data-plane)
 * [3.4. Ma trận so sánh các mô hình triển khai (Trade-off Matrix)](#34-ma-trận-so-sánh-các-mô-hình-triển-khai-trade-off-matrix)

[Phần 4. Lộ trình triển khai Production](#phần-4-lộ-trình-triển-khai-production)
 * [4.1. Kịch bản 1: Triển khai Độc lập với Docker Compose (Development & Simple VM)](#41-kịch-bản-1-triển-khai-độc-lập-với-docker-compose-development--simple-vm)
 * [Kịch bản 2: Tích hợp Kubernetes với Kong Ingress Controller (KIC)](#kịch-bản-2-tích-hợp-kubernetes-với-kong-ingress-controller-kic)
 * [4.3. Cấu hình mẫu: Triển khai KIC ở chế độ DB-less (Best Practice)](#43-cấu-hình-mẫu-triển-khai-kic-ở-chế-độ-db-less-best-practice)

[Phần 5. Quản lý cấu hình như mã (Configuration-as-Code) với GitOps](#phần-5-quản-lý-cấu-hình-như-mã-configuration-as-code-với-gitops)
 * [5.1. Triết lý GitOps và cấu hình khai báo (Declarative)](#51-triết-lý-gitops-và-cấu-hình-khai-báo-declarative)
 * [5.2. Hướng dẫn sử dụng `decK`: Đồng bộ hoá (Sync), khác biệt (Diff), và xác thực (Validate)](#52-hướng-dẫn-sử-dụng-deck-đồng-bộ-hoá-sync-khác-biệt-diff-và-xác-thực-validate)
 * [5.3. Xây dựng một đường ống (pipeline) CI/CD hoàn chỉnh cho Cấu hình Kong](#53-xây-dựng-một-đường-ống-pipeline-cicd-hoàn-chỉnh-cho-cấu-hình-kong)

[Phần 6. Ánh xạ và bảo mật Micorservices](#phần-6-ánh-xạ-và-bảo-mật-micorservices)
 * [6.1. Hướng dẫn: Ánh xạ Microservices (Services) tới các Lộ trình (Routes) công khai](#61-hướng-dẫn-ánh-xạ-microservices-services-tới-các-lộ-trình-routes-công-khai)
 * [6.2. Chiến lược Xác thực (Authentication) Toàn diện](#62-chiến-lược-xác-thực-authentication-toàn-diện)
 * [6.3. Triển khai các Plugin Bảo mật Thiết yếu (Rate Limiting, IP Restriction, CORS)](#63-triển-khai-các-plugin-bảo-mật-thiết-yếu-rate-limiting-ip-restriction-cors)

[Phần 7. Quản lý và điều khiển lưu lượng (traffic control) nâng cao](#phần-7-quản-lý-và-điều-khiển-lưu-lượng-traffic-control-nâng-cao)
 * [7.1. Cấu hình Active Health Checks và Passive Circuit Breakers](#71-cấu-hình-active-health-checks-và-passive-circuit-breakers)
 * [7.2. Các thuật toán Load Balancing (Round Robin, Consitent Hashing)](#72-các-thuật-toán-load-balancing-round-robin-consitent-hashing)
 * [7.3. Triển khai Canary Releases và BLue-Green Deployments](#73-triển-khai-canary-releases-và-blue-green-deployments)
 * [7.4. Caching: Tăng tốc phản hồi với Proxy Cache Plugin](#74-caching-tăng-tốc-phản-hồi-với-proxy-cache-plugin)

[Phần 8. Tích hợp Service Discovery và Observability (Khả năng quan sát)](#phần-8-tích-hợp-service-discovery-và-observability-khả-năng-quan-sát-)
 * [8.1. Tự động hoá phát hiện dịch vụ (Service Discovery)](#81-tự-động-hoá-phát-hiện-dịch-vụ-service-discovery)
 * [8.2. Chiến lược Logging: Tích hợp với ELK Stack và Grafana Loki](#82-chiến-lược-logging-tích-hợp-với-elk-stack-và-grafana-loki)
 * [8.3. Giám sát (Monitoring): Thiết lập Prometheus và Grafana](#83-giám-sát-monitoring-thiết-lập-prometheus-và-grafana)
 * [8.4. Truy vết phân tán (Distributed Tracing): OpenTelemetry và Jaeger](#84-truy-vết-phân-tán-distributed-tracing-opentelemetry-và-jaeger)

[Phần 9. Vận hành Production: High Availability (HA) và tinh chỉnh hiệu năng](#phần-9-vận-hành-production-high-availability-ha-và-tinh-chỉnh-hiệu-năng)
 * [9.1. Kiến trúc High Availability (HA) được khuyến nghị](#91-kiến-trúc-high-availability-ha-được-khuyến-nghị)
 * [9.2. Chiến lược mở rộng (Scaling): Horizontal vs. Vertical](#92-chiến-lược-mở-rộng-scaling-horizontal-vs-vertical)
 * [9.3. Tinh chỉnh hiệu năng: Tối ưu hoá Nginx Workers và `ulimit`](#93-tinh-chỉnh-hiệu-năng-tối-ưu-hoá-nginx-workers-và-ulimit)

[Phần 10. Lộ trình và danh sách kiểm tra (roadmap & checklist)](#phần-10-lộ-trình-và-danh-sách-kiểm-tra-roadmap--checklist)
 * [10.1. Danh sách kiểm tra (checklist) triển khai từ zero đến production](#101-danh-sách-kiểm-tra-checklist-triển-khai-từ-zero-đến-production)
 * [10.2. Quản lý vòng đời API (API Lifecycle Management) và Best Practices](#102-quản-lý-vòng-đời-api-api-lifecycle-management-và-best-practices)

[Kết luận](#kết-luận)


## Phần 1: Nền tảng và kiến trúc của KONG GATEWAY
### 1.1. Từ Nginx đến Kong: Phân tích chuyển đổi cho kiến trúc sư
Đối với một kiến trúc sư đã có nền tảng vững chắc về Nginx, việc chuyển sang Kong không phải là học lại từ đầu, 
mà là một sự nâng cấp chiến lược. Nginx là một "cỗ máy" (engine) proxy L4/L7 hiệu suất cao, nổi tiếng với khả năng xử lý 
sự kiện bất đồng bộ, non-blocking I/O và sự ổn định. Kong kế thừa toàn bộ "cỗ máy" này và sử dụng Nginx làm lõi proxy cốt lõi của mình. 

Sự khác biệt cơ bản nằm ở lớp quản lý (management plane). Nginx (mã nguồn mở) về cơ bản là một hệ thống tĩnh. Cấu hình của nó được định nghĩa trong các file 
`.conf`, và mọi thay đổi đều yêu cầu một hành động `reload` để áp dụng. Trong một kiến trúc microservices với hàng trăm dịch vụ thay đổi liên tục, việc quản lý 
hàng ngàn dòng file `.conf` và thực hiện `reload` liên tục là không khả thi, dễ gây lỗi và khó mở rộng. 

Kong giải quyết vấn đề này bằng cách bổ sung một "bỗ não" vào Nginx. Kong biến Nginx từ một reverse proxy tĩnh thành một API Gateway động. Thay vì chỉnh sửa file 
`.conf`, bạn tương tác với Kong thông qua một Admin RESTful (thường là port 8001) hoặc thông qua các file cấu hình khai báo (declarative configuration). 
Các plugin cho các tác vụ lặp đi lặp lại như xác thực, rate-limiting, và logging được trừu tượng hoá và có thể được áp dụng và thay đổi một cách linh hoạt mà không 
cần `reload` Nginx. 

Do đó, sự chuyển đổi của bạn không phải từ bỏ Nginx, mà là học cách sử dụng một lớp quản lý API tinh vi hơn cho chính proxy mà bạn đã tin tưởng và quen thuộc. 

### 1.2. Giải phẫu Kong: Mô hình Control Plane / Data Plane (CP/DP)

Để hiểu rõ kiến trúc của Kong, điều quan trọng là phải phân biệt hai thành phần chính của nó: **Control Plane (Mặt phẳng điều khiển - CP)** và **Data Plane (mặt phẳng dữ liệu - DP).**
1. **Data Plane (DP):** Đây chính là các worker Nginx. Nhiệm vụ duy nhất của DP là xử lý lưu lượng proxy thực tế. Nó thực thi các chính sách (plugins), thực hiện SSL/TLS termination, 
và định tuyến các request đến các microservices upstream. DP được thiết kế để có độ trễ cực thấp, hiệu suất cao và có thể được mở rộng (scale) độc lập. 

2. **Control Plane (CP):** Đây là "bộ não" của Kong. CP chứa Admin API (port 8001) và các giao diện quản lý (như Kong Manager). 
CP chịu trách nhiệm cấu hình từ người quản trị (ví dụ: "tạo một route mới", áp dụng "JWT plugins"), lưu trữ cấu hình từ người quản trị (ví dụ: "tạo một route mới"), "áp dụng JWT plugin", 
lưu trữ cấu hình đó trong database hoặc bộ nhớ, và sau đó đẩy (push) cấu hình đã được biên dịch xuốngh các node Data Planes. 

Trong một triển khai đơn giản, CP và DP có thể chạy chung trên cùng một node. Tuy nhiên, "best practice" cho môi trường production quy mô lớn, đặc biệt là trong các kiến trúc hybrid-cloud 
hoặc multi-cloud, là tách biệt chúng hoàn toàn (Hybrid Deployment).

Trong mô hình Hybrid, bạn chạy một cụm Control Plane tập trung (có thể được back-up bằng database) tại một trung tâm dữ liệu an toàn. Sau đó, bạn triển khai nhiều cụm Data Plane (chạy ở chế độ DB-less) 
tại các vùng, các cluster Kubernetes, hoặc các địa điểm biên (edge). Các DP này không cần kết nối trực tiếp database, mà chỉ cần nhận cấu hình đã được biên dịch từ CP. 
Kiến trúc này mang lại lợi ích vượt trội:
* **Bảo mật:** Giảm bề mặt tấn công. Chỉ CP (nằm trong mạng nội bộ) cần truy cập database. Admin API không bị lộ ra public. 
* **Hiệu suất:** DP trở nên hoàn toàn stateless. Mọi cấu hình đều nằm trong bộ nhớ, loại bỏ hoàn toàn độ trễ do truy cập database trên đường đi của request.
* **Độ tin cậy:** Các DP hoàn toàn độc lập. Nếu kết nối đến CP bị gián đoạn, các DP vẫn tiếp tục hoạt động bình thường với cấu hình cuối cùng mà chúng nhận được. 

### 1.3. Vai trò của OpenResty và Lua: "Bộ não" vận hành trên "Cỗ máy" Nginx

Vậy, làm thế nào Kong có thể "tiêm" logic động vào Nginx? Câu trả lời nằm ở **OpenResty.** Kong không được xây dựng trên Nginx thuần tuý, 
mà trên OpenResty, một bản phân phối Nginx đã được tăng cường sức mạnh. 

**OpenResty** tích hợp LuaJIT, một trình biên dịch Just-In-Time cực kỳ nhanh cho ngôn ngữ kịch bản Lua, vào thằng lõi Nginx. Nginx vốn có các móc (hooks) tại các giai đoạn (phases), 
khác nhau của vòng đời xử lý request (ví dụ: `rewrite`, `access`, `content`, `header_filter`, `body_filter`, `log`). OpenResty cho phép Kong đăng ký và thực thi các đoạn mã Lua tại bất kỳ
gaii đoạn nào trong số này. 

Toàn bộ hệ thống plugin của Kong được xây dựng trên cơ chế này. Khi bạn áp dụng một plugin, thực chất bạn đang nói với Kong: "Hãy chạy đoạn mã Lua này tại giai đoạn `access` của Nginx".
* **Ví dụ:** Plugin `jwt` là một file Lua đăng ký chạy tỏng giai đoạn `access`. Nó sẽ trích xuất JWT từ header, xác minh chữ ký, và nếu hợp lệ, nó cho phép request đi tiếp. 
Nếu không, nó ngắt requét và trả về lỗi 401.
* **Ví dụ:** Plugin `logging` đăng ký chạy trong giai đoạn `log`. Sau khi request đã hoàn tất và phản hồi được gửi đi, mã Lua của nó sẽ thu thập thông tin (status code, latency,...) 
và gửi đến một hệ thống logging bên ngoài (như ELK hoặc Loki).

Đây là lý do tại sao Kong vừa có hiệu suất của Nginx, vừa có sự linh hoạt của một nền tảng lập trình. Nó thực thi login nghiệp vụ (Lua) ngay bên trong vòng lặp sự kiện (event loop) hiệu suất cao của Nginx. 

## Phần 2. Mô hình dữ liệu lõi (Core Entities) của Kong
Để làm chủ Kong, bạn phải tư duy bằng các thực thể (Entities) của nó. Đây là các khối xây dựng cơ bản mà bạn sẽ định nghĩa qua API hoặc file YAML. 

### 2.1. Services: Ánh xạ đến Upstream Microservices
Một `services` là một thực thể trừu tượng đại diện cho một microservices upstream (dịch vụ backend) của bạn. Thuộc tính quan trọng nhất của nó là URL (hoặc các thành phần `protocol`, `host`, `port`, `path`) 
trỏ đến nơi mà microservices đó đang lắng nghe. 

Hãy xem `Service` như một bản đồ 1:1 tới microservices của bạn. Ví dụ, nếu bạn có một dịch vụ quản lý người dùng (`user-management-service`) đang chạy nội bộ tại `http://10.0.1.10:8080`, 
bạn sẽ tạo một Kong `Service` tên là `user-service` với `host` trỏ đến địa chỉ đó. `Service` tự không public ra ngoài; nó chỉ là một định nghĩa về "backend".

### 2.2. Routes: Định nghĩa điểm truy cập và quy tắc khớp (matching rules)

Một `Route` là thứ định nghĩa cách (và liệu) các request từ bên ngoài được định tuyến đến một `Service` cụ thể. `Route` là "frontend" hay điểm truy cập công khai. 

Các `Routes` định nghĩa các quy tắc khớp (matching rules) dựa trên các thuộc tính của request đến, 
chẳng hạn như `paths` (ví dụ: `/users`). `hosts` (ví dụ: `api.example.com`), hoặc `methods` (ví dụ: `GET`, `POST`)

Một trong những tính năng mạnh mẽ nhất của Kong là một `Service` có thể có nhiều `Routes` liên kết với nó. Trong các phiên bản Kong cũ, hai khái niệm này được gộp chung (gọi là "API"), 
nhưng việc tách rời chúng mang lại sự linh hoạt tối đa cho kiến trúc microservices: 
* Ví dụ: Cùng một `user-service` (đã định nghĩa ở trên) có thể được public qua hai `Routes` khác nhau: 
* 1. **Route 1 (cho public):** `hosts: ["api.example.com"]`, `paths: ["v1/users"]`.
* 2. **Route 2 (cho admin):** `hosts: ["admin.internal.com"]`, `paths: ["/users"]` (áp dụng plugin `ip-restriction`).

Sự tách biệt này cho phép bạn định nghĩa nhiều cách thức truy cập khác nhau cho cùng một logic nghiệp vụ backend. 

### 2.3. Upstreams và Targets: Tối ưu hoá Load Balancing và Health Checks
Đây là một khái niệm nâng cao và là "best practice" tuyệt đối cho môi trường production. Khi định nghĩa `host` của một Service, bạn có hai lựa chọn: 
1. **Cách đơn giản:** Đặt `host` là một DNS name (ví dụ: `user-service-lb`) (ví dụ: `user-service.default.svc.cluster.local`). Kong sẽ thực hiện DNS-based load balancing (thường là round-robin). 
Cách này đơn giản nhưng thiếu tính năng nâng cao. 
2. **Cách "Best Practices"**
   * Tạo một thực thể `Upstream` (ví dụ: `name: "user-service-lib"`). `Upstream` dại diện cho một "virtual hostname". 
   * Thêm các instance backend của bạn (ví dụ: IP và port của từng Pod/VM) làm các `Targets` cho `Upstream` đó. 
   * Cấu hình `Service` của bạn (từ 2.1) và đặt `host` của nó trỏ đến tên của `Upstream` (ví dụ: `host: "user-service-lb"`).

Tại sao phải phực tạp như vậy? Bởi vì chỉ khi sử dụng `Upstream` và `Target`, bạn mới có thể kích hoạt các tính năng production quan trọng nhất mà DNS-based balancing không thể cung cấp. 
* **Active Health Checks:** Kong chủ động ping các `Targets` để kiểm tra sức khoẻ. 
* **Passive Circuit Breakers:** Kong thụ động theo dõi traffic và tự động "ngắt mạch" (loại bỏ) các `Targets` đang trả về lỗi 5xx. 
* **Advanced Load Balancing:** Sử dụng thuật toán như `least-connections` (ít kết nối nhất) hoặc `consistent-hashing` (ghim một client vào một `Target`) cụ thể. 
* **Canary Deployments:** Dễ dàng điều khiển traffic bằng cách thay đổi `weight` (trọng số) của các `Targets`.

**Khuyến nghị:** Đối với bất kỳ microservice nào có nhiều hơn một instance, _luôn luôn_ sử dụng cặp `Upstream/Target` thay vì chỉ dựa vào `Service`, `host` DNS. 

### 2.4. Consumers và Credentials: Quản lý danh tính client
Một `Consumer` là một thực thể trừu tượng đại diện cho "ai đó" (hoặc "cái gì đó") đang sử dụng API của bạn. Đây có thể là một developer bên thứ ba, một ứng dụng di động, hoặc một microservice khác. 

`Consumer` tự nó không làm gì cả. Nó cần liên kết với `Credentials` (thông tin xác thực). Ví dụ, một `Consumer` tên "đối tác A" có thể là một `keyauth_credential` (một API key) và một `Consumer` tên 
"Ứng dụng di động" có thể có một `jwt_secret` (để xác minh JWT).

Các plugin xác thực (Authentication - AuthN) như `key-auth` hoặc `jwt` chịu trách nhiệm xác minh một credential đến (ví dụ: API Key cho header) và _liên kết_ request đó với một `Consumer` cụ thể. 

Đây là quy trình bảo mật cốt lõi trong Kong: 
1. Một request đến Kong, mang theo một `Credential` (ví dụ: `apikey: "abc12345"`).
2. Plugin `key-auth` (đã được áp dụng cho Route/Service) kiểm tra key "abc12345".
3. Kong phát hiện key này thuộc về `Consumer` "Đối tác A".
4. Từ thời điểm này trong request, Kong biết rằng request này đã được xác thực là "Đối tác A".
5. Bây giờ, các plugin khác (Authorization - AuthZ) có thể hành động. 
Plugin `rate-limiting` sẽ kiểm tra: "Đối tác A còn bao nhiêu request trong_phút_này?". 
Plugin `acl` sẽ kiểm tra: "Đối tác A có nằm trong nhóm 'admin' được phép truy cập endpoint này không?".

Sự trừu tượng hoá `Consumer` là chìa khoá. Nó tách rời login xác thực (bạn là ai?) khỏi logic _uỷ quyền_ và _chính sách_ (bạn được phép làm gì?)

## Phần 3. Lựa chọn mô hình triển khai (Topology) chiến lược
Đây là quyết định kiến trúc quan trọng nhất và phải được đưa ra trước khi bạn bắt đầu triển khai. 
Lựa chọn này sẽ ảnh hưởng sâu sắc đến cách bạn vận hành, tự động hóa và mở rộng hệ thống của mình.

### 3.1. Phân tích chuyên sâu: DB-backed (truyền thống) vs. DB-less (khai báo)
Kong hỗ trợ hai chế độ hoạt động cơ bản: 
1. **DB-backed (có database):** Đây là chế độ "classic". Kong kết nối với một database (PostgreSQL hoặc Cassandra) và lưu trữ tất cả cấu hình (services, routes, plugins, consumers) trong đó. 
* **Ưu điểm:** Admin API (port 8000) có đầy đủ chức năng đọc/ghi. Bạn có thể thay đổi cấu hình "nóng" (hot-reload) bất cứ lúc nào thông qua một lệnh `curl` hoặc giao diện GUI (như Kong Manager hoặc Konga). 
Rất linh hoạt và trực quan cho quản lý động. 
* **Nhược điểm:** Đưa vào một thành phần stateful (database). Bạn chịu trách nhiệm quản lý, backup, và đảm bảo HA cho cả cụm database, điều này làm tăng đáng kể sự phức tạp vận hành. 

2. **DB-less (không Database):** Đây là chế độ hiện đại. Kong không kết nối với bất kỳ database nào. Thay vào đó, khi khởi động, nó tải toàn bộ tệp cấu hình từ một file duy nhất (ví dụ: `kong.yml` hoặc JSON) vào bộ nhớ. 
* **Ưu điểm:** Vận hành cực kỳ đơn giản. Các node Kong trở nên hoàn toàn stateless, giống như các Nginx worker thuần tuý. Điều này lý tưởng cho tự động hoá, CI/CD, và các mẫu hình GitOps. 
* **Nhược điểm:** Admin API trở nên gần như read-only (chỉ đọc). Bạn không thể tạo một Route mới bằng cách gọi API. Để thay đổi cấu hình, bạn phải cập nhật file `kong.yml`, sau đó ra lệnh cho Kong tải lại (reload) toàn bộ file đó
(thông qua endpoint `/config` hoặc khởi động lại pod). 

### 3.2. Best Practice: Mô hình DB-less cho tự động hoá và GitOps
Đối với một hệ thống microservices mới được xây dựng trên các nguyên tắc cloud-native, **khuyến nghị "best practices" rõ ràng là sử dụng chế độ DB-less.**

Lý do là nó biến Kong từ một "ứng dụng" stateful cần được chăm sóc thành một "thành phần cơ sở hạ tầng" (infrastructure component) statelesss có thể dự đoán được. 
Cấu hình của Kong (`kong.yml`) giờ đây có thể được lưu trữ trong Git, trở thành "nguồn chân lý duy nhất" (Single Soucre of Truth).

Bạn sẽ phải cập một sự đánh đổi: bạn mất đi sự tiện lợi của việc "click-to-configure" trong GUI. Bù lại, bạn nhận được một hệ thống có thể lặp lại (repeatable), có thể kiểm toán (auditable), 
và hoạt động tự động. Mọi thay đổi cấu hình (ví dụ: thêm một route mới) giờ đây phải đi qua một quy trình Git chuẩn: tạo nhánh, tạo Pull Request, review, merge. Điều này giúp giảm "configuration driff"
(lệnh cấu hình) và tăng cường bảo mật. 

### 3.3. Mô hình Hybrid (Hybrid Mode): Tách biệt Control Plane và Data Plane

Mô hình Hybrid là sự kết hợp tinh vi của cả hai thế giới, 
được thiết kế cho các tổ chức quy mô lớn (ví dụ: Fortune 500) với các yêu cầu phức tạp về multi-cloud hoặc bảo mật.

Kiến trúc này hoạt động như sau:

1. Bạn chạy một (hoặc một cụm) **Control Plane (CP)** ở chế độ **DB-backed.** 
CP này chạy Admin API và kết nối với database. Nó nằm ở một nơi an toàn, tập trung.

2. Bạn chạy nhiều cụm **Data Plane (DP)** ở chế độ **DB-less.** 
Các DP này được triển khai ở biên (edge), gần với người dùng hoặc ứng dụng của bạn.

3. CP chịu trách nhiệm biên dịch cấu hình từ database và đẩy (push) cấu hình đó đến các DP, 
các DP này chỉ cần tải cấu hình vào bộ nhớ.

4. Mô hình này giải quyết được vấn đề mà người dùng trong gặp phải: 
"Tôi có hàng ngàn consumer và không muốn quản lý tất cả chúng trong một file YAML."

Với Hybrid Mode:

1. **Quản lý tập trung:** Bạn vẫn có một Admin API (trên CP) có thể đọc/ghi để dễ dàng quản lý các thực thể thay đổi thường xuyên (như Consumers và Credentials).

2. **Triển khai phi tập trung:** Các DP ở biên là stateless, nhẹ, và có độ trễ cực thấp vì chúng không bao giờ cần truy vấn database cho mỗi request.

3. **Bảo mật tối đa:** Chỉ CP cần truy cập DB. Các DP có thể bị cô lập hoàn toàn.

**Khuyến nghị:** Nếu bạn là một tổ chức lớn, có nhiều team, nhiều môi trường, hoặc triển khai đa đám mây, Hybrid Mode là kiến trúc production tối ưu. 
Nếu bạn đang xây dựng một hệ thống đơn lẻ, khép kín (ví dụ: chạy toàn bộ trên một cluster Kubernetes), chế độ DB-less thuần túy (sẽ được mô tả trong Phần 4) là đủ và đơn giản hơn.

### 3.4. Ma trận so sánh các mô hình triển khai (Trade-off Matrix)
Quyết định triển khai là một sự đánh đổi. Bảng dưới đây tóm tắt các yếu tố chính cần xem xét:

<table>
  <thead>
    <tr>
      <th>Đặc tính</th>
      <th>Chế độ DB-backed (Classic)</th>
      <th>Chế độ DB-less</th>
      <th>Chế độ Hybrid</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Quản lý Trạng thái</td>
      <td>Stateful (Database Postgres/Cassandra)</td>
      <td>Stateless (File kong.yml trong bộ nhớ)</td>
      <td>CP (Stateful), DP (Stateless)</td>
    </tr>
    <tr>
      <td>Admin API</td>
      <td>Đọc/Ghi (Port 8001)</td>
      <td>Gần như Chỉ Đọc (Port 8001)</td>
      <td>CP (Đọc/Ghi), DP (Chỉ Đọc)</td>
    </tr>
    <tr>
      <td>Tự động hóa CI/CD</td>
      <td>Khó khăn. Phải dùng decK để sync</td>
      <td>Lý tưởng. File YAML là SSoT</td>
      <td>Lý tưởng. Dùng decK/API trên CP</td>
    </tr>
    <tr>
      <td>Độ trễ Data Plane</td>
      <td>Thấp (nhưng có thể có DB lookup cache)</td>
      <td>Thấp nhất (In-memory, không DB lookup)</td>
      <td>Thấp nhất (In-memory, không DB lookup)</td>
    </tr>
    <tr>
      <td>Độ phức tạp Vận hành</td>
      <td>Cao (Phải quản lý DB HA)</td>
      <td>Thấp (Stateless)</td>
      <td>Rất cao (Phải quản lý cả CP, DP, và DB)</td>
    </tr>
    <tr>
      <td>Kịch bản Phù hợp</td>
      <td>Thử nghiệm, quy mô nhỏ, GUI-driven</td>
      <td>Cloud-native, K8s, GitOps, Tự động hóa</td>
      <td>Doanh nghiệp lớn, Multi-cloud, Bảo mật cao</td>
    </tr>
  </tbody>
</table>

## Phần 4. Lộ trình triển khai Production
Dựa trên các lựa chọn kiến trúc ở Phần 3, đây là các lộ trình triển khai thực tế. 
"Best practice" cho một hệ thống microservices hiện đại là Kịch bản 2.

### 4.1. Kịch bản 1: Triển khai Độc lập với Docker Compose (Development & Simple VM)

Đây là cách tuyệt vời để bắt đầu phát triển và thử nghiệm cục bộ. 
Bạn sẽ sử dụng Docker Compose để quản lý các container.

**Lựa chọn A: DB-backed (Truyền thống)** `docker-compose.yml` của bạn sẽ định nghĩa ít nhất 3 services:

1. `kong-database:` Một container PostgreSQL.

2. `kong-migrations:` Một container Kong chạy một lần (one-shot) với lệnh `kong migrations bootstrap` để khởi tạo schema database.

3. `kong-gateway:` Container Kong chính, được cấu hình để kết nối đến `kong-database.`

**Lựa chọn B: DB-less (khuyến nghị để học)** `docker-compose.yml` của bạn sẽ không có database:
1. Tạo một file `kong.yml` trong thư mục `api-gateway/`.
2. Container `kong-gateway` của bạn sẽ có các biến môi trường:
* `KONG_DATABASE=off`
* `KONG_DECLERATIVE_CONFIG=/api-gateway/kong.yml`
3. Mount thư mục cấu hình: `volumes: -./api-gateway:/api-gateway.`

Bắt đầu với Lựa chọn B sẽ buộc bạn phải học cách viết cấu hình khai báo (declarative) ngay từ đầu, đây là kỹ năng quan trọng nhất cho production.

### Kịch bản 2: Tích hợp Kubernetes với Kong Ingress Controller (KIC)

Đây là phương pháp "best practice" duy nhất và được hỗ trợ đầy đủ để chạy Kong trong Kubernetes. 

Thay vì bạn phải quản lý cấu hình Kong (như Services, Routes) một cách thủ công, **Kong Ingress Controller (KIC)** sẽ làm việc này tự động. 
KIC là một controller (control plane) chạy bên trong K8s, nó liên tục dịch (translate) các tài nguyên native của Kubernetes như 
(Ingress, HTTPRoute, và các CRD đặc biệt của Kong) thành cấu hình Kong (data plane).

Quy trình làm việc sẽ như sau: 
1. Bạn triển khai microservice của mình (ví dụ: `user-service`) và tạo một K8s `Service` (ví dụ: user-svc) cho nó. 
2. Bạn tạo một K8s `Ingress` (hoặc CRD `KongIngress`) định nghĩa: "Tôi muốn public `user-svc` tại đường dẫn `/users`".
3. KIC (Control Plane) phát hiện `Ingress` mới này. 
4. KIC tự động tạo ra một Kong `Service` và Kong `Route` tương ứng bên trong Kong (Data Plane) để thực thi quy tắc đó. 

### 4.3. Cấu hình mẫu: Triển khai KIC ở chế độ DB-less (Best Practice)

Kong cung cấp một Helm chart chính thức để cài đặt KIC một cách dễ dàng. 
Điều quan trọng là, chế độ cài đặt mặc định và được khuyến nghị của Helm Chart chính là **DB-less.**

Lộ trình triển khai K8s production:
1. Thêm King Helm repo: `helm repo add kong https://charts.konghq.com`.
2. Cập nhật repo: `helm repo update`.
3. Cài đặt KIC vào namespace `kong`: `helm install kong kong/ingress -n kong --create-namespace`

Trong kịch bản này, một pod KIC sẽ chứa container: một container (Control Plane) và một Kong gateway (Data Plane).

Một điểm khác biệt quan trọng cần lưu ý: KIC (ở chế độ DB-less) không sử dụng file `kong.yml` như kịch bản 1. Vậy cấu hình lưu ở đâu? 

Câu trả lời là: **Nguồn chân lý (source of truth) là chính K8s API server (etcd).** KIC (control plane) liên tục theo dõi (watch) K8s API Server. 
Khi bạn `kubectl apply` một `Ingress`, KIC sẽ nhận được sự kiện đó, xây dựng cấu hình Kong mong muốn trong bộ nhớ, và đẩy nó vào các pod Kong (data plane). 
Đây là một kiến trúc cloud-native thực thụ, tận dụng K8s làm "database" cấu hình của mình. 

## Phần 5. Quản lý cấu hình như mã (Configuration-as-Code) với GitOps
### 5.1. Triết lý GitOps và cấu hình khai báo (Declarative)

Nguyên tắc cốt lõi của GitOps là Git đóng vai trò là "nguồn chân lý duy nhất" (single source of truth). Đề làm được điều này, cấu hình của bạn phải có tính khai báo (declarative)
* **Imperative (mệnh lệnh):** "Kong, hãy tạo một service. Sau đó, tạo một route. Sau đó, áp dụng plugin.". Đây là một chuỗi các lệnh, nếu một lệnh thất bại, bạn sẽ ở trạng thái không nhất quán. 
* **Declarative (khai báo):** "Kong, đây là trạng thái cuối cùng tôi mong muốn (một file YAML chứa 1 service, 1 route và 1 plugin). Hãy tự tìm cách đạt được trạng thái đó."

Chế độ DB-less của Kong được thiết kế cho triết lý khai báo này. Nó cho phép bạn quản lý toàn bộ cấu hình API Gateway của mình giống như cách bạn quản lý mã nguồn ứng dụng: 
trong Git, với Pull Requests, code review, và lịch sử phiên bản. 

### 5.2. Hướng dẫn sử dụng `decK`: Đồng bộ hoá (Sync), khác biệt (Diff), và xác thực (Validate)
`decK` (Declarative Configuration for Kong) là một công cụ CLI chính thức của Kong được xây dựng để hỗ trợ quy trình GitOps. Nó hoạt động bằng cách giao tiếp với Admin API của Kong.

Các lệnh quan trọng nhất của `decK` bao gồm:
* `deck gateway validate -s kong.yml`: Chỉ kiểm tra cú pháp file `kong.yml` của bạn có hợp lệ hay không. Dùng trong bước "lint" của CI. 

* `desk gateway diff -s kong.yml`: So sánh file `kong.yml` cục bộ của bạn với trạng thái hiện tại đang chạy trên Kong. Nó sẽ hiển thị một bản "kế hoạch" (plan) chính xác những gì sẽ được 
CREATE, UPDATE, DELETE. Cực kỳ hữu ích để review trong pull request. 

* `desk gateway sync -s kong.yml`: Áp dụng các thay đổi từ file `kong.yml` trên Kong. 

### 5.3. Xây dựng một đường ống (pipeline) CI/CD hoàn chỉnh cho Cấu hình Kong
Sử dụng decK, bạn có thể xây dựng một pipeline CI/CD mạnh mẽ bằng GitHub Actions hoặc Jenkins.

**Lưu ý quan trọng về bối cảnh:** `decK` hoạt động bằng cách gọi Admin API. 
Do đó, pipeline GitOps sử dụng `deck sync` chủ yếu dành cho các môi trường **DB-backed** hoặc **Hybrid Control Plane.**

Một pipeline GitHub Actions mẫu cho kịch bản **DB-backed** sẽ trông như sau:
1. Workflow cho Pull Request (Validation)
```YAML
#.github/workflows/kong_pr_check.yml
name: Kong PR Check
on: pull_request
jobs:
  validate-and-diff:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: kong/setup-deck@v1 # Cài đặt decK
        with:
          deck-version: '1.20.0'

      - name: Validate Kong config
        run: deck gateway validate -s kong.yml # (S179)

      - name: Diff Kong config
        run: |
          deck gateway diff -s kong.yml \
            --kong-addr ${{ secrets.KONG_ADDR }} \
            --headers "Kong-Admin-Token:${{ secrets.KONG_TOKEN }}"
```

2. Workflow cho Merge vào main (Deployment):
```YAML
#.github/workflows/kong_deploy.yml
name: Deploy Kong Config
on:
  push:
    branches: [ main ]
jobs:
  sync-production:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: kong/setup-deck@v1
        with:
          deck-version: '1.20.0'

      - name: Sync Kong config
        run: |
          deck gateway sync -s kong.yml \
            --kong-addr ${{ secrets.KONG_ADDR }} \
            --headers "Kong-Admin-Token:${{ secrets.KONG_TOKEN }}" # (S179, S181)
```

**Quy trình GitOps cho DB-less thì sao?** Như đã làm rõ, `deck sync` không hoạt động với Admin API read-only của chế độ DB-less. Quy trình GitOps cho DB-less sẽ khác:

* Bạn vẫn dùng `deck gateway validate` trong PR.
* Bước "sync" của bạn không phải là `deck sync`. Thay vào đó, nó sẽ là:
  * **Nếu dùng Docker/VM:** Một script `curl` để POST toàn bộ nội dung file `kong.yml` mới lên endpoint `/config` của Admin API.

  * **Nếu dùng Kubernetes (không KIC):** `kubectl apply -f my-kong-configmap.yml` (chứa nội dung `kong.yml`) và sau đó là `kubectl rollout restart deploy/kong-gatewa`y để các pod tải ConfigMap mới.

  * **Nếu dùng KIC (Best Practice):** Bạn không cần `decK` hay `curl` cho việc deploy. Pipeline CI/CD của bạn chỉ đơn giản là `kubectl apply -f my-ingress.yml.` KIC sẽ tự động xử lý phần còn lại.

## Phần 6. Ánh xạ và bảo mật Micorservices
### 6.1. Hướng dẫn: Ánh xạ Microservices (Services) tới các Lộ trình (Routes) công khai
Với cá khái niệm đã học, việc ánh xạ microservices trở nên đơn giản. Giả sử bạn có hai microservices: `auth-service` (chạy tại `http://auth-svc-internal:8080`) 
và `order-service` (chạy tại `http://order-svc-internal:8080`).

File `kong.yml` (cho chế độ DB-less) của bạn sẽ trông như sau:
```YAML
_format_version: "3.0"

services:
- name: auth-service
  url: http://auth-svc-internal:8080 # (S65, S142)
  
- name: order-service
  url: http://order-svc-internal:8080 # (S142)

routes:
- name: auth-route
  service:
    name: auth-service # Liên kết Route này với "auth-service"
  paths:
  - /api/auth # (S142)
  strip_path: true # Xóa /api/auth trước khi gửi đến upstream

- name: order-route
  service:
    name: order-service # Liên kết Route này với "order-service"
  paths:
  - /api/orders # (S142)
  strip_path: true
  methods: # Chỉ cho phép các phương thức này
```

Với cấu hình này, một request `GET /api/orders` sẽ được Kong định tuyến đến `http://order-svc-internal:8080/`.

### 6.2. Chiến lược Xác thực (Authentication) Toàn diện

Kong đóng vai trò là "người gác cổng", thực thi xác thực (AuthN) để bạn không cần lặp lại logic này trong mỗi microservice. Kong cung cấp các plugin cho mọi kịch bản. 
* API Key (`key-auth`):
  * **Kịch bản:** Tốt nhất cho giao tiếp Server-to-Server (M2M) hoặc các đối tác bên thứ ba.
  * **Cấu hình:**
    * Tạo một `Consumer`
    * Tạo một `keyauth_credential` cho Consumer đó (ví dụ: `key: "my-secret-key"`)
    * Áp dụng plugin `key-auth` cho Service hoặc Route. Kong sẽ tìm key trong header hoặc query param. 

* **JWT:**
  * **Kịch bản:** Tốt nhất cho ứng dụng web/di động (client-side) hoặc M2M đã được xác thực. Client (ví dụ: trình duyệt) trình một JSON Web Token (JWT). 
  Kong chỉ cần xác minh chữ kỹ của token (sử dụng public key hoặc secret). 
  * **Cấu hình:**
    * Tạo `Consumer`.
    * Tạo một `jwt_secret` cho Consumer đó (chứa public key RS256 hoặc HS256 secret). 
    * Áp dụng plugin `jwt`.
  
* **OpenID Connect (OIDC)**:
  * **Kịch bản:** Tiêu chuẩn vàng để xác thực người dùng cuối (end-users) thông qua một Identity Provider (IdP) bên ngoài (như Okta, Keycloak, Google).
  * **Cấu hình:** Đây là plugin phức tạp nhất. Bạn cấu hình Kong làm OIDC Client (Relying Party). Cung cấp cho nó `issuer`, `client_id`, và `client_secret` từ IdP của bạn. Khi một người dùng chưa xác thực truy cập, plugin `openid-connect` sẽ tự động:
    * Chuyển hướng (redirect) người dùng đến trang đăng nhập của IdP.
    * Xử lý callback, trao đổi authorization_code để lấy access_token.
    * Xác minh token và tạo một session cookie cho người dùng.
  * **Lưu ý:** Đừng nhầm lẫn plugin `openid-connect` (Kong là Client) với plugin `oauth2` (Kong là Authorization Server). Đối với hầu hết các hệ thống microservices, bạn muốn dùng OIDC và liên kết với một IdP tập trung.
    
### 6.3. Triển khai các Plugin Bảo mật Thiết yếu (Rate Limiting, IP Restriction, CORS)

Ngoài AuthN, Kong còn cung cấp một loạt các plugin bảo mật và kiểm soát truy cập. 
* **Rate Limiting (`rate-limiting`):**
  * Cực kỳ quan trọng để bảo vệ dịch vụ của bạn khỏi lạm dụng và cuộc cuộc tấn công DoS. 
  * Plugin này rất linh hoạt: nó có thể giới hạn dựa trên `Consumer` (nếu đã xác thực) hoặc `ip` (nếu không xác thực).
  * Cấu hình mẫu: `config: {"minute": 100, "policy": "local"}`

* **IP Restriction (`ip-restriction`):**
  * Cho phép bạn tạo `whitelist` (danh sách trắng) hoặc backlist (danh sách đen) các địa chỉ IP hoặc dải CIDR. 
  * Rất hữu ích để khoá các endpoint nhạy cảm (ví dụ: các đường dẫn admin) chỉ cho phép truy cập từ mạng nội bộ (ví dụ: `config: { "allow": ["10.0.0.0/16"] }"`

* **CORS (`cors`)**
  * Trong kiến trúc microservices, các developer thường xuyên quên xử lý các request OPTIONS (pre-flight) của Cross-Origin Resource Sharing (CORS).
  * Hãy để Kong lo việc này. Áp dụng plugin `cors` (thường là áp dụng Global - cho mọi service). 
Nó sẽ tự động trả lời các request `OPTIONS` và thêm các header `Access-Control-Allow-Origin` cần thiết vào các request thực tế.

**Best practices về phạm vi (scope) cho plugin:** Các plugin có thể được áp dụng ở những cấp độ (scope). Kong luôn ưu tiên cấu hình ở cấp độ cụ thể nhất. 
Thứ tự ưu tiên là: `Consumer` > `Route` > `Service` > `Global`. 
* **Global**: Áp dụng cho mọi request đi qua Kong (ví dụ: `cors`, `prometheus`)
* **Service**: Áp dụng cho mọi route thuộc về service đó (ví dụ: `key-auth` cho một service nội bộ)
* **Route**: Áp dụng chỉ cho route cụ thể đó (ví dụ: `ip-restriction` cho route `/admin`)
* **Consumer**: Áp dụng chỉ cho consumer đó (ví dụ: `rate-limiting` với giới hạn "Pro Plan").

## Phần 7. Quản lý và điều khiển lưu lượng (traffic control) nâng cao
### 7.1. Cấu hình Active Health Checks và Passive Circuit Breakers
Như đã đề cập ở phần 2.3, các tính năng này yêu cầu bạn sử dụng `Upstream` và `Target`. Đây là các tính năng số còn để đảm bảo độ tin cậy của hệ thống. 
* **Active Health Checks (Kiểm tra chủ động):**
  * **Cách hoạt động:** Kong chủ động gửi các request (thường là HTTP GET) đến một endpoint (ví dụ: `/healthz`) trên các `Targets` của bạn theo một lịch trình (ví dụ: 30 giây một lần).
  * **Cấu hình:** Bạn định nghĩa các ngưỡng, ví dụ: "sau 3 lần `unhealthy` (ví dụ: 503) liên tiếp, đánh dấu Target là lỗi" và "sau 2 lần `healthy` (ví dụ: 200) liên tiếp, đánh dấu Target là khoẻ mạnh".

* **Passive Health Checks (Circuit Breakers - Bộ ngắt mạch):**
  * **Cách hoạt động:** Kong không gửi request chủ động. Thay vào đó, nó _thụ động_ phân tích lưu lượng truy cập thực tế đang đi qua nó. 
  * **Cấu hình:** Bạn định nghĩa các ngưỡng, ví dụ: "nếu Kong thấy 5 lỗi 5xx (HTTP failures) hoặc 10 `timeouts` liên tiếp từ một Target, hãy 'mở mạch' (open the circuit) và ngừng gửi traffic đến Target đó trong 60 giây".

**Best Practices - Kết hợp cả hai:** bạn phải sử dụng cả hai, **Passive checks** (circuit breakers) rất tuyệt vời trong việc _phát hiện lỗi nhanh (fast failure detection)_ vì chúng phân tích mọi request. 
Nhưng chúng không biết khi nào Target đã phục hồi. Ngược lại, **Active Checks** biết khi nào Target phục hồi, nhưng chúng có thể chậm (vì chỉ ping 30 giây một lần). 

**Mẫu kết hợp tối ưu:**
1. **Passive Check** được kích hoạt (ví dụ: 5 lỗi 5xx) và nhanh chóng mở mạch, loại Target khỏi vòng quay. 
2. **Active Check** (luôn chạy nền) tiếp tục ping Target đã lỗi đó. 
3. Khi **Active Check** xác nhận Target đã khoẻ mạnh (ví dụ: 3 lần 200 OK liên tiếp), nó sẽ ra lệnh "đóng mạch" (close the circuit), cho phép Kong gửi lại Traffic. 

### 7.2. Các thuật toán Load Balancing (Round Robin, Consitent Hashing)

Khi sử dụng `Upstream`, bạn có thể chọn các thuật toán load balancing:

* **Round Robin (Xoay vòng):** Mặc định. Phân phối request đều cho các `Targets`.
* **Least Connections (Ít kết nối nhất):** Gửi request đến Target đang có ít kết nối hoạt động nhất. Rất hữu ích nếu các request của bạn có thời gian xử lý không đồng đều (ví dụ: một số request mất 10ms, số khác mất 500ms).
* **Consistent Hashing (Băm nhất quán):**
  * Đây là một thuật toán cực kỳ quan trọng cho các kịch bản cụ thể. Nó cho phép bạn "ghim" (pin) một client vào một `Target` backend cụ thể.
  * Bạn có thể cấu hình Kong để hash dựa trên `consumer` (nếu đã xác thực) hoặc một header (ví dụ: `X-Session-ID`).
  * **Kịch bản sử dụng**: Khi các microservice của bạn là stateful hoặc dựa nhiều vào cache cục bộ. Bằng cách đảm bảo tất cả các request từ cùng một người dùng (hoặc cùng một session) luôn đi đến cùng một pod, bạn tăng đáng kể tỷ lệ cache-hit (cache hit ratio) và giảm tải cho service.

### 7.3. Triển khai Canary Releases và BLue-Green Deployments

Kong làm cho việc triển khai các chiến lược này trở nên dễ dàng thông qua việc điều chỉnh weight (trọng số) của các Targets trong một Upstream.

* **Blue-Green Deployment (Triển khai Xanh-Dương):**
  * Giả sử `target-v1` (Blue) đang chạy.
  * Bạn triển khai `target-v2` (Green).
  * Cấu hình Upstream: `target-v1` (weight=100), `target-v2` (weight=0). 100% traffic đi đến v1.
  * Khi bạn sẵn sàng chuyển đổi, bạn cập nhật Upstream: `target-v1 (weight=0)`, `target-v2 (weight=100)`. 100% traffic ngay lập tức chuyển sang v2.

* **Canary Release (Phát hành Chim hoàng yến):**
  * `target-v1 (stable)`: `weight=95`
  * `target-v2 (canary)`: `weight=5`
  * Kong sẽ gửi 5% traffic đến phiên bản v2 mới. Bạn theo dõi metrics. Nếu v2 ổn định, bạn tăng dần `weight` của nó (ví dụ: 10%, 25%, 50%) đồng thời giảm `weight` của v1, cho đến khi v2 nhận 100% traffic.
  * Đây là một ứng dụng tuyệt vời của CI/CD. Pipeline deploy của bạn (ví dụ: Jenkins, GitHub Actions) có thể tự động gọi Admin API của Kong để điều chỉnh các giá trị `weight` này như một phần của quy trình triển khai tự động, không downtime.

### 7.4. Caching: Tăng tốc phản hồi với Proxy Cache Plugin


## Phần 8. Tích hợp Service Discovery và Observability (Khả năng quan sát)
### 8.1. Tự động hoá phát hiện dịch vụ (Service Discovery)

### 8.2. Chiến lược Logging: Tích hợp với ELK Stack và Grafana Loki

### 8.3. Giám sát (Monitoring): Thiết lập Prometheus và Grafana

### 8.4. Truy vết phân tán (Distributed Tracing): OpenTelemetry và Jaeger

## Phần 9. Vận hành Production: High Availability (HA) và tinh chỉnh hiệu năng
### 9.1. Kiến trúc High Availability (HA) được khuyến nghị

### 9.2. Chiến lược mở rộng (Scaling): Horizontal vs. Vertical

### 9.3. Tinh chỉnh hiệu năng: Tối ưu hoá Nginx Workers và `ulimit`


## Phần 10. Lộ trình và danh sách kiểm tra (roadmap & checklist)
### 10.1. Danh sách kiểm tra (checklist) triển khai từ zero đến production
Báo cáo này đã bao gồm rất nhiều thông tin. Dưới đây là một danh sách kiểm tra (checklist) tóm tắt các bước và các "best practices" để đi từ zero đến production.

<table>
  <thead>
    <tr>
      <th>Hạng mục</th>
      <th>Tác vụ</th>
      <th>Best Practice / Khuyến nghị</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="3">1. Kiến trúc</td>
      <td>Chọn Deployment Topology</td>
      <td><strong>DB-less</strong> cho K8s. <strong>Hybrid</strong> cho doanh nghiệp/multi-cloud. Tránh DB-backed trong production mới.</td>
    </tr>
    <tr>
      <td>Nguồn chân lý (SSoT)</td>
      <td><strong>Git Repository</strong>. Đối với KIC, SSoT là K8s API (quản lý qua Git).</td>
    </tr>
    <tr>
      <td>Lập kế hoạch Resource</td>
      <td>Hiệu rõ: Throughput (CPU-bound), Latency (Memory-bound).</td>
    </tr>
    <tr>
      <td rowspan="2">2. Tự động hóa (CI/CD)</td>
      <td>Chọn Công cụ GitOps</td>
      <td><strong>Kong Ingress Controller (KIC)</strong> cho K8s. <code>decK</code> cho VM/Hybrid CP.</td>
    </tr>
    <tr>
      <td>Thiết lập Pipeline</td>
      <td>Tích hợp <code>validate</code> và <code>diff</code> vào Pull Requests. <code>sync</code> (hoặc <code>kubectl apply</code>) khi merge.</td>
    </tr>
    <tr>
      <td rowspan="3">3. Bảo mật</td>
      <td>Bảo vệ Admin API</td>
      <td>Không bao giờ public Admin API. Sử dụng mTLS, IP restriction, hoặc token (RBAC).</td>
    </tr>
    <tr>
      <td>Xác thực (AuthN)</td>
      <td>Chọn và áp dụng chiến lược AuthN: <strong>OIDC</strong> (cho người dùng), <strong>JWT/Key-Auth</strong> (cho M2M).</td>
    </tr>
    <tr>
      <td>Plugin Bảo mật Cơ bản</td>
      <td>Áp dụng <code>rate-limiting</code>, <code>cors</code>, và <code>ip-restriction</code> cho các dịch vụ.</td>
    </tr>
    <tr>
      <td rowspan="3">4. Vận hành & HA</td>
      <td>Triển khai HA</td>
      <td>Tối thiểu 3 node Kong (stateless, DB-less) sau một Load Balancer. (Trong K8s: <code>replicas: 3</code>).</td>
    </tr>
    <tr>
      <td>Health Checks</td>
      <td><em>Bắt buộc:</em> Sử dụng <code>Upstream/Target</code> và cấu hình <em>cả hai</em> Active và Passive Health Checks.</td>
    </tr>
    <tr>
      <td>Tinh chỉnh Nginx (K8s)</td>
      <td><em>Bắt buộc:</em> Set <code>KONG_NGINX_WORKER_PROCESSES</code> bằng với <code>limits.cpu</code> của pod.</td>
    </tr>
    <tr>
      <td rowspan="3">5. Observability</td>
      <td>Monitoring</td>
      <td>Bật plugin <code>prometheus</code>. Cài đặt qua Helm với <code>serviceMonitor.enabled=true</code>.</td>
    </tr>
    <tr>
      <td>Logging</td>
      <td>Cấu hình plugin logging (ví dụ: <code>http-log</code>) để gửi đến Loki/ELK. Sử dụng <code>custom_fields_by_lua</code> cho Loki.</td>
    </tr>
    <tr>
      <td>Tracing</td>
      <td>Bật plugin <code>opentelemetry</code>. Cấu hình <code>traces_endpoint</code> trỏ đến OTel Collector.</td>
    </tr>
  </tbody>
</table>

### 10.2. Quản lý vòng đời API (API Lifecycle Management) và Best Practices



## Kết luận

Việc xây dựng Kong làm API Gateway cho hệ thống microservices là một quyết định chiến lược, và nền tảng Nginx của bạn là một lợi thế vô giá. Kong kế thừa
hiệu suất non-blocking của Nginx và bổ sung một lớp quản lý động, linh hoạt thông quan OpenResty và một hệ sinh thái plugin phong phú. 

Để đi từ "zero-to-production", lộ trình "best practices" ở bên trên đã rất rõ ràng:
1. **Chọn kiến trúc hiện đại:** Ưu tiên chế độ DB-less để có một hệ thống stateless, dễ tự động hoá. 
2. **Triển khai Clout-Native:** Nếu sử dụng Kubernetes, **Kong Ingress Controller (KIC)** là lựa chọn duy nhất, sử dụng K8s API làm nguồn chân lý.
3. **Tư duy GitOps:** Quản lý cấu hình của bạn (dù là `kong.yml`) hay K8s `Ingress` manifests) trong Git và tự động hoá việc triển khai thông qua các pipeline CI/CD.
4. **Khai thác toàn diện:** Đừng chỉ dùng Kong như một Reverse Proxy. Hãy sử dụng tính năng production-ready: `Upstream` với **Active/Passive Health Checks**, 
các thuật toán **Load Balancing** nâng cao, và các **Plugin Bảo mật** (OIDC, Rate Limiting).
5. **Quan sát toàn diện:** Thiết lập đầy đủ bộ ba observability (Logging với **Loki**, Monitoring với **Prometheus**, Tracing với **OpenTelemetr**y).

Bằng cách tuân thủ lộ trình và các thực tiễn tốt nhất được nêu trong báo cáo này, bạn sẽ xây dựng được một hệ thống API Gateway không chỉ mạnh mẽ và hiệu suất cao, 
mà còn có khả năng mở rộng, phục hồi, và bảo mật cấp độ production.










