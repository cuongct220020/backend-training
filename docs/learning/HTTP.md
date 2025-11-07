# HTTP Request & Response - Giải thích chi tiết

## 1. HTTP Request (Yêu cầu từ Client → Server)

### Cấu trúc tổng quát

```
[Request Line]
[Headers]
[Blank Line]
[Body (optional)]
```

### 1.1. Request Line

Dòng đầu tiên chứa 3 phần:

```
GET /api/users/123 HTTP/1.1
```

- **Method**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, etc.
- **URI/Path**: `/api/users/123` (đường dẫn tài nguyên)
- **HTTP Version**: `HTTP/1.1` hoặc `HTTP/2`

### 1.2. Request Headers

Headers chứa metadata về request. Format: `Key: Value`

#### Headers phổ biến:

**Authentication & Authorization:**
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Cookie: session_id=abc123; user_token=xyz789
```

**Content Negotiation:**
```
Content-Type: application/json
Accept: application/json, text/html
Accept-Language: vi-VN, en-US
Accept-Encoding: gzip, deflate, br
```

**Client Information:**
```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)...
Referer: https://example.com/previous-page
Origin: https://example.com
```

**Connection & Caching:**
```
Connection: keep-alive
Cache-Control: no-cache
If-None-Match: "etag-12345"
If-Modified-Since: Wed, 21 Oct 2024 07:28:00 GMT
```

**Custom Headers:**
```
X-Request-ID: req-uuid-12345
X-API-Key: your-api-key-here
X-Forwarded-For: 203.113.45.67
```

### 1.3. Request Body

Body chứa dữ liệu gửi lên server (thường dùng với `POST`, `PUT`, `PATCH`).

#### JSON Body (phổ biến nhất):

```json
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}
```

#### Form Data (application/x-www-form-urlencoded):

```
username=john_doe&email=john@example.com&password=SecurePass123!
```

#### Multipart Form Data (upload files):

```
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="avatar"; filename="photo.jpg"
Content-Type: image/jpeg

[binary image data]
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

### Ví dụ HTTP Request hoàn chỉnh:

```http
POST /api/auth/login HTTP/1.1
Host: api.example.com
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Content-Length: 78
Connection: keep-alive

{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

---

## 2. HTTP Response (Phản hồi từ Server → Client)

### Cấu trúc tổng quát

```
[Status Line]
[Headers]
[Blank Line]
[Body]
```

### 2.1. Status Line

Dòng đầu tiên chứa:

```
HTTP/1.1 200 OK
```

- **HTTP Version**: `HTTP/1.1`
- **Status Code**: `200` (mã trạng thái)
- **Reason Phrase**: `OK` (mô tả ngắn gọn)

#### Các Status Code phổ biến:

**2xx - Success (Thành công):**
- `200 OK` - Request thành công
- `201 Created` - Tạo resource mới thành công
- `204 No Content` - Thành công nhưng không có body

**3xx - Redirection (Chuyển hướng):**
- `301 Moved Permanently` - Resource đã chuyển vĩnh viễn
- `302 Found` - Chuyển hướng tạm thời
- `304 Not Modified` - Resource chưa thay đổi (cache valid)

**4xx - Client Error (Lỗi từ client):**
- `400 Bad Request` - Request sai format
- `401 Unauthorized` - Chưa xác thực (cần login)
- `403 Forbidden` - Không có quyền truy cập
- `404 Not Found` - Không tìm thấy resource
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limit exceeded

**5xx - Server Error (Lỗi từ server):**
- `500 Internal Server Error` - Lỗi server
- `502 Bad Gateway` - Gateway/proxy lỗi
- `503 Service Unavailable` - Server quá tải hoặc maintenance

### 2.2. Response Headers

Headers chứa metadata về response.

#### Headers phổ biến:

**Content Information:**
```
Content-Type: application/json; charset=utf-8
Content-Length: 1234
Content-Encoding: gzip
Content-Language: vi-VN
```

**Caching:**
```
Cache-Control: public, max-age=3600
ETag: "abc123def456"
Expires: Thu, 01 Dec 2024 16:00:00 GMT
Last-Modified: Wed, 21 Oct 2024 07:28:00 GMT
```

**Security:**
```
Strict-Transport-Security: max-age=31536000
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Content-Security-Policy: default-src 'self'
```

**CORS (Cross-Origin Resource Sharing):**
```
Access-Control-Allow-Origin: https://example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

