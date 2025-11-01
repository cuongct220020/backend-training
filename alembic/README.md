# Hướng dẫn Sử dụng Alembic

## Nguyên tắc Cốt lõi

- **Model là nguồn chân lý duy nhất** - Mọi thay đổi database phải bắt đầu từ việc sửa model SQLAlchemy (`app/models/`). Luồng làm việc: **Model → Migration Script → Database**.
- **Không sửa database trực tiếp** - Thay đổi schema qua pgAdmin/DBeaver sẽ làm Alembic mất kiểm soát và gây lỗi.
- **Migration là lịch sử** - Mỗi file trong `versions/` ghi lại một thay đổi, cho phép tiến/lùi trong lịch sử một cách an toàn.

## Quy trình Chuẩn

### 1. Sửa Model
Thực hiện các thay đổi cần thiết trong các file model (VD: `app/models/user.py`): 
- Thêm một class model mới. 
- Thêm cột `Column` mới vào model hiện có. 
- Thay đổi kiểu dữ liệu (vd: `nullable`, hoặc thêm `index`)

### 2. Tạo Migration
Mở terminal tại thư mục gốc của dự án và chạy lệnh sau:
```bash
alembic revision --autogenerate -m "Mô tả ngắn gọn"
```
- `--autogenerate`: Tự động tạo script dựa trên thay đổi của model
- `-m`: Thông điệp rõ ràng (VD: "Add phone_number to User", "Create products table")

### 3. Kiểm tra Script
Mở file migration vừa được tạo trong `alembic/versions/`, **Luôn kiểm tra lại** file vừa tạo trong `alembic/versions/`:
- `autogenerate` không hoàn hảo. Nó có thể bỏ sót các thay đổi phức tạp như đổi tên bảng/cột, thay đổi `server_default`, hoặc các ràng buộc `CHECK`.
- Nếu bạn thêm một cột `NOT NULL` vào bảng đã có dữ liệu, bạn cần chỉnh sửa script để xử lý dữ liệu cũ trước (xem phần Kỹ thuật Nâng cao).
- Đây là cơ hội cuối cùng để đảm bảo script sẽ chạy đúng như mong đợi.

### 4. Áp dụng Migration
Sau khi đã hài lòng với kịch bản, hãy áp dụng nó vào database:
```bash
alembic upgrade head
```

## Lệnh Thường dùng
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

## Lưu ý Quan trọng

### Đặt tên Ràng buộc
Luôn sử dụng `naming_convention` trong `MetaData` để `autogenerate` hoạt động ổn định và migration di động được giữa các DB khác nhau (đã cấu hình trong `app/models/Base.py`).

### Data Migration
Khi cần chèn/cập nhật dữ liệu trong migration:
- Dùng `op.bulk_insert()` để seed dữ liệu
- Dùng `op.execute("UPDATE...")` để cập nhật

**Ví dụ** thêm cột `status` `NOT NULL` vào bảng có dữ liệu:
1. Tạo cột `nullable=True`
2. `op.execute("UPDATE users SET status = 'active'")`
3. `op.alter_column('users', 'status', nullable=False)`

### Làm việc Nhóm
Khi nhiều người tạo migration trên các nhánh khác nhau:
1. Sau `git merge`, chạy `alembic branches` - nếu thấy nhiều `head` nghĩa là bị phân nhánh
2. Chạy `alembic merge -m "Merge branches" <rev_A> <rev_B>`
3. Commit file merge, lịch sử trở lại tuyến tính
