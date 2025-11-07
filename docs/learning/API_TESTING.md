# API Testing with Sanic Framework

## Mục lục

[Phần I. Khung chiến lược để kiểm thử API](#phần-i-khung-chiến-lược-để-kiểm-thử-api)
  * [1. Kim tự tháp kiểm thử - Nền tảng cho chất lượng bền vững](#1-kim-tự-tháp-kiểm-thử---nền-tảng-cho-chất-lượng-bền-vững)
    * [1.1. Giới thiệu kim tự tháp kiểm thử (The Testing Pyramid)](#11-giới-thiệu-kim-tự-tháp-kiểm-thử-the-testing-pyramid)
    * [1.2. Ánh xạ kim tự tháp vào một ứng dụng Sanic CRUD](#12-ánh-xạ-kim-tự-tháp-vào-một-ứng-dụng-sanic-crud)
  * [2. Phân tích sâu các tầng kiểm thử](#2-phân-tích-sâu-các-tầng-kiểm-thử)
    * [2.1. Unit Tests: Nền tảng của sự tự tin](#21-unit-tests-nền-tảng-của-sự-tự-tin)
    * [2.2. Functional Tests: Xác thức "Hợp đồng" API](#22-functional-tests-xác-thức-hợp-đồng-api)
    * [2.3. Integration Tests: Đảm bảo hệ thống hoạt động đồng bộ](#23-integration-tests-đảm-bảo-hệ-thống-hoạt-động-đồng-bộ)

[Phần II. Kiến trúc bộ kiểm thử (Test Suite)](#phần-ii-kiến-trúc-bộ-kiểm-thử-test-suite)
  * [3. Bộ công cụ thiết yếu: Pytest và Sanic-Testing](#3-bộ-công-cụ-thiết-yếu-pytest-và-sanic-testing)
    * [3.1. Thiết lập môi trường](#31-thiết-lập-môi-trường)
    * [3.2. Sanic Test Clients: Phân tích và Lựa chọn](#32-sanic-test-clients-phân-tích-và-lựa-chọn)
  * [4. Cấu trúc Test Suite: Rõ ràng và dễ mở rộng](#4-cấu-trúc-test-suite-rõ-ràng-và-dễ-mở-rộng)
    * [4.1. Bố cục thư mục và tệp](#41-bố-cục-thư-mục-và-tệp)
    * [4.2. Vai trò của `conftest.py`: Trung tâm của Fixtures](#42-vai-trò-của-conftestpy-trung-tâm-của-fixtures)

[Phần III. Triển khai kiểm thử cho CRUD API](#phần-iii-triển-khai-kiểm-thử-cho-crud-api)
  * [5. Unit Testing: Xây dựng logic vững chắc](#5-unit-testing-xây-dựng-logic-vững-chắc)
    * [5.1. Kiểm thử logic nghiệp vụ (Service Layer)](#51-kiểm-thử-logic-nghiệp-vụ-service-layer)
    * [5.2. Kỹ thuật Mocking để cô lập phụ thuộc](#52-kỹ-thuật-mocking-để-cô-lập-phụ-thuộc)
  * [6. Functional Testing: Xác thực hoạt động của Endpoint.](#6-functional-testing-xác-thực-hoạt-động-của-endpoint-)
    * [6.1. Sử dụng `asgi_client` và mocking lớp dữ liệu](#61-sử-dụng-asgi_client-và-mocking-lớp-dữ-liệu)
    * [6.2. Viết Test cho từng Endpoint CRUD](#62-viết-test-cho-từng-endpoint-crud)
  * [7. Integrational Testing: Kiểm tra toàn vẹn hệ thống](#7-integrational-testing-kiểm-tra-toàn-vẹn-hệ-thống)
    * [7.1. Thiết lập Test Database](#71-thiết-lập-test-database)
    * [7.2 Quản lý trạng thái Database với Fixtures](#72-quản-lý-trạng-thái-database-với-fixtures)
    * [7.3. Viết Test cho một luồng nghiệp vụ hoàn chính](#73-viết-test-cho-một-luồng-nghiệp-vụ-hoàn-chính)

## Phần I. Khung chiến lược để kiểm thử API
### 1. Kim tự tháp kiểm thử - Nền tảng cho chất lượng bền vững
#### 1.1. Giới thiệu kim tự tháp kiểm thử (The Testing Pyramid)
Kim tự tháp kiểm thử là một khung chiến lược, không phải là một quy
tắc cứng nhắc, nhằm tối ưu hoá hiệu quả của quy trình kiểm thử tự động. 
Mô hình này phân bổ các loại kiểm thử khác nhau vào các tầng riêng biệt, 
nhấn mạnh việc có một số lượng lớn các bài kiểm thử đơn vị (unit test) nhanh 
và chi phí thấp ở tầng đáy, một số lượng vừa phải các bài kiểm thử tích hợp 
(integration test) ở tầng giữa, và ít hơn các bài kiểm thử đầu cuối 
(end-to-end test) chậm và tốn kém ở tầng đỉnh. Mục tiêu cuối cùng là đạt được 
một vòng lặp phản hồi nhanh chóng, độ bao phủ kiểm thử toàn diện, và giảm thiểu chi phí 
bảo trì, từ đó dẫn đến các quy trình kiểm thử hiệu quả và đáng tin cậy hơn.

Cấu trúc ba tầng của kim tự tháp bao gồm:
- **Unit Tests (Nền tảng):** Đây là tầng nền tảng, chiếm số lượng lớn nhất. Các bài kiểm thử này
nhanh, chi phí thấp, và tập trung vào việc xác minh các đơn vị mã nguồn nhỏ (như hàm, phương thức, hoặc lớp) 
một cách cô lập. 
- **Integration Tests (Tầng giữa):** Tầng này kiểm tra sự tương tác giữa các thành phần hoặc module của hệ thống. 
Chúng chậm hơn unit test vì thường liên quan đến các phụ thuộc bên ngoài như cơ sở dữ liệu hoặc các dịch vụ khác.
- **End-to-End (E2E) Tests (Đỉnh):** Tầng cao nhất, có số lượng ít nhất. Các bài kiểm thử này giả lập hành vi của 
người dùng thực tế, kiểm tra toàn bộ ứng dụng từ đầu đến cuối. Chúng là loại kiểm thử chậm nhất và tốn kém nhất để 
viết và bảo trì. 

Việc áp dụng mô hình kim tự tháp không chỉ là một lựa chọn kỹ thuật mà còn là một quyết định chiến lược về tốc độ 
phát triển và chi phí. Hình dạng của kim tử tháp phản ứng trực tiếp lợi tức đầu tư (ROI). Unit test ở tầng đáy cung 
cấp phản hồi ngay lập tức với chi phí thấp, tạo thành một nền tảng rộng và ổn định. Khi di chuyển lên các tầng cao hơn, 
các bài kiểm thử trở nên chậm hơn, dễ bị lỗi ("flaky") và tốn kém hơn để chạy và bảo trì. Mối quan hệ nhân quả này 
(độ phức tạp -> chi phí -> độ tin cậy thấp) định hình chiến lược: đẩy việc kiểm thử xuống các tầng thấp nhất có thể. 
Một dự án có kim tự tháp bị đảo ngược (mô hình "cây kem ốc quế") sẽ phải đối mặt với các pipeline CI/CD chậm chạp, các 
bài kiểm thử không ổn định, và chi phí gỡ lỗi cao do lỗi được phát hiện muộn trong quy trình. 

Lợi ích chính của việc tuân thủ mô hình này bao gồm: 
- **Tăng tốc độ thực thi:** Ưu tiên unit test đảm bảo phản hồi nhanh, đẩy nhanh chu kỳ phát triển. 
- **Giảm chi phí bảo trì:** Ít bài kiểm thử E2E hơn đồng nghĩa với việc tốn ít thời gian hơn để gỡ lỗi và bảo trì các bài 
kiểm thử phức tạp. 
- **Tăng độ tin cậy và độ bao phủ:** Một cách tiếp cận cân bằng đảm bảo độ bao phủ toàn diện ở tất cả các cấp mà không quá 
làm quá tải tầng trên cùng. 

#### 1.2. Ánh xạ kim tự tháp vào một ứng dụng Sanic CRUD
Khi áp dụng mô hình này vào một ứng dụng API CRUD được xây dựng bằng Sanic, các tầng kiểm thử được ánh xạ như sau: 
- **Unit Tests:** Sẽ kiểm thử logic nghiệp vụ thuần tuý nằm trong các lớp `service`, các hàm `helper`, và các phương thức 
tuỳ chỉnh `model`. Các bài kiểm thử này sẽ không khởi động server Sanic hay kết nối đến cơ sở dữ liệu thực. 
- **Functional Tests:** Sẽ kiểm thử từng API endpoint một cách độc lập để xác thực "hợp đồng" của API 
(input, output, status code, cấu trúc lỗi). Đây là tầng kiểm tra hành vi chính của ứng dụng, nơi lớp cơ sở dữ liệu sẽ được mock (giả lập).
- **Integrational Tests:** Sẽ kiểm thử một luồng hoạt động hoàn chỉnh: gọi một API endpoint, kích hoạt logic nghiệp vụ, và xác minh rằng dữ liệu 
được ghi, đọc, cập nhật, hoặc xoá một cách chính xác trong một cơ sở dữ liệu thử nghiệp. 

### 2. Phân tích sâu các tầng kiểm thử
#### 2.1. Unit Tests: Nền tảng của sự tự tin
**Định nghĩa và mục tiêu:** Unit Testing là một phương pháp kiểm thử phần mềm, trong đó các đơn vị (unit) mã nguồn riêng lẻ được kiểm tra một cách cô lập 
để xác thực rằng chúng hoạt động đúng như mong đợi. Một "unit" có thể là **một hàm, một phương thức trong một lớp, hoặc toàn bộ một lớp.**

**Nguyên tắc cốt lõi - Sự cô lập (isolation):** Đây là yếu tố quan trọng nhất của unit test. Mọi phụ thuộc bên ngoài như cơ sở dữ liệu, các API khác, 
hoặc hệ thống tệp tin phải được thay thế bằng các "test doubles" như Mocks hoặc Stubs. Điều này đảm bảo rằng một bài kiểm thử chỉ thất bại khi logic 
của chính unit đó bị sai, chứ không phải do lỗi từ một thành phần bên ngoài. Việc này giúp xác định và sửa lỗi nhanh hơn nhiều. 

**Trong Sanic:** Các unit test sẽ không khởi tạo một thực thể `Sanic app`. Thay vào đó, chúng sẽ import trực tiếp các module `service` hoặc `helper` và kiểm thử 
chúng như các module Python thông thường, hoàn toàn độc lập với web framework. 

#### 2.2. Functional Tests: Xác thức "Hợp đồng" API
**Định nghĩa và mục tiêu:** Functional testing là một loại kiểm thử hộp đen (Black Box testing), xác thực hệ thống dựa trên các yêu cầu chức năng của nó. 
Nó không quan tâm đến mã nguồn bên trong mà chỉ tập trung vào việc cung cấp đầu vào (input) và xác minh đầu ra (output) có khớp với mong đợi hay không. 

Thuật ngữ "functional test" có thể gây nhầm lẫn, vì một số tài liệu liệt kê cả unit test và integration test là các loại của functional testing. 
Để mang lại sự rõ ràng tối đa, trong khuôn khổ của sổ tay này, **Functional Tests** được định nghĩa là: **_Các bài kiểm thử hộp đen xác minh hành vi của từng API 
riêng lẻ so với đặc tả của nó, được thực thi một cách độc lập khỏi các phụ thuộc bên ngoài như cơ sở dữ liệu bền vững_**. Định nghĩa này mang lại một ý nghĩa cụ thể 
và có thể hoạt động được trong kim tự tháp kiểm thử của chúng ta, định vị nó giữa unit test thuần tuý và integration test toàn diện. 

**Trong Sanic:** Chúng ta sẽ triển khai các bài kiểm thử này bằng cách sử dụng **SanicASGITestClient** để gọi trực tiếp các route handler, bỏ qua lớp mạng, giúp các bài kiểm thử 
chạy cực kỳ nhanh. Lớp cơ sở dữ liệu sẽ được mock để cô lập hoàn toàn endpoint khỏi sự phụ thuộc vào trạng thái của DB. 

#### 2.3. Integration Tests: Đảm bảo hệ thống hoạt động đồng bộ
**Định nghĩa và mục tiêu:** Integration testing là loại kiểm thử trong đó các module phần mềm được tích hợp một cách logic và được kiểm thử như một nhóm. Mục đích chính là phát hiện 
các lỗi trong sự tương tác, giao tiếp, và luồng dữ liệu giữa các thành phần này khi chúng làm việc cùng nhau. 

**Khi nào cần Integration Test:** Loại kiểm thử này được áp dụng sau unit test và trước system test. Nó đặc biệt cần thiết khi các module cần chia sẻ dữ liệu, gọi API của nhau, hoặc tương tác 
với các hệ thống của bên thứ ba như cơ sở dữ liệu, cache, hoặc message queue. 

**Trong Sanic:** Đây là lúc chúng ta sử dụng `SanicTestClient` hoặc `ReusableClient` để gửi các request HTTP thực sự đến một ứng dụng Sanic đang chạy. Ứng dụng này sẽ được cấu hình để kết nối đến 
một cơ sở dữ liệu thử nghiệm riêng biệt. Các bài kiểm thử sẽ xác minh toàn bộ luồng hoạt động từ request HTTP, qua xử lý logic, đến response trả về, và quan trọng nhất là xác minh trạng thái của cơ sở 
dữ liệu sau khi request được thực thi.

## Phần II. Kiến trúc bộ kiểm thử (Test Suite)
### 3. Bộ công cụ thiết yếu: Pytest và Sanic-Testing
#### 3.1. Thiết lập môi trường
Để xây dựng một bộ kiểm thử hiện đại và hiểu quả cho Sanic, chúng ta cần các thư viện sau: 
- `pytest`: Một framework kiểm thử mạnh mẽ, linh hoạt và phổ biến cho Python, cung cấp các tính năng như test, discovery, fixtures và assesrtion introspection.
- `pytest-asyncio`: Một plugin của `pytest` cho phép chạy các hàm test bất đồng bộ (`async def`) một cách liền mạch, điều này là bắt buộc khi làm việc với Sanic.
- `sanic-testing`: Thư viện kiểm thử chính thức của Sanic. Nó cung cấp các test client để tương tác với ứng dụng Sanic trong môi trường kiểm thử. 

Cần lưu ý về sự phát triển của hệ sinh thái kiểm thử Sanic. Các phiên bản Sanic trước 21.3 có module kiểm thử được tích hợp sẵn. Các tài liệu cũ hơn có thể đề cập 
đến việc sử dụng `aiohttp` làm client nền tảng. Tuy nhiên, cách tiếp cận hiện đại và được khuyến nghị là sử dụng gói `sanic-testing` độc lập, gói này sử dụng `httpx` làm 
nền tảng, mang lại hiệu suất và tính tương thích tốt hơn. Sổ tay này sẽ chỉ tập trung vào bộ công cụ hiện đại này để đảm bảo bạn xây dựng một bộ kiểm thử có khả năng 
bảo trì và nâng cấp trong tương lai. 

#### 3.2. Sanic Test Clients: Phân tích và Lựa chọn
Thư viện `sanic-testing` cung cấp ba loại test client khác nhau, mỗi loại phù hợp với một mục đích sử dụng cụ thể. Việc lựa chọn đúng client cho đúng loại test là một 
quyết định chiến lược quan trọng. 
- `SanicTestClient` **(Sync Client)**: Client này khởi động một server Sanic thực sự trên một socket mạng cho mỗi request được gửi đi. Nó mô phỏng chính xác một request HTTP thực tế, 
bao gồm cả lớp mạng. Do có chi phí khởi động và tắt server cho mỗi lần gọi, nó chậm hơn các client khác nhưng lại lý tưởng cho integration test.
- `SanicASGITestClient` **(Async ASGI Client)**: Client này không khởi động server. Thay vào đó, nó sử dụng giao diện ASGI để "móc" trực tiếp vào bên trong ứng dụng và thực thi các route 
handler. Vì không có chi phí mạng, nó cực kỳ nhanh và là lựa chọn hoàn hảo cho functional test và unit test ở cấp độ route handler. 
- `ReusableClient` **(Persistent Client)**: Đây là một biến thể của `SanicTestClient`. Nó khởi động server một lần và tái sử dụng instance đó cho nhiều request trong cùng một ngữ cảnh 
(context manager). Điều này giúp tối ưu hoá hiệu năng cho các bộ integration test lớn cần thực hiện nhiều lệnh gọi API liên tiếp. 

Bảng dưới đây tóm tắt các đặc điểm và trường hợp sử dụng chính của từng client để giúp bạn đựa ra lưạ chọn phù hợp. 

### 4. Cấu trúc Test Suite: Rõ ràng và dễ mở rộng
#### 4.1. Bố cục thư mục và tệp
Một cấu trúc test suite được tổ chức tốt là yếu tố sống còn để đảm bảo khả năng bảo trì và mở rộng. Nguyên tắc vàng của thư mục `tests` 
nên phản chiếu cấu trúc của mã nguồn ứng dụng (thường là thư mục `app` hoặc `src`).

Một cấu trúc đuợc khuyến nghị là tách biệt các loại test và các thư mục con riêng biệt. Điều này không chỉ giúp tổ chức mã nguồn rõ ràng 
mà còn cho phép chạy riêng từng loại test một cách dễ dàng (ví dụ: `pytest tests/unit`)

```
project_root/
├── app/
│   └──... (mã nguồn ứng dụng)
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── unit/
    ├── functional/
    └── integration/
```
Pytest tuân theo các quy ước đặt tên tiêu chuẩn để tự động phát hiện các bài kiểm thử:
- Các tệp kiểm thử phải có tên bắt đầu bằng `test_` hoặc kết thúc bằng `_test.py`
- Các hàm hoặc phương thức kiểm thử bên trong các tệp này phải có tên bắt đàu bằng `test_`.

#### 4.2. Vai trò của `conftest.py`: Trung tâm của Fixtures
`conftest.py` là một tệp đặc biệt của Pytest, đóng vai trò là nơi trung tâm để định nghĩa các 
fixtures có thể được chia sẻ trên toàn bộ test suite hoặc trong một thư mục cụ thể. Đây là nơi 
lý tưởng để định nghĩa các fixtures "đắt tiền" (tốn thời gian để thiết lập) hoặc được sử dụng chung, 
chẳng hạn như: 
- Fixture để khởi tạo instance `Sanic app` cho môi trường testing.
- Fixture để tạo ra các test client (`asgi_client`, `test_client`).
- Fixture để thiết lập và dọn dẹp kết nối đến cơ sở dữ liệu thử nghiệp. 

Pytest fixtures có một tham số scope để kiểm soát vòng đời của chúng, giúp tối ưu hoá việc thiết lập và dọn dẹp, 
tránh lặp lại các thao tác không cần thiết. Các scope phổ biến bao gồm:
- `function`: Mặc định. Fixture được tạo lại cho mỗi hàm test. 
- `class`: Fixture được tạo một lần cho mỗi lớp test. 
- `module`: Fixture được tạo mỗi lần cho mỗi tệp test. 
- `session`: Fixture được tạo một lần cho toàn bộ phiên chạy test. Ví dụ, việc kết nối đến cơ sở dữ liệu nên 
sử dụng `scope="session"` để tránh phải tạo và huỷ kết nối liên tục.

## Phần III. Triển khai kiểm thử cho CRUD API
### 5. Unit Testing: Xây dựng logic vững chắc
#### 5.1. Kiểm thử logic nghiệp vụ (Service Layer)
Unit test tập trung vào việc xác minh các đơn vị logic nhỏ nhất. Trong kiến trúc ứng dụng được phân lớp, 
lớp `service` là nơi chứa logic nghiệp vụ chính, và do đó là đối tượng lý tưởng cho unit test. Các bài kiểm thử 
này nên hoàn toàn độc lập với framework web và không thực hiện bất kỳ thao tác I/O nào (không gọi DB, không gọi API ngoài).
### 5.2. Kỹ thuật Mocking để cô lập phụ thuộc
Để đạt được sự cô lập, chúng ta cần sử dụng kỹ thuật "mocking". Mocking là việc thay thế các đối tượng phục thuộc (dependences)
bằng các đối tượng giả (mock objects) mà chúng ta có thể kiểm soát hành vi. Thư viện `unitest.mock` của Python (hoặc plugin `pytest-mock`) 
là công cụ tiêu chuẩn cho việc này. 

Một phương pháp mocking truyền thống là sử dụng `patch`, tuy nhiên nó có thể dễ bị lỗi vì phụ thuộc vào đường dẫn import của đối tượng cần mock. 
Môt cách tiếp cận hiện đại và mạnh mẽ hơn là thiết kế ứng dụng để có thể kiểm thử ngay từ đầu bằng cách sử dụng Dependency Injection (DI). 
Sanic Extensions cung cấp một hệ thống DI mạnh mẽ. Bằng cách inject các phụ thuộc (như một `database repository`) vào một route handler, chúng ta 
tạo ra một "đường may" (seam) rõ ràng để thay thế trong quá trình kiểm thử. Trong các bài kiểm thử, chúng ta có thể dễ dàng cung cấp các phiên bản mock 
của phụ thuộc đó mà không cần dùng đến `patch`. Cách tiếp cận này giúp các bài kiểm thử trở nên mạnh mẽ hơn, dễ đọc hơn và ít bị ràng buộc vào cấu trúc 
nội bộ của ứng dụng. 

Ví dụ, khi kiểm thử hàm `create_user_service`, chúng ta sẽ mock đối tượng `database_repository` và xác minh rằng phương thức `repository.save()` được gọi 
với đúng các tham số mong đợi. 

### 6. Functional Testing: Xác thực hoạt động của Endpoint. 
#### 6.1. Sử dụng `asgi_client` và mocking lớp dữ liệu
Trong các functional test, chúng ta sẽ sử dụng `asgi_client` để đạt hiệu năng cao nhất. Lớp truy cập dữ liệu (repository hoặc ORM model) sẽ được mock để các 
endpoint không phụ thuộc vào trạng thái của cơ sở dữ liệu. Điều này cho phép chúng ta kiểm tra tất cả các luồng logic (thành công, lỗi validation, không tìm thấy) 
một cách độc lập và có thể dự đoán được.  

#### 6.2. Viết Test cho từng Endpoint CRUD
Mỗi endpoint CRUD cần được kiểm tra cho các trường hợp thành công và thất bại. 
- `POST /items` **(Create):**
  - **Trường hợp thành công:** Gửi một payload JSON hợp lệ. Xác nhận status code trả về là `201 Created`. Kiểm tra cấu trúc và nội dung của response body 
  để đảm bảo nó chứa dữ liệu của đối tượng vừa được tạo. 
  - **Trường hợp lỗi validation:** Gửi một payload không hợp lệ (thiếu trường bắt buộc, sai kiểu dữ liệu). Xác nhận status code là `400 Bad Request` hoặc `422 Unprocessable Entity`
  và kiểm tra nội dung thông báo lỗi có ý nghĩa. 

- `GET /items` và `GET /items/{item_id}` **(Read):**
  - **Trường hợp thành công:** Mock lớp repository để trả về một danh sách các đối tượng hoặc một đối tượng duy nhất. Gọi API và xác nhận status code là `200 OK`, 
  đồng thời kiểm tra dữ liệu trả về có khớp với dữ liệu đã được mock hay không.
  - **Trường hợp không tìm thấy:** Gọi `GET /items/{item_id}` với một ID không tồn tại. Xác nhận status code trả về là `404 Not Found`.

- `PUT /items/{item_id}` **(Update):**
  - **Trường hợp thành công:** Gửi một payload cập nhật hợp lệ đến một ID tồn tại. Xác nhận status code là `200 OK` và dữ liệu trong response body đã được cập nhật chính xác. 
  - **Trường hợp lỗi:** Cập nhật một ID không tồn tại (mong đợi `404 Not Found`), hoặc gửi dữ liệu không hợp lệ (mong đợi `400`/`422`).

- `DELETE /items/{item_id}` **(Delete):**
  - **Trường hợp thành công:** Gọi API với một ID hợp lệ. Xác nhận status code là `204 No Content` và không có response body.
  - **Trường hợp không tìm thấy:** Gọi API với một ID không tồn tại. Xác nhận status code là `404 Not Found`.

### 7. Integrational Testing: Kiểm tra toàn vẹn hệ thống
#### 7.1. Thiết lập Test Database
Nhiều nhà phát triển gặp khó khăn với việc kiểm thử cơ sở dữ liệu. Tuy nhiên, có một mô hình chuẩn và hiệu quả đã được cộng đồng công nhận. 
Mô hình này bao gồm việc sử dụng một cơ sở dữ liệu SQLite trong bộ nhớ (`sqlite://:memory:`) để đảm bảo tốc độ và sự cô lập. Toàn bộ quá trình thiết lập
và doàn dẹp này được đóng gói trong một `pytest fixture` với `scope="session"`. Fixture này sẽ:

1. Khởi tạo SQLAlchemy-ORM với một DB SQLite trong bộ nhớ. 
2. Tự động tạo tất cả các bảng dựa trên các model đã định nghĩa (`generate_schemas=True`).
3. `yield` kết nối để các bài kiểm thử có thể sử dụng. 
4. Huỷ toàn bộ cơ sở dữ liệu sau khi toàn bộ phiên kiểm thử kết thúc.

Cách tiếp cận này cung cấp một giải pháp mạnh mẽ, có thể tái sử dụng và tuân thủ các thực hành tốt nhất cho việc kiểm thử tích hợp.

#### 7.2 Quản lý trạng thái Database với Fixtures
Để các bài kiểm thử tích hợp có thể dự đoán được, chúng ta cần kiểm soát trạng thái của cơ sở dữ liệu. `Pytest fixtures` là công cụ hoàn hảo cho việc này. 
Chúng ta có thể tạo các fixtures để khởi tạo dữ liệu mẫu (seed data) trước khi mỗi bài kiểm thử chạy. 
Ví dụ, một fixture tên là `created_item` có thể tạo một bản ghi item trong cơ sở dữ liệu thử nghiệm và trả về đối tượng đó.

Để đảm bảo các bài kiểm thử không ảnh hưởng lẫn nhau, mỗi bài kiểm thử nên được chạy trong một transaction riêng biệt, 
và transaction đó sẽ được rollback sau khi bài kiểm thử kết thúc. Điều này đảm bảo cơ sở dữ liệu luôn ở trạng thái sạch sẽ trước khi bắt đầu một bài kiểm thử mới.

### 7.3. Viết Test cho một luồng nghiệp vụ hoàn chính
Đây là lúc kết hợp tất cả các thành phần lại với nhau. Một bài kiểm thử tích hợp có thể thực hiện một chuỗi các hành động mô phỏng một luồng sử dụng thực tế:
1. Gửi request **POST** để tạo một item mới. Xác nhận response là 201 Created và lưu lại ID của item.
2. Sử dụng ID vừa nhận được, gửi request **GET** `/items/{id}`. Xác nhận response là `200 OK` và dữ liệu trả về khớp với dữ liệu đã tạo.
3. Truy vấn trực tiếp vào cơ sở dữ liệu thử nghiệm để xác nhận rằng bản ghi đã thực sử tồn tại. 
4. Gửi request **PUT** `/items/{id}` để cập nhật item. Xác nhận response là `200 OK`.
5. Gửi lại request **GET** `/items/{id}`. Xác nhận rằng dữ liệu đã được cập nhật.
6. Gửi request **DELETE** `/items/{id}`. Xác nhận response là `204 No Content`.
7. Gửi lại request **GET** `/items/{id}`. Lần này, xác nhận nhận được response `404 Not Found`.

Bài kiểm thử này xác minh rằng tất cả các lớp của ứng dụng (routing, services, models, database) hoạt động một cách hài hòa và chính xác.