**Authentication:**
```
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict
WWW-Authenticate: Bearer realm="api"
```

**Custom Headers:**
```
X-Request-ID: req-uuid-12345
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1609459200
```

### 2.3. Response Body

Body chứa dữ liệu trả về cho client.

#### JSON Response (phổ biến nhất):

**Success Response:**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 123,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
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
      "field": "password",
      "message": "Password must be at least 8 characters"
    }
  ]
}
```

#### HTML Response:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Welcome</title>
</head>
<body>
    <h1>Hello World!</h1>
</body>
</html>
```

#### Plain Text Response:

```
User created successfully
```

### Ví dụ HTTP Response hoàn chỉnh:

```http
HTTP/1.1 200 OK
Date: Tue, 04 Nov 2025 10:30:00 GMT
Server: nginx/1.18.0
Content-Type: application/json; charset=utf-8
Content-Length: 245
Connection: keep-alive
Cache-Control: no-cache, no-store, must-revalidate
X-Request-ID: req-uuid-12345
Set-Cookie: session_id=abc123; HttpOnly; Secure; SameSite=Strict

{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": 123,
      "username": "john_doe",
      "email": "john@example.com"
    },
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

## 3. Flow hoàn chỉnh: Client ↔ Server

### Ví dụ Login Flow:

#### Step 1: Client gửi Request

```http
POST /api/auth/login HTTP/1.1
Host: api.example.com
Content-Type: application/json
Accept: application/json
User-Agent: Mozilla/5.0
Content-Length: 56

{
  "username": "john_doe",
  "password": "SecurePass123!"
}
```

#### Step 2: Server xử lý và trả về Response

```http
HTTP/1.1 200 OK
Content-Type: application/json
Set-Cookie: refresh_token=xyz789; HttpOnly; Secure
X-RateLimit-Remaining: 99

{
  "success": true,
  "data": {
    "access_token": "eyJhbGci...",
    "expires_in": 3600,
    "user": {
      "id": 123,
      "username": "john_doe"
    }
  }
}
```

#### Step 3: Client gửi Request tiếp theo với Token

```http
GET /api/users/me HTTP/1.1
Host: api.example.com
Authorization: Bearer eyJhbGci...
Accept: application/json
```

#### Step 4: Server trả về Protected Resource

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "success": true,
  "data": {
    "id": 123,
    "username": "john_doe",
    "email": "john@example.com",
    "role": "user"
  }
}
```

---

## 4. Best Practices

### 4.1. Request Best Practices

✅ **Luôn set đúng `Content-Type`:**
```python
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
```

✅ **Sử dụng proper HTTP methods:**
- `GET` - Đọc dữ liệu (không có body)
- `POST` - Tạo mới
- `PUT` - Cập nhật toàn bộ
- `PATCH` - Cập nhật một phần
- `DELETE` - Xóa

✅ **Handle authentication properly:**
```python
headers = {
    "Authorization": f"Bearer {access_token}"
}
```

### 4.2. Response Best Practices

✅ **Luôn trả về đúng Status Code:**
```python
# Success
return json({"success": True}, status=200)

# Created
return json({"success": True}, status=201)

# Validation error
return json({"errors": errors}, status=422)

# Unauthorized
return json({"message": "Unauthorized"}, status=401)
```

✅ **Consistent response format:**
```python
{
  "success": true/false,
  "message": "Human readable message",
  "data": {...},      # khi success
  "errors": [...]     # khi có lỗi
}
```

✅ **Set proper headers:**
```python
headers = {
    "Content-Type": "application/json",
    "X-Request-ID": request_id,
    "Cache-Control": "no-cache"
}
```

---

## 5. Tóm tắt quan trọng

### Request = "Client hỏi Server"
- **Headers** = thông tin về request (ai hỏi, muốn gì, format gì)
- **Body** = dữ liệu chi tiết (nếu có)

### Response = "Server trả lời Client"
- **Headers** = thông tin về response (loại dữ liệu, cache, security)
- **Body** = dữ liệu trả về (JSON, HTML, text, etc.)

### Headers quan trọng nhất:
- `Content-Type`: Loại dữ liệu
- `Authorization`: Xác thực
- `Accept`: Client muốn nhận gì
- `Cache-Control`: Caching policy
- `Set-Cookie`: Set cookies (response only)