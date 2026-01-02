# MICROSERVICES ARCHITECTURE PATTERN LANGUAGE

## Mục lục 

[I. Giới thiệu về Ngôn ngữ Mẫu hình (Pattern Language)](#i-giới-thiệu-về-ngôn-ngữ-mẫu-hình-pattern-language)
* [A. Vấn đề Thúc đẩy: Hạn chế của Kiến trúc Monolithic (Monolithic Architecture)](#a-vấn-đề-thúc-đẩy-hạn-chế-của-kiến-trúc-monolithic-monolithic-architecture)
* [B. Giải pháp Cấp cao: Kiến trúc Microservice (Microservice Architecture)](#b-giải-pháp-cấp-cao-kiến-trúc-microservice-microservice-architecture)
* [C. Phân tích chuyên sâu: Khái niệm về "Ngôn ngữ mẫu hình"](#c-phân-tích-chuyên-sâu-khái-niệm-về-ngôn-ngữ-mẫu-hình)

[II. Nền tảng của Microservices: Mẫu hình phân rã (Decomposition)](#ii-nền-tảng-của-microservices-mẫu-hình-phân-rã-decomposition)
* [A. Phân tích mẫu hình: Phân rã theo năng lực nghiệp vụ (Decompose by Businesss)](#a-phân-tích-mẫu-hình-phân-rã-theo-năng-lực-nghiệp-vụ-decompose-by-businesss)
* [B. Phân tích mẫu hình: Phân rã theo miền con (Decompose by Subdomain)](#b-phân-tích-mẫu-hình-phân-rã-theo-miền-con-decompose-by-subdomain)
* [C. Phân tích "Capability" so với "Subdomain" - Một sự cộng sinh](#c-phân-tích-capability-so-với-subdomain---một-sự-cộng-sinh)

[III. Thách thức nan giải nhất: Các mẫu hình dữ liệu phân tán (Data Patterns)](#iii-thách-thức-nan-giải-nhất-các-mẫu-hình-dữ-liệu-phân-tán-data-patterns)
* [A. Mẫu hình quyền sở hữu: Database per Service (Cơ sở dữ liệu cho mỗi Dịch vụ)](#a-mẫu-hình-quyền-sở-hữu-database-per-service-cơ-sở-dữ-liệu-cho-mỗi-dịch-vụ)
* [B. Giải quyết Giao dịch: Mẫu hình Saga](#b-giải-quyết-giao-dịch-mẫu-hình-saga)
* [C. Giải quyết tính nguyên tử: Mẫu hình Event Sourcing (nguồn sự kiện)](#c-giải-quyết-tính-nguyên-tử-mẫu-hình-event-sourcing-nguồn-sự-kiện)

[IV. Kết nối Hệ thống: Các Mẫu hình Giao tiếp (Communication Patterns)](#iv-kết-nối-hệ-thống-các-mẫu-hình-giao-tiếp-communication-patterns)
* [A. Phân tích Mẫu hình: Phong cách Giao tiếp (Communication Style)](#a-phân-tích-mẫu-hình-phong-cách-giao-tiếp-communication-style)
* [B. Phân tích Mẫu hình: API Gateway (Cổng API)](#b-phân-tích-mẫu-hình-api-gateway-cổng-api)
* [C. Phân tích Mẫu hình: Khám phá Dịch vụ (Service Discovery)](#c-phân-tích-mẫu-hình-khám-phá-dịch-vụ-service-discovery)

[V. Xây dựng Hệ thống Chống chịu Lỗi: Các Mẫu hình Độ tin cậy (Reliability Patterns)](#v-xây-dựng-hệ-thống-chống-chịu-lỗi-các-mẫu-hình-độ-tin-cậy-reliability-patterns)
* [A. Phân tích Mẫu hình: Circuit Breaker (Bộ ngắt mạch)](#a-phân-tích-mẫu-hình-circuit-breaker-bộ-ngắt-mạch)

[VI. Nhìn vào Hộp đen: Các Mẫu hình Khả năng Quan sát (Observability Patterns)](#vi-nhìn-vào-hộp-đen-các-mẫu-hình-khả-năng-quan-sát-observability-patterns)
* [A. Trụ cột 1 (Logs): Tổng hợp Nhật ký (Log Aggregation)](#a-trụ-cột-1-logs-tổng-hợp-nhật-ký-log-aggregation)
* [B. Trụ cột 2 (Metrics): API Kiểm tra Sức khỏe (Health Check API)](#b-trụ-cột-2-metrics-api-kiểm-tra-sức-khỏe-health-check-api)
* [C. Trụ cột 3 (Traces): Truy tìm Phân tán (Distributed Tracing)](#c-trụ-cột-3-traces-truy-tìm-phân-tán-distributed-tracing)

[VII. Vận hành Thực tế: Các Mẫu hình Triển khai (Deployment Patterns)](#vii-vận-hành-thực-tế-các-mẫu-hình-triển-khai-deployment-patterns)
* [A. Phân tích Mẫu hình: Service per Container (Dịch vụ trên mỗi Container)](#a-phân-tích-mẫu-hình-service-per-container-dịch-vụ-trên-mỗi-container)
* [B. Phân tích Mẫu hình: Service Mesh (Lưới Dịch vụ)](#b-phân-tích-mẫu-hình-service-mesh-lưới-dịch-vụ)

[VIII. Tổng kết: Sự hội tụ và Con đường Phía trước](#viii-tổng-kết-sự-hội-tụ-và-con-đường-phía-trước)


## I. Giới thiệu về Ngôn ngữ Mẫu hình (Pattern Language)
### A. Vấn đề Thúc đẩy: Hạn chế của Kiến trúc Monolithic (Monolithic Architecture)
Trong lịch sử phát triển phần mềm, kiến trúc nguyên khối (Monolithic Architecture) là điểm khởi đầu tiêu chuẩn. 
Trong mô hình này, toàn bộ ứng dụng được xây dựng và triển khai như một đơn vị duy nhất. Mặc dù cách tiếp cận này mang lại sự đơn giản trong giai đoạn đầu, 
nó nhanh chóng bộc lộ những hạn chế nghiêm trọng khi ứng dụng phát triển về quy mô và độ phức tạp. Việc bảo trì trở nên khó khăn, 
khả năng mở rộng bị giới hạn ở việc nhân bản toàn bộ khối ứng dụng, và một thay đổi nhỏ trong một mô-đun đòi hỏi phải kiểm thử và triển khai lại toàn bộ hệ thống. 
Những thách thức này đã thúc đẩy nhu cầu về một mô hình kiến trúc linh hoạt hơn.   

### B. Giải pháp Cấp cao: Kiến trúc Microservice (Microservice Architecture)
Kiến trúc Microservice nổi lên như một giải pháp cấp cao cho các vấn đề của kiến trúc Monolithic. 
Kiến trúc này cấu trúc một ứng dụng thành một tập hợp các dịch vụ nhỏ, được ghép nối lỏng lẻo (loosely coupled) và có thể triển khai độc lập. 
Mỗi dịch vụ thường được tổ chức xung quanh một năng lực nghiệp vụ cụ thể và có thể được phát triển, triển khai và mở rộng một cách độc lập. 

### C. Phân tích chuyên sâu: Khái niệm về "Ngôn ngữ mẫu hình"

![microservices-architecture-pattern-language](/docs/images/microservices_architecture_pattern_language.png)

Việc áp dụng sơ đồ "Ngôn ngữ Mẫu hình Kiến trúc Microservice" (The Microservice Architecture Pattern Language)  
thường bị hiểu nhầm là một "thực đơn" các mẫu hình mà từ đó các kiến trúc sư có thể tùy ý lựa chọn. 
Trên thực tế, sơ đồ này đại diện cho một bản đồ nhân quả (causal map), nơi các mũi tên chỉ ra một chuỗi các quyết định và hậu quả.

Việc lựa chọn "Microservice Architecture" không phải là giải pháp cuối cùng; nó là điểm khởi đầu của một loạt các thách thức thiết kế mới và phức tạp hơn. 
Ngôn ngữ mẫu hình này mô tả dòng chảy của các vấn đề và giải pháp của chúng. Dòng chảy này có thể được tóm tắt như sau: 
1. **Quyết định kiến trúc (architecture):** Dẫn đến vấn đề **Phân rã (Decomposition)**, vậy làm thế nào để chia nhỏ khối Monolith một cách hiệu quả? 
2. **Phân rã (Decomposition):** Tạo ra hai hậu quả ngay lập tức: 
   * **Các mấu hình dữ liệu (data patterns):**: Dữ liệu hiện bị phân tán. Làm thế nào để quản lý và duy trì tính nhất quán? 
   * **Các mẫu hình giao tiếp (communication patterns):** Các dịch vụ phải giao tiếp qua mạng. Làm thế nào chúng tìm thấy và nói chuyện với nhau.
3. **Các mẫu hình giao tiép (Communication patterns):** Dẫn đến nhu cầu về **độ tin cậy (reliability)**, Mạng vốn không đáng tin cậy. Làm thế nào để ngăn chặn lỗi xếp tầng (cascading failures). 
4. **Toàn bộ hệ thống phân tán:** Dẫn dễn hai nhu cầu
   * **Khả năng quan sát (observability):** Hệ thống trở thành một "hộp đen". Làm thế nào để gỡ lỗi và giám sát? 
   * **Triển khai (deployment):** Làm thế nào để vận hành hàng trăm dịch vụ một cách hiệu quả. 

Báo cáo này sẽ phân tích chi tiết "tất tần tật" nội dung của ngôn ngữ mẫu hình này bằng cách đi theo dòng chảy nhân quả này, 
giải thích từng nhóm mẫu hình như một giải pháp cho các vấn đề do nhóm trước đó tạo ra.

## II. Nền tảng của Microservices: Mẫu hình phân rã (Decomposition)

Sau khi chọn kiến trúc microservices, quyết định cơ bản đầu tiên là làm thế nào để phân ra ứng dụng. 
Mục tiêu là xác định các ranh giới dịch vụ để tạo ra các dịch vụ có tính gắn kết cao (high cohesion) và khớp nối lỏng (loose coupling). 
Ngôn ngữ mẫu hình cung cấp hai chiến lược chính cho việc này. 

### A. Phân tích mẫu hình: Phân rã theo năng lực nghiệp vụ (Decompose by Businesss)



Mẫu hình này đề xuất định nghĩa các dịch vụ tương ứng với năng lực nghiệp vụ (business capabilities) của tổ chức. 
Năng lực nghiệp vụ là mô tả cấp cao về những gì một doanh nghiệp làm để tạo ra giá trị, chứ không phải như thế nào. 
* **Định nghĩa:** Một dịch vụ được tạo ra cho mỗi năng lực nghiệp vụ (business capability). 
Ví dụ, một công ty bảo hiểm có thể có các năng lực như "Bán hàng" (Sales), "Xử lý bồi thường" (Claims), "Quản lý khách hàng" (Customer Management).
* **Lợi ích:** Lợi ích chính của phương pháp này là **tính ổn định.** Các năng lực nghiệp vụ cốt lõi của một công ty (ví dụ: nhận đơn hàng, quản lý hàng tồn kho) thay đổi rất chậm theo thời gian. 
Bằng cách căn chỉnh kiến trúc với các năng lực này, bản thân kiến trúc cũng trở nên ổn định. Hơn nữa, nó thúc đẩy các nhóm đa chức năng, 
tự chủ, được tổ chức xung quanh việc cung cấp giá trị nghiệp vụ (ví dụ: nhóm Bồi thường) thay vì các lớp kỹ thuật (ví dụ: nhóm Giao diện người dùng, nhóm Cơ sở dữ liệu).

### B. Phân tích mẫu hình: Phân rã theo miền con (Decompose by Subdomain)
Mẫu hình này áp dụng các khái niệm từ thiết kế hướng tên miền (Domain-Driven Design - DDD) để phân rã hệ thống.   
* **Định nghĩa:** DDD xem toàn bộ không gian vấn đề của doanh nghiệp là một tên "miền" (domain) được tạo thành từ nhiều miền con (subdomains). 
Các dịch vụ microservices được định nghĩa tương ứng với các miền con này. 
* **Liên kết DDD:** DDD phân loại các miền con thành ba loại: 
1. **Core (cốt lõi):** Yếu tố khác biệt chính của doanh nghiệp, nơi tạo ra lợi thế cạnh tranh. Đây là phần có giá trị nhất của ứng dụng. 
2. **Supporting (Hỗ trợ):** Các hoạt động liên quan đến nghiệp vụ nhưng không phải là yếu tố khác biệt (ví dụ: báo cáo nội bộ).
3. **Generic (Chung):** Các chức năng không đặc thù cho doanh nghiệp và có thể được giải quyết bằng các giải pháp có sẵn (ví dụ: xác thực, thanh toán).

Việc phân rã theo miền con giúp đảm bảo các dịch vụ có tính gắn kết cao (chứa mọi thứ liên quan đến một phần của nghiệp vụ) và khớp nối lỏng với các miền con khác.   

### C. Phân tích "Capability" so với "Subdomain" - Một sự cộng sinh

Thoạt nhìn, hai mẫu hình này có vẻ tương tự, và các lợi ích của chúng (kiến trúc ổn định, khớp nối lỏng) gần như giống hệt nhau. 
Tuy nhiên, chúng hoạt động ở các cấp độ trừu tượng khác nhau và bổ trợ cho nhau.   

`Decompose by Business Capability` là một cách tiếp cận chiến lược, cấp cao để xác định các dịch vụ lớn. 
Nó trả lời câu hỏi "Chúng ta nên xây dựng dịch vụ gì?" (ví dụ: chúng ta cần một dịch vụ bán hàng)

`Decompose by Subdomain` (sử dụng DDD) là một phương pháp chiến thuật, kỹ thuật để phân tích sâu hơn vào một năng lực nghiệp vụ và xác định ranh giới chính xác của nó. 
Nó trả lời câu hỏi "Như thế nào?" (ví dụ: phân tích năng lực "Bán hàng" cho thấy nó bao gồm các miền con "Mua hàng" (Purchasing) và "Xử lý bồi thường" (Claims)).
Do đó, một năng lực nghiệp vụ có thể được triển khai dưới dạng một microservice duy nhất, hoặc nó có thể được phân rã thêm thành nhiều microservice nhỏ hơn dựa trên các miền con của nó. 

Bảng dưới đây tóm tắt sự khác biệt chiến thuật giữa hai phương pháp:

**Bảng II-A: Phân tích So sánh Chiến lược Phân rã**
<table>
  <thead>
    <tr>
      <th>Mẫu hình</th>
      <th>Khái niệm Cốt lõi</th>
      <th>Mức độ chi tiết (Granularity)</th>
      <th>Lợi ích Chính</th>
      <th>Yêu cầu Bắt buộc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Decompose by Business Capability</td>
      <td>Căn chỉnh theo giá trị nghiệp vụ (Cái gì)</td>
      <td>Thường là trung bình (Medium-grained)</td>
      <td>Kiến trúc ổn định</td>
      <td>Hiểu biết sâu về nghiệp vụ</td>
    </tr>
    <tr>
      <td>Decompose by Subdomain</td>
      <td>Căn chỉnh theo mô hình DDD (Như thế nào)</td>
      <td>Có thể rất chi tiết (Fine-grained)</td>
      <td>Dịch vụ gắn kết cao, ranh giới rõ ràng</td>
      <td>Hiểu biết sâu về nghiệp vụ và chuyên môn về DDD</td>
    </tr>
  </tbody>
</table>


## III. Thách thức nan giải nhất: Các mẫu hình dữ liệu phân tán (Data Patterns)

Như đã phân tích trong và, quyết định **Decomposition (Phân rã)** trực tiếp tạo ra nhu cầu về các mẫu hình dữ liệu. 
Khi các chức năng ứng dụng được chia tách, cơ sở dữ liệu nguyên khối cũng phải bị chia tách. Điều này ngay lập tức 
giới thiệu hai thách thức lớn: **(1) Làm thế nào để quản lý quyền sở hữu dữ liệu**, và **(2) Làm thế nào để duy trì tính nhất 
quán của giao dịch trên nhiều cơ sở dữ liệu.** 

### A. Mẫu hình quyền sở hữu: Database per Service (Cơ sở dữ liệu cho mỗi Dịch vụ)

Đây là nguyên tắc vàng, mẫu hình nên tảng của quản lý dữ liệu trong microservice. 
* **Định nghĩa:** Mỗi microservice sở hữu dữ liệu riêng của mình trong một cơ sở dữ liệu riêng tư. Dữ liệu này chỉ có thể được truy cập 
thông qua API của dịch vụ sở hữu nó. Cấc dịch vụ khác bị cấm truy cập trực tiếp vào cơ sở dữ liệu của dịch vụ khác. Điều này có thể được 
triển khai dưới dạng máy chủ CSDL riêng, schema riêng, hoặc thậm chí là bảng riêng cho mỗi dịch vụ. 
* **Ưu điểm:**
1. **Khớp nối lỏng (Loose Coupling):**  Đây là lợi ích quan trọng nhất. Dịch vụ quản lý khách hàng có thể hay đổi schema cơ sở dữ liệu của mình (ví dụ: thêm một cột) mà không làm ảnh hưởng hoặc yêu cầu thay đổi ở bất kỳ dịch vụ nào khác.
2. **Đa ngôn ngữ lưu trữ (Polyglot Persistence):** Mỗi dịch vụ có thể chọn công nghệ cơ sở dữ liệu phù hợp nhất cho nhu cầu của mình. Ví dụ, dịch vụ Tìm kiếm có thể sử dụng ElasticSearch, trong khi dịch vụ Giao dịch sử dụng PostgreSQL

* **Nhược điểm:** Mẫu hình này giới thiệu hai nhược điểm cực kỳ phức tạp
1. **Giao dịch phân tán:** Làm thế nào để thực hiện một hoạt động nghiệp vụ đòi hỏi tính nguyên tử (atomicity) trên nhiều dịch vụ? Ví dụ: 
việc "Đặt hàng" phải cập nhật dịch vụ Đơn hàng, trừ kho ở dịch vụ Tồn kho, và trừ tiền ở dịch vụ khách hàng. 

2. **Truy vấn (JOINs):** Làm thế nào để thực hiện một truy vấn cần dữ liệu từ nhiều dịch vụ (ví dụ: lấy tất cả các đơn hàng và tên của khách hàng để đặt chúng).

Quyết định áp dụng `Database per Service` thực chất là một sự đánh đổi: 
Các kiến trúc sư đánh đổi sự đơn giản ACID và các lệnh `JOIN` SQL của kiến trúc monolithic để lấy sự khớp nối lỏng, khả năng mở rộng và tính linh hoạt. 
Các mẫu hình dữ liệu còn lại trong ngôn ngữ (như `Saga` và `API Composition`) tồn tại chủ yếu để quản lý sự đánh đổi này. 

### B. Giải quyết Giao dịch: Mẫu hình Saga
Vì các giao dịch phân tán (ví dụ: two-phase commit) thường được khuyến khích trong microservice do định lý CAP, 
mẫu hình `Saga` được sử dụng để duy trì tính nhất quán. 
* **Định nghĩa:** Một Saga là một chuỗi các giao dịch cục bộ (local transactions). 
Mỗi giao dịch cục bộ trong chuỗi cập nhật CSDL của một dịch vụ duy nhất và kích hoạt bước tiếp theo trong Saga.
Nếu một giao dịch cục bộ thất bại, Saga sẽ thực thi một loạt các giao dịch bù trừ (compensating transactions) để hoàn tác công việc 
đã được thực hiện ở các bước trước đó. 

* **Các cơ chế phối hợp:** Có hai cách chính để phối hợp một Saga:
1. **Choreography (biên đạo):** Một cách tiếp cận phi tập trung. Các dịch vụ giao tiếp bằng cách xuất bản (publish) và đăng ký (subcribe) 
các sự kiện (domain events). Ví dụ: `Order Service` tạo đơn hàng và phát sự kiện `Order Created`. `Customer Service` lắng nghe sự kiện đó và 
thực hiện giao dịch cục bộ `Reserve Credit`, sau đó phát sự kiện `Credit Reserved`.
2. **Orchestration (điều phối):** Một cách tiếp cận tập trung. Một đối tượng "nhạc trưởng" (orchestrator) 
trung tâm chịu trách nhiệm điều phối toàn bộ quy trình. Nó gửi các lệnh đến từng dịch vụ và chờ phản hồi. Ví dụ: `Create Order Saga Orchestrator`\
gửi lệnh `Reserve Credit` đến `Customer Service`, chờ phản hồi, sau đó gửi lệnh `Update Inventory` đến `Inventory Service`. 

Việc lựa chọn giữa Choreography và Orchestration là một sự đánh đổi quan trọng về độ phức tạp và khả năng kiểm soát.

**Bảng III-A: Phân tích So sánh Phối hợp Saga**
<table>
  <thead>
    <tr>
      <th>Cơ chế</th>
      <th>Luồng điều khiển</th>
      <th>Khớp nối (Coupling)</th>
      <th>Độ phức tạp (Quy trình)</th>
      <th>Khả năng Gỡ lỗi (Debuggability)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Choreography (Biên đạo)</td>
      <td>Phi tập trung (Sự kiện)</td>
      <td>Khớp nối lỏng (Dịch vụ không biết về nhau)</td>
      <td>Đơn giản cho các quy trình ngắn (1-3 bước)</td>
      <td>Rất khó gỡ lỗi (Khó theo dõi ai lắng nghe sự kiện gì)</td>
    </tr>
    <tr>
      <td>Orchestration (Điều phối)</td>
      <td>Tập trung (Lệnh)</td>
      <td>Khớp nối chặt hơn (Dịch vụ bị khớp nối với Orchestrator)</td>
      <td>Tốt cho các quy trình dài, phức tạp</td>
      <td>Dễ gỡ lỗi (Trạng thái của Orchestrator là trạng thái của quy trình)</td>
    </tr>
  </tbody>
</table>


### C. Giải quyết tính nguyên tử: Mẫu hình Event Sourcing (nguồn sự kiện)
Một thách thức cốt lõi trong các hệ thống hướng sự kiện (như Saga Choreography) là làm thế nào để vừa cập nhật cơ sở dữ liệu, 
vừa xuất bản (publish) một sự kiện một cách nguyên tử. Nếu dịch vụ cập nhật CSDL thành công nhưng bị sập trước khi xuất bản sự kiện, 
toàn bộ quy trình nghiệp vụ sẽ bị phá vỡ. Mẫu hình `Event Sourcing` (nguồn sự kiện) là một giải pháp mạnh mẽ cho vấn đề này. 
* **Định nghĩa:** Thay vì lưu trữ trạng thái hiện tại cảu một thực thể (ví dụ: số dư tài khoản là `$100`), `Event Sourcing` lưu trữ trạng thái
dưới dạng một chuỗi các sự kiện thay đổi trạng thái (ví dụ: `AccountCreated`, `AmmountDeposited($150)`, `AmountWithdrawn($50)`). 
* **Hoạt động:** Trạng thái hiện tại được tái tạo bằng cách phát lại (replaying) các sự kiện. Kho lưu trữ các sự kiện này (Event Store) hoạt động như một cơ sở dữ liệu. 
* **Lợi ích và giải pháp:** Lợi ích chính là việc "lưu vào CSDL" và "xuất bản sự kiện" _trở thành một hành động nguyên tử duy nhất_: Hành động thêm một (append) một sự kiện
mới vào Event Store. Event Store sau đó có thể hoạt đông như một message broker, thông báo cho các dịch vụ khác (các subscriber) về sự kiện mới này. 
Điều này đảm bảo rằng một sự kiện không bao giờ bị mất, cung cấp nền tảng đáng tin cậy cho các mẫu hình như **Saga Choreography**. Nó cung cấp một nhật ký kiểm toán (audit log)
hoàn hảo về tất cả thay đổi trong hệ thống. 

## IV. Kết nối Hệ thống: Các Mẫu hình Giao tiếp (Communication Patterns)
Cùng với các mẫu hình dữ liệu, việc phân rã một khối monolithic buộc các nhà phát triển phải giải quyết vấn đề giao tiếp. Các lệnh gọi hàm (function calls) đơn giản bên trong một tiến trình giờ đây trở thành các lệnh gọi mạng (network calls) phức tạp và không đáng tin cậy.   

### A. Phân tích Mẫu hình: Phong cách Giao tiếp (Communication Style)
Có hai phong cách giao tiếp cơ bản giữa các dịch vụ: 
1. **Remote Procedure Invocation (RPI):** Đây là phong cách giao tiếp đồng bộ (synchronous). 
Client (dịch vụ gọi) gửi một yêu cầu đến một dịch vụ khác và chờ (blocks) cho đến khi nhận được phản hồi. 
Các công nghệ phổ biến bao gồm REST (dựa trên HTTP) và gRPC. 
   * **Ưu điểm:** Đơn giản, quen thuộc và dễ hiểu. 
   * **Nhược điểm:** Nó tạo ra khớp nối thời gian chạy (temporal coupling). Nếu dịch vụ B (bị gọi) bị chậm hoặc ngừng hoạt động, 
dịch vụ A (đang gọi) cũng bị kẹt và có thể ngừng hoạt động, dẫn đến lỗi xếp tầng (cascading failures).

2. **Messaging (Nhắn tin):** Đây là phong cách giao tiếp bất đồng bộ (asynchronous). Client gửi một tin nhắn đến một message broker (như RabbitMQ hoặc Kafka) và tiếp tục công việc của mình mà không cần chờ phản hồi ngay lập tức.
   * **Ưu điểm:** Nó cung cấp khớp nối lỏng và cải thiện tính sẵn có. Dịch vụ A có thể gửi tin nhắn ngay cả khi dịch vụ B đang ngoại tuyến. Message broker hoạt động như một bộ đệm, lưu trữ tin nhắn cho đến khi dịch vụ B sẵn sàng xử lý chúng. 
   * **Nhược điểm:** Mô hình này phức tạp hơn để triển khai và gỡ lỗi.

**Bảng IV-A: Phân tích So sánh Phong cách Giao tiếp**

<table>
  <thead>
    <tr>
      <th>Phong cách</th>
      <th>Mô hình</th>
      <th>Khớp nối (Temporal)</th>
      <th>Độ tin cậy (Tác động lỗi)</th>
      <th>Trường hợp sử dụng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Remote Procedure Invocation (RPI)</td>
      <td>Đồng bộ (Request/Reply)</td>
      <td>Khớp nối thời gian chạy chặt chẽ</td>
      <td>Lỗi lan truyền (Cascading failures)</td>
      <td>Truy vấn dữ liệu (Queries), các lệnh cần phản hồi ngay</td>
    </tr>
    <tr>
      <td>Messaging (Nhắn tin)</td>
      <td>Bất đồng bộ (Event/Message)</td>
      <td>Khớp nối lỏng (Thông qua Broker)</td>
      <td>Lỗi được cô lập, độ bền cao</td>
      <td>Quy trình nghiệp vụ (Saga), thông báo (notifications), các hệ thống cần độ tin cậy cao</td>
    </tr>
  </tbody>
</table>

### B. Phân tích Mẫu hình: API Gateway (Cổng API)
Mẫu hình `API Gateway` giải quyết vấn đề làm thế nào để các client bên ngoài (ví dụ: ứng dụng di động, trình duyệt web) tương tác với hệ thống microservice.   

* **Định nghĩa:** `API Gateway` là một máy chủ trung gian đóng vai trò là điểm vào duy nhất (single entry point) cho tất cả các yêu cầu từ bên ngoài. 
Nó hoạt động như một reverse proxy, định tuyến các yêu cầu đến các dịch vụ nội bộ thích hợp.   

* **Lợi ích:**
1. **Đóng gói (Encapsulation):** Client không cần biết về kiến trúc microservice bên trong. Chúng chỉ giao tiếp với Gateway, giúp đơn giản hóa code phía client.
2. **Các mối quan tâm chung (Cross-cutting concerns):** Gateway là nơi lý tưởng để xử lý các tác vụ chung xác thực (authentication), uỷ quyền (authorization), giới hạn tốc độ (rate limiting), và caching. 
3. **Tổng hợp yêu cầu (Request Aggregation):** Gateway có thể nhận một yêu cầu duy nhất từ client, sau đó gọi nhiều dịch vụ nội bộ và tổng hợp kết quả trả về cho client. Điều này làm giảm số lượng lượt đi-về (round-trips) qua mạng.

* **Nhược điểm:** Gateway có thể trở thành một điểm nghẽn cổ chai (bottleneck) về hiệu suất  và tăng độ trễ. Nó cũng có nguy cơ trở thành một "Monolith mới" nếu chứa quá nhiều logic nghiệp vụ. 

### C. Phân tích Mẫu hình: Khám phá Dịch vụ (Service Discovery)
Mẫu hình `Service Discovery` giải quyết vấn đề giao tiếp bên trong (service-to-service). Trong một môi trường đám mây động, các phiên bản dịch vụ (ví dụ: các container) liên tục được tạo ra và phá huỷ, 
và địa chỉ IP của chúng thay đổi liên tục. Làm thế nào để dịch vụ A biết địa chỉ IP và cổng hiện tại của dịch vụ B? 
* **Giải pháp: Service Registry (sổ đăng ký dịch vụ):** Giải pháp trung tâm cho vấn đề này là `Service Registry`. Đây là một cơ sở dữ liệu (một "danh bạ điện thoại")
chứa vị trí mạng của tất cả phiên bản dịch vụ đang chạy.

Hoạt động:
* **Đăng ký (Registration)**: Khi một phiên bản dịch vụ mới khởi động, nó tự động đăng ký (Self registration) thông tin vị trí (IP, cổng) của mình với Service Registry.   

* **Khám phá (Discovery):** Khi Dịch vụ A muốn gọi Dịch vụ B, nó sẽ truy vấn Service Registry để lấy danh sách các địa chỉ khả dụng của Dịch vụ B.   

Tương tác Mẫu hình: `API Gateway` và `Service Registry` không phải là các mẫu hình thay thế nhau; chúng phối hợp với nhau. 
`API Gateway` giải quyết truy cập từ ngoài vào trong, trong khi `Service Registry` giải quyết truy cập bên trong giữa các service. 
Khi một yêu cầu bên ngoài đến `API Gateway`, Gateway phải hoạt động như một client của Service Registry để tìm ra địa chỉ của dịch vụ nội bộ mà nó cần chuyển tiếp yêu cầu đến

## V. Xây dựng Hệ thống Chống chịu Lỗi: Các Mẫu hình Độ tin cậy (Reliability Patterns)

Việc dựa vào giao tiếp mạng (như đã thấy trong Communication patterns) tạo ra nhu cầu cấp thiết về các mẫu hình `Reliability`. Mạng không đáng tin cậy; các dịch vụ có thể bị lỗi, quá tải, hoặc phản hồi chậm.   

Một hệ quả trực tiếp của việc sử dụng giao tiếp đồng bộ (RPI) là nguy cơ xảy ra lỗi xếp tầng (cascading failures). Nếu Dịch vụ B bị chậm, Dịch vụ A (đang chờ phản hồi từ B) cũng bị chậm. Khi các yêu cầu dồn lại, tài nguyên của A (như thread pool) sẽ cạn kiệt, khiến A cũng bị lỗi. Lỗi này tiếp tục lan truyền ngược dòng đến các dịch vụ gọi A.   

Mẫu hình `Circuit Breaker` (Bộ ngắt mạch) được thiết kế đặc biệt để ngăn chặn thảm họa này.

### A. Phân tích Mẫu hình: Circuit Breaker (Bộ ngắt mạch)

Mẫu hình này, được Michael Nygard phổ biến, hoạt động giống như một bộ ngắt mạch điện trong nhà bạn. Nó là một đối tượng proxy bao bọc các lệnh gọi mạng (đặc biệt là các lệnh gọi RPI) và theo dõi các lỗi. Nó có ba trạng thái: 

1. **Closed (Đóng):** Trạng thái hoạt động bình thường. Các yêu cầu được phép đi qua dịch vụ được gọi. Bộ đếm lỗi được duy trì. Nếu một lệnh gọi thất bại (ví dụ: timeout), bộ đếm lỗi sẽ tăng lên.   

2. **Open (Mở):** Khi số lượng lỗi vượt quá một ngưỡng nhất định trong một khoảng thời gian, mạch sẽ "ngắt" (trips) và chuyển sang trạng thái Mở. Ở trạng thái này, tất cả các lệnh gọi tiếp theo đến dịch vụ đó sẽ bị từ chối ngay lập tức (fail-fast) mà không cần thực hiện lệnh gọi mạng. 
Điều này mang lại hai lợi ích tức thì: (a) Dịch vụ gọi (A) được bảo vệ khỏi việc bị chặn và cạn kiệt tài nguyên, và (b) Dịch vụ bị lỗi (B) được giảm tải để có thời gian phục hồi.   

3. **Half-Open (Nửa Mở):** Sau một khoảng thời gian chờ (ví dụ: 30 giây) ở trạng thái Mở, mạch sẽ chuyển sang trạng thái Nửa Mở. Ở trạng thái này, nó cho phép một lệnh gọi "thử nghiệm" duy nhất đi qua.   
   * Nếu lệnh gọi thử nghiệm thành công, hệ thống giả định rằng Dịch vụ B đã phục hồi. Mạch chuyển về trạng thái Closed.   
   * Nếu lệnh gọi thử nghiệm thất bại, hệ thống giả định Dịch vụ B vẫn còn lỗi. Mạch quay lại trạng thái Open và bắt đầu lại bộ đếm thời gian chờ.

## VI. Nhìn vào Hộp đen: Các Mẫu hình Khả năng Quan sát (Observability Patterns)
Việc phân rã một khối monolith thành hằng trăm dịch vụ phân tán đã biến một hệ thống dễ gỡ lỗi thành một "hộp đen" phức tạp. 
Khi một yêu cầu thất bại hoặc bị chậm, việc xác định nguyên nhân gốc rễ trở nên cực kỳ khó khăn. `Observability` (khả năng quan sát) là một tập hợp
các mẫu hình bắt buộc để vận hành các hệ thống như vậy. Nó thường được xây dựng trên ba trụ cột. 

### A. Trụ cột 1 (Logs): Tổng hợp Nhật ký (Log Aggregation)
* **Vấn đề:** Mỗi phiên bản dịch vụ tạo ra các tệp nhật ký (logs) riêng. Trong một hệ thống có hàng trăm container, các nhật ký này bị phân tán, khiến việc điều tra lỗi trở nên bất khả thi.
* **Mẫu hình:** `Log Aggregation` (tổng hợp nhật ký)
* **Giải pháp:** Triển khai một đường ống (pipeline) thu thập nhật ký. Các tác nhân (agents) chạy trên mỗi máy chủ/container sẽ thu thập các luồng nhật ký và gửi chúng đến một kho lưu trữ trung tâm.
(ví dụ: Kafka hoặc Elasticsearch). Điều này cho phép các nhà phá triển truy vấn và phân tích tất cả các nhật ký từ một nơi duy nhất.   

### B. Trụ cột 2 (Metrics): API Kiểm tra Sức khỏe (Health Check API)
* **Vấn đề:** Một dịch vụ có thể đang chạy (process đang hoạt động) nhưng không khoẻ (unhealthy), ví dụ: nó không thể kết nối tứoi cơ sở dữ liệu của mình. 
Hệ thống cân bằng tải hoặc service registry cần biết điều này để không gửi lưu lượng truy cập mới đến phiên bản bị lỗi đó. 
* **Mẫu hình:** `Health Check API` (API Kiểm tra Sức khỏe).   
* **Giải pháp:** Mỗi dịch vụ cung cấp một endpoint API đặc biệt (ví dụ: `HTTP /health`). 
* **Hoạt động:** Một tác nhân bên ngoài (như `Service Registry`  hoặc một bộ điều phối như Kubernetes ) sẽ định kỳ gọi endpoint này. 
* Logic bên trong endpoint /health phải kiểm tra không chỉ bản thân dịch vụ mà còn cả các phụ thuộc quan trọng của nó (như kết nối CSDL). 
Nếu kiểm tra thất bại, endpoint sẽ trả về mã lỗi. Tác nhân bên ngoài sẽ ghi nhận phiên bản này là "unhealthy" và tạm thời loại bỏ nó khỏi danh sách các phiên bản có thể nhận yêu cầu. 

### C. Trụ cột 3 (Traces): Truy tìm Phân tán (Distributed Tracing)
* **Vấn đề:** Một yêu cầu của người dùng (ví dụ: thanh toán) đi qua 5 dịch vụ khác nhau (A $\rightarrow$ B $\rightarrow$ C $\rightarrow$ D $\rightarrow$ E). 
Yêu cầu này mất 2 giây, nhưng bình thường chỉ mất 200ms. Dịch vụ nào là điểm nghẽn cổ chai?
* **Mẫu hình:** `Distributed Tracing` (Truy tìm Phân tán).
* **Giải pháp:** (Ví dụ: sử dụng các công cụ như Jaeger ).  
1. Khi yêu cầu bắt đầu tại dịch vụ đầu tiên (A), một Trace ID (Mã Dấu vết) duy nhất được tạo ra.

2. Trace ID này được truyền đi trong metadata (ví dụ: HTTP headers) của mọi lệnh gọi mạng tiếp theo (A đến B, B đến C, v.v.).

3. Mỗi dịch vụ ghi lại công việc của mình dưới dạng một "span" (khoảng thời gian) và gắn nó với Trace ID đó.

4. Một hệ thống thu thập trung tâm (như Jaeger) tập hợp tất cả các span có cùng Trace ID và tái tạo lại toàn bộ hành trình của yêu cầu dưới dạng biểu đồ Gantt. 
Điều này cho phép các nhà phát triển thấy chính xác yêu cầu đã đi đâu và thời gian xử lý ở mỗi bước, giúp xác định điểm nghẽn một cách nhanh chóng.  

## VII. Vận hành Thực tế: Các Mẫu hình Triển khai (Deployment Patterns)
Cuối cùng, sau khi đã thiết kế, phân rã và xây dựng các dịch vụ, câu hỏi thực tế đặt ra là: Làm thế nào để đóng gói và vận hành hàng chục hoặc hàng trăm dịch vụ này trong môi trường production?.

### A. Phân tích Mẫu hình: Service per Container (Dịch vụ trên mỗi Container)
Đây là một trong những mẫu hình triển khai phổ biến và nền tảng nhất trong các hệ thống hiện đại.   

**Định nghĩa:** Đóng gói mỗi phiên bản dịch vụ dưới dạng một ảnh container (ví dụ: Docker) và triển khai mỗi phiên bản như một container duy nhất.   

**Lợi ích:**

* **Đóng gói Công nghệ:** Container bao bọc dịch vụ và tất cả các phụ thuộc của nó (thư viện, runtime) thành một đơn vị bất biến. Một dịch vụ viết bằng Java và một dịch vụ viết bằng Python được khởi động và quản lý theo cùng một cách thức chuẩn hóa.   

* **Cô lập Tài nguyên:** Container cung cấp sự cô lập nhẹ, cho phép giới hạn tài nguyên (CPU, bộ nhớ) mà mỗi dịch vụ có thể tiêu thụ.   

* **Tốc độ:** Container khởi động nhanh hơn đáng kể so với một máy ảo (VM) hoàn chỉnh, vì chúng chia sẻ nhân (kernel) của hệ điều hành chủ.   

* **Bối cảnh:** Mẫu hình này là sự cải tiến so với các mẫu hình cũ hơn như `Single Service per Host` hoặc `Service-per-VM` và là nền tảng cho các nền tảng điều phối (Service deployment platform) như Kubernetes.

### B. Phân tích Mẫu hình: Service Mesh (Lưới Dịch vụ)

`Service Mesh` là một sự tiến hóa quan trọng trong kiến trúc microservice, đại diện cho sự trừu tượng hóa của nhiều mẫu hình phức tạp.
**Định nghĩa:** Một Service Mesh là một lớp cơ sở hạ tầng (infrastructure layer) chuyên dụng, có thể cấu hình, được thiết kế để xử lý giao tiếp giữa các dịch vụ.
**Kiến trúc:** Nó bao gồm hai thành phần chính: 
1. **Data Plane (Mặt phẳng Dữ liệu):** Bao gồm các proxy "sidecar" (như Envoy). Một proxy sidecar được triển khai chạy bên cạnh mỗi container dịch vụ. Tất cả lưu lượng mạng đi vào và đi ra khỏi container dịch vụ đều bị chặn và định tuyến qua proxy này.
2. **Control Plane (Mặt phẳng Điều khiển):** (Ví dụ: Istio ). Đây là "bộ não" trung tâm, cung cấp API để định cấu hình và quản lý hành vi của tất cả các sidecar proxy trong Data Plane.

`Service Mesh`  đại diện cho một sự thay đổi mô hình mạnh mẽ. Theo truyền thống, các nhà phát triển phải triển khai các mẫu hình phức tạp (như Circuit Breaker, Service Discovery, Distributed Tracing) bằng cách thêm các thư viện (ví dụ: Netflix Hystrix ) trực tiếp vào mã nguồn nghiệp vụ của họ (một phương pháp được gọi là Microservice Chassis ).

`Service Mesh` chuyển tất cả logic này từ lớp ứng dụng sang lớp cơ sở hạ tầng (sidecar proxy).
* Sidecar Proxy có thể tự động thực hiện `Circuit Breaking.` 
* Nó tự động xử lý `Service Discovery`
* Nó tự động tảo ra và truyền bá metadata cho `Distributed Tracing`.
* Nó tự động mã hoá lưu lượng (mTLS) để đảm bảo `Security` (Bảo mật). 

Bằng cách này, `Service Mesh` cho phép các nhà phát triển tập trung gần như hoàn toàn vào logic nghiệp vụ cốt lõi (các mẫu hình `Decomposition`), 
trong khi các khía cạnh phức tạp của giao tiếp, độ tin cậy và khả năng quan sát được xử lý một cách nhất quán bởi lớp cơ sở hạ tầng.

## VIII. Tổng kết: Sự hội tụ và Con đường Phía trước
Báo cáo này đã trình bày một phân tích toàn diện về Ngôn ngữ Mẫu hình Kiến trúc Microservice. 
Phân tích cho thấy rõ ràng rằng đây không phải là một danh sách các lựa chọn độc lập, 
mà là một hành trình nhân quả của các quyết định và hậu quả.   

1. Quyết định nền tảng là **Decomposition** (phân rã)
2. Quyết định này tạo ra các thách thức phức tạp về **Data** (dữ liệu) (dẫn đến `Database per Service` và `Saga`) và **Communication** (giao tiếp) (dẫn đến `API Gateway` và `Service Discovery`).
3. Các thách thức giao tiếp mạng đòi hỏi các giải pháp **Reliablity** (độ tin cậy) (như `Circuit Breaker`) để ngăn chặn lỗi xếp tầng. 
4. Toàn bộ hệ thống phân tán buộc phải có **Observability** (khả năng quan sát) (Logs, Traces, Metrics) để duy trì khả năng quản lý và gỡ lỗi.
5. Cuối cùng, các mẫu hình **Deployment** (Triển khai) (như `Service per Container` và `Service Mesh`) cung cấp các giải pháp thực tế để vận hành sự phức tạp này, 
với `Service Mesh` đại diện cho sự trừu tượng hóa và tự động hóa cao nhất của nhiều mẫu hình cốt lõi.

Việc áp dụng kiến trúc microservice không phải là một mục tiêu, mà là một quá trình liên tục quản lý các đánh đổi. 
Ngôn ngữ mẫu hình này cung cấp bộ từ vựng và bản đồ tư duy cần thiết để các kiến trúc sư và các nhóm kỹ thuật thảo luận, 
tranh luận và lựa chọn các đánh đổi đó một cách thông minh, hiểu rõ các hệ quả sâu sắc của từng quyết định kiến trúc.