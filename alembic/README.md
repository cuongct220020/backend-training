Chắc chắn rồi. Đây là nội dung hoàn chỉnh cho tệp `README.md` mà bạn có thể sao chép trực tiếp.

# Hướng dẫn Sử dụng Alembic cho Dự án

Chào mừng bạn đến với thư mục quản lý migration của dự án\! Thư mục này chứa mọi thứ liên quan đến Alembic, công cụ chúng ta sử dụng để quản lý sự tiến hóa của schema database một cách an toàn và có hệ thống. Việc tuân thủ các quy tắc dưới đây là rất quan trọng để đảm bảo tính nhất quán và ổn định cho database của chúng ta.

## Triết lý Cốt lõi: "Schema as Code"

1.  **Model là Nguồn Chân lý Duy nhất (Single Source of Truth)**: Mọi thay đổi về cấu trúc database (thêm bảng, sửa cột,...) **PHẢI** bắt đầu bằng việc chỉnh sửa các file model trong SQLAlchemy (tại `app/models/`).
2.  **Không bao giờ sửa Database trực tiếp**: Việc thay đổi schema database bằng tay (qua pgAdmin, DBeaver,...) sẽ làm cho Alembic không thể theo dõi và gây ra lỗi. Luồng công việc luôn là: **Model -\> Migration Script -\> Database**.
3.  **Migration là Lịch sử**: Mỗi file trong thư mục `versions/` là một bản ghi lịch sử về một sự thay đổi. Chúng ta có thể tiến hoặc lùi trong lịch sử này một cách an toàn.

-----

## Quy trình Làm việc Tiêu chuẩn (Hàng ngày)

Đây là các bước bạn sẽ thực hiện thường xuyên nhất khi cần thay đổi cấu trúc database.

#### Bước 1: Sửa đổi Model SQLAlchemy

Thực hiện các thay đổi cần thiết trong các file model của bạn (ví dụ: `app/models/user.py`).

  * Thêm một class model mới.
  * Thêm một `Column` mới vào một model hiện có.
  * Thay đổi kiểu dữ liệu, `nullable`, hoặc thêm `index`.

#### Bước 2: Tự động Tạo Kịch bản Migration

Mở terminal tại thư mục gốc của dự án và chạy lệnh sau:bash
alembic revision --autogenerate -m "Mô tả ngắn gọn về thay đổi"

````
  * **`--autogenerate`**: Alembic sẽ kết nối tới database, so sánh trạng thái hiện tại với các model của bạn và tạo ra một file script trong `alembic/versions/` chứa các thay đổi cần thiết.
  * **`-m "..."`**: Cung cấp một thông điệp rõ ràng, súc tích. Ví dụ: `"Add phone_number to User model"` hoặc `"Create products table"`.

#### Bước 3: **(QUAN TRỌNG)** Xem xét và Chỉnh sửa Kịch bản

Mở file migration vừa được tạo trong `alembic/versions/`. **Luôn luôn kiểm tra lại nội dung!**

  * `autogenerate` không hoàn hảo. Nó có thể bỏ sót các thay đổi phức tạp như đổi tên bảng/cột, thay đổi `server_default`, hoặc các ràng buộc `CHECK`.
  * Nếu bạn thêm một cột `NOT NULL` vào bảng đã có dữ liệu, bạn cần chỉnh sửa script để xử lý dữ liệu cũ trước (xem phần Kỹ thuật Nâng cao).
  * Đây là cơ hội cuối cùng để đảm bảo script sẽ chạy đúng như mong đợi.

#### Bước 4: Áp dụng Migration

Sau khi đã hài lòng với kịch bản, hãy áp dụng nó vào database:

```bash
alembic upgrade head
````

  * **`head`**: Là một con trỏ chỉ đến phiên bản mới nhất. Lệnh này sẽ áp dụng tất cả các migration chưa được thực thi để đưa database lên trạng thái mới nhất.

-----

## Các Lệnh Thường dùng (Cheatsheet)

| Lệnh | Chức năng |
| :--- | :--- |
| `alembic history` | Xem toàn bộ lịch sử migration và vị trí hiện tại (`(head)`) |
| `alembic current` | Chỉ hiển thị phiên bản hiện tại của database. |
| `alembic upgrade head` | Nâng cấp database lên phiên bản mới nhất. |
| `alembic upgrade +1` | Nâng cấp lên 1 phiên bản so với hiện tại. |
| `alembic downgrade -1` | Quay về 1 phiên bản trước đó. Hữu ích khi cần rollback nhanh. |
| `alembic downgrade base` | **(CẨN THẬN)** Xóa tất cả các bảng, đưa database về trạng thái trống. |
| `alembic branches` | Hiển thị các nhánh trong lịch sử (khi có nhiều người cùng tạo migration). |
| `alembic merge <rev1> <rev2>` | Tạo một migration hợp nhất để giải quyết các nhánh. |

-----

## Thực hành Tốt nhất & Các Tình huống Đặc biệt

#### 1\. Luôn đặt tên cho Ràng buộc (Constraints)

Để `autogenerate` hoạt động ổn định và các migration có thể di động giữa các hệ quản trị DB khác nhau (ví dụ: PostgreSQL và SQLite cho testing), hãy sử dụng `naming_convention` trong `MetaData` của SQLAlchemy. Điều này đã được cấu hình trong `app/models/Base.py` (hoặc nơi bạn định nghĩa `declarative_base`).

#### 2\. Data Migrations (Di chuyển Dữ liệu)

Khi bạn cần chèn dữ liệu ban đầu (seeding) hoặc cập nhật dữ liệu hiện có như một phần của migration.

  * Sử dụng `op.bulk_insert()` để chèn dữ liệu ban đầu.
  * Sử dụng `op.execute("UPDATE...")` để cập nhật dữ liệu.
  * **Ví dụ**: Thêm cột `status` `NOT NULL` vào bảng `users` đã có dữ liệu:
    1.  Tạo cột dưới dạng `nullable=True`.
    2.  Chạy `op.execute("UPDATE users SET status = 'active'")` để điền giá trị mặc định.
    3.  Chạy `op.alter_column('users', 'status', nullable=False)`.

#### 3\. Làm việc Nhóm (Branching & Merging)

Khi bạn và một đồng nghiệp cùng tạo migration trên các nhánh Git khác nhau, lịch sử Alembic sẽ bị phân nhánh.

1.  Sau khi `git merge`, hãy chạy `alembic branches`. Nếu bạn thấy có nhiều `head`, nghĩa là lịch sử đã bị phân nhánh.
2.  Chạy `alembic merge -m "Merge feature branches" <revision_A> <revision_B>` để tạo một điểm hợp nhất.
3.  Commit file migration hợp nhất này. Bây giờ lịch sử đã trở lại tuyến tính.

<!-- end list -->

```
```