# Kiến trúc Hướng Dịch vụ (SOA): REST Architecture và HTTP với Python & Sanic

## Mục lục

1. [Tổng quan về Service-Oriented Architecture](#1-tổng-quan-về-service-oriented-architecture)
2. [HTTP - Nền tảng của Web Services](#2-http---nền-tảng-của-web-services)
3. [REST Architecture - Thế hệ thứ hai của SOA](#3-rest-architecture---thế-hệ-thứ-hai-của-soa)
4. [Thiết kế RESTful Web Services](#4-thiết-kế-restful-web-services)
5. [Microservices Architecture](#5-microservices-architecture)

---

## 1. Tổng quan về Service-Oriented Architecture

### 1.1. SOA là gì?

**Service-Oriented Architecture (SOA)** là một phong cách kiến trúc phần mềm trong đó ứng dụng được xây dựng bằng cách kết hợp các **dịch vụ (services)** độc lập, có thể tái sử dụng.

#### Khái niệm cốt lõi:

- **Service (Dịch vụ)**: Một công cụ phần mềm mà các phần mềm khác có thể sử dụng
- **Service Provider (Nhà cung cấp dịch vụ)**: Phần mềm cung cấp và thực hiện dịch vụ
- **Service Requester (Người yêu cầu dịch vụ)**: Phần mềm yêu cầu và sử dụng dịch vụ

### 1.2. Các nguyên tắc thiết kế dịch vụ

| Nguyên tắc | Mô tả |
|-----------|-------|
| **Modular & Loosely Coupled** | Dịch vụ phải độc lập, có thể kết hợp linh hoạt |
| **Composable** | Có thể kết hợp nhiều dịch vụ để tạo ứng dụng hoàn chỉnh |
| **Platform & Language Independent** | Độc lập với nền tảng và ngôn ngữ lập trình |
| **Self-Describing** | Dịch vụ tự mô tả cách tương tác với nó |
| **Self-Advertising** | Dịch vụ quảng bá sự tồn tại của mình |

### 1.3. Hai bối cảnh triển khai SOA

#### **Web Services (External SOA)**
- Dịch vụ được cung cấp trên Internet
- Kết hợp các dịch vụ bên ngoài để xây dựng ứng dụng
- Ví dụ: Tích hợp API thanh toán, API bản đồ, API thời tiết

#### **Enterprise SOA (Internal SOA)**
- Các phần mềm nội bộ được chuyển thành dịch vụ
- Chia sẻ và tái sử dụng trong toàn tổ chức
- Ví dụ: Dịch vụ quản lý nhân sự, dịch vụ kế toán nội bộ

---

## 2. HTTP - Nền tảng của Web Services

### 2.1. HTTP là gì?

**Hypertext Transfer Protocol (HTTP)** là giao thức quy định cách thức truyền tải thông tin, bao gồm hypertext, qua Internet.

#### Đặc điểm chính:
- Giao thức **client-server**: Web browser (client) giao tiếp với web server
- Xây dựng trên **TCP (Transmission Control Protocol)**
- Mặc định sử dụng **TCP port 80**
- Giao tiếp thông qua **request-response pattern**

### 2.2. Cấu trúc HTTP Request

```
[Request Line]      ← Phương thức, URI, và phiên bản HTTP
[Headers]           ← Metadata về request
[Blank Line]        ← Dòng trống bắt buộc
[Body (optional)]   ← Dữ liệu gửi đi (nếu có)
```

#### Request Line

```http
POST /api/students HTTP/1.1
```

Gồm 3 phần:
- **Method**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- **URI**: Đường dẫn tài nguyên (ví dụ: `/api/students`)
- **HTTP Version**: Thường là `HTTP/1.1`

#### Request Headers (Phổ biến)

```http
Host: api.example.com
Content-Type: application/json
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

**Các loại headers quan trọng:**

| Header | Mục đích |
|--------|----------|
| `Host` | Tên miền hoặc IP của server (bắt buộc) |
| `Content-Type` | Định dạng dữ liệu trong body |
| `Accept` | Định dạng dữ liệu client muốn nhận |
| `Authorization` | Thông tin xác thực |
| `User-Agent` | Thông tin về client |

#### Request Body

Body chứa dữ liệu gửi lên (thường với POST, PUT, PATCH):

**JSON Body:**
```json
{
  "fullname": "James Dean",
  "department": "Computing Science"
}
```

**Form Data:**
```
fullname=James+Dean&department=Computing+Science
```

### 2.3. Cấu trúc HTTP Response

```
[Status Line]       ← Phiên bản HTTP và mã trạng thái
[Headers]           ← Metadata về response
[Blank Line]        ← Dòng trống bắt buộc
[Body]              ← Dữ liệu trả về
```

#### Status Line

```http
HTTP/1.1 200 OK
```

Gồm:
- **HTTP Version**: `HTTP/1.1`
- **Status Code**: `200` (mã trạng thái)
- **Reason Phrase**: `OK` (mô tả ngắn)

#### HTTP Status Codes

| Nhóm | Mã | Ý nghĩa | Ví dụ sử dụng |
|------|-------|---------|---------------|
| **2xx Success** | 200 | OK | Request thành công |
| | 201 | Created | Tạo resource thành công |
| | 204 | No Content | Xóa thành công, không có body |
| **3xx Redirection** | 301 | Moved Permanently | Resource đã chuyển vĩnh viễn |
| | 304 | Not Modified | Cache vẫn còn hiệu lực |
| **4xx Client Error** | 400 | Bad Request | Request sai format |
| | 401 | Unauthorized | Chưa xác thực |
| | 403 | Forbidden | Không có quyền truy cập |
| | 404 | Not Found | Không tìm thấy resource |
| | 422 | Unprocessable Entity | Lỗi validation |
| **5xx Server Error** | 500 | Internal Server Error | Lỗi server |
| | 503 | Service Unavailable | Server quá tải |

#### Response Headers (Phổ biến)

```http
Content-Type: application/json; charset=utf-8
Content-Length: 245
Cache-Control: no-cache, no-store, must-revalidate
Set-Cookie: session_id=abc123; HttpOnly; Secure
Access-Control-Allow-Origin: https://example.com
```

### 2.4. Các phương thức HTTP

#### **GET - Lấy dữ liệu**

```http
GET /api/students/3 HTTP/1.1
Host: api.example.com
Accept: application/json
```

**Đặc điểm:**
- Chỉ đọc dữ liệu, **không thay đổi** trạng thái resource
- Không có body trong request
- Query parameters trong URI: `/api/students?department=CS&page=1`

#### **POST - Tạo mới**

```http
POST /api/students HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "fullname": "James Dean",
  "department": "Computing Science"
}
```

**Đặc điểm:**
- Tạo resource mới trong collection
- Có body chứa dữ liệu
- Server quyết định ID của resource mới

#### **PUT - Cập nhật toàn bộ**

```http
PUT /api/students/3 HTTP/1.1
Host: api.example.com
Content-Type: application/json

{
  "fullname": "James Dean Updated",
  "department": "Computing Science"
}
```

**Đặc điểm:**
- Cập nhật hoặc thay thế toàn bộ resource
- URI chỉ định chính xác resource cần cập nhật
- Idempotent: Gọi nhiều lần cho kết quả giống nhau

#### **DELETE - Xóa**

```http
DELETE /api/students/3 HTTP/1.1
Host: api.example.com
```

**Đặc điểm:**
- Xóa resource tại URI chỉ định
- Thường trả về 204 No Content

### 2.5. Ví dụ hoàn chỉnh: Tạo sinh viên mới

#### Request:

```http
POST /studentcourseapi/students HTTP/1.1
Host: example.com
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0
Content-Length: 72

{
  "fullname": "James Dean",
  "department": "Computing Science"
}
```

#### Response:

```http
HTTP/1.1 201 Created
Date: Tue, 04 Nov 2025 10:30:00 GMT
Server: Sanic/23.12.0
Content-Type: application/json; charset=utf-8
Content-Length: 156
Location: /studentcourseapi/students/123

{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 123,
    "fullname": "James Dean",
    "department": "Computing Science"
  }
}
```

### 2.6. HTTP Stateless - Phi trạng thái

**HTTP là stateless protocol** - nghĩa là mỗi request độc lập, server không "nhớ" các request trước đó.

#### Ý nghĩa:
- Server không lưu trạng thái phiên (session state) của client
- Mỗi request phải chứa **tất cả thông tin** cần thiết
- Cải thiện **khả năng mở rộng** (scalability)

#### Giải pháp theo dõi trạng thái:
- **Cookies**: Server gửi cookie, client lưu và gửi lại trong các request tiếp theo
- **Tokens**: JWT, OAuth tokens trong header `Authorization`

---

## 3. REST Architecture - Thế hệ thứ hai của SOA

### 3.1. REST là gì?

**Representational State Transfer (REST)** là một **kiểu kiến trúc (architectural style)** cho các hệ thống phân tán, không phải là một giao thức hay tiêu chuẩn cứng nhắc như SOAP.

#### Triết lý cốt lõi:

**SOAP/WS\* (Thế hệ 1):**
- **Hướng hoạt động** (Operation-oriented)
- Gọi các phương thức: `getUserDetails(userId)`, `createOrder(orderXml)`
- Phức tạp: SOAP, WSDL, UDDI
- XML-based, nặng nề

**REST (Thế hệ 2):**
- **Hướng tài nguyên** (Resource-based)
- Sử dụng HTTP trực tiếp như giao thức ứng dụng
- Đơn giản, nhẹ nhàng: URI + HTTP Methods
- JSON hoặc XML

### 3.2. Năm ràng buộc của REST

| Ràng buộc | Mô tả | Lợi ích |
|-----------|-------|---------|
| **1. Client-Server** | Tách biệt mối quan tâm: Client lo UI, Server lo business logic | Phát triển độc lập |
| **2. Stateless** | Server không lưu session state của client | Khả năng mở rộng cao |
| **3. Cacheable** | Response có thể được cache | Cải thiện hiệu suất |
| **4. Layered System** | Có thể thêm các lớp trung gian (proxy, load balancer) | Tăng tính bảo mật, hiệu suất |
| **5. Uniform Interface** | Giao diện đồng nhất cho mọi tương tác | Đơn giản hóa, tách rời client-server |

#### Chi tiết: Stateless Constraint

**Tại sao Stateless quan trọng?**

Nếu có trạng thái (stateful):
```
Client → (yêu cầu với giỏ hàng) → Server A
Client → (yêu cầu tiếp) → Server A (bắt buộc, vì chỉ A biết giỏ hàng)
```

Nếu phi trạng thái (stateless):
```
Client → (yêu cầu + toàn bộ info) → Server A, B, C, hoặc D (bất kỳ)
```

**Kết quả:** Có thể load balance giữa hàng ngàn servers!

### 3.3. Giao diện đồng nhất (Uniform Interface)

#### 3.3.1. HTTP Methods - "Động từ"

| Method | Mục đích | Idempotent? | Safe? |
|--------|----------|-------------|-------|
| **GET** | Lấy tài nguyên | ✅ Có | ✅ Có |
| **POST** | Tạo mới | ❌ Không | ❌ Không |
| **PUT** | Cập nhật/Thay thế | ✅ Có | ❌ Không |
| **DELETE** | Xóa | ✅ Có | ❌ Không |
| **PATCH** | Cập nhật một phần | ❌ Không | ❌ Không |

**Idempotent:** Gọi nhiều lần cho cùng kết quả  
**Safe:** Không thay đổi trạng thái server

#### 3.3.2. URI - "Danh từ"

```
GET    /students          → Lấy danh sách sinh viên
POST   /students          → Tạo sinh viên mới
GET    /students/3        → Lấy sinh viên ID 3
PUT    /students/3        → Cập nhật sinh viên ID 3
DELETE /students/3        → Xóa sinh viên ID 3
GET    /students/3/courses → Lấy khóa học của sinh viên 3
```

#### 3.3.3. HTTP Headers - "Siêu dữ liệu"

**Content Negotiation:**
```http
Content-Type: application/json    ← "Tôi gửi JSON"
Accept: application/json           ← "Tôi muốn nhận JSON"
```

#### 3.3.4. Status Codes - "Phản hồi"

```
200 OK          → GET thành công
201 Created     → POST tạo mới thành công
204 No Content  → DELETE thành công
400 Bad Request → Request sai format
404 Not Found   → Không tìm thấy resource
500 Server Error → Lỗi server
```

### 3.4. Resources và Representations

#### Resource (Tài nguyên)
- Bất cứ thứ gì có thể được đặt tên: document, image, object, collection
- Ví dụ: Sinh viên ID 3, Danh sách tất cả khóa học

#### Representation (Biểu diễn)
- Client không nhận được chính resource, mà nhận **biểu diễn** của trạng thái resource
- Định dạng: JSON, XML, HTML

**Ví dụ:**

Request:
```http
GET /students/3 HTTP/1.1
Accept: application/json
```

Response (JSON representation):
```json
{
  "id": 3,
  "fullname": "James Dean",
  "department": "Computing Science",
  "email": "james@example.com"
}
```

### 3.5. Workflow hoàn chỉnh: Tạo sinh viên

#### Bước 1: Client tạo request

```bash
curl -X POST "http://example.com/studentcourseapi/students" \
  -H "Content-Type: application/json" \
  -d '{"fullname":"James Dean", "department":"Computing Science"}'
```

#### Bước 2: HTTP Request trên đường truyền

```http
POST /studentcourseapi/students HTTP/1.1
Host: example.com
Content-Type: application/json
Content-Length: 72

{"fullname":"James Dean", "department":"Computing Science"}
```

#### Bước 3: Server xử lý (Python/Sanic)

```python
from sanic import Sanic, response
from sanic.request import Request
from dataclasses import dataclass, asdict

@dataclass
class Student:
    fullname: str
    department: str
    id: int = None
    email: str = None

app = Sanic("StudentCourseAPI")

@app.post("/studentcourseapi/students")
async def create_student(request: Request):
    # Parse JSON body
    data = request.json
    
    # Create student object
    student = Student(
        fullname=data.get('fullname'),
        department=data.get('department'),
        email=data.get('email')
    )
    
    # Save to database (giả lập)
    student.id = generate_id()
    save_to_db(student)
    
    # Return response
    return response.json(
        {
            "success": True,
            "message": "Student created successfully",
            "data": asdict(student)
        },
        status=201,
        headers={"Location": f"/studentcourseapi/students/{student.id}"}
    )
```

#### Bước 4: Server gửi Response

```http
HTTP/1.1 201 Created
Content-Type: application/json
Content-Length: 126
Location: /studentcourseapi/students/123

{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 123,
    "fullname": "James Dean",
    "department": "Computing Science"
  }
}
```

---

## 4. Thiết kế RESTful Web Services

### 4.1. Nguyên tắc thiết kế URI

#### ✅ Chỉ dùng Danh từ (Nouns)

```
❌ Tệ:  /getAllStudents, /createStudent, /deleteStudent
✅ Tốt: /students (dùng HTTP methods để chỉ hành động)
```

#### ✅ Dùng Danh từ Số nhiều (Plural)

```
❌ Tệ:  /student/3, /course/5
✅ Tốt: /students/3, /courses/5
```

#### ✅ Dùng Sub-resources cho quan hệ

```
GET /students/3/courses      → Tất cả khóa học của sinh viên 3
GET /students/3/courses/2    → Khóa học 2 của sinh viên 3
POST /students/3/courses     → Thêm khóa học cho sinh viên 3
```

### 4.2. Bản thiết kế API RESTful

| Resource | GET | POST | PUT | DELETE |
|----------|-----|------|-----|--------|
| `/students` | Danh sách sinh viên | Tạo sinh viên mới | Bulk update | Xóa tất cả |
| `/students/3` | Sinh viên ID 3 | ❌ 405 | Cập nhật sinh viên 3 | Xóa sinh viên 3 |
| `/courses` | Danh sách khóa học | Tạo khóa học mới | Bulk update | Xóa tất cả |
| `/courses/5` | Khóa học ID 5 | ❌ 405 | Cập nhật khóa học 5 | Xóa khóa học 5 |
| `/students/3/courses` | Khóa học của SV 3 | Thêm khóa học | ❌ 405 | Xóa tất cả khóa học |

### 4.3. Content Negotiation

**Request:**
```http
POST /api/students HTTP/1.1
Content-Type: application/json    ← Tôi gửi JSON
Accept: application/json           ← Tôi muốn nhận JSON

{"fullname": "John Doe"}
```

**Response:**
```http
HTTP/1.1 201 Created
Content-Type: application/json    ← Server trả về JSON

{"id": 123, "fullname": "John Doe"}
```

### 4.4. Filtering và Pagination

```http
GET /courses?department=CS                      ← Lọc theo department
GET /courses?department=CS&year=2024            ← Nhiều filter
GET /courses?offset=20&limit=10                 ← Phân trang
GET /students?sort=fullname&order=desc          ← Sắp xếp
```

### 4.5. Versioning API

```http
GET /v1/students/3       ← Version 1
GET /v2/students/3       ← Version 2 (có thay đổi breaking)
```

### 4.6. Sử dụng đúng Status Codes với Sanic

```python
from sanic import response

# Success
return response.json(student, status=200)        # OK
return response.json(student, status=201)        # Created
return response.empty(status=204)                # No Content

# Client Error
return response.json(errors, status=400)         # Bad Request
return response.json(message, status=401)        # Unauthorized
return response.json(message, status=404)        # Not Found
return response.json(errors, status=422)         # Validation Error

# Server Error
return response.json(message, status=500)        # Server Error
```

### 4.7. Response Format nhất quán

**Success Response:**
```json
{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 123,
    "fullname": "James Dean",
    "department": "Computing Science"
  }
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Validation failed",
  "errors": [
    {
      "field": "email",
      "message": "Email is required"
    },
    {
      "field": "department",
      "message": "Invalid department code"
    }
  ]
}
```

### 4.8. Caching với HTTP Headers

**Server Response:**
```http
HTTP/1.1 200 OK
Cache-Control: public, max-age=3600           ← Cache 1 giờ
ETag: "abc123def456"                          ← Version identifier
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
```

**Client Request tiếp theo:**
```http
GET /students/3 HTTP/1.1
If-None-Match: "abc123def456"                 ← Kiểm tra ETag
If-Modified-Since: Wed, 21 Oct 2024 07:28:00 GMT
```

**Server Response (nếu chưa thay đổi):**
```http
HTTP/1.1 304 Not Modified                     ← Dùng cache
```

---

## 5. Microservices Architecture

### 5.1. Microservices là gì?

**Microservices** là một biến thể của SOA ở **quy mô ứng dụng** (application scale) thay vì quy mô doanh nghiệp (enterprise scale).

#### Đặc điểm:
- Ứng dụng được chia thành **nhiều dịch vụ nhỏ, độc lập**
- Mỗi microservice chịu trách nhiệm **một chức năng nghiệp vụ cụ thể**
- Mỗi dịch vụ chạy trong **quy trình riêng**
- Giao tiếp qua **REST/HTTP**

#### Ví dụ: Ứng dụng thư viện trực tuyến

```
┌─────────────────┐    ┌─────────────────┐
│  Recommendation │    │      Order      │
│    Service      │    │     Service     │
└─────────────────┘    └─────────────────┘
         │                      │
         └──────────┬───────────┘
                    │ REST API
         ┌──────────┴───────────┐
         │                      │
┌─────────────────┐    ┌─────────────────┐
│     Account     │    │  Ebook Catalog  │
│    Service      │    │     Service     │
└─────────────────┘    └─────────────────┘
```

### 5.2. So sánh: Monolithic vs Microservices

| Khía cạnh | Monolithic | Microservices |
|-----------|------------|---------------|
| **Cấu trúc** | Một ứng dụng lớn duy nhất | Nhiều dịch vụ nhỏ độc lập |
| **Deployment** | Deploy toàn bộ ứng dụng | Deploy từng dịch vụ riêng |
| **Scaling** | Scale toàn bộ | Scale từng dịch vụ cần thiết |
| **Technology** | Một stack công nghệ | Mỗi dịch vụ dùng stack riêng |
| **Failure** | Lỗi một phần → sập toàn bộ | Lỗi được cô lập |

### 5.3. Mối quan hệ REST và Microservices

**REST là "chất keo" kết dính các microservices:**

```
┌─────────────┐                    ┌─────────────┐
│   Order     │  POST /payments    │   Payment   │
│  Service    │ ──────────────────>│   Service   │
│             │  {amount: 100}     │             │
│             │<────────────────── │             │
│             │  {success: true}   │             │
└─────────────┘                    └─────────────┘
```

**Lợi ích của REST trong Microservices:**

1. **Stateless** → Có thể chạy nhiều instances, load balance
2. **Uniform Interface** → Các service khác nhau vẫn giao tiếp dễ dàng
3. **Platform Independent** → Service A (Python) gọi Service B (Node.js)

### 5.4. Ưu điểm của Microservices

| Ưu điểm | Giải thích |
|---------|------------|
| **Technology Flexibility** | Mỗi service dùng ngôn ngữ/framework phù hợp nhất |
| **Independent Deployment** | Deploy service riêng lẻ mà không ảnh hưởng toàn hệ thống |
| **Scalability** | Scale service cần thiết (ví dụ: chỉ scale Recommendation) |
| **Resilience** | Lỗi một service không làm sập toàn bộ |
| **Small Teams** | Team nhỏ sở hữu và phát triển một service |

### 5.5. Nhược điểm của Microservices

| Nhược điểm | Giải thích |
|-----------|------------|
| **Operational Complexity** | Quản lý 50 services khó hơn 1 monolith |
| **Transaction Management** | Đảm bảo consistency trên nhiều databases phân tán |
| **Testing Complexity** | Khó tái tạo lỗi từ tương tác phức tạp |
| **Communication Overhead** | HTTP call chậm hơn in-process call hàng ngàn lần |
| **Data Consistency** | Distributed transaction, eventual consistency |

### 5.6. Ví dụ thực tế: Ứng dụng đặt nhà hàng

#### Kiến trúc Microservices:

```
                    ┌──────────────┐
                    │  Web/Mobile  │
                    │      UI      │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
   ┌────────▼───────┐ ┌───▼──────┐ ┌────▼─────────┐
   │  Restaurant    │ │   User   │ │ Reservation  │
   │   Catalog      │ │  Account │ │    Service   │
   └────────┬───────┘ �└──────────┘ └──────┬───────┘
            │                              │
            │         ┌────────────┐       │
            └────────>│   Review   │<──────┘
                      │  Service   │
                      └────────────┘
```

#### Flow: Người dùng đặt bàn

1. **UI Service** → `GET /restaurants?location=HaNoi` → **Catalog Service**
2. **Catalog Service** → Trả về danh sách nhà hàng
3. **UI Service** → `GET /restaurants/123/reviews` → **Review Service**
4. **Review Service** → Trả về đánh giá
5. **UI Service** → `POST /reservations` → **Reservation Service**
6. **Reservation Service** → Xác nhận đặt bàn thành công

#### Code ví dụ (REST Communication):

**Order Service gọi Payment Service:**

```python
import httpx
from sanic import Sanic, response
from sanic.request import Request
from dataclasses import dataclass, asdict
from typing import Optional

app = Sanic("OrderService")

@dataclass
class Order:
    id: Optional[int] = None
    total_amount: float = 0.0
    status: str = "PENDING"
    items: list = None

@dataclass
class PaymentRequest:
    order_id: int
    amount: float

class OrderService:
    PAYMENT_SERVICE_URL = "http://payment-service:8001/api/payments"
    
    async def create_order(self, order_data: dict) -> Order:
        # 1. Tạo order
        order = Order(
            id=generate_order_id(),
            total_amount=order_data['total_amount'],
            items=order_data.get('items', []),
            status="PENDING"
        )
        await save_order_to_db(order)
        
        # 2. Gọi Payment Service qua REST
        payment_request = {
            "order_id": order.id,
            "amount": order.total_amount
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.PAYMENT_SERVICE_URL,
                    json=payment_request,
                    timeout=10.0
                )
                
                # 3. Xử lý kết quả
                if response.status_code == 200:
                    payment_response = response.json()
                    
                    if payment_response.get('success'):
                        order.status = "PAID"
                        await save_order_to_db(order)
                        
            except httpx.RequestError as e:
                # Handle service unavailable
                order.status = "PAYMENT_FAILED"
                await save_order_to_db(order)
        
        return order

@app.post("/api/orders")
async def create_order_endpoint(request: Request):
    order_service = OrderService()
    order = await order_service.create_order(request.json)
    
    return response.json({
        "success": True,
        "data": asdict(order)
    }, status=201)
```

### 5.7. Best Practices cho Microservices

#### 1. **Thiết kế Service Boundaries**

```
❌ Tệ: Chia theo technical layers
   - Database Service
   - UI Service
   - Business Logic Service

✅ Tốt: Chia theo business capabilities
   - Order Service
   - Payment Service
   - Inventory Service
   - Shipping Service
```

#### 2. **Database per Service**

```
┌─────────────┐     ┌─────────────┐
│   Order     │     │   Payment   │
│  Service    │     │   Service   │
└──────┬──────┘     └──────┬──────┘
       │                   │
┌──────▼──────┐     ┌──────▼──────┐
│   Order DB  │     │ Payment DB  │
└─────────────┘     └─────────────┘
```

**Lợi ích:**
- Mỗi service độc lập với database của mình
- Có thể chọn database phù hợp (SQL, NoSQL)
- Thay đổi schema không ảnh hưởng services khác

#### 3. **API Gateway Pattern**

```
                ┌──────────────┐
                │ API Gateway  │
                └──────┬───────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
┌───────▼──────┐  ┌────▼─────┐ ┌──────▼──────┐
│   Service A  │  │ Service B│ │  Service C  │
└──────────────┘  └──────────┘ └─────────────┘
```

**API Gateway chịu trách nhiệm:**
- Routing requests đến đúng service
- Load balancing
- Authentication & Authorization
- Rate limiting
- Caching

**Implementation với Sanic:**

```python
from sanic import Sanic, response
import httpx

app = Sanic("APIGateway")

# Service registry
SERVICES = {
    "order": "http://order-service:8001",
    "payment": "http://payment-service:8002",
    "inventory": "http://inventory-service:8003"
}

@app.route("/api/<service_name:str>/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(request, service_name, path):
    # Check if service exists
    if service_name not in SERVICES:
        return response.json({"error": "Service not found"}, status=404)
    
    # Get service URL
    service_url = f"{SERVICES[service_name]}/api/{path}"
    
    # Forward request
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=request.method,
                url=service_url,
                json=request.json,
                headers=request.headers,
                timeout=30.0
            )
            return response.raw(
                resp.content,
                status=resp.status_code,
                headers=dict(resp.headers)
            )
        except httpx.RequestError:
            return response.json(
                {"error": "Service unavailable"},
                status=503
            )
```

#### 4. **Service Discovery**

```python
import consul
from sanic import Sanic

app = Sanic("OrderService")

# Consul client
consul_client = consul.Consul(host='consul', port=8500)

@app.listener('before_server_start')
async def register_service(app, loop):
    """Đăng ký service với Consul khi khởi động"""
    consul_client.agent.service.register(
        name='order-service',
        service_id='order-service-1',
        address='order-service',
        port=8001,
        tags=['order', 'v1'],
        check=consul.Check.http(
            'http://order-service:8001/health',
            interval='10s'
        )
    )

@app.listener('after_server_stop')
async def deregister_service(app, loop):
    """Hủy đăng ký khi tắt service"""
    consul_client.agent.service.deregister('order-service-1')

@app.get("/health")
async def health_check(request):
    """Health check endpoint"""
    return response.json({"status": "healthy"})

# Gọi service khác qua service discovery
async def call_payment_service():
    # Discover payment service
    _, services = consul_client.health.service('payment-service', passing=True)
    
    if not services:
        raise Exception("Payment service not available")
    
    # Get first healthy instance
    service = services[0]
    service_address = service['Service']['Address']
    service_port = service['Service']['Port']
    
    url = f"http://{service_address}:{service_port}/api/payments"
    
    # Make REST call
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json={"amount": 100})
        return response.json()
