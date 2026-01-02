# IMPORTANT NOTEBOOK

## Quy tắc thiết kế Middleware và Decorators

### Nguyên tắc cơ bản

**1. Middleware = Bảo vệ cổng chính (xử lý chung cho nhiều route)**

Middleware chạy cho toàn bộ ứng dụng hoặc một nhóm route (blueprint). Chỉ làm những việc nhẹ nhàng như:
- Phân tích token (parse JWT)
- Đọc từ cache (Redis)
- Từ chối cơ bản (basic deny)

**KHÔNG làm** những việc nặng như:
- ❌ Join nhiều bảng trong database
- ❌ Commit transaction vào database

**2. Decorators = Kiểm tra riêng từng cửa (xử lý đặc thù cho từng endpoint)**

Decorator dùng cho logic riêng biệt của từng route:
- Kiểm tra dữ liệu đầu vào (`body`, `query`, `path`)
- Kiểm tra quyền hạn (`roles`, `authorization`)
- Kiểm tra session có bị thu hồi không (cần tra database)
- Giới hạn số lần gọi API cho từng route
- Ghi log hành động người dùng

**3. Tránh làm việc trùng lặp**

- Nếu middleware đã parse JWT và lưu `request.ctx.user` → decorator không cần parse lại
- Nếu middleware đã kiểm tra body toàn cục → decorator không cần kiểm tra lại
- Ngược lại, nếu muốn kiểm soát rõ ràng từng route → dùng decorator `validate_request`

**4. Ưu tiên đọc Cache trước trong Middleware**

- Middleware nên query Redis (rất nhanh) để lấy thông tin user/session
- Nếu không có trong cache → decorator hoặc service sẽ đọc từ database

**5. Service layer là nguồn chân lý**

- Service vẫn phải kiểm tra logic nghiệp vụ (user có tồn tại không? tài khoản còn active không?)
- Decorator chỉ kiểm tra quyền truy cập hoặc điều kiện tiên quyết

**6. Giữ Middleware thật nhanh**

Tránh:
- ❌ Blocking I/O (chờ đợi lâu)
- ❌ Query database phức tạp

---

## Các Middleware nên dùng cho `auth_bp`

### `auth_parse_middleware` **(BẮT BUỘC)**

**Làm gì:**
- Đọc header `Authorization`
- Kiểm tra chữ ký JWT (JWT Signature)
- Giải mã thông tin trong token (decode claims)
- Lưu vào `request.ctx.token_claims` và `request.ctx.user_id` (lấy từ `sub`)

**Chi tiết:**
- Kiểm tra chữ ký và thời gian hết hạn
- Nếu token không hợp lệ → trả về lỗi `401 Unauthorized`
- Nếu token hợp lệ → thử đọc thông tin session từ Redis (VD: `jti` có bị blacklist không?)
- Lưu `request.ctx.session` hoặc `request.ctx.jti`

### `public_paths_middleware` **(TÙY CHỌN)**

**Làm gì:**
Bỏ qua kiểm tra xác thực cho các endpoint công khai như `login`, `register`, `docs`

**Chi tiết:**
- Sử dụng hàm `is_required_authenticate()` đã có sẵn
- Trả về `None` sớm để route chạy mà không cần xác thực

### `rate_limit_middleware` **(TÙY CHỌN - kiểm tra nhẹ toàn cục)**

**Làm gì:**
Giới hạn số lần gọi API toàn cục theo IP hoặc theo user, sử dụng Redis counters

**Chi tiết:**
- Rất nhẹ, từ chối ngay nếu vượt quá giới hạn

### `response_wrapper_middleware` **(TÙY CHỌN)**

**Làm gì:**
Đảm bảo tất cả response đều dùng format `GenericResponse`; có thể bọc output nếu view trả về dict thông thường

**Chi tiết:**
- Chỉ format dữ liệu, không xử lý logic nghiệp vụ

