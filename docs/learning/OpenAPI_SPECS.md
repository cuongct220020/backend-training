# OpenAPI Specs Handbook

## Mục lục

### Phần I. OpenAPI Specification (OAS)

1.  [Tổng quan về OpenAPI Specification (OAS) - Nền tảng API hiện đại](#1-tổng-quan-về-openapi-specification-oas---nền-tảng-api-hiện-đại)
    * [1.2. Cấu trúc tài liệu: YAML so với JSON](#12-cấu-trúc-tài-liệu-yaml-so-với-json)
    * [1.3. Đối tượng gốc `openapi`, `info` và `servers`](#13-đối-tượng-gốc-openapi-info-và-servers)
2.  [Định nghĩa bề mặt API với paths và operations](#2-định-nghĩa-bề-mặt-api-với-paths-và-operations)
    * [2.1. Đối tượng `paths`: Ánh xạ URL tới các thao tác](#21-đối-tượng-paths-ánh-xạ-url-tới-các-thao-tác)
    * [2.2. Đối tượng `operations`: Các phương thức HTTP và Siêu dữ liệu](#22-đối-tượng-operations-các-phương-thức-http-và-siêu-dữ-liệu)
    * [2.3. Mô tả tham số (`path`, `query`, `header`, `cookie`)](#23-mô-tả-tham-số-path-query-header-cookie)
3.  [Nền tảng của tái sử dụng `components` và `schemas`](#3-nền-tảng-của-tái-sử-dụng-components-và-schemas)
    * [3.1. Nguyên tắc DRY trong định nghĩa API: Đối tượng `components`](#31-nguyên- tắc-dry-trong-định-nghĩa-api-đối-tượng-components)
    * [3.2. Định nghĩa cấu trúc dữ liệu với `schemas`](#32-định-nghĩa-cấu-trúc-dữ-liệu-với-schemas)
    * [3.3. Liên kết mọi thứ với `$ref`](#33-liên-kết-mọi-thứ-với-ref)
4.  [Mô tả tải trọng và phản hồi](#4-mô-tả-tải-trọng-và-phản-hồi)
    * [4.1. Đối tượng `requestBody`](#41-đối-tượng-requestbody)
    * [4.2. Đối tượng `responses`](#42-đối-tượng-responses)
    * [4.3. Kết hợp lại một định nghĩa Endpoint hoàn chỉnh](#43-kết-hợp-lại-một-định-nghĩa-endpoint-hoàn-chỉnh)

### Phần II. Tài liệu hoá API Sanic với `sanic-ext`

5.  [Hệ sinh thái Sanic và vai trò của `sanic-ext`](#5-hệ-sinh-thái-sanic-và-vai-trò-của-sanic-ext)
    * [5.1. Giới thiệu về `sanic-ext`](#51-giới-thiệu-về-sanic-ext)
6.  [Tài liệu hoá dựa trên Decorator trong Sanic](#6-tài-liệu-hoá-dựa-trên-decorator-trong-sanic)
    * [6.1. Decorator `@openapi`](#61-decorator-openapi)
    * [6.2. Tài liệu hoá thao tác và tham số](#62-tài-liệu-hoá-thao-tác-và-tham-số)
    * [6.3. Định nghĩa phần thân yêu cầu và phản hồi](#63-định-nghĩa-phần-thân-yêu-cầu-và-phản-hồi)
7.  [Triển khai CRUD Sanic hoàn chỉnh](#7-triển-khai-crud-sanic-hoàn-chỉnh)

### Phần III. Các chủ đề nâng cao và phương pháp kiến trúc tốt nhất

8.  [Các chiến lược đánh phiên bản API trong OpenAPI](#8-các-chiến-lược-đánh-phiên-bản-api-trong-openapi)
    * [8.1. Tại sao đánh phiên bản lại quan trọng](#81-tại-sao-đánh-phiên-bản-lại-quan-trọng)
    * [8.2. Các chiến lược đánh phiên bản phổ biến](#82-các-chiến-lược-đánh-phiên-bản-phổ-biến)
9.  [Thiết kế vì tính nhất quán và khả năng bảo trì](#9-thiết-kế-vì-tính-nhất-quán-và-khả-năng-bảo-trì)
    * [9.1. Cuộc tranh luận "Design-First" và "Code-First"](#91-cuộc-tranh-luận-design-first-và-code-first)
    * [9.2. Tối đa hóa tái sử dụng với `components`](#92-tối-đa-hóa-tái-sử-dụng-với-components)
    * [9.3. Phản hồi lỗi được tiêu chuẩn hoá](#93-phản-hồi-lỗi-được-tiêu-chuẩn-hoá)
10. [Kết luận](#10-kết-luận)

## Phần I. OpenAPI Specification (OAS)

### 1. Tổng quan về OpenAPI Specification (OAS) - Nền tảng API hiện đại

Trong phát triển API hiện đại, việc bắt đầu bằng việc viết tài liệu không còn là một công việc tẻ nhạt sau khi đã hoàn thành, 
mà đã trở thành một bước đi chiến lược, một công cụ thiết kế cộng tác mạnh mẽ. **OpenAPI Specification (OAS)** chính là trung tâm của triết lý này.

**OpenAPI Specification** (trước đây là Swagger Specification) là một định dạng mô tả API cho các REST API. Nó định nghĩa một giao diện tiêu chuẩn, 
độc lập với ngôn ngữ lập trình, cho phép cả con người và máy tính khám phá và hiểu được khả năng của một dịch vụ mà không cần truy cập vào mã nguồn, tài liệu bổ sung, hay kiểm tra lưu lượng mạng.

**Triết lý "Design First"**: Cốt lõi của việc sử dụng OAS là triết lý "design-first" (thiết kế trước). Thay vì viết mã trước rồi tạo tài liệu sau, 
việc xác định "hợp đồng" API (API Contract) bằng một tệp YAML hoặc JSON mang lại nhiều lợi ích chiến lược:

- **Kiến trúc tốt hơn**: Buộc các nhà phát triển phải suy nghĩ thấu đáo về các tài nguyên, endpoints, tham số và schema dữ liệu trước khi viết một dòng mã nào.
- **Phát triển song song**: Khi hợp đồng đã được thống nhất, các nhóm frontend, backend và QA có thể làm việc song song. Nhóm frontend có thể tạo mock server dựa trên đặc tả, 
trong khi nhóm backend triển khai logic nghiệp vụ.
- **Tự động hóa**: Một đặc tả OpenAPI có thể được sử dụng để tự động tạo ra server stubs (khung sườn server), client libraries (thư viện phía client) cho hơn 40 ngôn ngữ, 
và các bộ kiểm thử tự động, giúp giảm đáng kể thời gian và công sức phát triển.

**Swagger và OpenAPI**: "OpenAPI Specification" là tên của bản thân đặc tả tiêu chuẩn, 
"Swagger" là tên của một bộ công cụ mã nguồn mở được xây dựng xung quanh đặc tả này:

- **Swagger Editor**: Trình soạn thảo dựa trên trình duyệt để viết các định nghĩa OpenAPI.
- **Swagger UI**: Công cụ hiển thị các định nghĩa OpenAPI dưới dạng tài liệu API tương tác, cho phép người dùng thử gọi API trực tiếp từ trình duyệt.
- **Swagger Codegen**: Công cụ tạo ra server stubs và client libraries từ một định nghĩa OpenAPI.

#### 1.2. Cấu trúc tài liệu: YAML so với JSON
Một tài liệu OpenAPI (OpenAPI Document) về bản chất là một đối tượng JSON, có thể được biểu diễn dưới định dạng JSON hoặc YAML. Trong suốt báo cáo này, 
YAML sẽ được sử dụng cho tất cả các ví dụ do khả năng đọc vượt trội của nó đối với các cấu trúc lồng nhau, một đặc điểm phổ biến trong các định nghĩa API.   

Có một số quy tắc định dạng quan trọng cần tuân thủ. Tất cả các tên trường trong đặc tả đều phân biệt chữ hoa chữ thường. Khi sử dụng YAML, 
các khóa trong map phải là chuỗi vô hướng (scalar string), và các thẻ (tags) phải tuân theo bộ quy tắc lược đồ JSON của YAML.

#### 1.3. Đối tượng gốc `openapi`, `info` và `servers`
Một tài liệu API hợp lệ phải chứa một số trường ở cấp cao nhất để thiết lập bối cảnh và metadata cơ bản: 
- `openapi`: Một chuỗi **bắt buộc** chỉ định phiên bản của đặc tả OpenAPI mà tài liệu đang sử dụng (ví dụ: `3.1.0`).
Điều quan trọng là phải phân biệt phiên bản này với phiên bản của chính API của bạn. Phiên bản đặc tả (ví dụ `3.1`)
chỉ định bộ tính năng OAS, trong khi các phiên bản vá lỗi (patch versions) chỉ giải quyết các lỗi hoặc làm rõ tài liệu
chứ không thay đổi tính năng.
- `info`: Một đối tượng **bắt buộc** cung cấp siêu dữ liệu về API. Nó bao gồm `title` (tiêu đề) `version`
(phiên bản của API, ví dụ `1.0.0`), và một `description` (mô tả) hỗ trợ Markdown để định dạng văn bản phong phú.
- `servers`: Một mảng các đối tượng máy chủ (server objects) cung cấp thông tin kết nối đến một máy chủ mục tiêu.
Trường này thay thế các từ khoá `host`, `basePath`, và `schemas` đã lỗi thời từ OAS 2.0, cho phép định nghĩa nhiều
môi trường như phát triển (development), thử nghiệm (staging), và sản xuất (production). Nếu trường `servers` không
được cung cấp, giá trị mặc định sẽ là một trường Server duy nhất với giá trị `url` là `/`.

Việc cấu trúc đối tượng gốc ngay lập tức thiết lập hai mối quan tâm về phiên bản riêng biệt trong bất kỳ dự án API nào:
phiên bản của đặc tả (`openapi`) và phiên bản logic nghiệp vụ của API (`info.version`). Sự tách biệt này là nền tảng.
Trường `openapi` cho các công cụ biết cách phân tích cú pháp tài liệu, xác định các tính năng và cú pháp có sẵn theo tiêu chuẩn.
Ngược lại, trường `info.version` cho người tiêu dùng biết họ đang tương tác với phiên bản nào của chức năng API. Sự phân tách này
cho phép một API phát triển (ví dụ, từ `v1.0.0` lên `v2.0.0`) trong khi vẫn được mô tả bởi cùng một phiên bản ổn định của đặc tả
OpenAPI (ví dụ, `3.1.0`), đảm bảo khả năng tương thích của công cụ theo thời gian. 

#### Ví dụ YAML: Khung sườn tài liệu cơ bản
```YAML
openapi: 3.1.0
info:
  title: Simple Items API
  description: Một API mẫu để quản lý các mặt hàng trong danh mục. Hỗ trợ **Markdown**.
  version: "1.0.0"
servers:
  - url: https://api.example.com/v1
    description: Production Server
  - url: http://localhost:8000/v1
    description: Local Development Server
```

### 2. Định nghĩa bề mặt API với paths và operations
#### 2.1. Đối tượng `paths`: Ánh xạ URL tới các thao tác
Đối tượng `paths` là thành viên cốt lõi của một tài liệu OpenAPI, chứa các đường dẫn và thao tác có sẵn cho API. 
Mỗi khoá trong đối tượng `paths` là một đường dẫn tương đối đến một điểm cuối (endpoint) cụ thể, ví dụ `/users`

Đặc tả hỗ trợ việc tạo mẫu đường dẫn (path templating), sử dụng dấu ngoặc nhọn `{}` để đánh dấu một phần của đường
dẫn URL có thể thay thế bằng các tham số đường dẫn. Ví dụ, đường dẫn `/users/{userId}` chỉ định phần `{userId}` là một biến.
Mỗi biểu thức mẫu trong đường dẫn là **bắt buộc** phải tương ứng với một tham số đường dẫn được định nghĩa trong chính đối tượng
mục đường dẫn (Path Item Object) hoặc tỏng mỗi thao tác (operation) của nó.

#### 2.2. Đối tượng `operations`: Các phương thức HTTP và Siêu dữ liệu
Đối với mỗi đường dẫn, bạn định nghĩa các `operations` (thao tác), là các phương thức HTTP có thể được sử dụng để tương tác
với đường dẫn đó. OAS 3.0 hỗ trợ `get`, `post`, `put`, `patch`, `delete`, `head`, `options`, và `trace`. Một thao tác duy nhất
được định nghĩa là sự kết hợp của một đường dẫn và một phương thức HTTP; do đó, không thể có hai thao tác `get` trên cùng một đường dẫn.

Mỗi đối tượng thao tác có thể chứa các trường siêu dữ liệu quan trọng để làm phong phú tài liệu:
- `tags`: Một mảng các chuỗi được sử dụng để nhóm các thao tác trong các giao diện người dùng tài liệu (như Swagger UI), điều này rất quan trọng
để tổ chức.
- `summary`: Một giải thích ngắn gọn, một dòng mục đích của thao tác.
- `description`: Một mô tả dài hơn, hỗ trợ markdown.
- `operationId`: Một định danh duy nhất của thao tác. Các công cụ tạo mã thường sử dụng `operationId` để tạo tên các phương thức, 
vì vậy việc đảm bảo tính duy nhất là rất quan trọng.

#### 2.3. Mô tả tham số (`path`, `query`, `header`, `cookie`)
Các tham số được định nghĩa trong một mảng `parameters`, có thể tồn tại ở cấp độ đường dẫn (áp dụng cho tất cả các thao tác trong đường dẫn đó)
hoặc cấp độ thao tác. Đặc tả phân biệt bốn loại tham số dựa trên từ khoá `in`:
1. `path`: Các biến tỏng chính đường dẫn URL (ví dụ: `{userId}`). Chúng phải được đánh dấu là `required: true`.
2. `query`: Các tham số được nối với URL sau dấu `?` (ví dụ: `?limit=10`)
3. `header`: Các header HTTP tuỳ chỉnh được gửi cùng với yêu cầu.
4. `cookie`: Các tham số được truyền qua header `Cookie`.
Đối với mỗi tham số, bạn phải định nghĩa `name` (tên), `in` (vị trí), và `schema` (lược đồ) để mô tả kiểu dữ liệu của nó. Các trường `description`
và `required` cũng rất được khuyến khích.

Ví dụ YAML: Endpoint GET với tham số Path và QUERY

```YAML
paths:
  /users/{userId}:
    get:
      tags:
        - Users
      summary: Lấy thông tin người dùng bằng ID
      operationId: getUserById
      parameters:
        - name: userId
          in: path
          description: Định danh duy nhất của người dùng.
          required: true
          schema:
            type: integer
            format: int64
        - name: include_details
          in: query
          description: Có bao gồm chi tiết mở rộng của người dùng hay không.
          required: false
          schema:
            type: boolean
```
### 3. Nền tảng cảu tái sử dụng `components` và `schemas`
#### 3.1. Nguyên tắc DRY tỏng định nghĩa API: Đối tượng `components`
Đối tượng `components` là một kho lưu trữ trung tâm cho các định nghĩa có thể tái sử dụng trong toàn bộ tài liệu OpenAPI.
Việc sử dụng nó là một phương pháp hay nhất, giúp giảm đáng kể sự dư thừa, cải thiện khả năng bảo trì, và đảm bảo tính nhất quán.
Thay vì định nghĩa cùng một đối tượng dữ liệu hoặc phản hồi lỗi ở nhiều nơi, bạn định nghĩa nó một lần trong `components` và tham
chiếu đến nó khi cần.

Đối tượng `components` chứa một tập hợp các trường, mỗi trường là một map các đối tượng có thể tái sử dụng. Các loại thành phần chính
bao gồm `schemas`, `responses`, `parameters`, `examples`, `requestBodies`, `headers` và `securitySchemas`.

#### 3.2. Định nghĩa cấu trúc dữ liệu với `schemas`
Phần `schemas` trong `components` được sử dụng để định nghĩa các mô hình dữ liệu có thể tái sử dụng. Các lược đồ này tuân thủ
đặc tả lược đồ JSON (JSON Schema Specification), cung cấp một bộ từ vựng phong phú để mô tả cấu trúc dữ liệu JSON.

Khi định nghĩa một lược đồ, bạn chỉ định `type` (kiểu) của nó (ví dụ: `object`, `string`, `integer`), các `properties` (thuộc tính) 
của nó nếu đó là một đối tượng, và một mảng `required` liệt kê các thuộc tính bắt buộc.

Ví dụ YAML: Định nghĩa một lược đồ `User` có thể tái sử dụng
```YAML
components:
  schemas:
    User:
      type: object
      required:
        - id
        - username
        - email
      properties:
        id:
          type: integer
          format: int64
          description: Định danh duy nhất cho người dùng.
        username:
          type: string
          description: Tên người dùng đã chọn.
        email:
          type: string
          format: email
          description: Địa chỉ email của người dùng.
        fullName:
          type: string
          description: Tên đầy đủ của người dùng (tùy chọn).
```
#### 3.3. Liên kết mọi thứ với `$ref`
Đối tượng tham chiếu (reference object), được biểu thị bằng từ khoá `$ref`, là cơ chế để liên kết đến các định nghĩa trong đối tượng `components`. 
Nó hoạt động như một con trỏ, cho phép bạn bạn chèn một định nghĩa được chia sẻ với bất kỳ vị trí nào mà một đối tượng cùng loại được mong đợi.

Cú pháp cho các tham chiếu nội bộ trong cùng một tài liệu là một con trỏ `JSON`, ví dụ: `$ref:'#/components/schemas/User'`. Dấu `#` chỉ ra rằng tham chiếu
là đến tài liệu hiện tại.

Đối tượng `components` biến một định nghĩa API từ một danh sách phẳng các điểm cuối thành một hệ thống có cấu trúc, có quan hệ. Nó giới thiệu một lớp trừu
tượng trực tiếp với việc định nghĩa các lớp hoặc kiểu trong một ngôn ngữ lập trình trước khi sử dụng chúng. Nếu không có `components`, một lược đồ cho đối tượng
`User` sẽ phải được sao chép và dán vào mọi điểm cuối chấp nhận hoặc trả về một người dùng. Sự trùng lặp thủ công này dễ gây ra lỗi và khó bảo trì. 
Bằng cách cung cấp một "nguồn chân lý duy nhất", `components` đảm bảo rằng một thay đổi đối với lược đồ `User` sẽ tự động được áp dụng cho mọi nơi tham chiếu đến nó, 
thực thi tính nhất quán trên toàn bộ bề mặt API.   

### 4. Mô tả tải trọng và phản hồi
#### 4.1. Đối tượng `requestBody`
Đối với các thao tác `POST`, `PUT`, và `PATCH` thường gửi dữ liệu đến máy chủ, đối tượng `requestBody` được sử dụng để mô tả tải trọng (payload). Nó chứa một `description`
(mô tả), một cờ `required` (bắt buộc), và một đối tượng `content`.

Đối tượng `content` ánh xạ các loại phương tiện (media types), như `application/json`, đến các lược đồ tương ứng của chúng. Đây là nơi sức mạnh của việc tái sử dụng phát huy
tác dụng: thay vì định nghĩa lược đồ nội tuyến, bạn sẽ tham chiếu đến một lược đồ được định nghĩa trong `components` bằng cách sử dụng `$ref`.

#### 4.2. Đối tượng `responses`
Đối tượng `responses` là một phần bắt buộc của một định nghĩa thao tác, ánh xạ các mã trạng thái HTTP đến các kết quả dự kiến của chúng. Bạn nên định nghĩa các phản hồi cho các
trường hợp thành công (ví dụ: `200 OK`, `201 Created`) và các trường hợp lỗi đã biết (`400 Bad Request`, `404 Not Found`).

Mỗi định nghĩa phản hồi bao gồm một `description` bắt buộc và, nếu có, một đối tượng `content` mô tả cấu trúc của phần thân phản hồi. Một lần nữa, đây là một nơi lý tưởng để sử dụng
`$ref` để tham chiếu đến các lược đồ được chia sẻ, đảm bảo rằng tất cả các phản hồi thành công và lỗi đều có một định dạng nhất quán.

#### 4.3. Kết hợp lại một định nghĩa Endpoint hoàn chỉnh

```YAML
paths:
  /users:
    post:
      tags:
        - Users
      summary: Tạo một người dùng mới
      operationId: createUser
      requestBody:
        description: Đối tượng người dùng sẽ được tạo.
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/User' # Tái sử dụng lược đồ của chúng ta
      responses:
        '201':
          description: Người dùng được tạo thành công.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User' # Tái sử dụng lược đồ của chúng ta
        '400':
          description: Dữ liệu đầu vào không hợp lệ.
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/Error' # Tái sử dụng một lược đồ lỗi tiêu chuẩn

components:
  schemas:
    User:
      #... (được định nghĩa trong 3.2)
    Error:
      type: object
      properties:
        code:
          type: integer
        message:
          type: string
```

## Phần II. Tài liệu hoá API Sanic với `sanic-ext`
### 5. Hệ sinh thái Sanic và vai trò của `sanic-ext`
#### 5.1. Giới thiệu về `sanic-ext`
`sanic-ext` là plugin được hỗ trợ chính thức để thêm các tính năng vào Sanic, bao gồm hỗ trợ OpenAPI, CORS, và xác thực đầu vào.
Nó được coi là sự kế thừa của dự án `sanic-openapi` trước đây, hiện đã chuyển sang chế độ bảo trì.

Việc thiết lập rất đơn giản. Bằng cách cài đặt `sanic[ext]`, chức năng OpenAPI được kích hoạt tự động. Không cần mã khởi tạo rõ ràng;
`sanic-ext` sẽ tự động gán với ứng dụng Sanic của bạn và phục vụ tài liệu tương tác (Swagger và Redoc) tại `/docs`

### 6. Tái liệu hoá dựa trên Decorator trong Sanic
#### 6.1. Decorator `@openapi`
Cơ chế chính để thêm nội dung vào lược đồ OpenAPI của bạn trong `sanic-ext` là thông qua việc trang trí các điểm cuối (endpoint) của bạn
bằng decorator `@openapi` và các phương thức của nó. Cách tiếp cận này rõ ràng và tách biệt hơn so với phương pháp gợi ý kiểu của FastAPI.

#### 6.2. Tài liệu hoá thao tác và tham số
Bạn có thể thêm metadata (siêu dữ liệu) vào một thao tác bằng cách sử dụng các decorator cụ thể:
- `@openapi.summary("...")` và `@openapi.description("...")` để cung cấp văn bản mô tả.
- `@openapi.tag("...")` để nhóm các thao tác.
- `@openapi.parameter("name", schema=str, location="query")` để định nghĩa rõ ràng các tham số.

#### 6.3. Định nghĩa phần thân yêu cầu và phản hồi
Các decorator quan trọng nhất để mô tả tải trọng là `body` và `response`:
- `@openapi.body({"application/json": YourModel})`: Chỉ định phần thân yêu cầu. Bạn có thể truyền một mô hình dữ liệu 
(như một lớp Pydantic hoặc database) để định nghĩa lược đồ.
- `@openapi.response(200, {"application/json": YourModel}, "...")`: Định nghĩa một phản hồi cụ thể cho một mã trạng thái. Nó nhận mã
trạng thái, một mô hình cho phần thân phản hồi

Cách tiếp cận của sanic-ext mang lại sự kiểm soát chi tiết nhưng cũng đi kèm với trách nhiệm lớn hơn. Logic xác thực thời gian chạy của API 
và tài liệu OpenAPI của nó được định nghĩa riêng biệt. Trong FastAPI, chữ ký hàm def `create(item: Item)` ngầm định nghĩa cả mô hình phần thân 
yêu cầu cho việc xác thực và lược đồ tài liệu. Trong Sanic, điều tương đương sẽ là một hàm xử lý `async def create(request)` được kết hợp với một 
decorator riêng biệt `@openapi.body({"application/json": Item})`. Sự tách biệt này cho phép bạn tài liệu hóa một điểm cuối mà không bị ràng buộc với 
một thư viện xác thực cụ thể, nhưng nó cũng tạo ra khả năng sai lệch: một nhà phát triển có thể cập nhật logic xác thực nhưng quên cập nhật decorator 
`@openapi.body`, dẫn đến tài liệu không đồng bộ với thực tế—chính vấn đề mà thiết kế của FastAPI giải quyết.

### 7. Triển khai CRUD Sanic hoàn chỉnh
```python
from sanic import Sanic, Blueprint, json
from sanic.views import HTTPMethodView
from sanic_ext import Extend, openapi

UserCreateSchema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "example": "Alice"},
        "email": {"type": "string", "example": "alice@example.com"}
    },
    "required": ["name", "email"]
}

UserResponseSchema = {
    "type": "object",
    "properties": {
        "id": {"type": "integer", "example": 1},
        "name": {"type": "string", "example": "Alice"},
        "email": {"type": "string", "example": "alice@example.com"}
    }
}

user_bp = Blueprint("user", url_prefix="/users")

# Dữ liệu demo trong bộ nhớ
FAKE_DB = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

class UserView(HTTPMethodView):
    # GET /users
    @openapi.summary("Get all users")
    @openapi.response(200, {"application/json": {"schema": {"type": "array", "items": UserResponseSchema}}})
    async def get(self, request, user_id=None):
        if user_id:
            user = next((u for u in FAKE_DB if u["id"] == user_id), None)
            if user:
                return json(user)
            return json({"error": "User not found"}, status=404)
        return json(FAKE_DB)

    # POST /users
    @openapi.summary("Create a new user")
    @openapi.body({"application/json": {"schema": UserCreateSchema}})
    @openapi.response(201, {"application/json": {"schema": UserResponseSchema}})
    async def post(self, request):
        data = request.json
        new_user = {
            "id": len(FAKE_DB) + 1,
            "name": data["name"],
            "email": data["email"],
        }
        FAKE_DB.append(new_user)
        return json(new_user, status=201)

    # PUT /users/<id>
    @openapi.summary("Update a user by ID")
    @openapi.parameter("user_id", int, "path", description="User ID")
    @openapi.body({"application/json": {"schema": UserCreateSchema}})
    @openapi.response(200, {"application/json": {"schema": UserResponseSchema}})
    async def put(self, request, user_id):
        user = next((u for u in FAKE_DB if u["id"] == user_id), None)
        if not user:
            return json({"error": "User not found"}, status=404)
        data = request.json
        user.update(data)
        return json(user)

    # DELETE /users/<id>
    @openapi.summary("Delete a user by ID")
    @openapi.parameter("user_id", int, "path", description="User ID")
    @openapi.response(204, {"description": "User deleted successfully"})
    async def delete(self, request, user_id):
        global FAKE_DB
        FAKE_DB = [u for u in FAKE_DB if u["id"] != user_id]
        return json({}, status=204)

user_bp.add_route(UserView.as_view(), "/")
user_bp.add_route(UserView.as_view(), "/<user_id:int>")

app = Sanic("UserApp")
Extend(app)  # Bật OpenAPI & Swagger UI
app.blueprint(user_bp)

if __name__ == "__main__":
    app.run(port=8000, dev=True)
```

## Phần III. Các chủ đề nâng cao và phương pháp kiến trúc tốt nhất
Phần cuối cùng này nâng cuộc thảo luận lên các mối quan tâm về kiến trúc, cung cấp các nguyên tắc để thiết kế 
các API mạnh mẽ, có thể bảo trì và chuyên nghiệp.
### 8. Các chiến lược đánh phiên bản API trong OpenAPI
#### 8.1. Tại sao đánh phiên bản lại quan trọng
Việc đánh phiên bản là rất quan trọng để quản lý các thay đổi có thể phá vỡ (breaking changes) và cho phép 
các API phát triển mà không làm gián đoạn các máy khách hiện có. Nó cung cấp một đường dẫn di chuyển rõ ràng cho 
người tiêu dùng và cho phép giới thiệu các tính năng mới một cách an toàn. 

#### 8.2. Các chiến lược đánh phiên bản phổ biến
Chiến lược đánh phiên bản phổ biến và được khuyến nghị nhất là đánh phiên bản qua URI (URI Versioning), trong đó số
phiên bản được bao gồm trực tiếp trong đường dẫn URL (ví dụ: `v1/items`, `v2/items`). Cách tiếp cận này rõ ràng, dễ hiểu
đối với các nhà phát triển và dễ dàng được lưu vào bộ nhớ đệm bởi các proxy web.

Trong tài liệu OpenAPI, điều này thường được thể hiện bằng cách có một tiền tố phiên bản trong tất cả các đường dẫn hoặc 
bằng cách sử dụng đối tượng `servers` để chỉ định các URL cơ sở khác nhau cho mỗi phiên bản.

```YAML
servers:
  - url: https://api.example.com/v1
    description: Version 1 (Legacy)
  - url: https://api.example.com/v2
    description: Version 2 (Current)
paths:
  /items:
    get:
      # Định nghĩa cho điểm cuối /items trên cả v1 và v2
      # Logic cụ thể sẽ khác nhau giữa các phiên bản
```

Các phương pháp thay thế bao gồm đánh phiên bản qua `Header` (sử dụng header `Accept`) và đánh phiên bản qua tham số truy vấn 
(sử dụng một tham số như `?version=2`), nhưng chúng ít phổ biến hơn và có thể có những nhược điểm về khả năng khám phá và lưu vào bộ nhớ đệm.

#### Tổng kết các chiến lược đánh phiên bản
<table>
  <thead>
    <tr>
      <th>Chiến lược</th>
      <th>Ưu điểm</th>
      <th>Nhược điểm</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Đánh phiên bản qua URI</td>
      <td>Rõ ràng, dễ hiểu, dễ đánh dấu trang, dễ lưu vào bộ nhớ đệm.</td>
      <td>Có thể làm lộn xộn không gian tên URI.</td>
    </tr>
    <tr>
      <td>Đánh phiên bản qua Header</td>
      <td>Giữ URI "sạch sẽ".</td>
      <td>Ít rõ ràng hơn đối với người dùng cuối, khó kiểm tra hơn trong trình duyệt.</td>
    </tr>
    <tr>
      <td>Đánh phiên bản qua Tham số Query</td>
      <td>Dễ dàng chuyển đổi phiên bản.</td>
      <td>Làm lộn xộn URI, có thể gây ra vấn đề với việc lưu vào bộ nhớ đệm.</td>
    </tr>
  </tbody>
</table>

### 9. Thiết kế vì tính nhất quán và khả năng bảo trì
#### 9.1. Cuộc tranh luận "Design-First" và "Code-First"
Sáng kiến OpenAPI khuyến nghị một cách tiếp cận "Design-First", trong đó tài liệu OpenAPI được viết trước, và sau đó mã 
được triển khai để phù hợp với nó. Điều này đảm bảo rằng hợp đồng API được suy nghĩ kỹ lưỡng và hoạt động như một bản thiết kế.   

Tuy nhiên, các framework như Sanic, FastAPI phổ biến cách tiếp cận "Code-First". Mặc dù điều này có vẻ trái ngược, 
nhưng cách tiếp cận của Sanic, FastAPI mang lại một góc nhìn tinh tế: nếu mã nguồn, với các mô hình và kiểu được định nghĩa chặt chẽ, 
được coi là tài liệu thiết kế chính tắc, thì nó sẽ đạt được nhiều lợi ích tương tự như Design-First, đặc biệt là việc đảm bảo sự nhất quán giữa hợp đồng và triển khai.

#### 9.2. Tối đa hóa tái sử dụng với `components`
Như đã được nhấn mạnh, đối tượng `components` là công cụ quan trọng nhất để đạt được một định nghĩa API có thể bảo trì. 
Bất cứ khi nào một lược đồ, tham số hoặc phản hồi được sử dụng ở nhiều hơn một nơi, nó nên được chuyển vào `components` và được tham chiếu bằng `$ref`.

#### 9.3. Phản hồi lỗi được tiêu chuẩn hoá 
Một dấu hiệu của một API được thiết kế chuyên nghiệp là tính nhất quán, đặc biệt trong việc xử lý lỗi. Client nên có thể
dựa vào cấu trúc lỗi duy nhất trên toàn bộ API của bạn. Đối tượng `components` làm cho việc này trở nên đơn giản.

Bằng cách định nghĩa một lược đồ `ErrorResponse` có thể tái sử dụng và một phản hồi `400BadRequest`, bạn có thể đảm bảo rằng
tất cả các lỗi do client gây ra đều có một định dạng có thể dự đoán được

Ví dụ YAML: Định nghĩa phản hồi lỗi có thể tái sử dụng

```YAML
components:
  schemas:
    ErrorResponse:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Mã lỗi dành riêng cho ứng dụng.
        message:
          type: string
          description: Mô tả lỗi mà con người có thể đọc được.
  responses:
    BadRequest:
      description: Yêu cầu không hợp lệ.
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/ErrorResponse'

paths:
  /items:
    post:
      #...
      responses:
        '201':
          #...
        '400':
          $ref: '#/components/responses/BadRequest' # Tái sử dụng phản hồi lỗi tiêu chuẩn
  /users:
    post:
      #...
      responses:
        '201':
          #...
        '400':
          $ref: '#/components/responses/BadRequest' # Tái sử dụng lại!
```

## 10. Kết luận
Đặc tả OpenAPI cung cấp một ngôn ngữ mạnh mẽ để định nghĩa và tài liệu hóa các API HTTP, 
hoạt động như một hợp đồng trung tâm thúc đẩy toàn bộ vòng đời của API. 
Bằng cách nắm vững các cấu trúc cốt lõi của nó `info`, `servers`, `paths`, 
và đặc biệt là đối tượng `components` có thể tái sử dụng—các nhà phát triển 
có thể tạo ra các đặc tả rõ ràng, nhất quán và có thể bảo trì.

Các framework Python hiện đại như FastAPI và Sanic đã tích hợp sâu các tiêu chuẩn này, mặc dù với các triết lý khác nhau. 
FastAPI, với cách tiếp cận "code-first" dựa trên Pydantic, tự động tạo ra tài liệu như một sản phẩm phụ của mã được định kiểu tốt, 
gần như loại bỏ khả năng sai lệch giữa tài liệu và triển khai. Ngược lại, `sanic-ext` cung cấp một hệ thống decorator rõ ràng, 
mang lại cho nhà phát triển sự kiểm soát chi tiết đối với tài liệu của họ, mặc dù có thêm trách nhiệm duy trì sự đồng bộ.

Việc lựa chọn giữa các framework này phụ thuộc vào sở thích của nhà phát triển về sự ngầm định so với sự rõ ràng. 
Tuy nhiên, các nguyên tắc cơ bản của một thiết kế API tốt vẫn không thay đổi: ưu tiên tính nhất quán, áp dụng việc tái sử dụng thông qua `components`, 
và thực hiện một chiến lược đánh phiên bản rõ ràng. Bằng cách áp dụng các kỹ thuật được trình bày trong hướng dẫn này, các nhà phát triển có thể nâng cao 
API của mình từ chỉ đơn thuần là chức năng thành chuyên nghiệp, mạnh mẽ và dễ sử dụng, mang lại lợi ích cho cả người tạo và người tiêu dùng API.
