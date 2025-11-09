## 1. Đăng nhập (login)

Luồng này mô tả quá trình người dùng xác thực để truy cập hệ thống.

1. **Người dùng -> Frontend**
* Người dùng nhập username và mật khẩu vào giao diện web/app.

2. **Frontend -> Backend (API Gateway)**
* Frontend gửi một request `POST` đến endpoint `/api/v1/auth/login`.
* **HTTP Request Body:**
    ```json
    {
        "username": "user@example.com",
        "password": "user_password"
    }
    ```
* `email`: (string, required) Địa chỉ email của người dùng.
* `password`: (string, required) Mật khẩu của người dùng.

3. **Sanic App -> View (`LoginView`)**
* Ứng dụng Sanic nhận request và chuyển đến phương thức `post` của `LoginView`.

4.  **Decorator (`@validate_request`)**
* Decorator này kiểm tra tính hợp lệ của dữ liệu trong body request theo schema `LoginSchema`. Nếu không hợp lệ, trả về lỗi 400.

5.  **View -> Service (`AuthService.login_user`)**
* `LoginView` gọi hàm `AuthService.login_user`, truyền vào email và mật khẩu đã xác thực.

6.  **Bên trong `AuthService.login_user`**
*   **Xác thực người dùng:**
    *   Sử dụng `UserRepository` để tìm người dùng theo email trong PostgreSQL.
    *   Kiểm tra mật khẩu đã nhập với mật khẩu đã hash trong cơ sở dữ liệu.
    *   Kiểm tra trạng thái `is_active` của người dùng. Nếu không active hoặc sai mật khẩu, trả về lỗi 401 Unauthorized.
*   **Tạo phiên làm việc (session):**
    *   Nếu xác thực thành công, tạo một `UserSession` mới trong PostgreSQL.
    *   Tạo `access_token` và `refresh_token` bằng `jwt_utils`.
    *   Lưu `refresh_token` vào `UserSession` trong PostgreSQL.

7.  **Hoàn tất Request**
    *   `LoginView` trả về một response `200 OK` cho frontend.
    *   **HTTP Response Body (Success):**
        ```json
        {
            "message": "Login successful",
            "data": {
                "access_token": "eyJhbGciOiJIUzI1Ni...",
                "refresh_token": "eyJhbGciOiJIUzI1Ni...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }
        ```
        *   `access_token`: (string) Token truy cập được sử dụng để xác thực các request tiếp theo.
        *   `refresh_token`: (string) Token được sử dụng để lấy `access_token` mới khi `access_token` hết hạn.
        *   `token_type`: (string) Loại token, thường là "bearer".
        *   `expires_in`: (integer) Thời gian hiệu lực của `access_token` tính bằng giây.
    *   **HTTP Response Body (Error - Example 401 Unauthorized):**
        ```json
        {
            "message": "Invalid credentials",
            "status_code": 401
        }
        ```

## 2. Đăng ký tài khoản (register)
Luồng này có thể được chia thành 2 giai đoạn chính:
* **Giai đoạn 1:** Yêu cầu Đăng ký và Gửi OTP
* **Giai đoạn 2:** Xác thực OTP và Kích hoạt Tài khoản


### Giai đoạn 1: Yêu cầu Đăng ký và Gửi OTP

Đây là những gì xảy ra khi người dùng điền vào form đăng ký và nhấn nút "Submit".

1. Người dùng -> Frontend
* Người dùng nhập email, mật khẩu và các thông tin khác vào giao diện web/app.

2. Frontend -> Backend (API Gateway)
* Frontend gửi một request POST đến endpoint /api/v1/auth/register.
* **HTTP Request Body:**
     ```json
     {
         "username": "yourusername",
         "email": "user@example.com",
         "password": "strong_password",
         "first_name": "John",
         "last_name": "Doe",
         "gender": "male",
         "age": "22", 
         "height": "175cm",
         "weight": "67 kg",
         "ward": "yourward",
         "district": "yourdistrict",
         "city": "yourcity",
         "province": "province"
     }
     ```
  * `username`: (string, required) - Tên đăng nhập của người dùng
  * `email`: (string, required) - Địa chỉ email của người dùng.
  * `password`: (string, required) - Mật khẩu của người dùng (sẽ được hash).
  * `first_name`: (string, required) - Tên của người dùng.
  * `last_name`: (string, required) - Họ của người dùng.
  * `gender`: "male" (enum(Male, Female, Other), required)
  * `age`: "22", (int, required) - Tuổi tác
  * `height`: "175 cm", (string, required) - Chiều cao
  * `weight`: "67 kg" (string, required) - Cân nặng
  * `ward`: "yourward", (string, required) - Phường, xã
  * `district`: "yourdistrict" (string, required) - Quận
  * `city`: "yourcity" (string, required) - Thành phố
  * `province`: "province" (string, required) - Tỉnh thành

3. Sanic App -> View (`RegisterView`)
* Ứng dụng Sanic của bạn nhận request và, dựa trên routing, chuyển nó đến phương thức post của RegisterView.

4. Decorator (`@validate_request`)
* Decorator này chạy trước cả view. Nó kiểm tra xem dữ liệu trong body có hợp lệ theo schema RegisterRequest không. Nếu không, nó sẽ tự động trả về lỗi 400. Nếu hợp lệ, nó sẽ tiếp tục.

5. View -> Service (`AuthService.register_user`)
* RegisterView gọi hàm AuthService.register_user, truyền vào dữ liệu đã được xác thực.