### `error_handler_middleware` (cấp ứng dụng)

**Làm gì:**
Bắt các exception và trả về schema lỗi chuẩn hóa

---

## Các Decorators nên dùng (cho từng route)

### `@validate_request(schema)`

**Công dụng:**
- Kiểm tra dữ liệu đầu vào (`body`, `query`, `path`) bằng Pydantic
- Lưu dữ liệu đã kiểm tra vào `request.ctx.payload`
- Dùng khi muốn kiểm soát schema rõ ràng cho từng route
- Nếu thích mapping schema cấp blueprint → có thể bỏ qua decorator này

### `@require_auth` (nhẹ)

**Công dụng:**
- Đảm bảo `request.ctx.token_claims` tồn tại (do middleware gán)
- Nếu không có → trả về `401`
- Hơi thừa nếu `auth_parse_middleware` đã trả về `401` khi token không hợp lệ
- Nhưng hữu ích để đánh dấu rằng view này yêu cầu đăng nhập

### `@require_active_session` **(kiểm tra session)**

**Công dụng:**
- Kiểm tra Redis (hoặc DB) xem `jti` có bị thu hồi/blacklist không
- Kiểm tra session có hết hạn không
- Nếu không có trong cache → query database qua repository
- Dùng cho các route nhạy cảm phải đảm bảo refresh token/session chưa bị thu hồi
- Vì phụ thuộc DB/cache nên nên là decorator, không phải middleware

### `@require_roles(*roles)`

**Công dụng:**
- Kiểm soát truy cập theo vai trò (Role-based access control)
- Kiểm tra `request.ctx.token_claims['roles']` hoặc lấy roles từ cache/DB
- Dùng cho các endpoint admin (VD: `/auth/sessions` chỉ admin xem được)

### `@audit_event(event_name)`

**Công dụng:**
- Ghi log kiểm toán (audit log): user, hành động, IP, user-agent
- Dùng decorator để chỉ các endpoint cần audit mới được ghi log

### `@limit_per_user(rate_spec)` **(giới hạn theo route)**

**Công dụng:**
- Dùng Redis để áp dụng giới hạn số lần gọi riêng cho từng endpoint

---

## Ai làm gì — Phân công cho các endpoint auth

Blueprint `/auth/*` gồm: `login`, `logout`, `refresh`, `otp`, `sessions`, `change-password`, `unlock`

### `login_view` (Đăng nhập)

**Middleware:**
- Bỏ qua kiểm tra auth (public path - không cần token)

**Decorator:**
- `@validate_request(LoginRequestSchema)` - Kiểm tra dữ liệu đăng nhập
- `@limit_per_user` - Giới hạn số lần đăng nhập (chống brute force)

**Service:**
- Kiểm tra username/password
- Tạo session mới trong database
- Lưu thông tin session & refresh token vào database
- Lưu `jti` vào Redis để tra cứu nhanh

### `logout_view` (Đăng xuất)

**Middleware:**
- Parse JWT (gán claims vào request)

**Decorator:**
- `@require_auth` - Yêu cầu đăng nhập
- `@require_active_session` - Session phải còn hiệu lực

**Service:**
- Thu hồi session
- Lưu `jti` vào Redis blacklist với TTL = thời gian còn lại của token
- Hoặc đánh dấu revoked trong database
- Xóa cache session của user

### `refresh_view` (Làm mới token)

**Middleware:**
- Parse refresh token (nếu truyền qua cookie/body)
- Có thể tách ra `refresh_token_middleware` riêng vì format khác access token

**Decorator:**
- `@validate_request(RefreshRequestSchema)` - Kiểm tra dữ liệu
- `@require_active_session` - Kiểm tra `jti`

**Service:**
- Xoay vòng tokens (rotate)
- Thu hồi refresh token cũ
- Lưu refresh token mới
- Cập nhật cache

### `otp_view` (Mã OTP)