```

#### 5. **Circuit Breaker Pattern**

```python
from pybreaker import CircuitBreaker
from sanic import Sanic, response
import httpx

app = Sanic("OrderService")

# Circuit breaker cho Payment Service
payment_breaker = CircuitBreaker(
    fail_max=5,           # Fail sau 5 lần
    timeout_duration=60,  # Open trong 60 giây
    name="PaymentServiceBreaker"
)

class PaymentServiceClient:
    PAYMENT_SERVICE_URL = "http://payment-service:8002/api/payments"
    
    @payment_breaker
    async def process_payment(self, payment_data: dict):
        """Gọi Payment Service với circuit breaker"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.PAYMENT_SERVICE_URL,
                json=payment_data,
                timeout=10.0
            )
            return response.json()

@app.post("/api/orders")
async def create_order(request):
    payment_client = PaymentServiceClient()
    
    try:
        # Thử gọi Payment Service
        payment_response = await payment_client.process_payment({
            "amount": request.json['total_amount']
        })
        
        # Xử lý order
        order = create_order_with_payment(request.json, payment_response)
        
        return response.json({
            "success": True,
            "data": order
        }, status=201)
        
    except Exception as e:
        # Fallback khi Payment Service down
        # Queue order để xử lý sau hoặc trả về pending
        order = create_pending_order(request.json)
        
        return response.json({
            "success": True,
            "message": "Order created, payment pending",
            "data": order
        }, status=202)  # 202 Accepted

@app.get("/api/circuit-breaker/status")
async def breaker_status(request):
    """Kiểm tra trạng thái circuit breaker"""
    return response.json({
        "name": payment_breaker.name,
        "state": payment_breaker.current_state,
        "fail_counter": payment_breaker.fail_counter,
        "failure_count": payment_breaker.fail_max
    })
```

### 5.8. Khi nào nên dùng Microservices?

#### ✅ Nên dùng khi:

1. **Ứng dụng lớn, phức tạp**
   - Nhiều chức năng nghiệp vụ khác nhau
   - Team lớn (>50 developers)

2. **Cần scale linh hoạt**
   - Một số tính năng có traffic cao hơn nhiều
   - Ví dụ: Netflix (streaming service scale khác catalog service)

3. **Cần deploy độc lập**
   - Cập nhật features liên tục
   - Không muốn deploy toàn bộ app

4. **Technology diversity**
   - Các phần khác nhau cần công nghệ khác nhau
   - Ví dụ: ML service (Python), API service (Node.js)

#### ❌ Không nên dùng khi:

1. **Ứng dụng nhỏ, đơn giản**
   - Team nhỏ (<5 developers)
   - Chức năng đơn giản

2. **Chưa rõ business domain**
   - Vẫn đang thử nghiệm, pivot nhiều
   - Chưa biết chia boundaries như thế nào

3. **Thiếu DevOps capability**
   - Không có infrastructure cho deployment automation
   - Không có monitoring, logging tools

---

## 6. Tổng kết và So sánh

### 6.1. Timeline Evolution

```
1960s-1980s           1990s-2000s         2000s-2010s        2010s-Present
─────────────────────────────────────────────────────────────────────────>
  Monolithic      →    SOAP/WS*      →      REST         →   Microservices
  Applications         (SOA 1.0)            (SOA 2.0)         + REST
```

### 6.2. So sánh SOAP vs REST

| Đặc điểm | SOAP | REST |
|----------|------|------|
| **Kiểu** | Protocol | Architectural Style |
| **Format** | XML only | XML, JSON, HTML, text |
| **Complexity** | Phức tạp (WSDL, UDDI) | Đơn giản (HTTP) |
| **Performance** | Chậm hơn (XML overhead) | Nhanh hơn |
| **Caching** | Khó cache | Dễ cache (HTTP) |
| **Stateful** | Có thể stateful | Stateless |
| **Use case** | Enterprise, banking | Web, mobile apps |

### 6.3. REST Best Practices - Tổng hợp

#### URI Design

```http
✅ GET    /api/v1/students
✅ GET    /api/v1/students/123
✅ GET    /api/v1/students/123/courses
✅ POST   /api/v1/students
✅ PUT    /api/v1/students/123
✅ DELETE /api/v1/students/123

❌ GET    /api/v1/getAllStudents
❌ POST   /api/v1/createStudent
❌ GET    /api/v1/student/123
```

#### HTTP Methods

```http
GET    → Chỉ đọc, không thay đổi
POST   → Tạo mới
PUT    → Cập nhật toàn bộ
PATCH  → Cập nhật một phần
DELETE → Xóa
```

#### Status Codes

```
2xx → Success (200, 201, 204)
3xx → Redirection (301, 304)
4xx → Client Error (400, 401, 404, 422)
5xx → Server Error (500, 503)
```

#### Headers

```http
Content-Type: application/json        ← Định dạng body
Accept: application/json              ← Định dạng mong muốn
Authorization: Bearer <token>         ← Xác thực
Cache-Control: max-age=3600          ← Caching policy
```

#### Response Format

```json
{
  "success": true/false,
  "message": "Human readable message",
  "data": { ... },      // khi success
  "errors": [ ... ]     // khi có lỗi
}
```

### 6.4. Checklist thiết kế RESTful API

- [ ] **URIs chỉ dùng danh từ số nhiều**
  - `/students`, không phải `/getAllStudents`

- [ ] **GET không thay đổi state**
  - GET chỉ đọc dữ liệu

- [ ] **Sử dụng đúng HTTP methods**
  - GET (read), POST (create), PUT (update), DELETE (delete)

- [ ] **Trả về đúng status codes**
  - 200, 201, 204 cho success
  - 400, 404, 422 cho client error
  - 500 cho server error

- [ ] **Content negotiation rõ ràng**
  - `Content-Type` và `Accept` headers

- [ ] **Hỗ trợ filtering và pagination**
  - `/students?department=CS&page=1&limit=20`

- [ ] **Versioning API**
  - `/api/v1/students`, `/api/v2/students`

- [ ] **Consistent response format**
  - Luôn có `success`, `message`, `data`/`errors`

- [ ] **Stateless**
  - Mỗi request độc lập, chứa đủ thông tin

- [ ] **Cacheable**
  - Sử dụng `Cache-Control`, `ETag`

- [ ] **HATEOAS (nâng cao)**
  - Include links to related resources

---

## 7. Ví dụ thực tế: Student Course API với Sanic

### 7.1. API Specification

#### Resources và Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/students` | GET | Lấy danh sách tất cả sinh viên |
| `/students` | POST | Tạo sinh viên mới |
| `/students/{id}` | GET | Lấy thông tin sinh viên cụ thể |
| `/students/{id}` | PUT | Cập nhật sinh viên |
| `/students/{id}` | DELETE | Xóa sinh viên |
| `/students/{id}/courses` | GET | Lấy khóa học của sinh viên |
| `/students/{id}/courses` | POST | Thêm khóa học cho sinh viên |
| `/courses` | GET | Lấy danh sách khóa học |
| `/courses` | POST | Tạo khóa học mới |
| `/courses/{id}` | GET | Lấy thông tin khóa học |

### 7.2. Implementation (Python/Sanic)

#### Student Model

```python
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Student:
    fullname: str
    department: str
    id: Optional[int] = None
    email: Optional[str] = None
    
    def to_dict(self):
        """Convert to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create from dictionary"""
        return cls(
            id=data.get('id'),
            fullname=data.get('fullname'),
            department=data.get('department'),
            email=data.get('email')
        )
```

#### REST Resource với Sanic

```python
from sanic import Sanic, response
from sanic.request import Request
from sanic.exceptions import NotFound, InvalidUsage
from typing import Dict, List

app = Sanic("StudentCourseAPI")

# Mock database
students: Dict[int, Student] = {}
id_counter = 1

# Middleware để log requests
@app.middleware('request')
async def log_request(request):
    app.ctx.logger.info(f"{request.method} {request.path}")

# Error handler
@app.exception(NotFound)
async def handle_not_found(request, exception):
    return response.json({
        "success": False,
        "message": "Resource not found"
    }, status=404)

@app.exception(Exception)
async def handle_error(request, exception):
    return response.json({
        "success": False,
        "message": str(exception)
    }, status=500)

# GET /students - Lấy tất cả sinh viên
@app.get("/studentcourseapi/students")
async def get_all_students(request: Request):
    # Query parameters
    department = request.args.get('department')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Get all students
    result = list(students.values())
    
    # Filter by department
    if department:
        result = [s for s in result if s.department == department]
    
    # Pagination
    total = len(result)
    result = result[offset:offset + limit]
    
    return response.json({
        "success": True,
        "data": [s.to_dict() for s in result],
        "total": total,
        "limit": limit,
        "offset": offset
    })

# GET /students/{id} - Lấy một sinh viên
@app.get("/studentcourseapi/students/<student_id:int>")
async def get_student(request: Request, student_id: int):
    student = students.get(student_id)
    
    if not student:
        return response.json({
            "success": False,
            "message": "Student not found"
        }, status=404)
    
    return response.json({
        "success": True,
        "data": student.to_dict()
    })

# POST /students - Tạo sinh viên mới
@app.post("/studentcourseapi/students")
async def create_student(request: Request):
    global id_counter
    
    data = request.json
    
    # Validation
    errors = []
    if not data.get('fullname'):
        errors.append({
            "field": "fullname",
            "message": "Fullname is required"
        })
    
    if not data.get('department'):
        errors.append({
            "field": "department",
            "message": "Department is required"
        })
    
    if errors:
        return response.json({
            "success": False,
            "message": "Validation failed",
            "errors": errors
        }, status=422)
    
    # Create student
    student = Student(
        id=id_counter,
        fullname=data['fullname'],
        department=data['department'],
        email=data.get('email')
    )
    
    students[id_counter] = student
    id_counter += 1
    
    return response.json({
        "success": True,
        "message": "Student created successfully",
        "data": student.to_dict()
    }, status=201, headers={
        "Location": f"/studentcourseapi/students/{student.id}"
    })

# PUT /students/{id} - Cập nhật sinh viên
@app.put("/studentcourseapi/students/<student_id:int>")
async def update_student(request: Request, student_id: int):
    student = students.get(student_id)
    
    if not student:
        return response.json({
            "success": False,
            "message": "Student not found"
        }, status=404)
    
    data = request.json
    
    # Update fields
    if 'fullname' in data:
        student.fullname = data['fullname']
    if 'department' in data:
        student.department = data['department']
    if 'email' in data:
        student.email = data['email']
    
    return response.json({
        "success": True,
        "message": "Student updated successfully",
        "data": student.to_dict()
    })

# PATCH /students/{id} - Cập nhật một phần
@app.patch("/studentcourseapi/students/<student_id:int>")
async def patch_student(request: Request, student_id: int):
    student = students.get(student_id)
    
    if not student:
        return response.json({
            "success": False,
            "message": "Student not found"
        }, status=404)
    
    data = request.json
    
    # Update only provided fields
    for field, value in data.items():
        if hasattr(student, field):
            setattr(student, field, value)
    
    return response.json({
        "success": True,
        "message": "Student updated successfully",
        "data": student.to_dict()
    })

# DELETE /students/{id} - Xóa sinh viên
@app.delete("/studentcourseapi/students/<student_id:int>")
async def delete_student(request: Request, student_id: int):
    if student_id not in students:
        return response.json({
            "success": False,
            "message": "Student not found"
        }, status=404)
    
    del students[student_id]
    
    # Return 204 No Content
    return response.empty(status=204)

# Health check endpoint
@app.get("/health")
async def health_check(request: Request):
    return response.json({
        "status": "healthy",
        "service": "StudentCourseAPI"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
```

### 7.3. Testing với cURL

#### Tạo sinh viên mới

```bash
curl -X POST http://localhost:8000/studentcourseapi/students \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "James Dean",
    "department": "Computing Science",
    "email": "james@example.com"
  }'
```

**Response:**
```json
{
  "success": true,
  "message": "Student created successfully",
  "data": {
    "id": 1,
    "fullname": "James Dean",
    "department": "Computing Science",
    "email": "james@example.com"
  }
}
```

#### Lấy danh sách sinh viên

```bash
curl "http://localhost:8000/studentcourseapi/students?department=CS&limit=5"
```

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": 1,
      "fullname": "James Dean",
      "department": "Computing Science",
      "email": "james@example.com"
    }
  ],
  "total": 1,
  "limit": 5,
  "offset": 0
}
```

#### Cập nhật sinh viên

```bash
curl -X PUT http://localhost:8000/studentcourseapi/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "fullname": "James Dean Updated",
    "department": "Computing Science",
    "email": "james.new@example.com"
  }'
```

#### Cập nhật một phần (PATCH)

```bash
curl -X PATCH http://localhost:8000/studentcourseapi/students/1 \
  -H "Content-Type: application/json" \
  -d '{
    "email": "james.updated@example.com"
  }'
```

#### Xóa sinh viên

```bash
curl -X DELETE http://localhost:8000/studentcourseapi/students/1
```

### 7.4. Testing với Python requests

```python
import requests
import json

BASE_URL = "http://localhost:8000/studentcourseapi"

# 1. Tạo sinh viên mới
def create_student():
    url = f"{BASE_URL}/students"
    data = {
        "fullname": "John Doe",
        "department": "Computer Science",
        "email": "john@example.com"
    }
    
    response = requests.post(url, json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.json()['data']['id']

# 2. Lấy danh sách sinh viên
def get_students():
    url = f"{BASE_URL}/students"
    params = {"department": "Computer Science", "limit": 10}
    
    response = requests.get(url, params=params)
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# 3. Lấy sinh viên theo ID
def get_student(student_id):
    url = f"{BASE_URL}/students/{student_id}"
    response = requests.get(url)
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# 4. Cập nhật sinh viên
def update_student(student_id):
    url = f"{BASE_URL}/students/{student_id}"
    data = {
        "fullname": "John Doe Updated",
        "department": "Computer Science",
        "email": "john.updated@example.com"
    }
    
    response = requests.put(url, json=data)
    print(f"Response: {json.dumps(response.json(), indent=2)}")

# 5. Xóa sinh viên
def delete_student(student_id):
    url = f"{BASE_URL}/students/{student_id}"
    response = requests.delete(url)
    print(f"Status: {response.status_code}")

# Run tests
if __name__ == "__main__":
    student_id = create_student()
    get_students()
    get_student(student_id)
    update_student(student_id)
    delete_student(student_id)
```

### 7.5. Advanced Features

#### Authentication Middleware

```python
from sanic import Sanic
from functools import wraps
import jwt

app = Sanic("StudentCourseAPI")
SECRET_KEY = "your-secret-key-here"

def protected(wrapped):
    """Decorator để bảo vệ routes"""
    @wraps(wrapped)
    async def decorated_function(request, *args, **kwargs):
        # Get token from header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return response.json({
                "success": False,
                "message": "Missing or invalid authorization header"
            }, status=401)
        
        token = auth_header.split(' ')[1]
        
        try:
            # Verify token
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.ctx.user = payload
            
        except jwt.ExpiredSignatureError:
            return response.json({
                "success": False,
                "message": "Token has expired"
            }, status=401)
            
        except jwt.InvalidTokenError:
            return response.json({
                "success": False,
                "message": "Invalid token"
            }, status=401)
        
        return await wrapped(request, *args, **kwargs)
    
    return decorated_function

# Protected route
@app.get("/studentcourseapi/students")
@protected
async def get_all_students(request: Request):
    # Access user info from token
    user = request.ctx.user
    
    # Your logic here
    return response.json({
        "success": True,
        "data": [],
        "user": user['username']
    })
```

#### Rate Limiting

```python
from sanic_limiter import Limiter, get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour", "10 per minute"]
)

@app.get("/studentcourseapi/students")
@limiter.limit("5 per minute")
async def get_all_students(request: Request):
    # Rate limited endpoint
    return response.json({"data": []})
```

#### CORS Support

```python
from sanic_cors import CORS

app = Sanic("StudentCourseAPI")

# Enable CORS
CORS(app, resources={
    r"/studentcourseapi/*": {
        "origins": ["http://localhost:3000", "https://yourdomain.com"],
        "methods": ["GET", "POST", "PUT", "DELETE", "PATCH"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

#### Logging

```python
import logging
from sanic import Sanic
from sanic.log import logger

app = Sanic("StudentCourseAPI")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

@app.middleware('request')
async def log_request(request):
    logger.info(f"Incoming: {request.method} {request.path}")

@app.middleware('response')
async def log_response(request, response):
    logger.info(f"Response: {request.method} {request.path} - {response.status}")

@app.post("/studentcourseapi/students")
async def create_student(request):
    try:
        logger.info("Creating new student")
        # Your logic
        logger.info(f"Student created successfully with ID: {student.id}")
        return response.json({"success": True})
    except Exception as e:
        logger.error(f"Error creating student: {str(e)}")
        raise
```

#### Database Integration (với SQLAlchemy)

```python
from sanic import Sanic, response
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

app = Sanic("StudentCourseAPI")

# Database setup
DATABASE_URL = "postgresql://user:password@localhost/studentdb"
engine = create_engine(DATABASE_URL)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

Base = declarative_base()

# Student Model
class StudentModel(Base):
    __tablename__ = 'students'
    
    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    department = Column(String(50), nullable=False)
    email = Column(String(100))

Base.metadata.create_all(engine)

# Middleware to manage sessions
@app.middleware('request')
async def setup_session(request):
    request.ctx.session = Session()

@app.middleware('response')
async def close_session(request, response):
    request.ctx.session.close()

# GET /students with database
@app.get("/studentcourseapi/students")
async def get_all_students(request):
    session = request.ctx.session
    
    # Query parameters
    department = request.args.get('department')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Build query
    query = session.query(StudentModel)
    
    if department:
        query = query.filter(StudentModel.department == department)
    
    total = query.count()
    students = query.offset(offset).limit(limit).all()
    
    return response.json({
        "success": True,
        "data": [{
            "id": s.id,
            "fullname": s.fullname,
            "department": s.department,
            "email": s.email
        } for s in students],
        "total": total
    })

# POST /students with database
@app.post("/studentcourseapi/students")
async def create_student(request):
    session = request.ctx.session
    data = request.json
    
    # Validation
    if not data.get('fullname') or not data.get('department'):
        return response.json({
            "success": False,
            "message": "Fullname and department are required"
        }, status=422)
    
    # Create student
    student = StudentModel(
        fullname=data['fullname'],
        department=data['department'],
        email=data.get('email')
    )
    
    session.add(student)
    session.commit()
    session.refresh(student)
    
    return response.json({
        "success": True,
        "message": "Student created successfully",
        "data": {
            "id": student.id,
            "fullname": student.fullname,
            "department": student.department,
            "email": student.email
        }
    }, status=201)
```

#### Async Database with Tortoise ORM

```python
from sanic import Sanic, response
from tortoise import fields
from tortoise.models import Model
from tortoise.contrib.sanic import register_tortoise

app = Sanic("StudentCourseAPI")

# Define model
class Student(Model):
    id = fields.IntField(pk=True)
    fullname = fields.CharField(max_length=100)
    department = fields.CharField(max_length=50)
    email = fields.CharField(max_length=100, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    
    class Meta:
        table = "students"

# Register Tortoise ORM
register_tortoise(
    app,
    db_url="sqlite://db.sqlite3",
    modules={"models": ["__main__"]},
    generate_schemas=True
)

# Async endpoints
@app.get("/studentcourseapi/students")
async def get_all_students(request):
    # Query parameters
    department = request.args.get('department')
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    
    # Build query
    query = Student.all()
    
    if department:
        query = query.filter(department=department)
    
    total = await query.count()
    students = await query.offset(offset).limit(limit)
    
    return response.json({
        "success": True,
        "data": [await student.to_dict() for student in students],
        "total": total
    })

@app.post("/studentcourseapi/students")
async def create_student(request):
    data = request.json
    
    # Create student
    student = await Student.create(
        fullname=data['fullname'],
        department=data['department'],
        email=data.get('email')
    )
    
    return response.json({
        "success": True,
        "message": "Student created successfully",
        "data": {
            "id": student.id,
            "fullname": student.fullname,
            "department": student.department,
            "email": student.email
        }
    }, status=201)

@app.get("/studentcourseapi/students/<student_id:int>")
async def get_student(request, student_id: int):
    student = await Student.get_or_none(id=student_id)
    
    if not student:
        return response.json({
            "success": False,
            "message": "Student not found"
        }, status=404)
    
    return response.json({
        "success": True,
        "data": {
            "id": student.id,
            "fullname": student.fullname,
            "department": student.department,
            "email": student.email
        }
    })

@app.put("/studentcourseapi/students/<student_id:int>")
async def update_student(request, student_id: int):
    student = await Student.get_or_none(id=student_id)
    
    if not student:
        return response.json({
            "success": False,
            "message": "Student not found"
        }, status=404)
    
    data = request.json
    
    # Update fields
    await student.update_from_dict(data).save()
    
    return response.json({
        "success": True,
        "message": "Student updated successfully",
        "data": {
            "id": student.id,
            "fullname": student.fullname,
            "department": student.department,
            "email": student.email
        }
    })

@app.delete("/studentcourseapi/students/<student_id:int>")
async def delete_student(request, student_id: int):
    student = await Student.get_or_none(id=student_id)
    
    if not student:
        return response.json({
            "success": False,
            "message": "Student not found"
        }, status=404)
    
    await student.delete()
    
    return response.empty(status=204)
```

### 7.6. Docker Deployment

#### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Run application
CMD ["python", "app.py"]
```

#### requirements.txt

```txt
sanic==23.12.0
sanic-cors==2.2.0
httpx==0.25.2
tortoise-orm==0.20.0
asyncpg==0.29.0
pydantic==2.5.0
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
```

#### docker-compose.yml

```yaml
version: '3.8'

services:
  student-service:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/studentdb
      - SECRET_KEY=your-secret-key
    depends_on:
      - db
    volumes:
      - ./:/app
    command: python app.py

  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=studentdb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

#### Run with Docker

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f student-service

# Stop services
docker-compose down

# Rebuild after code changes
docker-compose up -d --build
```

---

## 8. Kết luận

### 8.1. Hành trình SOA

```
Monolithic → SOAP/WS* → REST → Microservices
   (Phức tạp)  (Nặng nề)  (Đơn giản)  (Linh hoạt)
```

### 8.2. Key Takeaways

1. **SOA = Triết lý xây dựng hệ thống từ các dịch vụ**
   - Tái sử dụng, mô-đun hóa, linh hoạt

2. **REST = Cách thực thi SOA đơn giản, hiệu quả**
   - Dựa trên HTTP, URI, và resources
   - 5 ràng buộc: Client-Server, Stateless, Cacheable, Layered, Uniform Interface

3. **HTTP = Giao thức nền tảng**
   - Request-Response pattern
   - Methods, Headers, Status Codes
   - Stateless protocol

4. **Microservices = SOA ở quy mô ứng dụng**
   - Dịch vụ nhỏ, độc lập
   - Giao tiếp qua REST
   - Ưu điểm: Scalability, Resilience, Independent Deployment
   - Nhược điểm: Complexity, Transaction Management

5. **Python & Sanic = Công cụ mạnh mẽ cho REST API**
   - Async/await cho performance cao
   - Đơn giản, dễ học
   - Ecosystem phong phú

### 8.3. Bước tiếp theo

Để thực sự thành thạo:

1. **Thực hành xây dựng RESTful API với Sanic**
   - Implement CRUD operations
   - Thêm authentication & authorization
   - Test với pytest và Postman

2. **Áp dụng best practices**
   - URI design theo chuẩn REST
   - HTTP methods và status codes đúng
   - Error handling và validation
   - API versioning

3. **Khám phá Microservices**
   - Chia ứng dụng thành services
   - Service discovery với Consul
   - API Gateway pattern
   - Circuit breaker với pybreaker

4. **Học về DevOps**
   - Docker containerization
   - Kubernetes orchestration
   - CI/CD với GitHub Actions
   - Monitoring với Prometheus & Grafana

---

## Phụ lục

### A. HTTP Status Codes - Tham khảo đầy đủ

#### 1xx: Informational
- `100 Continue` - Client có thể tiếp tục request
- `101 Switching Protocols` - Server chuyển protocol theo yêu cầu

#### 2xx: Success
- `200 OK` - Request thành công
- `201 Created` - Resource được tạo thành công
- `202 Accepted` - Request được chấp nhận nhưng chưa xử lý xong
- `204 No Content` - Thành công nhưng không có content trả về

#### 3xx: Redirection
- `301 Moved Permanently` - Resource chuyển vĩnh viễn
- `302 Found` - Resource tạm thời ở URL khác
- `304 Not Modified` - Client có thể dùng cached version

#### 4xx: Client Errors
- `400 Bad Request` - Request sai format
- `401 Unauthorized` - Cần authentication
- `403 Forbidden` - Không có quyền truy cập
- `404 Not Found` - Không tìm thấy resource
- `405 Method Not Allowed` - Method không được phép
- `422 Unprocessable Entity` - Validation errors
- `429 Too Many Requests` - Rate limit exceeded

#### 5xx: Server Errors
- `500 Internal Server Error` - Lỗi server chung
- `502 Bad Gateway` - Gateway/proxy error
- `503 Service Unavailable` - Server quá tải
- `504 Gateway Timeout` - Gateway timeout

### B. Sanic Cheat Sheet

#### Basic App Setup

```python
from sanic import Sanic, response

app = Sanic("MyApp")

# Simple route
@app.route("/")
async def index(request):
    return response.text("Hello, World!")

# Route with parameter
@app.route("/users/<user_id:int>")
async def get_user(request, user_id):
    return response.json({"user_id": user_id})

# Multiple methods
@app.route("/items", methods=["GET", "POST"])
async def items(request):
    if request.method == "GET":
        return response.json([])
    else:
        return response.json({"created": True})

# Run app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

#### Request Object

```python
@app.post("/data")
async def handle_data(request):
    # JSON body
    data = request.json
    
    # Form data
    form_data = request.form
    
    # Files
    files = request.files
    
    # Query parameters
    param = request.args.get('param')
    
    # Headers
    auth = request.headers.get('Authorization')
    
    # Cookies
    session = request.cookies.get('session_id')
    
    return response.json({"received": True})
```

#### Response Types

```python
# JSON response
@app.get("/json")
async def json_response(request):
    return response.json({"key": "value"})

# Text response
@app.get("/text")
async def text_response(request):
    return response.text("Plain text")

# HTML response
@app.get("/html")
async def html_response(request):
    return response.html("<h1>Hello</h1>")

# Empty response (204)
@app.delete("/item")
async def delete_item(request):
    return response.empty(status=204)

# Redirect
@app.get("/old")
async def redirect_old(request):
    return response.redirect("/new")

# File download
@app.get("/download")
async def download_file(request):
    return await response.file("/path/to/file.pdf")
```

#### Middleware

```python
# Request middleware
@app.middleware('request')
async def add_start_time(request):
    request.ctx.start_time = time.time()

# Response middleware
@app.middleware('response')
async def add_elapsed_time(request, response):
    elapsed = time.time() - request.ctx.start_time
    response.headers['X-Elapsed-Time'] = str(elapsed)
```

#### Error Handling

```python
from sanic.exceptions import NotFound, ServerError

@app.exception(NotFound)
async def handle_not_found(request, exception):
    return response.json(
        {"error": "Not found"},
        status=404
    )

@app.exception(Exception)
async def handle_exception(request, exception):
    return response.json(
        {"error": str(exception)},
        status=500
    )
```

#### Blueprints

```python
from sanic import Blueprint

# Create blueprint
api = Blueprint("api", url_prefix="/api/v1")

@api.get("/users")
async def get_users(request):
    return response.json([])

@api.post("/users")
async def create_user(request):
    return response.json({"created": True})

# Register blueprint
app.blueprint(api)
```

### C. Testing RESTful APIs

#### Unit Tests với pytest

```python
import pytest
from app import app

@pytest.fixture
def test_cli():
    return app.test_client

def test_get_students(test_cli):
    request, response = test_cli.get('/studentcourseapi/students')
    assert response.status == 200
    assert response.json['success'] == True

def test_create_student(test_cli):
    data = {
        "fullname": "Test Student",
        "department": "CS"
    }
    request, response = test_cli.post(
        '/studentcourseapi/students',
        json=data
    )
    assert response.status == 201
    assert response.json['success'] == True
    assert 'id' in response.json['data']

def test_get_student_not_found(test_cli):
    request, response = test_cli.get('/studentcourseapi/students/9999')
    assert response.status == 404
    assert response.json['success'] == False

def test_validation_error(test_cli):
    data = {"fullname": ""}  # Missing department
    request, response = test_cli.post(
        '/studentcourseapi/students',
        json=data
    )
    assert response.status == 422
    assert 'errors' in response.json
```

#### Integration Tests

```python
import pytest
import asyncio
from app import app

@pytest.fixture
def test_cli():
    return app.test_client

def test_full_crud_workflow(test_cli):
    # 1. Create
    create_data = {
        "fullname": "John Doe",
        "department": "CS",
        "email": "john@example.com"
    }
    _, create_response = test_cli.post(
        '/studentcourseapi/students',
        json=create_data
    )
    assert create_response.status == 201
    student_id = create_response.json['data']['id']
    
    # 2. Read
    _, read_response = test_cli.get(
        f'/studentcourseapi/students/{student_id}'
    )
    assert read_response.status == 200
    assert read_response.json['data']['fullname'] == "John Doe"
    
    # 3. Update
    update_data = {
        "fullname": "John Doe Updated",
        "department": "CS",
        "email": "john.updated@example.com"
    }
    _, update_response = test_cli.put(
        f'/studentcourseapi/students/{student_id}',
        json=update_data
    )
    assert update_response.status == 200
    
    # 4. Delete
    _, delete_response = test_cli.delete(
        f'/studentcourseapi/students/{student_id}'
    )
    assert delete_response.status == 204
    
    # 5. Verify deletion
    _, verify_response = test_cli.get(
        f'/studentcourseapi/students/{student_id}'
    )
    assert verify_response.status == 404
```

### D. Tài nguyên học tập

#### Documentation
- [Sanic Documentation](https://sanic.dev/)
- [MDN HTTP Guide](https://developer.mozilla.org/en-US/docs/Web/HTTP)
- [REST API Tutorial](https://restfulapi.net/)
- [Microservices.io](https://microservices.io/)
- [Python AsyncIO](https://docs.python.org/3/library/asyncio.html)

#### Books
- "RESTful Web Services" by Leonard Richardson
- "Building Microservices" by Sam Newman
- "Designing Data-Intensive Applications" by Martin Kleppmann
- "Python Web Development with Sanic" by Adam Hopkins

#### Tools
- **Postman**: Test REST APIs
- **HTTPie**: Command-line HTTP client
- **Swagger/OpenAPI**: API documentation
- **Docker**: Containerization
- **Kubernetes**: Orchestration
- **pytest**: Python testing framework

#### Python Libraries cho REST API
- **Sanic**: Async web framework (nhanh nhất)
- **FastAPI**: Modern, fast với automatic OpenAPI docs
- **Flask**: Lightweight, dễ học
- **Django REST Framework**: Full-featured, batteries included
- **Tornado**: Scalable, non-blocking
- **aiohttp**: Async HTTP client/server

---

## E. Complete Example Project Structure

```
student-course-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── config.py               # Configuration
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── student.py
│   │   └── course.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── students.py
│   │   └── courses.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── student_service.py
│   │   └── course_service.py
│   │
│   ├── middleware/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── logging.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── validators.py
│       └── responses.py
│
├── tests/
│   ├── __init__.py
│   ├── test_students.py
│   └── test_courses.py
│
├── migrations/
│   └── versions/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── .env
├── .gitignore
├── requirements.txt
├── README.md
└── pytest.ini
```

### Sample Files

#### app/main.py

```python
from sanic import Sanic
from app.routes import students, courses
from app.middleware.auth import setup_auth
from app.middleware.logging import setup_logging
from app.config import Config

def create_app():
    app = Sanic("StudentCourseAPI")
    
    # Load config
    app.config.update_config(Config)
    
    # Setup middleware
    setup_logging(app)
    setup_auth(app)
    
    # Register blueprints
    app.blueprint(students.bp)
    app.blueprint(courses.bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
        auto_reload=True
    )
```

#### app/config.py

```python
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "postgresql://user:pass@localhost/studentdb"
    )
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    
    # API
    API_VERSION = "v1"
    API_PREFIX = f"/api/{API_VERSION}"
    
    # Pagination
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100
```

---

**Chúc bạn học tốt và thành công trong việc xây dựng các hệ thống Service-Oriented Architecture với Python và Sanic!**

---

## F. Quick Reference Card

### REST Principles
✓ Resources (nouns) not actions (verbs)  
✓ HTTP methods for operations  
✓ Stateless communication  
✓ Use proper status codes  
✓ Support content negotiation  

### HTTP Methods
- **GET**: Retrieve resources
- **POST**: Create new resources
- **PUT**: Update/replace resources
- **PATCH**: Partial update
- **DELETE**: Remove resources

### Status Codes Quick Guide
- **2xx**: Success (200, 201, 204)
- **3xx**: Redirection (301, 304)
- **4xx**: Client errors (400, 401, 404, 422)
- **5xx**: Server errors (500, 503)

### Sanic Quick Start
```python
from sanic import Sanic, response

app = Sanic("MyAPI")

@app.get("/resource")
async def get_resource(request):
    return response.json({"data": []})

app.run(host="0.0.0.0", port=8000)
```