6. Bên trong `AuthService.register_user`
* Kiểm tra User: Dùng UserRepository để truy vấn vào database PostgreSQL xem có tài khoản nào với email user@gmail.com đã tồn tại và is_active=True không. Nếu có, trả về lỗi 409 Conflict.
* Tạo User (nếu cần): Nếu chưa có user, nó sẽ hash mật khẩu và INSERT một bản ghi mới vào bảng users trong PostgreSQL với is_active=False.
* Gọi `request_otp`: Sau khi đảm bảo có một user (chưa active) trong DB, nó gọi một hàm khác là AuthService.request_otp.

7. Bên trong `AuthService.request_otp`
* Ủy quyền cho `OTPService`: Hàm này gọi otp_service.generate_and_store_otp("user@gmail.com", "REGISTER").
* Logic của `OTPService`:
    1. Tạo một mã số ngẫu nhiên, ví dụ: 357819.
    2. Hash mã số này.
    3. Tạo một key có cấu trúc: otp:register:user@gmail.com.
    4. Thực hiện lệnh SETEX trong Redis: SETEX otp:register:user@gmail.com 300 <hashed_code>. Lệnh này lưu mã OTP đã hash vào Redis và tự động xóa nó sau 300 giây (5 phút).
    5. Trả về mã OTP dạng plain text (357819) cho AuthService.
* Ủy quyền cho `EmailService`: AuthService nhận được mã 357819 và gọi email_service.send_otp("user@gmail.com", "357819", "REGISTER").

8. Bên trong `EmailService.send_otp`
* Tạo nội dung Email: Dựa vào action REGISTER, nó tạo ra tiêu đề ("Welcome! Your Verification Code") và nội dung HTML cho email.
* Gửi Email thật:
    1. Kết nối đến máy chủ SMTP của Google (smtp.gmail.com:587).
    2. Đăng nhập bằng EMAIL_SENDER và Mật khẩu ứng dụng (EMAIL_PASSWORD) đã được cấu hình.
    3. Gửi email chứa mã OTP đến địa chỉ user@gmail.com.

9. Hoàn tất Request
* RegisterView nhận lại quyền kiểm soát và trả về một response 201 Created cho frontend, báo rằng "Đăng ký thành công, vui lòng kiểm tra email để lấy mã OTP."
* **HTTP Response Body (Success):**
     ```json
     {
         "message": "Registration successful, please check your email for OTP."
     }
     ```
   *   **HTTP Response Body (Error - Example 409 Conflict):**
       ```json
       {
           "message": "User with this email already exists and is active.",
           "status_code": 409
       }
       ```

   Kết quả của Giai đoạn 1:
* Trong PostgreSQL: có một user mới với is_active=False.
* Trong Redis: có một key otp:register:user@gmail.com chứa mã OTP đã hash, sẽ tự hủy sau 5 phút.
* Trong Hộp thư của người dùng: có một email mới chứa mã OTP 357819.


### Giai đoạn 2: Xác thực OTP và Kích hoạt Tài khoản

1. Người dùng -> Frontend
* Người dùng mở email, thấy mã 357819, quay lại trang web và nhập mã này vào ô xác thực.

2. Frontend -> Backend
* Frontend gửi một request POST đến endpoint /api/v1/auth/otp/verify với body là {"email": "user@gmail.com", "otp_code": "357819"}.
* **HTTP Request Body:**
     ```json
     {
         "email": "user@example.com",
         "otp_code": "123456"
     }
     ```
     *   `email`: (string, required) Địa chỉ email của người dùng đã đăng ký.
     *   `otp_code`: (string, required) Mã OTP nhận được qua email.

3. Sanic App -> View (`OTPVerifyView`)
* Request được chuyển đến phương thức post của OTPVerifyView.

4. View -> Service (`AuthService.verify_registration_otp`)
* View gọi hàm AuthService.verify_registration_otp.

5. Bên trong `AuthService.verify_registration_otp`
* Ủy quyền cho `OTPService`: Hàm này gọi otp_service.verify_otp("user@gmail.com", "REGISTER", "357819").
* Logic của `OTPService`:
    1. Tạo key otp:register:user@gmail.com.
    2. Thực hiện lệnh GET trong Redis để lấy mã đã hash.
    3. Nếu key không tồn tại (đã hết hạn), trả về False.
    4. Nếu key tồn tại, so sánh hash của mã 357819 với mã hash lấy từ Redis.
    5. Nếu khớp, thực hiện lệnh DEL trong Redis để xóa key ngay lập tức và trả về True.
    6. Nếu không khớp, trả về False.
* Kiểm tra kết quả: AuthService nhận được True. Nếu là False, nó sẽ trả về lỗi 401 Unauthorized.
* Kích hoạt User: Vì kết quả là True, AuthService dùng UserRepository để UPDATE bản ghi của user@gmail.com trong PostgreSQL, set is_active=True.

6. Hoàn tất Request
* OTPVerifyView trả về response 200 OK cho frontend với thông báo "Tài khoản đã được kích hoạt thành công."
* **HTTP Response Body (Success):**
     ```json
     {
         "message": "Account activated successfully."
     }
     ```
   *   **HTTP Response Body (Error - Example 401 Unauthorized):**
       ```json
       {
           "message": "Invalid or expired OTP.",
           "status_code": 401
       }
       ```

   Kết quả cuối cùng:
* Tài khoản của người dùng trong PostgreSQL giờ đã có is_active=True.
* Key OTP trong Redis đã bị xóa.
* Người dùng bây giờ có thể đăng nhập vào hệ thống.