**Middleware:**
- Public hoặc xác thực một phần (gửi OTP là public, xác minh OTP có thể là public)

**Decorator:**
- `@validate_request(OTPRequest)` - Kiểm tra dữ liệu

**Service:**
- Tạo bản ghi OTP trong database
- Push OTP vào Redis nếu muốn lưu tạm thời
- Gửi SMS/Email

### `sessions_view` (Danh sách session)

**Middleware:**
- Parse JWT

**Decorator:**
- `@require_auth` - Yêu cầu đăng nhập
- `@require_roles('admin')` - Nếu chỉ admin xem được, hoặc user chỉ xem session của chính mình

**Service:**
- Lấy danh sách sessions (dùng Redis cache, fallback về DB)

### `change_password_view` (Đổi mật khẩu)

**Middleware:**
- Parse JWT

**Decorator:**
- `@require_auth` - Yêu cầu đăng nhập
- `@validate_request(ChangePasswordRequest)` - Kiểm tra dữ liệu

**Service:**
- Kiểm tra mật khẩu cũ (query DB)
- Cập nhật hash mật khẩu mới
- Thu hồi các session/refresh token khác (tùy chọn)

### `unlock_view` (Mở khóa tài khoản)

**Middleware:**
- Parse JWT cho admin HOẶC public với OTP

**Decorator:**
- `@require_roles('admin')` nếu admin unlock
- Hoặc flow xác minh OTP nếu user tự unlock

---

## Luồng dữ liệu & Pattern caching (Redis)

### JWT parsing (trong middleware)

1. Giải mã token, kiểm tra chữ ký và thời gian hết hạn
2. Lấy `sub` (user_id), `jti` (token ID), `roles` (vai trò)
3. Gán vào `request.ctx.token_claims`
4. Kiểm tra Redis:
   - `GET revocation:{jti}` - Token này có bị thu hồi không?
   - `SISMEMBER revoked_jtis:{user_id}` - User này có token nào bị thu hồi không?
5. Nếu bị thu hồi → trả về `401`

### Session & Refresh tokens

**Khi đăng nhập (login):**
- Lưu metadata session vào database
- Cache vào Redis với key `session:{jti}`, TTL = thời gian hết hạn token
- Lưu `user_sessions:{user_id}` dưới dạng sorted set để list nhanh

**Khi đăng xuất/thu hồi (logout/revoke):**
- Set `revocation:{jti}` → `True` trong Redis với TTL = thời gian còn lại của token
- Middleware sẽ thấy ngay trong O(1)
- Đồng thời đánh dấu revoked trong database

### User cache

Cache thông tin user nhỏ gọn (`user:{id}`) để middleware đọc nhanh:
- VD: ngôn ngữ (locale), trạng thái active
- Nếu không có trong cache → service sẽ load từ database

### Giới hạn (Limits)

Dùng Redis counters để:
- Giới hạn theo IP
- Giới hạn theo user

---

## Tóm tắt - Sự khác biệt chính

### 🔷 Middleware (Bảo vệ toàn bộ)
- ✅ Chạy cho nhiều route
- ✅ Xử lý nhẹ, nhanh
- ✅ Parse token, check cache
- ❌ Không làm việc nặng với DB

### 🔶 Decorator (Kiểm tra riêng)
- ✅ Chạy cho từng route cụ thể
- ✅ Validate dữ liệu, check quyền
- ✅ Có thể query DB nếu cần
- ✅ Ghi audit log, rate limit

### 💾 Redis (Cache)
- Lưu token đã thu hồi
- Lưu session để tra nhanh
- Đếm rate limit
- Cache thông tin user

### 🗄️ Database (Source of truth)
- Lưu session đầy đủ
- Lưu user, roles
- Kiểm tra logic nghiệp vụ
- Backup khi cache miss

## Câu hỏi: Kong (API Gateway) có thể thay thế hoàn toàn Auth Service trong hệ thống Microservices hay không? 

