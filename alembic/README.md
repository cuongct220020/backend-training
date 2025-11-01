# Hướng dẫn sử dụng Alembic

Tài liệu này là kim chỉ nam cho việc quản lý và cập nhật schema cơ sở dữ liệu của dự án.

> **Cảnh báo:** Mọi thay đổi vào database **BẮT BUỘC** phải được thực hiện thông qua Alembic. Không bao giờ sửa schema trực tiếp bằng các công cụ như pgAdmin hay DBeaver.

## 1. Thiết lập ban đầu

Nếu bạn là thành viên mới hoặc cần thiết lập database từ đầu:

1.  **Cấu hình kết nối:** Đảm bảo file `.env` ở thư mục gốc đã có đủ thông tin `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`.
2.  **Tạo và áp dụng tất cả migration:** Chạy lệnh sau để tạo tất cả các bảng và cấu trúc theo lịch sử đã có.
    ```bash
    alembic upgrade head
    ```

## 2. Quy trình chuẩn khi thay đổi Schema

Khi bạn cần thay đổi cấu trúc database (thêm bảng, thêm cột, etc.), hãy tuân thủ nghiêm ngặt quy trình sau:

1.  **Sửa Model:** Thay đổi các class model trong `app/models/`.
2.  **Tạo Script Migration:** Chạy lệnh sau để Alembic tự động phát hiện thay đổi.
    ```bash
    alembic revision --autogenerate -m "Mô tả ngắn gọn về thay đổi"
    ```
    > **Ví dụ:** `alembic revision --autogenerate -m "Add phone_number to User model"`
3.  **KIỂM TRA SCRIPT (QUAN TRỌNG NHẤT):** Mở file migration vừa tạo trong `alembic/versions/` và đọc kỹ.
    *   `autogenerate` không hoàn hảo. Nó có thể bỏ sót thay đổi phức tạp như đổi tên bảng/cột, thay đổi `server_default`, hoặc các ràng buộc `CHECK`.
    *   **Luôn tự hỏi:** "Hàm `downgrade()` có hoạt động đúng không? Nó có thể hoàn tác thay đổi một cách an toàn không?"
4.  **Áp dụng Migration:** Sau khi đã chắc chắn script đúng, áp dụng nó vào database của bạn.
    ```bash
    alembic upgrade head
    ```
5.  **Commit:** Commit cả file model đã sửa và file migration mới vào Git.

## 3. Lệnh thường dùng

<table>
  <thead>
    <tr>
      <th>Lệnh</th>
      <th>Chức năng</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>alembic history</code></td>
      <td>Xem toàn bộ lịch sử và vị trí hiện tại</td>
    </tr>
    <tr>
      <td><code>alembic current</code></td>
      <td>Hiển thị phiên bản hiện tại</td>
    </tr>
    <tr>
      <td><code>alembic upgrade head</code></td>
      <td>Nâng cấp lên phiên bản mới nhất</td>
    </tr>
    <tr>
      <td><code>alembic upgrade +1</code></td>
      <td>Nâng cấp lên 1 phiên bản</td>
    </tr>
    <tr>
      <td><code>alembic downgrade -1</code></td>
      <td>Rollback về 1 phiên bản trước</td>
    </tr>
    <tr>
      <td><code>alembic downgrade base</code></td>
      <td>Xóa tất cả bảng (về trạng thái trống)</td>
    </tr>
    <tr>
      <td><code>alembic branches</code></td>
      <td>Hiển thị các nhánh trong lịch sử</td>
    </tr>
    <tr>
      <td><code>alembic merge &lt;rev1&gt; &lt;rev2&gt;</code></td>
      <td>Hợp nhất các nhánh</td>
    </tr>
  </tbody>
</table>

## 4. Kỹ thuật nâng cao & Best Practices

### Đặt tên ràng buộc (Naming Convention)

> Luôn sử dụng `naming_convention` trong `MetaData` (đã cấu hình trong `app/models/__init__.py`). Điều này giúp Alembic không bị "bối rối" bởi các tên ràng buộc (constraint) do CSDL tự sinh ra, đảm bảo `autogenerate` hoạt động ổn định.

### Data Migration (Di trú Dữ liệu)

Khi cần chèn/cập nhật dữ liệu như một phần của migration.

**Ví dụ: Thêm cột `status` `NOT NULL` vào bảng `users` đã có dữ liệu.**

Cách tiếp cận an toàn là chia làm 3 bước trong cùng một migration script:
```python
def upgrade() -> None:
    # Bước 1: Thêm cột mới nhưng cho phép NULL
    op.add_column('users', sa.Column('status', sa.String(50), nullable=True))

    # Bước 2: Cập nhật giá trị mặc định cho tất cả các dòng hiện có
    op.execute("UPDATE users SET status = 'active' WHERE status IS NULL")

    # Bước 3: Thay đổi cột thành NOT NULL
    op.alter_column('users', 'status', nullable=False)
```

### Làm việc nhóm & Xử lý xung đột

Khi nhiều người cùng tạo migration trên các nhánh Git khác nhau, lịch sử Alembic có thể bị phân nhánh.

1.  **Phòng ngừa:** Trước khi tạo migration mới, hãy luôn `git pull` hoặc `git rebase` nhánh chính để cập nhật code mới nhất.
2.  **Phát hiện:** Sau khi `git merge`, chạy `alembic branches`. Nếu thấy nhiều `head`, nghĩa là lịch sử đã bị phân nhánh.
3.  **Hợp nhất (Merge):** Chạy lệnh `merge` để tạo một file migration hợp nhất.
    ```bash
    alembic merge -m "Merge feature-A and feature-B branches" <rev_A> <rev_B>
    ```
4.  **Kiểm tra và Commit:** Kiểm tra lại file merge và commit nó. Lịch sử sẽ trở lại tuyến tính.

## 5. Kết luận

Alembic không chỉ là công cụ mà là phương pháp luận chuyên nghiệp để quản lý sự tiến hóa của database. Các nguyên tắc cốt lõi: Schema as Code, Model là nguồn chân lý, đặt tên ràng buộc rõ ràng, và lập kế hoạch cẩn thận cho migration phức tạp.

**Khuyến nghị:**
- Luôn tạo migration sau khi thay đổi model
- Xem xét kỹ mọi script được tạo tự động
- Tích hợp migrations vào quy trình CI/CD
- Sử dụng `alembic check` trong CI để đảm bảo đồng bộ

Làm chủ Alembic là bước quan trọng trên con đường trở thành kỹ sư backend cấp cao.

