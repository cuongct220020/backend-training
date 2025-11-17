# SQLAlchemy 2.0: Phát triển Backend bất đồng bộ với Pydantic và Alembic

[Phần I. Giải mã triết lý và kiến trúc của SQLAlchemy](#phần-i-giải-mã-triết-lý-và-kiến-trúc-của-sqlalchemy)
* [1.1. Giới thiệu về "Database Toolkit"](#11-giới-thiệu-về-database-toolkit)
* [1.2. Trụ cột 1: SQLAlchemy Core - Người kiểm soát SQL](#12-trụ-cột-1-sqlalchemy-core---người-kiểm-soát-sql)
* [1.3. Trụ cột 2: SQLAlchemy ORM - Người quản lý đối tượng](#13-trụ-cột-2-sqlalchemy-orm---người-quản-lý-đối-tượng)
* [1.4. Bảng 1: So sánh kiến trúc (Core vs. ORM)](#14-bảng-1-so-sánh-kiến-trúc-core-vs-orm)
* [1.5. Phân tích chuyên sâu: Sự "hợp nhất" (Unification) trong SQLAlchemy 2.0](#15-phân-tích-chuyên-sâu-sự-hợp-nhất-unification-trong-sqlalchemy-20)

[Phần II. Cú pháp ORM hiện đại (Phong cách 2.0) - Khai báo Models](#phần-ii-cú-pháp-orm-hiện-đại-phong-cách-20---khai-báo-models)
* [2.1 Sự Dịch chuyển sang Phong cách 2.0: Lý do và Lợi ích](#21-sự-dịch-chuyển-sang-phong-cách-20-lý-do-và-lợi-ích)
* [2.2 Khai báo Cơ bản (Declarative Mapping)](#22-khai-báo-cơ-bản-declarative-mapping)
* [2.3. Cú pháp cột mới: `Mapped` và `mapped_column()`](#23-cú-pháp-cột-mới-mapped-và-mapped_column)
* [2.4. Bảng 2: So sánh cú pháp khai báo Model (1.x vs. 2.0)](#24-bảng-2-so-sánh-cú-pháp-khai-báo-model-1x-vs-20)

[Phần III. Quản lý Kết nối và Trạng thái (Engine và Session)](#phần-iii-quản-lý-kết-nối-và-trạng-thái-engine-và-session)
* [3.1. Engine: Cổng kết nối đến Cơ sở dữ liệu](#31-engine-cổng-kết-nối-đến-cơ-sở-dữ-liệu)
* [3.2. Session: Giao diện chính của ORM](#32-session-giao-diện-chính-của-orm)
* [3.3. Phân tích chuyên sâu cạm bẫy của `AsyncSession` và `expire_on_commit`](#33-phân-tích-chuyên-sâu-cạm-bẫy-của-asyncsession-và-expire_on_commit)

[Phần IV. Thao tác dữ liệu (CRUD) với ORM 2.0](#phần-iv-thao-tác-dữ-liệu-crud-với-orm-20)
* [4.1. Tạo (Create)](#41-tạo-create)
* [4.2. Đọc (Read) - Sự thay đổi lớn nhất](#42-đọc-read---sự-thay-đổi-lớn-nhất)
* [4.3. Cập nhật (Update)](#43-cập-nhật-update)
* [4.4. Xoá (Delete)](#44-xoá-delete)
* [4.5. Hoàn tất giao diện (Commit, Rollback, Refresh)](#45-hoàn-tất-giao-diện-commit-rollback-refresh)

[Phần V. Mô hình hoá các mối quan hệ dữ liệu (Relationships)](#phần-v-mô-hình-hoá-các-mối-quan-hệ-dữ-liệu-relationships)
* [5.1. Nền tảng `ForeignKey` và `relationship()`](#51-nền-tảng-foreignkey-và-relationship)
* [5.2 `back_populates` vs. `backref`](#52-back_populates-vs-backref)
* [5.3. Triển khai các Mẫu Quan hệ (với Cú pháp 2.0)](#53-triển-khai-các-mẫu-quan-hệ-với-cú-pháp-20)
  * [5.3.1 One-to-Many (Một-nhiều)](#531-one-to-many-một-nhiều)
  * [5.3.2. One-to-One (một-một)](#532-one-to-one-một-một)
  * [5.3.3 Many-to-Many (Nhiều-nhiều)](#533-many-to-many-nhiều-nhiều)

[Phần VI. Kỹ thuật truy vấn nâng cao và tối ưu hiệu suất](#phần-vi-kỹ-thuật-truy-vấn-nâng-cao-và-tối-ưu-hiệu-suất)
* [6.1 Lọc động (Dynamic Filtering)](#61-lọc-động-dynamic-filtering)
* [6.2. Sắp xếp động (Dynamic Sorting)](#62-sắp-xếp-động-dynamic-sorting)
* [6.3. Hàm tổng hợp (Aggregates) và Nhóm (Grouping)](#63-hàm-tổng-hợp-aggregates-và-nhóm-grouping)
* [6.4. Giải quyết Vấn đề N+1 (N+1 Problem) bằng Eager Loading](#64-giải-quyết-vấn-đề-n1-n1-problem-bằng-eager-loading)

[Phần VII: Tích hợp SQLAlchemy và Pydantic (Hệ sinh thái Sanic)](#phần-vii-tích-hợp-sqlalchemy-và-pydantic-hệ-sinh-thái-sanic)
* [7.1. Tách biệt vai trò: Models(SQLAlchemy) vs. Schemas(Pydantic)](#71-tách-biệt-vai-trò-modelssqlalchemy-vs-schemaspydantic)
* [7.2 Cấu hình "Kỳ diệu": from_attributes = True](#72-cấu-hình-kỳ-diệu-from_attributes--true)

[Phần VIII. Quản lý Vòng đời Cơ sở dữ liệu với Alembic](#phần-viii-quản-lý-vòng-đời-cơ-sở-dữ-liệu-với-alembic)
* [8.1 Tại sao cần Alembic?](#81-tại-sao-cần-alembic)
* [8.2 Thiết lập Môi trường](#82-thiết-lập-môi-trường)
* [8.3 Cấu hình env.py cho Autogenerate](#83-cấu-hình-envpy-cho-autogenerate)
* [8.4 Quy trình Di trú (Migration Workflow) Hàng ngày](#84-quy-trình-di-trú-migration-workflow-hàng-ngày)

[Phần IX. Kết luận và các phương pháp tốt nhất (best practices)](#phần-ix-kết-luận-và-các-phương-pháp-tốt-nhất-best-practices)


## Phần I. Giải mã triết lý và kiến trúc của SQLAlchemy

SQLAlchemy là một bộ công cụ cơ sở dữ liệu (database toolkit) toàn diện cho Python. 
Sự nhầm lẫn thường gặp khi tiếp cận SQLAlchemy bắt nguồn từ việc không phân biệt rõ ràng hai tầng kiến trúc chính của nó: **Core** và **ORM**.
Hiểu rõ sự tách biệt và mối quan hệ giữa hai thành phần này là nền tảng để làm chủ thư viện

### 1.1. Giới thiệu về "Database Toolkit"
Không giống như nhiều thư viện khác chỉ tập trung vào một mục đích, SQLAlchemy được thiết kế như một "bộ công cụ". 
Nó cung cấp các công cụ để quản lý kết nối, tương tác với các truy vấn và kết quả, cũng như xây dựng các câu lệnh SQL
một cách có lập trình. Trên nền tảng này, nó cung cấp một lớp Object Relation Mapper (ORM) tuỳ chọn. 

### 1.2. Trụ cột 1: SQLAlchemy Core - Người kiểm soát SQL

SQLAlchemy Core là một API cấp thấp, linh hoạt, cho phép nhà phát triển tương tác trực tiếp với CSDL bằng các biểu thức SQL. 
Nó không trừu tượng hóa hoàn toàn CSDL; thay vào đó, nó cung cấp các công cụ Pythonic để xây dựng các câu lệnh SQL.   

* **Mô hình tư duy:** Core sử dụng mô hình tư duy "schema-centric" (tập trung vào lược đồ). Nhà phát triển suy nghĩ về các đối 
tượng `Table`, `Column`, và các câu lệnh như `select()`, `insert()`.
* **Mô hình lập trình:** Core mang tính "command-oriented" (hướng lệnh). Nhà phát triển xây dựng một câu lệnh và thực thi nó. 
Trạng thái không được quản lý tự động. 
* **Trường hợp sử dụng:** Core lý tưởng cho các tình huống đòi hỏi kiểm soát chi tiết, viết các truy vấn SQL phức tạp, hoặc tối ưu hiệu suất
ở mức độ cao. Nó yêu cầu kiến thức về SQL. 
* **Quản lý giao dịch:** Nhà phát triển phải tự quản lý các giao dịch và connection pooling một cách thủ công. 

### 1.3. Trụ cột 2: SQLAlchemy ORM - Người quản lý đối tượng
SQL Alchemy ORM được xây dựng trên Core, cung cấp một API cấp cao để ánh xạ các lớp Python (classes) sang các bảng CSDL (tables). 
Điều này cho phép nhà phát triển tương tác với CSDL bằng cách sử dụng các đối tượng Python thay vì các câu lệnh SQL.
* **Mô hình tư duy:** ORM sử dụng mô hình tư duy "domain-centric" (tập trung vào miền nghiệp vụ). 
Nhà phát triển suy nghĩ về các lớp nghiệp vụ như `User`, `Address`
* **Mô hình lập trình:** ORM mang tính "state-oriented" (hướng trạng thái). Nó sử dụng một mẫu thiết kế cốt lõi gọi là "Unit of Work" (đơn vị công việc)
thông qua một đối tượng `Session`. `Session` theo dõi mọi thay đổi đối với các đối tượng (thêm, sửa, xoá) và tự động chuyển các thay đổi này thành các câu lệnh SQL
khi được yêu cầu (ví dụ: khi gọi `commit()`). 
* **Trường hợp sử dụng:** ORM lý tưởng cho các hoạt động CRUD (Create, Read, Update, Delete) và phát triển ứng dụng nhanh, nơi trừu tượng hoá Pythonic được ưu tiên. 
* **Quản lý giao dịch:** ORM cung cấp hỗ trợ tích hợp sẵn cho quản lý giao dịch và connection pooling, giúp đơn giản hoá việc phát triển. 

### 1.4. Bảng 1: So sánh kiến trúc (Core vs. ORM)
Để giải quyết sự "chưa rõ" của các nhà phát triển, bảng sau đây tóm tắt các khác biệt triết lý chính:

<table>
  <thead>
    <tr>
      <th>Khía cạnh</th>
      <th>SQLAlchemy Core</th>
      <th>SQLAlchemy ORM</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Cấp độ trừu tượng</td>
      <td>Thấp (Low-level). Gần với SQL.</td>
      <td>Cao (High-level). Trừu tượng hóa SQL.</td>
    </tr>
    <tr>
      <td>Mô hình tư duy</td>
      <td>"Schema-centric" (Hướng lược đồ).</td>
      <td>"Domain-centric" (Hướng nghiệp vụ).</td>
    </tr>
    <tr>
      <td>Mô hình lập trình</td>
      <td>"Command-oriented" (Hướng lệnh).</td>
      <td>"State-oriented" (Hướng trạng thái).</td>
    </tr>
    <tr>
      <td>Đối tượng tương tác chính</td>
      <td><code>Table</code>, <code>Column</code>, <code>select()</code></td>
      <td><code>User</code> (class), <code>Session</code></td>
    </tr>
    <tr>
      <td>Trường hợp sử dụng</td>
      <td>Truy vấn phức tạp, tối ưu hóa hiệu suất.</td>
      <td>CRUD, phát triển ứng dụng nhanh.</td>
    </tr>
    <tr>
      <td>Quản lý giao dịch</td>
      <td>Thủ công (Developers handle manually).</td>
      <td>Tích hợp sẵn (Built-in support).</td>
    </tr>
  </tbody>
</table>


### 1.5. Phân tích chuyên sâu: Sự "hợp nhất" (Unification) trong SQLAlchemy 2.0

Sự nhầm lẫn khi xem các đoạn mã thường bắt nguồn từ sự thay đổi triết lý lớn trong SQLAlchemy 2.0.

Trong các phiên bản 1.x, ORM và Core có hai cách truy vấn gần như hoàn toàn riêng biệt. ORM sử dụng một giao diện gọi là
`session.query()`, trong khi Core sử dụng hàm `select()` và `connection.execute()`. Điều này tạo ra hai phương nghĩa (dialect) 
riêng biệt trong cùng một thư viện. 

SQLAlchemy 2.0 giới thiệu một triết lý "hợp nhất" (Unified Tutorial). 
Thay đổi cơ bản nhất là: **ORM giờ đây sử dụng cú pháp `select()` của Core làm phương thức truy vấn chính.** 

Điều đấy có ý nghĩa là gì?
1. **Một cách để học:** Nhà phát triển không còn phải học hai hệ thống truy vấn song song
2. **Sức mạnh của Core cho ORM:** ORM giờ đây có thể tận dụng toàn bộ sức mạnh và sự linh hoạt của cấu trúc `select()` của Core một cách trực tiếp. 
3. **Nguồn gốc của sự nhầm lẫn:** Các đoạn mã bạn thấy có thể đang lẫn lộn giữa cú pháp `session.query()` cũ (1.x) và cú pháp `session.execute(select(...))` mới (2.0)

Để làm chủ SQLAlchemy 2.0 cho phát triển backend, nhà phát triển không thể chỉ học ORM. 
Họ bắt buộc phải học cú pháp `select()` của Core, vì nó đã trở thành cú pháp truy vấn tiêu chuẩn của ORM hiện đại. 
Báo cáo này sẽ tập trung hoàn toàn vào cú pháp 2.0 thống nhất này.

## Phần II. Cú pháp ORM hiện đại (Phong cách 2.0) - Khai báo Models
Phần này tập trung vào cú pháp khai báo Models, một trong những thay đổi trực quan và quan trọng nhất trong SQLAlchemy 2.0, 
được thiết kế để tích hợp hoàn toàn với các chú thích kiểu (type annotations) của Python.

### 2.1 Sự Dịch chuyển sang Phong cách 2.0: Lý do và Lợi ích

Sự ra đời của SQLAlchemy 2.0 đánh dấu một sự thay đổi lớn về cú pháp khai báo model. Lý do chính là để tích hợp hoàn toàn với các chú thích kiểu PEP 484.

Lợi ích của phong cách 2.0 bao gồm:

* **Kiểm tra kiểu (Type-Checking):** Các công cụ như mypy giờ đây có thể hiểu và xác thực các model SQLAlchemy, giúp phát hiện lỗi sớm.

* **IDE Hỗ trợ Tốt hơn:** Tự động hoàn thành (auto-complete) và gợi ý (intellisense) trong các IDE (như VS Code) trở nên chính xác hơn đáng kể.

* **Rõ ràng và Tường minh:** Cú pháp mới tách biệt rõ ràng giữa kiểu dữ liệu phía Python và cấu hình phía CSDL, giảm bớt sự "ma thuật" (magic) và làm cho mã dễ đọc hơn.

### 2.2 Khai báo Cơ bản (Declarative Mapping)
Để định nghĩa các model, chúng ta sử dụng hệ thống "Declarative Mapping".

**Bước 1:** `DeclarativeBase` Trong phong cách 2.0, tất cả các model phải kế thừa từ một lớp cơ sở (base class) được tạo từ `DeclarativeBase`.

```Python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
```

Lớp `Base` này sẽ chứa một `MetaData` object, nơi đăng ký tất cả các bảng và model được liên kết. 

**Bước 2:** `__tablename__` Bên trong một lớp model, thuộc tính `__tablename__` được sử dụng để chỉ định tên của bảng trong CSDL mà lớp này sẽ ánh xạ tới. 

```Python
class User(Base):
    __tablename__ = "user_account"
    #... các cột sẽ được định nghĩa ở đây
```

### 2.3. Cú pháp cột mới: `Mapped` và `mapped_column()`

Đây là thay đổi cú pháp cốt lõi của 2.0. Nó thay thế hoàn toàn cấu trúc Column() cũ ở cấp độ lớp. Cú pháp mới tách biệt vai trò một cách rõ ràng :   

1. `Mapped[...]`: Đây là một chú thích kiểu (type annotation). Nó cho Python (ví dụ: IDE, mypy, và chính bạn) biết kiểu dữ liệu của thuộc tính phía Python là gì. Ví dụ, user.name sẽ là một str.   

2. `mapped_column(...)`: Đây là hàm cấu hình. Nó cho SQLAlchemy biết các thông số chi tiết của cột phía CSDL (database-side), chẳng hạn như kiểu dữ liệu SQL (ví dụ: String(30)), có phải là khóa chính không, v.v..   

Một trong những điểm mạnh nhất của cú pháp 2.0 là khả năng suy luận (inference). SQLAlchemy có thể tự động suy ra cấu hình CSDL từ chú thích kiểu Mapped.

Hãy xem các ví dụ sau :

**Trường hợp 1:** Suy luận đầy đủ (Type Hint Only)
```Python
from typing import Optional
from sqlalchemy.orm import Mapped

class User(Base):
    __tablename__ = "user_account"

    # SQLAlchemy tự động suy luận:
    # - Kiểu CSDL là INTEGER từ `int`
    # - `nullable=False` vì không có `Optional`
    id: Mapped[int] = mapped_column(primary_key=True)

    # SQLAlchemy tự động suy luận:
    # - Kiểu CSDL là VARCHAR (mặc định) từ `str`
    # - `nullable=False`
    username: Mapped[str]

    # SQLAlchemy tự động suy luận:
    # - `nullable=True` vì có `Optional`
    full_name: Mapped[Optional[str]]
```

Như bạn thấy, `mapped_column()` có thể được bỏ qua hoàn toàn nếu không có cấu hình đặc biệt nào (ngoại trừ `primary_key`). 
Việc sử dụng `Optional` từ mô-đun `typing` sẽ tự động thiết lập `nullable=True` cho cột CSDL.   


**Trường hợp 2:** Ghi đè (Overriding) suy luận Khi các suy luận mặc định không đủ, 
chúng ta sử dụng `mapped_column()` để cung cấp thông tin chi tiết:

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Ghi đè kiểu VARCHAR mặc định
    # để sử dụng String(30) cụ thể
    name: Mapped[str] = mapped_column(String(30)) [8]
```

### 2.4. Bảng 2: So sánh cú pháp khai báo Model (1.x vs. 2.0)
<table>
  <thead>
    <tr>
      <th>Khái niệm</th>
      <th>Cú pháp 1.x (Legacy)</th>
      <th>Cú pháp 2.0 (Hiện đại)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Lớp cơ sở (Base)</td>
      <td><code>Base = declarative_base()</code></td>
      <td>
        <code>from sqlalchemy.orm import DeclarativeBase</code>
        <br><br>
        <code>class Base(DeclarativeBase): pass</code>
      </td>
    </tr>
    <tr>
      <td>Cột khóa chính</td>
      <td><code>id = Column(Integer, primary_key=True)</code></td>
      <td><code>id: Mapped[int] = mapped_column(primary_key=True)</code></td>
    </tr>
    <tr>
      <td>Cột chuỗi (bắt buộc)</td>
      <td><code>name = Column(String(50), nullable=False)</code></td>
      <td>
        <code>name: Mapped[str] = mapped_column(String(50))</code>
        <em>(nullable=False được suy ra từ str)</em>
      </td>
    </tr>
    <tr>
      <td>Cột tùy chọn (Nullable)</td>
      <td><code>fullname = Column(String, nullable=True)</code></td>
      <td>
        <code>fullname: Mapped[Optional[str]]</code>
        <em>(nullable=True được suy ra từ Optional)</em>
      </td>
    </tr>
    <tr>
      <td>Khóa ngoại</td>
      <td><code>user_id = Column(Integer, ForeignKey("user.id"))</code></td>
      <td><code>user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))</code></td>
    </tr>
  </tbody>
</table>


## Phần III. Quản lý Kết nối và Trạng thái (Engine và Session)

Sau khi đã định nghĩa cái gì (models), phần này sẽ giải thích cách thức (session) để thiết lập kết nối và tương tác với chúng.

### 3.1. Engine: Cổng kết nối đến Cơ sở dữ liệu
`Engine` là điểm khởi đầu của mọi tương tác SQLAlchemy. Nó là một đối tượng quản lý một "bể bơi kết nối" (connection pool) đến CSDL. 
* `create_engine` (Đồng bộ - Synchoronous): Đây là cú pháp chuẩn cho các ứng dụng đồng bộ

```Python
from sqlalchemy import create_engine

# Sử dụng SQLite cho ví dụ
engine = create_engine("sqlite:///./test.db", echo=True)
```

* `create_async_engine`**(Bất đồng bộ - Asynchronous)**: Đây là chìa khóa để tích hợp với các framework bất đồng bộ như FastAPI. 
Nó trả về một `AsyncEngine`.

```Python
from sqlalchemy.ext.asyncio import create_async_engine

# Yêu cầu một trình điều khiển CSDL (DBAPI) bất đồng bộ
# Ví dụ: 'asyncpg' cho PostgreSQL
# 'aiosqlite' cho SQLite
async_engine = create_async_engine(
    "postgresql+asyncpg://user:password@localhost/mydb", 
    echo=True
)
```

### 3.2. Session: Giao diện chính của ORM
Đây là một trong những khái niệm quan trọng nhất. Session không phải là một kết nối CSDL. 

Thay vào đó, `Session` là một đối tượng quản lý trạng thái, triển khai mẫu thiết kế "Unit of Work". 
Nó hoạt động như một "vùng đệm" (cache) hoặc "khu vực dàn dựng" (staging area) cho các đối tượng python mà bạn đã tải
hoặc tạo ra. Nó theo dõi mọi thay đổi bạn thực hiện (thêm, sửa, xoá). Khi bạn gọi `session.commit()`, `Session` sẽ "xả"
(flush) tất cả các thay đổi này ra CSDL dưới dạng các câu lệnh SQL một cách hiệu quả. 

**Vòng đời (Lifecycle) của Session:**
**1. Tạo (Creation):** Cách tốt nhất để tạo các `Session` là sử dụng một `sessionmaker` (hoặc `async_sessionmaker` cho bất đồng bộ). 
Đây là một "nhà máy" (factory) tạo ra các đối tượng `Session` mới đã được cấu hình. 

**Sync:**
```Python
from sqlalchemy.orm import sessionmaker

SessionLocal = sessionmaker(bind=engine)
```

**Async:**
```Python
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine, 
    class_=AsyncSession,
    expire_on_commit=False # Rất quan trọng, sẽ giải thích dưới đây
)
```

**2. Sử dụng (Usage - Best Practice):** Luôn sử dụng `Session` trong context manager (khối `with`). 
Điều này đảm bảo `Session` luôn được đóng đúng cách, ngay cả khi có lỗi xảy ra. 

**Sync:**
```Python
with SessionLocal() as session:
    #... thực hiện công việc với session...
    session.commit()
# session.close() được gọi tự động ở đây
```


**Async:**
```Python
async with AsyncSessionLocal() as session:
    #... thực hiện công việc với session...
    await session.commit()
# await session.close() được gọi tự động ở đây
```

**3. Đóng (closing):** Như đã nêu, `session.close()` được gọi tự động bởi context manager. 
Việc này giải phóng mọi tài nguyên kết nối tới `Session` đang nắm giữ và giữ chúng trở lại connection pool. 

### 3.3. Phân tích chuyên sâu cạm bẫy của `AsyncSession` và `expire_on_commit`

Một trong những vấn đề "khó hiểu" nhất  và là nguồn gây lỗi phổ biến nhất khi chuyển sang `AsyncSession` là lỗi `"IO attempted in an unexpected place"`.

Đây là lý do tại sao nó xảy ra, và tại sao `expire_on_commit=False` là một thiết lập quan trọng: 

1. **Hành vi mặc định:** Theo mặt định, SQLAlchemy được cấu hình với `expire_on_commit=True`
2. **Cơ chế "Expire":** Điều này có nghĩa là ngay sau khi `session.commit()` được thực hiện thành công, 
tất cả đối tượng Python (như `my_user`) mà `Session` đó đang quản lý sẽ bị đánh dấu là "hết hạn" (expired). 
3. **Cơ chế "Auto-Refresh"** Khi bạn cố gắng truy cập lại một thuộc tính trên đối tượng đã hết hạn  (ví dụ: `print(my_user.name)`),
SQLAlchemy sẽ tự động và ngầm phát ra một câu lệnh `SELECT` mới đến CSDL để làm mới (refresh) đối tượng đó, đảm bảo bạn đang xem dữ liệu mới nhất. 
4. **Tại sao nó tốt trong Sync:** Trong môi trường đồng bộ, đây là một tính năng an toàn, giúp ngăn ngừa việc sử dụng dữ liệu cũ (stale data).
5. **Tại sao nó là thảm hoạ (trong Async):** Trong môi trường bất đồng bộ (`async def`), một truy vấn I/O ngầm và chặn (blocking) là điều cấm kị. 
Khi bạn truy cập `my_user.name` sau khi commit, SQLAlchemy cố gắng thực hiện một truy vấn DB đồng bộ, chặn đứng các vòng lặp sự kiện (event loop) 
và gây ra lỗi "IO attemped...".

**Giải pháp:** Bằng cách thiết lập `expire_on_commit=False` khi tạo `async_sessionmaker`, 
bạn đang bảo SQLAlchemy: "Sau khi commit, đừng làm hết hạn đối tượng của tôi. Cứ tin rằng dữ liệu của tôi có trong Python vẫn ổn". 

**Hệ quả (sự đánh đổi):** Điều này giải quyết được lỗi I/O, nhưng bản phải trả giá bằng một sự đánh đổi: dữ liệu của bạn có thể trở nên cũ (stale). 

Ví dụ: Khi bạn tạo một người dùng mới `(session.add(new_user))` và `commit`, 
các giá trị do CSDL dữ liệu tạo ra (như `id` khoá chính hoặc `created_at` từ `server_default`)
sẽ không xuất hiện trên đối tượng `new_user` của bạn. 

**Quy tắc mới của Async:** Nếu bạn cần dữ liệu mới nhất từ CSDL sau khi commit (hoặc sau khi thêm một đối tượng mới), 
bạn phải chủ động (explicitly), gọi `await session.refresh(my_object)`. Đây là sự đánh đổi bắt buộc khi dùng `async`:
Bạn phải rõ ràng về thời điểm I/O xảy ra để đối lấy hiệu suất không bị chặn. 

## Phần IV. Thao tác dữ liệu (CRUD) với ORM 2.0

Đây là phần cú pháp "tất tần tật" mà các nhà phát triển sử dụng hàng ngày, tập trung hoàn toàn vào phong cách 2.0.

### 4.1. Tạo (Create)

Để thêm một đối tượng mới vào CSDL, bạn chỉ cần khởi tạo đối tượng Python và thêm nó vào `Session` bằng `session.add()`.

```Python
# 1. Tạo đối tượng Python
new_user = User(name="spongebob", fullname="Spongebob Squarepants")

async with AsyncSessionLocal() as session:
    # 2. Thêm vào Session (vùng dàn dựng)
    session.add(new_user)
    
    # 3. Commit để lưu vào CSDL
    await session.commit()
    
    # 4. (Rất quan trọng) Làm mới để lấy ID và các giá trị server_default
    await session.refresh(new_user)
    
    # Giờ đây new_user.id sẽ có giá trị
    print(new_user.id)
```

Để thêm nhiều đối tượng, hãy sử dụng `session.add_all([...])`.

### 4.2. Đọc (Read) - Sự thay đổi lớn nhất

Đây là nơi cú pháp "hợp nhất" 2.0 tỏa sáng. Hãy quên session.query() đi. Cú pháp đó là của 1.x. 
Giờ đây, chúng ta sử dụng hàm `select()` từ Core, ngay cả trong ORM. 

**Bước 1: Xây dựng câu lệnh (Statement):** Sử dụng hàm `select()` và truyền vào lớp Model bạn muốn truy vấn.
```Python
from sqlalchemy import select

# Lấy tất cả người dùng
stmt_all = select(User)

# Lấy người dùng theo điều kiện
stmt_one = select(User).where(User.name == "spongebob") [22]

# Sắp xếp kết quả
stmt_sorted = select(User).order_by(User.id.desc())
```

**Bước 2: Thực thi cấu lệnh (Executing):** Sử dụng `session.execute()` (hoặc `await session.execute()`) cho async) để chạy câu lệnh.

```Python
# bên trong `async with AsyncSessionLocal() as session:`
result = await session.execute(stmt_one)
```

**Bước 3: Xử lý đối tượng `Result`** `session.execute()` không trả về một danh sách các đối tượng, mà trả về một đối tượng `Result`. 
Đây là một bước đệm quan trọng, và bạn có thể lấy dữ liệu từ nó. 

* `result.scalars():` Phương thức này được sử dụng trong 90% trường hợp khi truy vấn ORM. Nó trả về một iterator của chính đối tượng Model. (ví dụ: các đối tượng `User`).
```Python
# Lấy một danh sách các đối tượng User
users_list = result.scalars().all()

# Lấy đối tượng User đầu tiên, hoặc None nếu không có
user_obj = result.scalars().first() [17]

# Lấy chính xác MỘT đối tượng, báo lỗi nếu không có hoặc có nhiều hơn 1
user_obj_one = result.scalars().one()
```

* `result.scalar():` Được sử dụng khi bạn chỉ mong đợi một giá trị duy nhất (không phải một đối tượng hay một hàng). 
Rất lý tưởng cho các truy vấn tổng hợp như `func.count()`. 

```Python
from sqlalchemy import func
count_stmt = select(func.count()).select_from(User)
count_result = await session.execute(count_stmt)

# Lấy giá trị số nguyên (integer) đếm được
total_users = count_result.scalar()
```

### 4.3. Cập nhật (Update)

Có hai cách cơ bản để cập nhật dữ liệu, tương ứng với hai triết lý Core và ORM. 

**Phương pháp 1: Hướng trạng thái (Stateful ORM - "Pythonic")** Đây là cách làm "kiểu ORM". 
Bạn tải một đối tượng, thay đổi thuộc tính Python của nó, và `commit`. 

```Python
async with AsyncSessionLocal() as session:
    # 1. Tải đối tượng
    stmt = select(User).where(User.id == 1)
    user = (await session.execute(stmt)).scalars().first()
    
    if user:
        # 2. Thay đổi thuộc tính Python
        user.name = "new_name"
    
    # 3. Commit. SQLAlchemy thấy sự thay đổi và tự động tạo UPDATE
    await session.commit()
```
* **Ưu điểm:** Rất trực quan và Pythonic.
* **Nhược điểm:** Yêu cầu ít nhất hai truy vấn CSDL (một `SELECT` và một `UPDATE`)

**Phương pháp 2: Hướng lệnh (Stateless / Bulk - "SQL-like"):** Phương phá này sử dụng hàm `update()` của Core. 
Nó hiệu quả hơn nhiều cho các cập nhật hàng loạt vì nó thực hiện một câu lệnh `UPDATE` duy nhất trên CSDL mà không cần
tải đối tượng vào Python trước.
```Python
from sqlalchemy import update

# 1. Xây dựng câu lệnh UPDATE
stmt = (
    update(User)
   .where(User.id == 1)
   .values(name="new_name") # Cập nhật trực tiếp
)

async with AsyncSessionLocal() as session:
    # 2. Thực thi
    await session.execute(stmt)
    
    # 3. Commit
    await session.commit()
```
* **Ưu điểm**: Hiệu suất cao, chỉ 1 truy vấn. 
* **Nhược điểm:** Không kích hoạt các "object lifecycle" hooks của ORM.

### 4.4. Xoá (Delete)
Tương tự như Cập nhật, có hai cách để Xóa.

**Phương pháp 1: Hướng trạng thái (Stateful ORM):** Tải đối tượng, sau đó sử dụng `session.delete()`.
```Python
async with AsyncSessionLocal() as session:
    # 1. Tải đối tượng
    stmt = select(User).where(User.id == 1)
    user = (await session.execute(stmt)).scalars().first()
    
    if user:
        # 2. Đưa vào trạng thái "pending delete"
        await session.delete(user) # Trong async, delete là một coroutine
    
    # 3. Commit để thực thi DELETE
    await session.commit()
```

**Phương pháp 2: Hướng Lệnh (Stateless / Bulk):** Sử dụng hàm `delete()` của Core. Rất nhanh và hiệu quả.
```Python
from sqlalchemy import delete

# 1. Xây dựng câu lệnh DELETE
stmt = delete(User).where(User.id == 1)

async with AsyncSessionLocal() as session:
    # 2. Thực thi
    await session.execute(stmt)
    
    # 3. Commit
    await session.commit()
```

### 4.5. Hoàn tất giao diện (Commit, Rollback, Refresh)
* `await session.commit():` Xác nhận tất cả các thay đổi (add, update, delete) đang chờ trong `Session` và lưu chúng vào CSDL. Nó kết thúc giao dịch hiện tại. 
* `await session.rollback():` Huỷ bỏ mọi thay đổi đã được thực hiện trong `Session` kể từ lần `commit` cuối cùng. Thường được sử dụng trong khối `except` để xử lý lỗi.
* `await session.refresh(obj):` Như đã thảo luận trong Phần III, đây là một thao tác quan trọng trong `AsyncSession`. 
Nó cập nhật một đối tượng Python cụ thể bằng cách phát ra một SELECT để lấy dữ liệu mới nhất từ CSDL.   

## Phần V. Mô hình hoá các mối quan hệ dữ liệu (Relationships)

Đây là phần mạnh mẽ nhất của ORM, cho phép bạn điều hướng CSDL của mình như một biểu đồ đối tượng Python.

### 5.1. Nền tảng `ForeignKey` và `relationship()`

Để liên kết hai model, chúng ta cần hai cấu trúc hoạt động song song:

1. `ForeignKey:` Đây là ràng buộc vật lý trong CSDL. Nó là một phần của định nghĩa `CREATE TABLE`. 
Trong SQLAlchemy 2.0, nó được định nghĩa bên trong `mapped_column()`. Nó nói với CSDL rằng "giá trị trong cột này phải tồn tại trong cột của bảng kia".   
* Cú pháp: `user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))`.   

2. `relationship()`: Đây là liên kết logic trong ORM. Nó không tồn tại trong CSDL. 
Nó nói với SQLAlchemy rằng "khi tôi truy cập `user.addresses`, hãy thực hiện một JOIN (hoặc truy vấn liên quan) đến bảng Address bằng cách sử dụng khóa ngoại `user_id`". 
Nó được định nghĩa ở cấp độ lớp, bên ngoài `mapped_column()`.

Bạn cần cả hai để có một quan hệ ORM hoạt động đầy đủ. 

### 5.2 `back_populates` vs. `backref`

Trong các ví dụ cũ, bạn có thể thấy `backref`. Đây là một "shortcut" (đường tắt)  tự động tạo `relationship()` ở phía bên kia. Tuy nhiên, nó khá ẩn (implicit).   

Phong cách 2.0 và các phương pháp thực hành tốt nhất hiện đại ưu tiên sự tường minh (explicit) của `back_populates`.   

Với `back_populates`, bạn phải chủ động định nghĩa `relationship()` trên cả hai model và chỉ cho chúng "biết" về nhau bằng cách cung cấp tên thuộc tính của phía bên kia.   

Tại sao điều này lại tốt? Nó cho phép đồng bộ hóa trong bộ nhớ (in-memory synchronization). 
Khi bạn thực hiện một hành động như `parent.children.append(child)`, ORM, nhờ back_populates, 
sẽ biết rằng nó cũng phải tự động thiết lập `child.parent = parent` trong bộ nhớ Python, 
ngay cả trước khi bạn commit. Điều này giữ cho biểu đồ đối tượng của bạn luôn nhất quán.  

### 5.3. Triển khai các Mẫu Quan hệ (với Cú pháp 2.0)
Hãy xem cách triển khai các mẫu quan hệ phổ biến bằng cú pháp `Mapped` và `back_populates`.

#### 5.3.1 One-to-Many (Một-nhiều)
Ví dụ: một `User` có nhiều `Address`, nhưng một `Address` chỉ thuộc về một `User`.

```Python
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

class User(Base):
    __tablename__ = "user_account"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    
    # Phía "One": Mối quan hệ này là một DANH SÁCH
    # `Mapped[List["Address"]]` là rất quan trọng 
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user",  # Trỏ đến thuộc tính 'user' trong Address
        cascade="all, delete-orphan"
    )

class Address(Base):
    __tablename__ = "address"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    
    # Phía "Many": Chứa Khóa ngoại
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    
    # Phía "Many": Mối quan hệ này là một đối tượng ĐƠN LẺ
    user: Mapped["User"] = relationship(
        back_populates="addresses" # Trỏ đến thuộc tính 'addresses' trong User
    )
```

Lưu ý: `cascade="all, delete-orphan"` là một cấu hình hữu ích. Nó có nghĩa là khi bạn xóa một `User`, tất cả `Address` liên quan của nó cũng sẽ bị xóa.

#### 5.3.2. One-to-One (một-một)

Một mối quan hệ Một-một về cơ bản là một mối quan hệ Một-nhiều, nhưng được ràng buộc ở cả hai phía. Chúng ta thực hiện điều này bằng hai thay đổi:

1. **Cú pháp 2.0:** Trong chú thích `Mapped`, chúng ta loại bỏ `List`. SQLAlchemy 2.0 đủ thông minh để suy luận (deduce) rằng đây là mối quan hệ `uselist=False` (tức là Một-một) từ chính type hint này.   

2. **Ràng buộc CSDL:** Thêm unique=True vào ForeignKey để đảm bảo phía CSDL rằng một Profile chỉ có thể được liên kết với một User.   

```Python
class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    
    # KHÔNG CÓ `List` -> SQLAlchemy hiểu đây là Một-một
    profile: Mapped["Profile"] = relationship(
        back_populates="user", 
        cascade="all, delete-orphan"
    )

class Profile(Base):
    __tablename__ = "profile"
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[Optional[str]]
    
    # Thêm `unique=True` vào ForeignKey
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
    
    # KHÔNG CÓ `List`
    user: Mapped["User"] = relationship(back_populates="profile")
```

#### 5.3.3 Many-to-Many (Nhiều-nhiều)
Ví dụ: một `Student` có thể tham gia nhiều `Course`, và một `Course` có thể có nhiều `Student`.

Mối quan hệ này luôn yêu cầu một **Bảng liên kết (Association Table) ở giữa để lưu trữ các cặp liên kết.**

**Bước 1. Định nghĩa Bảng liên kết:** Bảng này thường được định nghĩa bằng cú pháp Core `Table` (không phải là một Model) 
và không có các cột nào khác ngoài các khoá ngoại (mặc dù nó có thể có). 

from sqlalchemy import Table, Column, Integer
```Python
# Bảng liên kết
student_course_table = Table(
    "student_course_association",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("course_id", Integer, ForeignKey("courses.id"), primary_key=True),
)
```

**Bước 2: Định nghĩa các Model** với `relationship()` Cả hai model sẽ có một `relationship()` trỏ đến bảng liên kết thông qua tham số `secondary`.

```Python
class Student(Base):
    __tablename__ = "students"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    
    # Cả hai phía đều là `List`
    courses: Mapped[List["Course"]] = relationship(
        secondary=student_course_table, # Chỉ định bảng liên kết
        back_populates="students"
    )

class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    
    students: Mapped[List["Student"]] = relationship(
        secondary=student_course_table, # Chỉ định bảng liên kết
        back_populates="courses"
    )
```

## Phần VI. Kỹ thuật truy vấn nâng cao và tối ưu hiệu suất
Đối với phát triển backend thực thụ, việc thực hiện CRUD cơ bản là chưa đủ. Bạn cần các truy vấn động và hiệu suất cao.

### 6.1 Lọc động (Dynamic Filtering)
Một yêu cầu backend phổ biến là xây dựng các truy vấn `WHERE` động dựa trên các tham số đầu vào (ví dụ: query params từ URL như `/items?status=active&user_id=5`).

Bạn có thể xâu chuỗi các phương thức `.where()` một cách có điều kiện. 
Tuy nhiên, một kỹ thuật Pythonic mạnh mẽ hơn là sử dụng `getattr()` để truy cập các thuộc tính model một cách linh động. 

Giả sử bạn có một `dict` các bộ lcoj: `filters = {"name": "Bob", "status": "active"}`

Bạn có thể xây dựng truy vấn như sau:

```Python
stmt = select(User)

for key, value in filters.items():
    # Kiểm tra xem 'key' có phải là thuộc tính hợp lệ của User không
    if hasattr(User, key):
        column_attr = getattr(User, key) # Tương đương với User.name
        stmt = stmt.where(column_attr == value) # Thêm điều kiện WHERE

# Bây giờ `stmt` là:
# SELECT... FROM user WHERE user.name = 'Bob' AND user.status = 'active'
```

### 6.2. Sắp xếp động (Dynamic Sorting)
Kỹ thuật tương tự cũng áp dụng cho `order_by()`. Bạn có thể nhận `sort_by="name"` và `sort_dir="desc"` từ API.

```Python
from sqlalchemy import asc, desc

sort_by_column = "name"
sort_direction = "desc"

stmt = select(User)

if hasattr(User, sort_by_column):
    column_attr = getattr(User, sort_by_column) [46]
    
    # Chọn hàm sắp xếp
    sort_func = desc if sort_direction == "desc" else asc [48]
    
    stmt = stmt.order_by(sort_func(column_attr))

# Bây giờ `stmt` là:
# SELECT... FROM user ORDER BY user.name DESC
```

### 6.3. Hàm tổng hợp (Aggregates) và Nhóm (Grouping)
Để thực hiện các phép tính như `COUNT`, `SUM`, `AVG`, hãy sử dụng đối tượng `func` từ sqlalchemy

* **Đếm (Count)**
```Python
from sqlalchemy import func

# Cách 1: Đếm đơn giản, trả về một con số
count_stmt = select(func.count()).select_from(User) [24, 26]
# Thực thi bằng.scalar()
total_users = (await session.execute(count_stmt)).scalar()

# Cách 2: Đếm và nhóm theo một cột
stmt = (
    select(User.status, func.count(User.id))
   .group_by(User.status)
)
# Kết quả sẽ là các hàng (Row) như ('active', 10), ('inactive', 5)
results = (await session.execute(stmt)).all()
```

### 6.4. Giải quyết Vấn đề N+1 (N+1 Problem) bằng Eager Loading

Đây là vấn đề hiệu suất quan trọng nhất trong bất kỳ ORM nào. 
* **Vấn đề (N+1):** SQLAlchemy sử dụng "Lazy Loading" (tải lười) làm mặc định. Giả sử bạn:
1. Tải 100 `User`: `stmt = select(User)` (1 truy vấn)
2. Lặp qua danh sách user: `for user in users:`
3. Truy cập `user.addresses` cho mỗi user (ví dụ: `print(user.addresses)`)...
ORM sẽ phát ra 100 truy vấn `SELECT` bổ sung (mỗi truy vấn cho một user). 
Tổng cộng: 1 + 100 = 101 truy vấn. Đây là một thảm họa về hiệu suất.

* **Yêu cầu bắt buộc trong Async:** Trong môi trường `AsyncSession`, Lazy Loading không chỉ chậm, nó còn bị cấm. 
Giống như vấn đề "expire on commit", việc truy cập `user.addressess` sẽ cố gắng thực hiện một I/O ngầm, chặn (blocking)
và làm hỏng ứng dụng của bạn. Do đó, trong môi trường bất đồng bộ, bạn bắt buộc phải sử dụng "Eager Loading" (tải chủ động) để tải trước tất cả các dữ liệu bạn cần. 

SQLAlchemy cung cấp hai chiến lược Eager Loading chính thông qua phương thức `.optional()`:

#### 6.4.1. Giải pháp 1: joinedload()
* **Cơ chế:** Sử dụng `LEFT OUTER JOIN` để tải cả hai bảng (`User` và `Addresss`) trong một câu lệnh SQL duy nhất. 
* **Cú pháp:**
```Python
from sqlalchemy.orm import joinedload

stmt = select(User).options(joinedload(User.addresses))
```
**Phù hợp nhất cho:** Các mối quan hệ `Many-to-One` (ví dụ: tải `Address` và `joinedload(Address.user)`) hoặc `One-to-One`. 
Lý do là nó không làm tăng đáng kể số lượng hàng trả về. 
* **Hạn chế:** Khi sử dụng với quan hệ `One-to-Many`, nó có thể tạo ra "tích Descartes" (Cartesian product), trả về rất nhiều 
hàng bị trùng lặp (Ví dụ: `User` có 10 `Address` sẽ xuất hiện 10 lần trong kết quả `JOIN`). 

#### 6.4.2. Giải pháp 2: `selectinload()`
* **Cơ chế:** Sử dụng hai (hoặc nhiều hơn) câu lệnh SQL một cách thông minh. 
1. Truy vấn 1: `SELECT * FROM user_account`
2. Truy vấn 2: `SELECT * FROM address WHERE user_id IN (1, 2, 3,...);` (trong đó (1, 2, 3) là ID của các user từ truy vấn 1).

* **Cú pháp:**
```Python
from sqlalchemy.orm import selectinload

stmt = select(User).options(selectinload(User.addresses))
```

* **Phù hợp nhất cho:** Các mối quan hệ `One-to-Many` hoặc `Many-to-Many`. 
Nó tránh được việc trùng lặp hàng của `joinedload` và thường là chiến lược hiệu quả nhất cho các tập dữ liệu lớn. 

### 6.5. Bảng 3: So sánh Chiến lược Eager Loading (joinedload vs. selectinload)
Bảng này cung cấp một hướng dẫn tham khảo nhanh để ra quyết định tối ưu hóa.
<table>
  <thead>
    <tr>
      <th>Chiến lược</th>
      <th>Cơ chế SQL</th>
      <th>Số lượng Truy vấn</th>
      <th>Phù hợp nhất cho</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>joinedload()</code></td>
      <td>LEFT OUTER JOIN</td>
      <td>1</td>
      <td>Quan hệ <code>Many-to-One</code> hoặc <code>One-to-One</code></td>
    </tr>
    <tr>
      <td><code>selectinload()</code></td>
      <td>SELECT... + SELECT... WHERE... IN (...)</td>
      <td>2 (hoặc nhiều hơn)</td>
      <td>Quan hệ <code>One-to-Many</code> hoặc <code>Many-to-Many</code></td>
    </tr>
  </tbody>
</table>

## Phần VII: Tích hợp SQLAlchemy và Pydantic (Hệ sinh thái Sanic)
### 7.1. Tách biệt vai trò: Models(SQLAlchemy) vs. Schemas(Pydantic)

Một lỗi phổ biến của người mới bắt đầu là nhầm lẫn giữa hai loại "model" này. 
Trong một ứng dụng backend hiện đại, chúng có hai vai trò hoàn toàn khác biệt nhưng bổ trợ cho nhau:   

1. **SQLAlchemy Models (ví dụ: `models.py`):**

* **Vai trò:** Đại diện cho lược đồ CSDL (Database Schema).
* **Mục đích:** Là "nguồn chân lý" (source of truth) cho cấu trúc dữ liệu của bạn, bao gồm các mối quan hệ, ràng buộc CSDL.
* **Ví dụ:** Một User model sẽ có một cột hashed_password.

2. **Pydantic Schemas (ví dụ: `schemas.py`):**

* **Vai trò:** Đại diện cho lược đồ API (API Schema).   

* **Mục đích:** Xác thực dữ liệu đi vào (request validation) từ client và định hình dữ liệu đi ra (response serialization).

* Ví dụ: Bạn sẽ có nhiều schema cho một model:

  * `UserCreate:` Schema cho việc tạo user, yêu cầu `password` (dạng rõ) nhưng không có id.

  * `UserRead:` Schema cho việc đọc user, có `id` và `username` nhưng hoàn toàn không có `hashed_password` để tránh rò rỉ dữ liệu nhạy cảm.

  * `UserBase:` Chứa các trường chung (như `username`) mà `UserCreate` và `UserRead` kế thừa để tránh trùng lặp mã.   

Sự tách biệt này là một phương pháp thực hành tốt nhất về bảo mật và kiến trúc.

### 7.2 Cấu hình "Kỳ diệu": `from_attributes = True`
Với làm thế nào để bạn chuyển đổi một đối tượng SQLAlchemy (từ CSDL) thành một Pydantic schema (để gửi đi dưới dạng JSON). 

Trong Pydantic V1, bạn sẽ thấy `class Config: orm_mode = True`. 
Trong Pydantic V2 (hiện đại), cú pháp đã thay đổi thành: `model_config = ConfigDict(from_attributes=True)`

**Nó chính xác là gì?** 
1. **Hành vi mặc định của Pydantic:** Pydantic được thiết kế để phân tích và xác thực (parse and validate) dữ liệu thô, 
mà nó mặc định giả định là một `dict`. Nếu bạn truyền một `dict`, nó sẽ truy cập các giá trị bằng cách sử dụng `my_dict["key"]`.
2. **Vấn đề:** Một đối tượng ORM (ví dụ: `db_user`) bạn lấy từ `result.scalars().first()` không phải là một `dict`. 
Nó là thể hiện của lớp (class instance). 
3. **Lỗi:** Nếu bạn cố gắng gọi `UserRead.model_validate(db_user)` mà không có cấu hình, Pydantic sẽ cố gắng truy cập `db_user["id"]` và thất bại,
vì cách đúng để truy cập là `db_user.id`. 
4. **Giải pháp:** `from_attributes=True` là một công tắc bảo Pydantic: 
"Đừng mong đợi một dict. Thay vào đó, hãy đọc dữ liệu bằng cách truy cập các thuộc tính (attributes) của đối tượng".

Đây chính là "cây cầu" cho phép Pydantic đọc dữ liệu trực tiếp từ các đối tượng SQLAlchemy của bạn.

```Python
from pydantic import BaseModel, ConfigDict

# Đây là schema của API
class UserRead(BaseModel):
    # Cấu hình "cầu nối"
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    
    # Chúng ta cũng có thể tải các relationship!
    # Pydantic sẽ tự động gọi `db_user.addresses`
    addresses: List
```

### 7.3. Luồng làm việc (Workflow) Backend điển hình
Đây là cách mọi thứ kết hợp với nhau trong một API endpoint của Sanic. 

**Luồng 1: Tạo (Create) (Request -> DB)**
1. Sanic nhận JSON, tự động xác thực bằng Pydantic UserCreate schema: `user_in: UserCreate`.
2. Chuyển Pydantic sang SQLAlchemy: `db_user = User(**user_in.model_dump())` (Hàm `model_dump()` chuyển Pydantic model thành `dict`). 
3. Thêm `Session: session.add(db_user)` và `await.session.commit()` 

**Luồng 2: Đọc (Read) (DB -> Response)**
1. Truy vấn CSDL: `stmt = select(User).where(User.id == 1)`
2. Tải đối tượng SQLAlchemy: `db_user = (await session.execute(stmt)).scalars().first()`
3. Chuyển SQLAlchemy sang Pydantic (sử dụng `from_attributes=True`): `response_data = UserRead.model_validate(db_user)`
4. Sanic nhận Pydantic model `response_data` và tự động chuyển nó thành JSON cho client. 

## Phần VIII. Quản lý Vòng đời Cơ sở dữ liệu với Alembic
Phần cuối cùng này cung cấp công cụ thiết yếu để "phát triển backend" một cách chuyên nghiệp: quản lý di trú CSDL (database migrations).

### 8.1 Tại sao cần Alembic?
Khi bạn phát triển ứng dụng, các model của bạn sẽ thay đổi. Bạn sẽ thêm cột mới (ví dụ: age vào User), đổi tên cột, hoặc thêm bảng mới.

CSDL hiện có của bạn không tự động cập nhật khi bản thay đổi mã `models.py`.

Alembic là một công cụ di trú CSDL được xây dựng cho SQLAlchemy. Nó cho phép bạn tạo các "phiên bản" (versions) cho lược đồ CSDL của mình. 
Mỗi phiên bản là một script Python mô tả cách "nâng cấp" (upgrade) lược đồ (ví dụ: `ADD COLUMN age INTEGER`) và cách "hạ cấp" (downgrade) (ví dụ: `DROP COLUMN age`).  


### 8.2 Thiết lập Môi trường
1. **Cài đặt:** `pip install alembic`

2. **Khởi tạo:** Chạy lệnh này trong thư mục gốc dự án của bạn:

* Đối với ứng dụng đồng bộ: `alembic init alembic`.   

* Đối với ứng dụng bất đồng bộ (FastAPI): `alembic init -t async alembic`. Template "async" này rất quan trọng vì nó cung cấp sẵn một tệp `env.py` có cấu trúc để xử lý asyncio.   

3. **Cấu hình `alembic.ini`:** Mở tệp `alembic.ini `vừa được tạo. Tìm dòng `sqlalchemy.url` và đặt nó thành chuỗi kết nối CSDL của bạn (ví dụ: `sqlalchemy.url = postgresql://user:pass@host/db`).   

   * _Lưu ý quan trọng:_ Ngay cả khi ứng dụng của bạn dùng driver async (`asyncpg`), 
   Alembic thường hoạt động tốt nhất với driver đồng bộ (như `postgresql`) trong tệp `.ini` này, 
   vì bản thân công cụ Alembic thường chạy đồng bộ.   

#### 8.3 Cấu hình `env.py` cho Autogenerate
Đây là bước quan trọng nhất và là nơi 90% người mới thất bại.

Làm thế nào lệnh `alembic revision --autogenerat`e biết được những thay đổi bạn đã thực hiện trong `models.py`?

Nó hoạt động bằng cách so sánh hai thứ :   

1. **Lược đồ (A):** Lược đồ của CSDL hiện tại (bằng cách kết nối và đọc).

2. **Lược đồ (B):** Lược đồ mong muốn của bạn (từ mã Python).

**Cạm bẫy:** Làm thế nào Alembic biết được Lược đồ (B)? Nó đọc biến target_metadata trong tệp `alembic/env.py`. 
Theo mặc định, tệp `env.py` được tạo ra có `target_metadata = None`.   

Nếu bạn để nguyên như vậy, Alembic sẽ so sánh Lược đồ (A) với `None` và kết luận "không có gì thay đổi". 
Nó sẽ tạo ra một tệp migration rỗng, và bạn sẽ bối rối không hiểu tại sao cột `age` mới của mình không được phát hiện.   

**Giải pháp:** Bạn bắt buộc phải chỉnh sửa tệp `alembic/env.py`:

1. Tìm đến dòng `target_metadata = None`.

2. Import lớp `Base` từ `models.py` của bạn.

3. Đặt `target_metadata` trỏ đến `metadata` của `Base`.

```Python
# bên trong alembic/env.py

# Import Base từ file models của bạn
from my_app.models import Base  # [72, 74, 75]
#... các import khác...

config = context.config
#...

# Trỏ target_metadata đến metadata của Base
target_metadata = Base.metadata [72, 74]

#... phần còn lại của tệp...
```

#### 8.4 Quy trình Di trú (Migration Workflow) Hàng ngày
Đây là quy trình bạn sẽ lặp lại hàng chục lần trong quá trình phát triển :   

* **Thay đổi Model:** Chỉnh sửa `models.py` (ví dụ: thêm `age: Mapped[Optional[int]] vào User`).

* **Tạo Migration Script:** `alembic revision --autogenerate -m "Add age column to user" `   

* **(QUAN TRỌNG) Xem xét Script:** Mở tệp script vừa tạo trong `alembic/versions/`. Luôn luôn xem xét lại script này. `autogenerate` không hoàn hảo và đôi khi cần được chỉnh sửa thủ công.   

* **Áp dụng Migration:** `alembic upgrade head`  Lệnh này sẽ chạy script "upgrade" và áp dụng thay đổi (ví dụ: `ADD COLUMN age`) vào CSDL của bạn.   

* **(Nếu cần) Hoàn tác:** `alembic downgrade -1 ` Lệnh này sẽ chạy script "downgrade" (ví dụ: `DROP COLUMN age`) của phiên bản mới nhất.   

### Phần IX. Kết luận và các phương pháp tốt nhất (best practices)

Để tóm tắt báo cáo toàn diện này, đây là 5 quy tắc vàng để làm chủ SQLAlchemy 2.0 trong phát triển backend:

* **Quy tắc 1 (Cú pháp):** Luôn sử dụng cú pháp 2.0. Ưu tiên `class Base(DeclarativeBase)`, các chú thích kiểu `Mapped / mapped_column`, 
và hàm `select() `cho tất cả các truy vấn ORM. Hãy bỏ `session.query() `ra khỏi bộ nhớ của bạn.

* **Quy tắc 2 (Async):** Khi sử dụng `AsyncSession`, luôn luôn cấu hình `async_sessionmaker` với `expire_on_commit=False`để tránh lỗi I/O ngầm. 
Chấp nhận rằng bạn phải chủ động gọi `await session.refresh(obj)` khi bạn cần dữ liệu mới.   

* **Quy tắc 3 (Hiệu suất):** Không bao giờ dựa vào Lazy Loading trong code bất đồng bộ. 
Nó sẽ làm hỏng ứng dụng của bạn. Hãy chủ động tải trước (Eager Load) mọi thứ bạn cần bằng cách sử dụng `.options().` 
Quy tắc chung: dùng `selectinload` cho các mối quan hệ -to-many và `joinedload` cho các mối quan hệ -to-one.   

* **Quy tắc 4 (Kiến trúc):** Giữ sự tách biệt vai trò rõ ràng giữa `models.py` (SQLAlchemy - đại diện CSDL) và `schemas.py` (Pydantic - đại diện API). 
Sử dụng `model_config = ConfigDict(from_attributes=True)` làm "cầu nối" để chuyển đổi các đối tượng ORM thành các schema API một cách an toàn.   

* **Quy tắc 5 (Migrations):** Thiết lập Alembic ngay từ đầu. Quan trọng nhất, hãy nhớ chỉnh sửa env.py để đặt `target_metadata = Base.metadata`. 
Và luôn luôn xem xét lại bằng mắt các tệp migration mà `autogenerate` tạo ra trước khi áp dụng chúng