> Trả lời ngắn gọn: Kong có thể làm nhiều thứ liên quan nhưng không thể, và không nên thay thế hoàn toàn một Auth Service!

Dưới đây là phân tích sâu, có hệ thống, nêu rõ **những gì Gateway có thể/không nên là**m, những gì chỉ **Auth Service (hoặc Identity Provider)** mới làm được, 
và pattern triển khai thực tế (hybrid) để cân bằng hiệu năng, bảo mật và khả năng vận hành. 

### 1) Nguyên tắc nền tảng - Why not put everything in Gateway?
* **Gateway tối ưu cho tốc độ, routing, tuyến tính (stateless), policy enforcement đơn giản.**
* **Auth Service/IdP** tối ưu cho **quản lý danh tính, xử lý nghiệp vụ nhạy cảm, lưu trữ trạng thái/credential, phát hành token, audit & compliance.**
* Nếu nhồi nhét Auth vào Gateway bạn sẽ: 
  * Làm Gateway phình to, khó scale, trở thành điểm lỗi duy nhất. 
  * Lặp lại/ đánh đổi tránh nhiệm bảo mật (ví dụ: lưu mật khẩu, xử lý MFA trong proxy là rủi ro).
  * Mất khả năng quản lý lifecycle của người dùng/token. 

### 2) Những chức năng Gateway có thể tốt (nên giữ ở Gateway)
* **Verify self-contained JWT** (signature `exp`, `iss, `aud`) bằng JWKS - local and fast. 
* **Rate Limiting, IP Backlists, WAF rules, TLS termination.**
* **Routing / Load balancing / path-based routing.**
* **Simple role-based checks** dựa trên claim có trong JWT (ví dụ: `role: admin`) - khi rules đơn giản. 
* **Forwarding user info** (inject `X-User-Id`, `X-User-Roles` vào header) cho downstream services. 
* **Caching PDP/OPA** cho policy enforcement (build minimal latency).
* **Reject Invalid tokens** (exp, signature fail) ngay ở edge. 

### 3) Những chức năng Auth Service (IdP) phải xử lý -- Gateway không thể thay thế được
> Đây là danh sách các dịnh vụ chỉ Auth Service nên làm: 

#### A. Quản lý danh tính & thông tin người dùng
* Lưu trữ **credential** (mật khẩu hashed, salt), profile, email, phone. 
* **User lifecycle:** register, verify email, deactive, delete, admin user managemant. 
* **Account linking (social login kết hợp local account), provisioning (SCIM)**
* **Password reset** flows (token email), account lockout. 

#### B. Phát hành token & quản lý lifecycle
* **Issue Access Token (JWT or opaque)** và **Refresh Token.**
* **Ký token** (private key) - private key không bao giờ nằm trên Gateway. 
* **Refresh token rotation** & detecting reuse. 
* **Token revocation** (logout/revoke) - maintain revocation lists / backlist / token state in DB/Redis. 
* **Token intropection endpoint** (RFC7662) cho opaque tokens hoặc when Gateway needs server-side verify. 

#### C. Sensitive Authentication Flows
* **MFA / 2FA** (OTP via SMS/email, WebAuthn)
* **Adaptive/risk-based Auth** (geolocation, device trust, anomaly detection)
* **Consent screen / OAuth2 authorization code flow / PKCE.**
* **SSO / Federation (SAML, OIDC, social identity providers).**
* **OAuth2 client registration**, scopes management.

#### D. Policy & Authorization complex
* **Fine-grained authorization:** ABAC, PBAC, attribute retrieval, context-aware decisions (time-of-day, resource attributes).
* **Permission management / roles / group** (complex mapping beyond simple JWT claims).

#### E. Audit, compliance * security ops
* **Audit logs** for auth events (login, token issue, password reset).
* **Compliance features** (consent records, GDPR support, data erasure).
* **Credential rotation, secret management** (integrate KMS/HSM).
* **Rate-limited sensitive endpoints** (login throttling, lockout rules).

#### F. User-facing UX for auth
* **Login pages**, consent UX, email templates, account recovery UIs — components Gateway không xử lý.

### 4) Khi nào Gateway phải gọi Auth Service

* **Token introspection:** nếu Access Token là opaque (không thể verify cục bộ).
* **Check blacklist / revocation:** nếu Gateway không có cache đủ tin cậy, hoặc blacklist thay đổi liên tục.
* **Refresh token flow / login / logout:** bằng định tuyến đến Auth Service.
* **Complex authZ:** nghị quyết cần attributes mà token không chứa → Gateway gọi PDP / Auth Service để lấy attributes.
* **Adaptive auth/MFA step-up:** Gateway may redirect to Auth Service to perform step-up.

### 5) Kiến trúc hybrid (best practice) — pattern chuẩn
* **Auth Service (IdP):** thực hiện identity provider (OAuth2/OIDC), phát JWT, JWKS endpoint, refresh/revoke, MFA, user mgmt, audit.
* **Gateway:** verify JWT cục bộ (JWKS), enforce simple RBAC, rate limit, routing, caching introspection results, forward requests.
* **If opaque tokens / revocation required:** Gateway calls Auth Service introspection – but cache the response (very short TTL) to avoid áp lực.
* **Policy decisions:** lightweight rules in Gateway; complex policies delegated to PDP (OPA) or AuthZ Service.
* **Key management:** private keys remain with Auth Service/KMS; Gateway consumes JWKS (public keys).
* **Blacklist/Revocation:** store in Redis; Gateway checks Redis (fast) or consult Auth Service if needed.

### 6) Một vài kỹ thuật, chiến lược cụ thể (think harder)
* **Prefer short-lived access tokens** (e.g., 5–15 min) + **refresh tokens** (longer, securely stored) để giảm tác động khi token bị leak.
* **Use JWT (self-contained) for performance**, but **support opaque tokens** if you need instant revocation.
* **Refresh token rotation + reuse detection:** Auth Service must implement; Gateway cannot.
* **Cache JWKS & introspection result** at Gateway with conservative TTL + automatic refresh backoff.
* **Use JTI + blacklist in Redis:** on logout, Auth Service inserts jti into Redis with TTL = remaining time; Gateway checks Redis (fast).
* **Key rotation procedure:** Auth Service publishes new JWKS; Gateway fetches and switches; ensure overlap period.
* **Least privilege claims:** place only minimal claims in JWT; fetch more attributes from Auth Service when necessary.
* **Delegated Authorization:** use OPA or CASBIN as PDP — Gateway queries PDP for complex decisions.
* **Audit trail:** Auth Service must log auth events (sso, login, fail) for security analysis.

### 7) Bảng so sánh nhanh (Gateway vs Auth Service)
| Chức năng                              | Gateway (Kong)   | Auth Service / IdP |
| -------------------------------------- | ---------------- |-----------------|
| Verify JWT signature, exp, aud         | ✅ (local, fast)  | ❌ (not typical) |
| Issue JWT / sign token (private key)   | ❌                | ✅               |
| Store credentials / password hashing   | ❌                | ✅               |
| Refresh token rotation, revoke         | ❌ (can proxy)    | ✅               |
| MFA / adaptive auth                    | ❌                | ✅               |
| OAuth2 authorization code / PKCE       | ❌                | ✅               |
| JWKS endpoint (public keys)            | ❌                | ✅               |
| Token introspection endpoint           | ❌ (can call)     | ✅               |
| User registration / profile mgmt       | ❌                | ✅               |
| Delegated complex ABAC / PDP           | ❌ (can call PDP) | ✅ (may host PDP)|
| Rate-limit / TLS termination / routing | ✅                | ❌               |
