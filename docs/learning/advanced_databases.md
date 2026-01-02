# Từ Lý thuyết đến Thực tiễn: Bài giảng Chuyên sâu về 12 Chủ đề Cơ sở dữ liệu Nâng cao

## Mở đầu

Tài liệu này được biên soạn nhằm mục đích không chỉ định nghĩa 12 khái niệm cơ sở dữ liệu nâng cao, mà còn liên kết chúng thành một bức tranh toàn cảnh về kiến trúc hệ thống dữ liệu hiện đại. Trong thực tế, các chủ đề này không tồn tại độc lập; chúng là một chuỗi các quyết định và đánh đổi (trade-offs) mà mọi kiến trúc sư hệ thống phải đối mặt.

### Lộ trình học tập

Tài liệu được chia thành ba phần chính:

**Phần I - Nền tảng:** Khám phá các nguyên tắc đảm bảo tính toàn vẹn và hiệu suất trên một node đơn lẻ. Đây là nền móng của mọi cơ sở dữ liệu, bao gồm Transactions, ACID, Normalization và Indexes.

**Phần II - Tương tác:** Phân tích cầu nối quan trọng giữa lớp ứng dụng và cơ sở dữ liệu. Tập trung vào việc tối ưu hóa thông qua ORMs (với SQLAlchemy), giải quyết vấn đề N+1, và sử dụng các công cụ Profiling như EXPLAIN plan.

**Phần III - Mở rộng quy mô:** Giải quyết các thách thức khi hệ thống vượt qua giới hạn của một máy chủ. Bao gồm các chiến lược cho hệ thống phân tán, chịu lỗi và mở rộng: Failure Modes, Migration, Replication, Sharding, và Định lý CAP.

### Chủ đề trung tâm

Xuyên suốt tài liệu này, một chủ đề trung tâm sẽ xuất hiện: **mọi quyết định kiến trúc đều là một sự đánh đổi**. Lựa chọn về Replication (Phần III) ảnh hưởng trực tiếp đến cam kết ACID (Phần I). Việc sử dụng ORM (Phần II) đòi hỏi sự hiểu biết sâu sắc về Indexes (Phần I) để tránh thảm họa hiệu suất N+1.

---

## Phần I: Nền tảng của Tính toàn vẹn và Hiệu suất

Phần này đặt nền móng cho mọi hệ thống cơ sở dữ liệu, tập trung vào cách một database đơn lẻ đảm bảo rằng dữ liệu là chính xác, nhất quán và có thể được truy cập hiệu quả.

### 1. Transactions và ACID

#### 1.1. Transaction: Đơn vị công việc không thể chia nhỏ

**Transaction** là một chuỗi các thao tác cơ sở dữ liệu được thực hiện như một đơn vị công việc logic duy nhất, không thể chia nhỏ. Vòng đời của một transaction bao gồm việc bắt đầu, thực thi các truy vấn, và cuối cùng là `COMMIT` hoặc `ROLLBACK`.

- **Commit:** Nếu tất cả các thao tác thành công, transaction sẽ commit. Tại thời điểm này, các thay đổi trở nên vĩnh viễn trong cơ sở dữ liệu.

- **Rollback:** Nếu có bất kỳ lỗi nào xảy ra, cơ chế rollback cho phép hoàn tác mọi thay đổi đã thực hiện, đưa hệ thống trở lại trạng thái an toàn trước khi transaction bắt đầu.

**Các trạng thái của Transaction:**

1. **Active** (Đang hoạt động): Trạng thái ban đầu, transaction đang thực thi
2. **Partially Committed** (Cam kết một phần): Transaction đã hoàn thành thao tác cuối cùng và đang chờ để commit
3. **Committed** (Đã cam kết): Transaction đã hoàn tất thành công và các thay đổi đã được ghi vĩnh viễn
4. **Failed** (Thất bại): Transaction gặp lỗi trong quá trình thực thi
5. **Aborted** (Bị hủy bỏ): Transaction đã bị rollback và database được khôi phục về trạng thái ban đầu

Trạng thái **Partially Committed** là một khái niệm lý thuyết quan trọng. Nó đại diện cho khoảnh khắc mong manh khi logic transaction đã hoàn thành nhưng hệ thống chưa xác nhận các thay đổi là vĩnh viễn. Nếu hệ thống sập nguồn ngay tại thời điểm này, khi khởi động lại, DBMS phải đủ thông minh để nhận ra transaction này chưa bao giờ hoàn tất và phải bắt buộc rollback. Đây là "điểm không chắc chắn" cốt lõi mà các thuộc tính ACID phải giải quyết.

#### 1.2. ACID: Bốn trụ cột của RDBMS

**ACID** là một tập hợp các thuộc tính đảm bảo rằng các transactions được xử lý một cách đáng tin cậy. ACID là viết tắt của Atomicity, Consistency, Isolation, và Durability.

##### A - Atomicity (Tính nguyên tử)

Tính nguyên tử đảm bảo nguyên tắc "tất cả hoặc không có gì". Nó quy định rằng một transaction phải được thực hiện trọn vẹn; hoặc tất cả các thao tác của nó đều thành công và được áp dụng, hoặc nếu có bất kỳ thao tác nào thất bại, toàn bộ transaction sẽ bị hủy bỏ và database trở về trạng thái ban đầu. Điều này ngăn chặn tình trạng dữ liệu bị thay đổi một phần.

##### C - Consistency (Tính nhất quán)

Tính nhất quán đảm bảo rằng một transaction chỉ có thể đưa database từ "một trạng thái hợp lệ sang một trạng thái hợp lệ khác". Transaction phải tuân thủ tất cả các quy tắc và ràng buộc đã được định nghĩa trong database (như khóa ngoại, ràng buộc CHECK).

Trong bốn thuộc tính ACID, **Consistency là thuộc tính duy nhất mà cả hệ thống (DBMS) và lập trình viên cùng phải chịu trách nhiệm**. Các thuộc tính A, I, và D phần lớn được DBMS tự động đảm bảo. Tuy nhiên, DBMS không thể tự đảm bảo tính nhất quán về mặt nghiệp vụ.

**Ví dụ về chuyển tiền:**

Giao dịch bao gồm:
1. Kiểm tra số dư
2. Trừ tiền tài khoản gửi
3. Cộng tiền tài khoản nhận

- DBMS sẽ đảm bảo Atomicity (cả (2) và (3) cùng xảy ra hoặc không gì cả)
- DBMS sẽ đảm bảo Isolation (không ai có thể đọc số dư "nửa vời" ở giữa (2) và (3))
- DBMS sẽ đảm bảo Durability (nếu commit, tiền sẽ được chuyển vĩnh viễn)

Tuy nhiên, nếu lập trình viên quên bước (1) (Kiểm tra số dư), DBMS vẫn sẽ thực hiện một transaction nguyên tử, cô lập và bền vững, dẫn đến số dư âm. Đây là một trạng thái không hợp lệ về mặt nghiệp vụ. Do đó, **Consistency là một hợp đồng**: DBMS cung cấp các ràng buộc, và lập trình viên phải cung cấp logic nghiệp vụ đúng đắn.

##### I - Isolation (Tính cô lập)

Tính cô lập đảm bảo rằng các transactions được thực hiện đồng thời sẽ không can thiệp hoặc ảnh hưởng lẫn nhau. Về mặt lý thuyết, nó làm cho mỗi transaction có vẻ như đang được thực hiện một cách tuần tự, mặc dù trên thực tế chúng đang chạy song song.

Isolation không phải là một công tắc bật/tắt; nó là một thang đo đánh đổi giữa "tính đúng đắn" và "hiệu suất".

**Bốn mức độ cô lập:**

1. **Read Uncommitted** (Đọc chưa cam kết): Mức thấp nhất. Cho phép "dirty read" (đọc dữ liệu từ một transaction khác chưa commit)

2. **Read Committed** (Đọc đã cam kết): Ngăn "dirty read". Đây là mức mặc định của nhiều database

3. **Repeatable Read** (Đọc lặp lại): Ngăn "dirty read" và "non-repeatable read" (đọc lại cùng một hàng thấy dữ liệu đã bị thay đổi)

4. **Serializable** (Tuần tự hóa): Mức cao nhất. Ngăn cả "phantom read" (đọc lại thấy có hàng mới xuất hiện)

Nếu **Serializable** là mức an toàn nhất, tại sao không phải lúc nào cũng sử dụng nó? Bởi vì để đạt được mức Serializable, DBMS thường phải sử dụng các cơ chế khóa (locking) rất chặt chẽ, biến các hoạt động song song thành gần như tuần tự, làm giảm đáng kể hiệu suất và throughput của hệ thống. Hầu hết các database chọn **Read Committed** làm mặc định, đây là một sự đánh đổi có ý thức: chấp nhận khả năng xảy ra "non-repeatable read" để đổi lấy hiệu suất cao hơn.

##### D - Durability (Tính bền vững)

Tính bền vững đảm bảo rằng một khi transaction đã được commit, các thay đổi của nó sẽ được "lưu trữ vĩnh viễn" và tồn tại ngay cả khi hệ thống gặp sự cố như mất điện hoặc lỗi phần mềm.

Trong thực tế, tính bền vững thường được thực hiện thông qua cơ chế **Write-Ahead Logging (WAL)**. Khi một transaction COMMIT, điều thực sự xảy ra không phải là dữ liệu ngay lập tức được ghi vào các tệp dữ liệu chính trên đĩa (thường là thao tác Random I/O, rất chậm). Thay vào đó, một bản ghi log mô tả sự thay đổi đó được ghi tuần tự (append) vào một tệp log (Sequential I/O, rất nhanh). Chỉ khi bản ghi log này được ghi an toàn xuống đĩa, transaction mới được coi là commit. Dữ liệu thực tế có thể được ghi vào các tệp dữ liệu chính sau đó (một cách "lười biếng"). Nếu hệ thống sập, khi khởi động lại, nó có thể "replay" các log chưa được áp dụng để đảm bảo Durability mà không hủy hoại hiệu suất ghi.

---

### 2. Normalization và Denormalization

#### 2.1. Các dạng chuẩn (1NF, 2NF, 3NF)

**Normalization** (Chuẩn hóa dữ liệu) là quá trình tổ chức và cấu trúc dữ liệu trong database nhằm "loại bỏ sự trùng lặp", "đảm bảo tính nhất quán" và giảm thiểu các bất thường khi cập nhật dữ liệu. Quá trình này bao gồm việc chia dữ liệu thành các bảng nhỏ hơn và thiết lập mối quan hệ giữa chúng.

**Ba dạng chuẩn phổ biến:**

1. **Dạng chuẩn 1 (1NF):** Đảm bảo rằng mỗi cột trong bảng chứa các giá trị "nguyên tử" (không thể chia nhỏ được) và không có các nhóm lặp lại

2. **Dạng chuẩn 2 (2NF):** Đạt 1NF và loại bỏ các "phụ thuộc một phần". Điều này có nghĩa là tất cả các cột không phải khóa (non-key) phải phụ thuộc vào toàn bộ khóa chính, chứ không phải chỉ một phần của khóa chính (trong trường hợp khóa chính là khóa tổ hợp)

3. **Dạng chuẩn 3 (3NF):** Đạt 2NF và loại bỏ các "phụ thuộc bắc cầu" (transitive dependency). Điều này có nghĩa là một thuộc tính không phải khóa không được phép phụ thuộc vào một thuộc tính không phải khóa khác

**Normalization là một chiến lược được thiết kế để tối ưu hóa việc GHI (WRITE) và đảm bảo "Single Source of Truth", nhưng thường phải trả giá bằng hiệu suất ĐỌC (READ).**

**Ví dụ:**

Hãy tưởng tượng một bảng `Order_Customer` nơi thông tin khách hàng (tên, địa chỉ) được lặp lại trong mỗi đơn hàng họ đặt. Khi khách hàng đó thay đổi địa chỉ, ứng dụng sẽ phải tìm và UPDATE N bản ghi (tất cả các đơn hàng của họ). Điều này vừa chậm chạp vừa dễ gây lỗi.

Bằng cách chuẩn hóa (tách thành bảng `Orders` với khóa ngoại `CustomerID` và bảng `Customers`), khi khách hàng đổi địa chỉ, ứng dụng chỉ cần UPDATE một bản ghi duy nhất trong bảng `Customers`. Tính nhất quán được đảm bảo. Tuy nhiên, cái giá phải trả là: bây giờ, mỗi khi muốn đọc thông tin đơn hàng kèm theo tên và địa chỉ khách hàng, hệ thống luôn phải thực hiện một thao tác JOIN tốn kém giữa hai bảng.

#### 2.2. Denormalization (Phi chuẩn hóa)

**Denormalization** là quá trình "đưa các trường dữ liệu cần thiết", các giá trị được tính toán trước, hoặc dữ liệu trùng lặp một cách có chủ đích vào một cơ sở dữ liệu đã chuẩn hóa. Mục tiêu duy nhất của denormalization là để "tối ưu hóa hiệu suất truy vấn" (tối ưu hóa ĐỌC).

**Ví dụ điển hình:**

Giả sử một hệ thống thương mại điện tử có bảng `Orders` (Đơn hàng) và `Order_Details` (Chi tiết đơn hàng). Để hiển thị tổng số lượng sản phẩm trong một đơn hàng, một truy vấn chuẩn hóa sẽ yêu cầu JOIN hai bảng và dùng hàm `SUM()` trên bảng `Order_Details`. Để phi chuẩn hóa, chúng ta có thể "thêm cột dẫn xuất mới chứa tổng số lượng sản phẩm (`TotalQuantity`)" trực tiếp vào bảng `Orders`.

Denormalization thực chất là một hình thức "caching" ở cấp độ database. Giống như mọi cache, nó mang lại hiệu suất đọc nhanh chóng, nhưng phải trả giá bằng sự phức tạp trong việc "cache invalidation".

Sử dụng ví dụ `TotalQuantity`, lợi ích là một truy vấn `SELECT * FROM Orders` trở nên cực kỳ nhanh, không cần JOIN hay `SUM()`. Cái giá phải trả là: bây giờ, logic ứng dụng (hoặc trigger database) phải chịu trách nhiệm tính toán lại và cập nhật cột `TotalQuantity` này mỗi khi một dòng được INSERT, UPDATE, hoặc DELETE trong bảng `Order_Details`. Nếu logic này thất bại, dữ liệu sẽ trở nên không nhất quán. **Denormalization là một sự đánh đổi rõ ràng: nó chuyển gánh nặng tính toán từ "read-time" sang "write-time".**

#### So sánh Normalization và Denormalization

| Đặc điểm | Normalization | Denormalization |
|----------|---------------|-----------------|
| Mục tiêu chính | Tối ưu hóa GHI, giảm trùng lặp, đảm bảo tính nhất quán | Tối ưu hóa ĐỌC, tăng tốc độ truy vấn |
| Tác động đến Ghi | Nhanh và hiệu quả. Chỉ cập nhật dữ liệu ở một nơi | Chậm hơn. Phải cập nhật dữ liệu ở nhiều nơi và tính toán lại các giá trị dẫn xuất |
| Tác động đến Đọc | Chậm hơn. Thường yêu cầu nhiều thao tác JOIN phức tạp | Nhanh hơn đáng kể. Dữ liệu thường có sẵn trong một bảng duy nhất |
| Tính nhất quán | Cao. Khó xảy ra dị thường dữ liệu | Thấp hơn. Có rủi ro dữ liệu trở nên không nhất quán nếu logic cập nhật thất bại |
| Trường hợp sử dụng | Hệ thống OLTP, nơi tính toàn vẹn dữ liệu là tối quan trọng | Hệ thống OLAP, Data Warehouse, hệ thống báo cáo |

---

### 3. Database Indexes

#### 3.1. Index: "Mục lục" của Database

Trong cơ sở dữ liệu, **Index** là một "cấu trúc dữ liệu" riêng biệt được tạo ra trên một hoặc nhiều cột của bảng. Mục đích của nó là cho phép "tìm kiếm nhanh các bản ghi" bằng cách "giảm thiểu lượng dữ liệu cần phải quét".

Về cơ bản, một index hoạt động giống như mục lục ở cuối một cuốn sách. Thay vì lật từng trang (Full Table Scan) để tìm một chủ đề, bạn tra cứu chủ đề đó trong mục lục (Index Seek), mục lục sẽ cho bạn biết chính xác số trang (pointer) chứa thông tin đó. Một index-file bao gồm các bản ghi chứa "Search-key" (giá trị của cột được đánh index) và "Pointer" (con trỏ đến vị trí của bản ghi đầy đủ trên đĩa).

#### 3.2. Phân tích sâu: B-Tree vs Hash Index

Có hai loại cấu trúc index cơ bản: Ordered (có thứ tự) và Hash (băm).

##### B-Tree Index (Ordered)

Đây là loại index phổ biến nhất và là mặc định trong hầu hết các storage engine quan hệ như InnoDB và MyISAM. B-Tree (Cây B) lưu trữ dữ liệu theo một "cấu trúc cây phân cấp" (cụ thể là cây B+), trong đó các khóa (keys) luôn được duy trì "theo thứ tự".

**Ưu điểm:**
- Vì dữ liệu được sắp xếp, B-Tree không chỉ hiệu quả cho các truy vấn tìm kiếm chính xác (ví dụ: `WHERE id = 10`) mà còn "phù hợp" và hiệu quả cao cho các "range query" (truy vấn phạm vi), ví dụ: `WHERE age > 30` hoặc `WHERE date BETWEEN '2023-01-01' AND '2023-01-31'`
- Hỗ trợ các truy vấn `ORDER BY`

**Nhược điểm:**
- Thường "chậm hơn" Hash Index khi thực hiện tìm kiếm chính xác thuần túy

##### Hash Index

Hash Index (được hỗ trợ bởi các engine như MEMORY/HEAP) sử dụng một "hàm hash" (hàm băm) để ánh xạ khóa index vào một "vị trí cố định" (bucket).

**Ưu điểm:**
- "Đặc biệt nhanh" (độ phức tạp O(1) trong trường hợp lý tưởng) đối với các so sánh bằng chính xác (ví dụ: `WHERE email = '...'`)

**Nhược điểm:**
- Vì hàm băm không bảo toàn thứ tự, dữ liệu không được sắp xếp. Do đó, Hash Index "Không hỗ trợ range query"

**Lưu ý quan trọng:**

Sự lựa chọn giữa B-Tree và Hash không chỉ là về hiệu suất, mà còn là về các toán tử (operators) SQL mà hệ thống có thể sử dụng một cách hiệu quả. Nếu một index kiểu Hash được tạo trên cột `age`, truy vấn `WHERE age = 30` sẽ siêu nhanh. Tuy nhiên, truy vấn `WHERE age > 30` sẽ hoàn toàn không sử dụng được index đó. DBMS sẽ buộc phải thực hiện Full Table Scan, vì hàm băm không lưu trữ `hash(30)` và `hash(31)` cạnh nhau. Ngược lại, B-Tree lưu trữ `30` và `31` theo thứ tự, cho phép nó "đi bộ" trên cây để tìm tất cả các giá trị lớn hơn `30` một cách hiệu quả.

#### 3.3. Tác động hai mặt của Index

Index không phải là một giải pháp miễn phí; nó là một sự đánh đổi.

**Lợi ích (ĐỌC):**
- Cải thiện đáng kể tốc độ của các truy vấn SELECT

**Chi phí (GHI & LƯU TRỮ):**
- **Lưu trữ:** Index "tốn ổ cứng" vì chúng là các cấu trúc dữ liệu riêng biệt, sao chép một phần dữ liệu của bảng
- **Hiệu suất Ghi:** Đây là chi phí lớn nhất. Index "làm chậm các thao tác INSERT và UPDATE"

Tại sao index làm chậm việc ghi? Khi một bản ghi mới được INSERT vào bảng, DBMS không chỉ ghi dữ liệu vào bảng, mà còn phải cập nhật mọi B-Tree index liên quan đến bảng đó. Nó phải chèn "pointer" mới vào đúng vị trí trong cây B-Tree để duy trì trật tự đã sắp xếp. Nếu một bảng có 5 indexes, một thao tác INSERT duy nhất sẽ dẫn đến 6 thao tác ghi I/O (1 vào bảng, 5 vào 5 cây index).

**Quy tắc thiết kế quan trọng:**

- Hệ thống **"Ghi nhiều, Đọc ít"** (Write-Heavy) (ví dụ: hệ thống logging, thu thập dữ liệu IoT) nên có càng ít index càng tốt để tối đa hóa throughput ghi

- Hệ thống **"Đọc nhiều, Ghi ít"** (Read-Heavy) (ví dụ: blog, trang thương mại điện tử, data warehouse) được hưởng lợi từ việc có nhiều index được tối ưu hóa cẩn thận để tăng tốc các truy vấn SELECT

#### So sánh B-Tree và Hash Index

| Đặc điểm | B-Tree Index | Hash Index |
|----------|--------------|------------|
| Cấu trúc | Cấu trúc cây phân cấp, cân bằng, lưu dữ liệu theo thứ tự | Bảng băm, sử dụng hàm băm, dữ liệu không theo thứ tự |
| Tìm kiếm chính xác (=, IN) | Nhanh (O(log N)) | Rất nhanh (O(1) trong trường hợp lý tưởng) |
| Tìm kiếm phạm vi (>, <, BETWEEN) | Hỗ trợ rất tốt | Không hỗ trợ |
| Hỗ trợ ORDER BY | Có, vì dữ liệu đã được sắp xếp | Không, gây khó khăn cho database khi sắp xếp |
| Chi phí Ghi (INSERT/UPDATE) | Trung bình (cần tái cân bằng cây) | Thấp (chỉ cần tính toán hash và chèn) |
| Storage Engine phổ biến | InnoDB, MyISAM | MEMORY/HEAP |

---

## Phần II: Tối ưu hóa Tương tác Ứng dụng

Phần này chuyển trọng tâm từ cấu trúc bên trong database sang lớp tương tác—cách ứng dụng (application code) nói chuyện với database và các cạm bẫy hiệu suất phổ biến nhất phát sinh từ sự tương tác đó.

### 4. ORMs và Vấn đề N+1

#### 4.1. ORM (Object-Relational Mapping): Lớp trừu tượng hóa

**ORM** là một kỹ thuật lập trình "ánh xạ dữ liệu từ cơ sở dữ liệu quan hệ... vào các đối tượng" trong một ngôn ngữ lập trình hướng đối tượng (OOP).

**Ưu điểm của ORM:**

- **Tập trung vào OOP:** Giúp lập trình viên tập trung vào logic nghiệp vụ và thiết kế đối tượng thay vì cấu trúc database
- **Trừu tượng hóa SQL:** "Ẩn chi tiết của những truy vấn SQL". Lập trình viên có thể thực hiện các thao tác CRUD (Create, Read, Update, Delete) mà không cần viết SQL phức tạp
- **Độc lập Database:** Tăng "tính độc lập", cho phép chuyển đổi giữa các loại database khác nhau (ví dụ: từ PostgreSQL sang MySQL) mà không cần thay đổi logic nghiệp vụ
- **Năng suất:** "Viết code ít hơn" và cho phép "tái sử dụng code"

**Nhược điểm của ORM:**

- **Phức tạp:** "Tính phức tạp cao" khi mới tìm hiểu
- **Hạn chế:** "Hạn chế trong khả năng truy vấn". Đôi khi, lập trình viên "vẫn phải dùng đến native SQL" (SQL thuần) cho các truy vấn phức tạp
- **Tối ưu hóa:** "Khó khăn trong việc tối ưu câu lệnh SQL" vì ORM tự động sinh ra các câu lệnh SQL
- **Truy xuất thừa:** Lập trình viên "dễ gặp tình trạng bị truy xuất quá nhiều dữ liệu"

**Vấn đề cốt lõi của ORM:**

Vấn đề cốt lõi của ORM là một "leaky abstraction" (sự trừu tượng hóa bị rò rỉ). ORM hứa hẹn che giấu SQL, nhưng thực tế, để tối ưu hiệu suất, lập trình viên vẫn phải hiểu sâu về SQL.

Sự mâu thuẫn này được thể hiện rõ: ưu điểm là "ẩn chi tiết truy vấn SQL", nhưng nhược điểm là "phải dùng đến native SQL". Như chúng ta sẽ thấy trong phần tiếp theo, cách viết mã ORM "ngây thơ" có thể dẫn đến 1001 truy vấn, trong khi cách viết mã ORM "tối ưu" chỉ tạo ra 2 truy vấn. Cả hai đều là mã ORM, nhưng sự khác biệt nằm ở chỗ người lập trình viên tối ưu hiểu được SQL mà ORM sẽ tạo ra bên dưới. **ORM không giải phóng bạn khỏi SQL; nó chỉ thay đổi cách bạn tương tác với nó.**

#### 4.2. Vấn đề N+1: Thảm họa hiệu suất tiềm ẩn

**Vấn đề N+1** là một thảm họa hiệu suất phổ biến xảy ra khi một ứng dụng thực hiện một truy vấn ban đầu để lấy danh sách các đối tượng, và sau đó, trong một vòng lặp, thực hiện N truy vấn bổ sung để lấy dữ liệu liên quan cho từng đối tượng đó.

**Ví dụ kinh điển:**

1. **Truy vấn 1:** Lấy tất cả người dùng (users). (`SELECT * FROM users`)

2. **Vòng lặp (N truy vấn):** Lặp qua từng user và lấy các bình luận (comments) của họ:
   - `SELECT * FROM comments WHERE user_id = 1`
   - `SELECT * FROM comments WHERE user_id = 2`
   - ...
   - `SELECT * FROM comments WHERE user_id = N`

Nếu có 1000 người dùng, hệ thống sẽ thực hiện **"1001 truy vấn"**. Đây là một vấn đề nghiêm trọng.

Vấn đề này là "lỗi" phổ biến và tốn kém nhất trong các ứng dụng hiện đại, chính xác là bởi vì các ORM làm cho việc truy cập dữ liệu liên quan trở nên quá "dễ dàng" thông qua một kỹ thuật gọi là "Lazy Loading". Lập trình viên chỉ cần gọi `user.comments`, và ORM sẽ "lười biếng" thực thi một truy vấn mới để lấy dữ liệu đó. Trong một vòng lặp, sự tiện lợi này biến thành một thảm họa N+1. Trong SQL thuần, lập trình viên không thể "vô tình" viết 1001 truy vấn; họ sẽ phải có ý thức viết một JOIN ngay từ đầu.

#### 4.3. Giải quyết N+1: Lazy vs Eager Loading

##### Lazy Loading (Tải lười biếng)

Đây là chiến lược tải mặc định trong nhiều ORM. Dữ liệu liên quan (ví dụ: `comments` của `user`) không được tải cùng với đối tượng chính (`user`). Thay vào đó, một truy vấn SELECT riêng biệt được phát ra "tại thời điểm truy cập" (at the time of access)—tức là khi code gọi `user.comments`. Đây chính là nguyên nhân trực tiếp gây ra N truy vấn trong vòng lặp.

##### Eager Loading (Tải chủ động)

Đây là kỹ thuật giải quyết bài toán N+1. Eager Loading là chiến lược tải dữ liệu liên quan "ở phía trước" (at front) hoặc "thủ công", thường là trong cùng một truy vấn ban đầu hoặc ngay sau đó. Lập trình viên phải "tự mình chỉ định" rằng họ muốn tải dữ liệu liên quan.

**Ví dụ:**

Thay vì chỉ lấy `users`, lập trình viên sẽ yêu cầu ORM tải `users` cùng với (with) `comments` của họ. Bằng cách này, ORM có thể tối ưu hóa và giảm 1001 truy vấn xuống chỉ còn 2 truy vấn:

1. `SELECT * FROM users`
2. `SELECT * FROM comments WHERE user_id IN (1, 2, 3,..., 1000)`

**Lưu ý quan trọng:**

Tuy nhiên, Eager Loading không phải lúc nào cũng là giải pháp. Lập trình viên không nên "dùng quá nhiều trong cùng dòng code". Giải pháp cho N+1 không phải là thay thế tất cả Lazy Loading bằng Eager Loading. Nếu một trang API chỉ cần hiển thị tên `user` nhưng lập trình viên lại Eager Load cả `user.posts` (một mối quan hệ 1-N lớn), họ đã lãng phí tài nguyên database và làm chậm truy vấn ban đầu một cách không cần thiết.

**Giải pháp đúng đắn là phân tích từng trường hợp (case-by-case):**
- "Trong API này, tôi có cần hiển thị `comments` không?"
- Nếu có, hãy sử dụng Eager Loading
- Nếu không (ví dụ: chỉ hiển thị tên `user`), hãy dựa vào Lazy Loading (hoặc không tải gì cả) để tránh truy vấn không cần thiết

---

### 5. Nghiên cứu Thực tế: SQLAlchemy

SQLAlchemy là một ORM phổ biến và mạnh mẽ trong hệ sinh thái Python, nổi tiếng với kiến trúc phân lớp rõ ràng và khả năng kiểm soát chi tiết.

#### 5.1. Kiến trúc SQLAlchemy: Core vs ORM và Quản lý Session

SQLAlchemy có hai thành phần chính:
- **Core:** Cung cấp một bộ xây dựng truy vấn SQL (SQL Expression Language) trừu tượng
- **ORM:** Ánh xạ các lớp Python (models) vào các bảng database, sử dụng Core bên dưới

##### Session trong SQLAlchemy

Đối với các hoạt động bền vững (persistence) trong ORM, "giao diện sử dụng chính" là `Session`. `Session` là một đối tượng trung gian quản lý tất cả các đối tượng (models) mà bạn đã tải hoặc liên kết với nó.

**Best practice:** Sử dụng `Session` trong một "Python context manager" (câu lệnh `with:`), điều này đảm bảo `Session` được `close()` đúng cách sau khi khối lệnh kết thúc, giải phóng kết nối về pool.

**Các hoạt động của Session:**

- `add()`: Đưa một đối tượng mới vào `Session` để theo dõi
- `flush()`: Gửi các thay đổi đang chờ (INSERT, UPDATE, DELETE) đến database, nhưng chưa commit transaction
- `commit()`: Cam kết transaction hiện tại, làm cho các thay đổi trở nên vĩnh viễn
- `rollback()`: Hủy bỏ transaction, hoàn tác các thay đổi
- `close()`: Đóng `Session`, giải phóng kết nối

##### Hai mẫu thiết kế quan trọng

`Session` của SQLAlchemy không chỉ đơn giản là một Connection. Nó thực hiện hai mẫu thiết kế quan trọng:

**1. Identity Map:**

`Session` hoạt động như một cache cho các đối tượng nó quản lý. Nếu bạn truy vấn một `User` có `id=5`, `Session` sẽ tạo đối tượng `User` và giữ nó trong bộ nhớ của mình. Nếu bạn truy vấn lại `User` `id=5` trong cùng một `Session`, SQLAlchemy sẽ trả về cùng một đối tượng Python trong bộ nhớ mà không cần thực hiện truy vấn database lần thứ hai.

**2. Unit of Work:**

Bạn có thể thực hiện nhiều thay đổi (thêm `obj1`, sửa `obj2`, xóa `obj3`) trên các đối tượng được `Session` quản lý. Tất cả các thay đổi này được "theo dõi" trong bộ nhớ. Khi bạn gọi `session.commit()`, `Session` sẽ "flush" tất cả các thay đổi đó vào database một cách thông minh bên trong một Transaction duy nhất, đảm bảo tính Atomicity (Chương 1).

#### 5.2. Các kỹ thuật Loading của SQLAlchemy để chống N+1

SQLAlchemy cung cấp các chiến lược Eager Loading mạnh mẽ để giải quyết N+1, chủ yếu là `joinedload()` và `selectinload()`.

##### 1. joinedload() (Joined Loading)

**Cách thức:**

Chiến lược này sử dụng SQL JOIN (thường là LEFT OUTER JOIN) để "tải đồng thời" đối tượng chính và các đối tượng liên quan trong "một truy vấn duy nhất".

**Vấn đề:**

Khi sử dụng `joinedload()` cho một mối quan hệ 1-N (một-tới-nhiều), nó sẽ "khiến các hàng của bảng chính bị nhân bản". Ví dụ, nếu một `User` có 10 `Posts`, truy vấn JOIN sẽ trả về 10 hàng, mỗi hàng chứa cùng một dữ liệu `User` nhưng với một `Post` khác nhau. Điều này đòi hỏi SQLAlchemy phải thực hiện khử trùng lặp ở phía ứng dụng, thường bằng cách yêu cầu lập trình viên gọi phương thức `.unique()` trên kết quả.

**Trường hợp sử dụng:**

`joinedload()` hoạt động tốt nhất cho các mối quan hệ "Nhiều-tới-Một" (many-to-one), ví dụ: tải `Book` và `Author` của nó (`book.author`). Vì mỗi `Book` chỉ có một `Author`, không có sự nhân bản hàng nào xảy ra.

##### 2. selectinload() (Select IN Loading)

**Cách thức:**

Chiến lược này (thay thế cho `subqueryload()` cũ) thực hiện một cách tiếp cận khác, thanh lịch hơn. Nó không sử dụng JOIN. Thay vào đó, nó thực hiện (ít nhất) hai truy vấn:

1. **Truy vấn 1:** Tải các đối tượng chính (ví dụ: `SELECT * FROM users WHERE...`)
2. **Truy vấn 2:** Tải các đối tượng liên quan cho tất cả các đối tượng chính đã tải, bằng cách sử dụng mệnh đề IN (ví dụ: `SELECT * FROM comments WHERE user_id IN (id1, id2, id3,...)`)

**Trường hợp sử dụng:**

`selectinload()` là chiến lược được ưu tiên cho các mối quan hệ "Một-tới-Nhiều" (one-to-many) và "Nhiều-tới-Nhiều" (many-to-many).

**Tại sao selectinload tốt hơn joinedload cho collections?**

`selectinload` hầu như luôn là chiến lược Eager Loading tốt hơn `joinedload` cho các tập hợp (collections, tức là quan hệ 1-N hoặc N-N), vì nó tránh được "thảm họa Cartesian Product" và tạo ra các truy vấn đơn giản, có thể dự đoán được.

**Ví dụ minh họa:**

Hãy tưởng tượng bạn `joinedload` một `User` cùng 3 mối quan hệ 1-N của anh ta: `posts` (10), `comments` (20), và `addresses` (2). Truy vấn SQL kết quả sẽ là một JOIN khổng lồ giữa 4 bảng, và số hàng database trả về sẽ là `1 * 10 * 20 * 2 = 400` hàng. Dữ liệu `User` bị lặp lại 400 lần. Đây là một thảm họa về băng thông mạng và sử dụng bộ nhớ.

`selectinload` giải quyết điều này một cách hiệu quả:
1. Truy vấn 1: `SELECT * FROM users WHERE id = 1` (1 hàng)
2. Truy vấn 2: `SELECT * FROM posts WHERE user_id IN (1)` (10 hàng)
3. Truy vấn 3: `SELECT * FROM comments WHERE user_id IN (1)` (20 hàng)
4. Truy vấn 4: `SELECT * FROM addresses WHERE user_id IN (1)` (2 hàng)

Tổng cộng là 4 truy vấn đơn giản, nhanh chóng, chỉ trả về `1 + 10 + 20 + 2 = 33` hàng, thay vì 1 truy vấn JOIN khổng lồ trả về 400 hàng.

#### So sánh các Kỹ thuật Loading của SQLAlchemy

| Kỹ thuật | Tên (SQLAlchemy) | Số lượng truy vấn | Kiểu truy vấn | Ưu điểm | Nhược điểm | Trường hợp tốt nhất |
|----------|------------------|-------------------|---------------|---------|------------|---------------------|
| Lazy Loading | `lazy='select'` (mặc định) | N+1 | SELECT... WHERE id=? (lặp lại N lần) | Chỉ tải dữ liệu khi cần thiết | Gây ra vấn đề N+1 | Truy cập các mối quan hệ không thường xuyên, ngoài vòng lặp |
| Joined Loading | `options(joinedload(...))` | 1 | SELECT... LEFT OUTER JOIN... | Một truy vấn duy nhất | Gây nhân bản hàng (Cartesian Product), lãng phí băng thông | Quan hệ N-1 (ví dụ: `book.author`) |
| Select IN Loading | `options(selectinload(...))` | 2 (hoặc nhiều hơn) | Q1: SELECT...<br>Q2: SELECT... WHERE... IN (...) | Tránh Cartesian Product. Truy vấn sạch sẽ | Nhiều lượt round-trip đến database (nhưng thường nhanh hơn 1 JOIN lớn) | Quan hệ 1-N và N-N (ví dụ: `user.posts`) |

---

### 6. Phân tích Hiệu suất (Profiling Performance)

#### 6.1. SQL Execution Plan (Query Plan) là gì?

**SQL Execution Plan** (hay Query Plan) là một "kế hoạch chi tiết" hoặc "tập hợp các bước" mà hệ quản trị database sẽ thực hiện để chạy một câu truy vấn SQL. Khi nhận được một truy vấn, Query Optimizer sẽ phân tích và xác định cách thức hiệu quả nhất để lấy dữ liệu: nên sử dụng index nào (nếu có), nên quét bảng nào trước, sử dụng thuật toán JOIN nào (Hash Join, Nested Loop, v.v.).

**Hai loại Execution Plan:**

1. **Estimated Execution Plan (Kế hoạch Ước tính):** Là kế hoạch dự đoán được Optimizer tạo ra trước khi truy vấn thực sự được chạy, dựa trên các thống kê (statistics) mà nó có về dữ liệu

2. **Actual Execution Plan (Kế hoạch Thực tế):** Là kế hoạch thực tế mà database đã sử dụng sau khi chạy truy vấn, kèm theo các số liệu thực tế (ví dụ: số hàng đã đọc)

Việc so sánh giữa Kế hoạch Ước tính và Kế hoạch Thực tế là một công cụ gỡ lỗi hiệu suất cực kỳ mạnh mẽ.

#### 6.2. Cách đọc một Execution Plan (EXPLAIN)

Để xem Execution Plan, hầu hết các database đều cung cấp lệnh `EXPLAIN` (hoặc `EXPLAIN ANALYZE` trong PostgreSQL để có Kế hoạch Thực tế) đặt trước câu lệnh SQL. Trong SQL Server, có các nút trên thanh công cụ để hiển thị kế hoạch đồ họa.

**Các toán tử (Operators) phổ biến:**

- **Table Scan** (hoặc Clustered Index Scan): Quét toàn bộ bảng. Đây thường là toán tử tốn kém nhất
- **Index Seek:** Sử dụng một index (thường là B-Tree) để nhảy thẳng đến dữ liệu cần thiết. Đây là toán tử hiệu quả nhất
- **Index Scan:** Quét toàn bộ index (thay vì toàn bộ bảng)
- **Sort:** Sắp xếp dữ liệu (tốn kém)
- **Hash Join / Nested Loop:** Các thuật toán khác nhau để JOIN bảng

**Mục tiêu chính của tối ưu hóa truy vấn** là chuyển các toán tử "Scan" (Quét) đắt đỏ thành các toán tử "Seek" (Tìm kiếm) rẻ tiền. Khi bạn thấy một Table Scan trên một bảng lớn (hàng triệu hàng), đó là dấu hiệu rõ ràng nhất cho thấy truy vấn của bạn đang thiếu một mệnh đề WHERE hiệu quả, hoặc cột trong mệnh đề WHERE của bạn đang thiếu một Index (như đã thảo luận ở Chương 3).

#### 6.3. Sử dụng Execution Plan để chẩn đoán

Execution Plan giúp lập trình viên "đánh giá hiệu suất" và "xác định được những phần... có thể được tối ưu hóa" hoặc tìm ra "hiện tượng 'bottleneck' (điểm nghẽn)".

**Chỉ số chẩn đoán quan trọng:**

Một trong những chỉ số chẩn đoán quan trọng nhất là so sánh "Estimated Number of Rows" (Số hàng ước tính) với "Actual Number of Rows for All Executions" (Số hàng thực tế).

**Tại sao điều này quan trọng?**

Query Optimizer của database quyết định nên dùng Index Seek (rẻ) hay Table Scan (đắt) dựa trên chi phí ước tính của mỗi thao tác. Chi phí này được tính toán dựa trên thống kê (statistics) về sự phân phối dữ liệu (ví dụ: "Tôi nghĩ rằng cột `status` này có 5 giá trị duy nhất, vì vậy `WHERE status = 'pending'` sẽ trả về 20% dữ liệu của bảng").

Nếu thống kê này bị cũ hoặc sai (ví dụ: dữ liệu bị lệch và `status='pending'` thực tế chỉ chiếm 0.1% dữ liệu), Optimizer có thể đưa ra một quyết định tồi tệ. Nó có thể nghĩ rằng nó cần đọc 20% bảng (một con số lớn) và quyết định rằng Table Scan sẽ nhanh hơn là dùng index.

**Giải pháp:**

Khi bạn xem Actual Plan và thấy Estimated Rows (ví dụ: 1,000,000) chênh lệch rất lớn với Actual Rows (ví dụ: 10), đó là dấu hiệu cho thấy thống kê của database đã lỗi thời. Giải pháp thường là chạy lệnh `ANALYZE` (hoặc `UPDATE STATISTICS`) trên bảng đó để database cập nhật lại thống kê. Với thống kê mới, lần chạy truy vấn tiếp theo, Optimizer sẽ có khả năng chọn được kế hoạch tốt hơn (ví dụ: Index Seek).

---

## Phần III: Kiến trúc Hệ thống Phân tán và Khả năng phục hồi

Phần này giải quyết các thách thức phát sinh khi một database đơn lẻ không còn đủ khả năng đáp ứng về mặt lưu trữ, hiệu suất, hoặc tính sẵn sàng, đòi hỏi chúng ta phải bước vào thế giới của các hệ thống phân tán.

### 7. Failure Modes và Chiến lược Phục hồi

#### 7.1. Các loại lỗi và Chiến lược Backup

Bảo vệ dữ liệu là ưu tiên hàng đầu. Một chiến lược backup và restore (sao lưu và khôi phục) là nền tảng của mọi kế hoạch phục hồi. Trong SQL Server, hành vi ghi log và khả năng phục hồi được quyết định bởi "Recovery Model" (Mô hình phục hồi) của database.

**Ba mô hình phục hồi:**

1. **SIMPLE:**
   - SQL Server tự động xóa các bản ghi transaction log sau khi chúng đã commit
   - Tiết kiệm không gian log nhưng có "rủi ro mất dữ liệu rất cao"
   - Chỉ có thể phục hồi về thời điểm bản backup cuối cùng

2. **FULL:**
   - Mọi transaction đều được ghi lại trong file log và chỉ bị xóa đi sau khi file log đó đã được sao lưu (Log Backup)
   - Cho phép "phục hồi database về một thời điểm cụ thể" (Point-in-Time Recovery)
   - Ví dụ: khôi phục database về trạng thái chính xác lúc 10:05:30 AM

3. **BULK-LOGGED:**
   - Một biến thể của FULL
   - Ghi log tối thiểu cho các hoạt động hàng loạt (như BULK INSERT) để cải thiện hiệu suất

**Các loại backup chính:**

1. **Full Backup (Sao lưu Toàn bộ):** Một bản sao hoàn chỉnh của toàn bộ database. Đây là nền móng của mọi chiến lược phục hồi

2. **Differential Backup (Sao lưu Vi sai):** Chỉ sao lưu những thay đổi đã xảy ra kể từ lần Full Backup gần nhất

3. **Transaction Log Backup (Sao lưu Log Giao dịch):** Chỉ sao lưu các bản ghi transaction (chỉ dùng với mô hình FULL hoặc BULK-LOGGED). Đây là yếu tố cho phép Point-in-Time Recovery

**RPO (Recovery Point Objective):**

Sự lựa chọn Recovery Model thực chất là một quyết định kinh doanh về RPO—tức là doanh nghiệp chấp nhận mất bao nhiêu dữ liệu khi có thảm họa.

- Nếu chọn **SIMPLE** và chạy Full Backup hàng đêm, RPO là 24 giờ. Doanh nghiệp đã chấp nhận mất toàn bộ dữ liệu của 1 ngày làm việc

- Nếu chọn **FULL** và chạy Transaction Log Backup mỗi 15 phút, RPO là 15 phút. Doanh nghiệp có thể khôi phục đến "một thời điểm cụ thể" trước khi thảm họa xảy ra

#### 7.2. Restore và Failover

##### Restore (Phục hồi)

Restore là quá trình lấy một bản backup (từ đêm qua hoặc từ file log 15 phút trước) và khôi phục lại database.

##### Failover (Chuyển đổi dự phòng)

Failover là một "chiến lược giảm thiểu rủi ro" để cải thiện "tính liên tục của dịch vụ" và "giảm downtime". Nó hoạt động bằng cách duy trì một hệ thống dự phòng (thường là một bản sao nóng).

**Kiến trúc cơ bản:**

1. **Primary (Chính):** Máy chủ đang hoạt động, xử lý traffic
2. **Secondary (Phụ):** Máy chủ dự phòng, liên tục sao chép dữ liệu từ Primary và ở trạng thái chờ
3. **Fault Detector (Bộ phát hiện lỗi):** Một thành phần (ví dụ: heartbeat monitoring) liên tục theo dõi "sức khỏe" của Primary

Khi Primary được xác định là "failed" (thất bại), Fault Detector sẽ "tự động... chuyển traffic" đi vào hệ thống Secondary, biến nó thành Primary mới.

**So sánh Restore và Failover:**

Restore và Failover giải quyết hai vấn đề khác nhau:

- **Failover** là một chiến lược chủ động (proactive) để đạt được "High Availability" (Tính sẵn sàng cao - HA). Nó giải quyết **RTO (Recovery Time Objective)**—mất bao lâu để hệ thống hoạt động trở lại? (Với failover, câu trả lời là vài giây đến vài phút)

- **Restore** là một chiến lược phản ứng (reactive) để "Disaster Recovery" (Phục hồi thảm họa - DR). Nó giải quyết **RPO (Recovery Point Objective)**—mất bao nhiêu dữ liệu? (Với restore, câu trả lời là vài phút đến vài giờ, tùy thuộc vào tần suất backup log)

**Lưu ý quan trọng:**

Một hệ thống có tính sẵn sàng cao (dùng Failover) vẫn cần một chiến lược phục hồi thảm họa (dùng Backups) để phòng trường hợp toàn bộ cụm (cluster) (cả Primary và Secondary) bị phá hủy (ví dụ: hỏa hoạn trung tâm dữ liệu).

---

### 8. Database Migration

Migration là một thuật ngữ rộng, bao gồm hai khái niệm rất khác nhau: Schema Migration và Data Migration.

#### 8.1. Phân loại Migration: Schema vs Data

##### 1. Schema Migration (Di chuyển Lược đồ)

Schema Migration đề cập đến việc quản lý các thay đổi cấu trúc database một cách "có phiên bản" (version-controlled), "tăng dần" (incremental) và đôi khi "có thể đảo ngược" (reversible). Các thay đổi này bao gồm `ALTER TABLE`, `CREATE INDEX`, v.v.

Schema Migration là một phần thiết yếu, diễn ra hàng ngày của quy trình DevOps và CI/CD. Các công cụ như Flyway, Alembic, hay golang-migrate được thiết kế để chạy mỗi khi ứng dụng được triển khai (deploy). Chúng so sánh phiên bản hiện tại của database với các file migration trong mã nguồn và tự động áp dụng các thay đổi cần thiết, đảm bảo rằng mã ứng dụng và lược đồ database luôn khớp phiên bản với nhau.

##### 2. Data Migration (Di chuyển Dữ liệu)

Data Migration là "quá trình... chuẩn bị, trích xuất và chuyển đổi dữ liệu" và "chuyển vĩnh viễn" chúng từ hệ thống lưu trữ này sang hệ thống lưu trữ khác.

**Ví dụ bao gồm:**
- Di chuyển từ database on-premises (tại chỗ) lên "đám mây" (Cloud Migration)
- Chuyển đổi giữa các hệ quản trị database khác nhau (ví dụ: từ Oracle sang PostgreSQL, hoặc từ SQL sang NoSQL)

**Sự khác biệt:**

Không giống như Schema Migration (diễn ra hàng ngày), Data Migration thường là một dự án lớn, một lần (hoặc rất ít thường xuyên), đòi hỏi lập kế hoạch cẩn thận, chuẩn bị môi trường đích, và kiểm tra toàn diện.

#### 8.2. Thách thức lớn nhất: Zero-Downtime Migration

Đối với cả hai loại migration, thách thức lớn nhất trong các hệ thống quan trọng là thực hiện chúng mà không gây gián đoạn dịch vụ (Zero Downtime). Downtime có thể xảy ra do "khối lượng dữ liệu" quá lớn (trong Data Migration) hoặc do "thay đổi cấu trúc" database (trong Schema Migration).

**Các nguyên tắc chính:**

Để đạt được Zero-Downtime Migration, các nguyên tắc chính cần tuân thủ là:
- "Tương thích ngược" (backward compatibility)
- "Đảm bảo toàn vẹn dữ liệu" (data integrity)
- "Tối ưu hiệu suất"

**Các chiến lược thường được sử dụng:**
- Blue-green deployments
- Canary releases

##### Tương thích ngược: Chìa khóa tuyệt đối

"Tương thích ngược" là chìa khóa tuyệt đối cho Zero-Downtime Schema Migration. Nó đòi hỏi một quy trình "expand-and-contract" (mở rộng và thu hẹp) gồm nhiều giai đoạn, cho phép "nhiều phiên bản của ứng dụng chạy đồng thời".

**Ví dụ: Đổi tên cột username thành email**

**Cách làm sai (gây downtime):**
- Triển khai mã mới (dùng `email`) và chạy migration (đổi tên cột) cùng lúc
- Sẽ có một khoảng thời gian (downtime) mà code cũ (tìm `username`) hoặc code mới (tìm `email`) bị lỗi

**Cách làm đúng (Zero Downtime "expand-and-contract"):**

1. **Giai đoạn 1 (Mở rộng):** Deploy migration thêm cột `email` (với giá trị `NULL`)

2. **Giai đoạn 2 (Deploy Code v1):** Triển khai mã ứng dụng mới (phiên bản 1) ghi vào cả `username` và `email`, nhưng vẫn đọc từ `username`. (Mã này tương thích ngược với cả schema cũ và mới)

3. **Giai đoạn 3 (Backfill):** Chạy một tiến trình nền để sao chép dữ liệu từ `username` sang `email` cho tất cả các bản ghi cũ (`UPDATE users SET email = username WHERE email IS NULL`)

4. **Giai đoạn 4 (Deploy Code v2):** Triển khai mã ứng dụng (phiên bản 2) bắt đầu đọc từ `email` thay vì `username` (vẫn ghi vào cả hai)

5. **Giai đoạn 5 (Thu dọn):** Deploy mã (phiên bản 3) ngừng ghi vào `username`. Cuối cùng, chạy một migration mới để xóa cột `username`

Đây là một quy trình phức tạp, nhưng nó là cách duy nhất để đảm bảo tính tương thích ngược và không gây gián đoạn dịch vụ.

---

### 9. Data Replication

#### 9.1. Mục tiêu: High Availability và Read Scale

**Replication** (Nhân bản) là quá trình "duy trì nhiều bản sao của dữ liệu" trên nhiều máy chủ khác nhau. Mục tiêu chính của replication là để "cải thiện tính sẵn sàng (availability), khả năng chịu lỗi (fault-tolerance)... và hiệu suất (performance)".

**Lợi ích chính:**

1. **Tính sẵn sàng / Chịu lỗi:** Nếu máy chủ chính (Master) bị hỏng, một bản sao (Slave) có thể được đôn lên làm Master mới (đây chính là cơ chế Failover ở Chương 7)

2. **Hiệu suất:** Các truy vấn ĐỌC (SELECT) có thể được phân phối đến nhiều máy chủ Slave, giảm tải cho máy chủ Master

#### 9.2. Mô hình Master-Slave

Mô hình phổ biến nhất là Master-Slave.

**Các thành phần:**

1. **Master (Chủ):**
   - Là database "chính", "có tất cả quyền hạn"
   - Đây là nơi duy nhất nhận các thao tác GHI (INSERT, UPDATE, DELETE)

2. **Slave (Tớ):**
   - Là các database "chịu sự điều khiển"
   - Sao chép (đồng bộ hóa) dữ liệu từ Master

**Luồng hoạt động:**

Trong một hệ thống điển hình, "mọi request [ghi] sẽ được đưa vào MySQL master". Các máy chủ Slave được sử dụng để xử lý các request đọc hoặc để dự phòng khi "MySQL Master gặp sự cố".

**Ưu điểm và hạn chế:**

Mô hình Master-Slave giải quyết xuất sắc vấn đề "mở rộng đọc" (Read Scalability). Bạn có thể có 1 Master và 100 Slaves để xử lý lưu lượng đọc gấp 100 lần.

Tuy nhiên, nó **không giải quyết vấn đề "mở rộng ghi" (Write Scalability)**. Tất cả các lượt ghi vẫn phải đi qua một nút Master duy nhất. Nếu ứng dụng của bạn bị giới hạn bởi hiệu suất ghi (ví dụ: một mạng xã hội có hàng ngàn lượt đăng bài mỗi giây), mô hình Master-Slave là không đủ.

#### 9.3. Đánh đổi cốt lõi: Synchronous vs Asynchronous

Cách thức Master sao chép dữ liệu cho Slave quyết định các đặc tính cốt lõi của hệ thống.

##### Synchronous Replication (Sao chép Đồng bộ)

**Cách thức:**

Dữ liệu được ghi vào Primary (Master) và Replica (Slave) "đồng thời" (simultaneously). Khi ứng dụng gửi một lệnh GHI, Master sẽ GHI vào đĩa của mình, sau đó gửi cho Slave, và chỉ báo cáo thành công cho ứng dụng sau khi cả Slave cũng xác nhận đã GHI thành công.

**Ưu điểm:**
- Đảm bảo "Strong Consistency" (Tính nhất quán mạnh)
- Dữ liệu trên Master và Slave luôn giống hệt nhau
- "RPO (Mục tiêu điểm phục hồi) bằng không"

**Nhược điểm:**
- "Gây ra độ trễ (latency)"
- Thao tác GHI của ứng dụng bây giờ phải chờ đợi round-trip mạng đến Slave, làm chậm ứng dụng chính
- Thường chỉ hoạt động hiệu quả ở khoảng cách ngắn (dưới 300 km)

##### Asynchronous Replication (Sao chép Bất đồng bộ)

**Cách thức:**

Dữ liệu được ghi vào Primary (Master) trước, và Master báo cáo thành công cho ứng dụng ngay lập tức. Sau đó, ở chế độ nền, Master mới gửi các thay đổi đó cho Replica (Slave). (Replication mặc định của MySQL là bất đồng bộ).

**Ưu điểm:**
- Độ trễ GHI cực thấp (low latency), vì ứng dụng không phải chờ Slave
- Hoạt động tốt ở khoảng cách xa

**Nhược điểm:**
- "Delayed" (bị trễ)
- Chỉ đạt được "Eventual Consistency" (Tính nhất quán cuối cùng)
- Có "rủi ro mất dữ liệu": nếu Master bị hỏng ngay sau khi báo cáo thành công cho ứng dụng nhưng trước khi kịp gửi thay đổi đó cho Slave, thay đổi đó sẽ bị mất vĩnh viễn

##### Liên kết với CAP Theorem

Sự lựa chọn giữa Đồng bộ và Bất đồng bộ là một ví dụ hoàn hảo về sự đánh đổi trong Định lý CAP (sẽ thảo luận ở Chương 11).

**Replication Đồng bộ** là một hệ thống **CP** (Consistency, Partition Tolerance):
- Khi có sự cố mạng (Partition - P), Master không thể nhận xác nhận từ Slave
- Để đảm bảo Consistency (C) (dữ liệu trên Master và Slave giống hệt nhau), Master phải từ chối GHI
- Nó đã hy sinh Availability (A) (khả năng GHI của hệ thống)

**Replication Bất đồng bộ** là một hệ thống **AP** (Availability, Partition Tolerance):
- Khi có sự cố mạng (Partition - P), Master vẫn tiếp tục nhận GHI (ưu tiên Availability (A)) và báo cáo thành công
- Nó hy sinh Consistency (C) (vì Slave sẽ bị tụt hậu) và có nguy cơ mất dữ liệu

#### So sánh Replication Đồng bộ và Bất đồng bộ

| Đặc điểm | Replication Đồng bộ | Replication Bất đồng bộ |
|----------|---------------------|-------------------------|
| Luồng Ghi dữ liệu | Ghi vào Master → Ghi vào Slave → Báo cáo thành công | Ghi vào Master → Báo cáo thành công → Ghi vào Slave (sau) |
| Độ trễ khi Ghi (Write Latency) | Cao (bị ảnh hưởng bởi round-trip mạng) | Rất thấp (chỉ phụ thuộc vào Master) |
| Tính nhất quán (Consistency) | Mạnh (Strong Consistency) | Cuối cùng (Eventual Consistency) |
| Rủi ro mất dữ liệu (Data Loss) | Không (Zero RPO) | Có (Nếu Master hỏng trước khi sao chép) |
| Liên kết với CAP | Ưu tiên Consistency (CP) | Ưu tiên Availability (AP) |

---

### 10. Sharding Strategies

#### 10.1. Sharding là gì: Vượt qua giới hạn Write Scale

**Sharding** (Phân mảnh) là "công việc tách Database thành nhiều Database khác nhau", mỗi database (được gọi là một shard hay phân mảnh) "sẽ chứa 1 phần dữ liệu". Đây là một kỹ thuật "phân vùng ngang" (horizontal partition).

**Ví dụ:**

Thay vì có 1 bảng `Users` khổng lồ với 1 tỷ người dùng, Sharding sẽ chia nó thành 1000 bảng `Users` nhỏ hơn (mỗi bảng 1 triệu người dùng), và mỗi bảng này nằm trên một máy chủ database riêng biệt.

**Khi nào cần Sharding?**

Sharding là bước đi logic tiếp theo khi Replication (Chương 9) không còn đủ. Như đã phân tích, Replication Master-Slave giải quyết "mở rộng đọc", nhưng vẫn có một điểm nghẽn (bottleneck) là một Master duy nhất phải xử lý tất cả các lượt ghi.

**Ví dụ thực tế:**

Trong ví dụ của Instagram, với hàng ngàn bài đăng mỗi giây, một Master duy nhất không thể xử lý nổi khối lượng GHI đó. Sharding giải quyết điều này bằng cách chia 1 tỷ người dùng ra 1000 shards. Giả sử lưu lượng GHI được phân bổ đều, mỗi shard bây giờ chỉ phải xử lý 1/1000 lưu lượng GHI ban đầu. **Đây là cách duy nhất để mở rộng quy mô GHI (Write Scalability) gần như vô hạn.**

#### 10.2. Các chiến lược Sharding và Thách thức

**Hai chiến lược phổ biến nhất:**

1. **Key-based (Algorithmic) Sharding:**
   - Sử dụng một "shard key" (ví dụ: `user_id`)
   - Và một hàm băm (ví dụ: `hash(user_id) % N_shards`) để quyết định dữ liệu sẽ nằm ở shard nào

2. **Range-based Sharding:**
   - Chia theo phạm vi (ví dụ: User A-D ở Shard 1, E-H ở Shard 2)

**Sự phức tạp của Sharding:**

Sharding là một giải pháp cực kỳ mạnh mẽ nhưng cũng vô cùng phức tạp. Nó "đòi hỏi một cách tiếp cận 'tự làm'" và "tài liệu... rất khó tìm". Đó là lý do đề xuất các giải pháp thay thế đơn giản hơn trước (như "thực hiện caching" hoặc "nâng cấp lên server lớn hơn" – còn gọi là vertical scaling), ngụ ý sharding là giải pháp cuối cùng.

**Các thách thức chính:**

Sharding biến database của bạn từ một thực thể đơn giản thành một hệ thống phân tán phức tạp, và lập trình viên (hoặc lớp hạ tầng) phải gánh chịu sự phức tạp đó:

1. **Routing (Định tuyến):**
   - Lớp ứng dụng của bạn bây giờ phải có một "Routing Layer" đủ thông minh
   - Biết `user_id = 500` thì truy vấn Shard 5, nhưng `user_id = 1050` thì truy vấn Shard 11

2. **Cross-shard JOINs / Transactions:**
   - Đây là vấn đề lớn nhất
   - Làm thế nào để JOIN bảng `Users` (ở Shard 1) với `Posts` (ở Shard 2)?
   - Hoặc thực hiện một transaction ACID (Chương 1) trên cả hai shards?
   - Hầu hết các database sharded không hỗ trợ điều này
   - Các thao tác này phải được thực hiện ở cấp độ ứng dụng (Application-level JOIN/Transaction) – rất phức tạp và khó đảm bảo tính nhất quán

3. **Rebalancing (Tái cân bằng):**
   - Điều gì xảy ra khi Shard 1 bị đầy (ví dụ: "hot shard") trong khi Shard 2 vẫn trống?
   - Việc di chuyển dữ liệu giữa các shards (rebalancing) là một hoạt động cực kỳ nguy hiểm và phức tạp
   - Có nguy cơ làm mất dữ liệu hoặc gây downtime

---

### 11. CAP Theorem

Định lý CAP, do Giáo sư Eric Brewer phát biểu, là lý thuyết nền tảng giải thích cho tất cả các đánh đổi mà chúng ta đã thảo luận trong Phần III.

#### 11.1. Giải thích CAP: C-A-P

Định lý CAP phát biểu rằng trong một "hệ thống lưu trữ phân tán", không thể đồng thời đảm bảo cả ba tính chất sau đây cùng một lúc:

**C - Consistency (Tính nhất quán):**
- Tính nhất quán trong CAP khác với C trong ACID
- Ở đây, nó có nghĩa là "mọi lượt đọc đều nhận được nội dung mới nhất" hoặc lỗi
- Tất cả các clients "thấy cùng một dữ liệu tại cùng một thời điểm", bất kể họ kết nối đến node nào

**A - Availability (Tính sẵn sàng):**
- Mọi yêu cầu (request) gửi đến một node đang hoạt động đều phải nhận được phản hồi (không phải lỗi)
- Hệ thống luôn sẵn sàng cho cả ĐỌC và GHI

**P - Partition Tolerance (Khả năng chịu lỗi phân vùng):**
- Hệ thống "tiếp tục hoạt động" bất chấp "trục trặc mạng giữa các nodes"
- "Phân vùng" (Partition) là một sự cố truyền thông (mất gói tin, mạng chậm) làm các nodes không thể liên lạc được với nhau

#### 11.2. Đánh đổi thực tế: CP vs AP

Trong một hệ thống phân tán (bao gồm nhiều nodes), lỗi mạng (P) là không thể tránh khỏi và là một điều "bắt buộc" (must) phải có khả năng xử lý. Do đó, **sự đánh đổi thực sự không phải là chọn 2 trong 3, mà là: Khi một phân vùng mạng (P) xảy ra, bạn phải chọn hy sinh Consistency (C) hay Availability (A).**

Điều này chia các hệ thống phân tán làm hai loại chính:

##### Hệ thống CP (Consistent and Partition Tolerant)

**Đặc điểm:**
- Khi có lỗi mạng (P), hệ thống ưu tiên Consistency (C)
- Để đảm bảo mọi lượt đọc đều nhận được dữ liệu mới nhất (C), hệ thống phải ngừng chấp nhận các thao tác GHI (hoặc thậm chí cả ĐỌC) ở phía bị phân vùng
- Nó hy sinh Availability (A) để đảm bảo tính nhất quán

**Ví dụ:**
- Các hệ thống database quan hệ dùng Replication Đồng bộ (Chương 9)
- Các hệ thống yêu cầu giao dịch tài chính chặt chẽ

##### Hệ thống AP (Available and Partition Tolerant)

**Đặc điểm:**
- Khi có lỗi mạng (P), hệ thống ưu tiên Availability (A)
- Các nodes ở mỗi bên của phân vùng vẫn tiếp tục chấp nhận các thao tác ĐỌC và GHI
- Nó hy sinh Consistency (C). Dữ liệu trên hệ thống sẽ trở nên không nhất quán (ví dụ: một node có dữ liệu cũ hơn node kia) cho đến khi phân vùng mạng được giải quyết và các nodes có thể đồng bộ hóa lại (đạt được "Eventual Consistency")

**Ví dụ:**
- Cassandra, HBase
- Các hệ thống NoSQL
- Mạng xã hội (thà hiển thị một "like count" cũ còn hơn là không hiển thị gì cả)

##### Thế còn Hệ thống CA?

Hệ thống CA (Consistent and Available) cung cấp C và A, nhưng không thể chịu lỗi phân vùng (P). Trong thực tế, đây chính là các database chạy trên một instance độc lập (single-node). Một database chạy trên một máy chủ duy nhất thì không có "phân vùng mạng" (P) để mà chịu lỗi. Nó hoàn hảo về C (ACID) và A (miễn là nó không sập), nhưng nó không thể mở rộng quy mô.

#### 11.3. CAP trong thực tế: Kết nối toàn bộ Phần III

Định lý CAP không có ý nghĩa trong một database đơn (Chương 1, 2, 3). Nó chỉ áp dụng khi bạn bắt đầu phân tán hệ thống (Chương 9, 10). **CAP là lý thuyết nền tảng giải thích cho tất cả các đánh đổi kiến trúc trong Phần III.**

**Liên kết với Chương 9 (Replication):**
- **Sync Replication** là một thiết kế CP. Nó ưu tiên C (Master và Slave giống hệt nhau) và hy sinh A (Master phải chặn GHI nếu Slave mất kết nối)
- **Async Replication** là một thiết kế AP. Nó ưu tiên A (Master luôn GHI) và hy sinh C (Slave có thể bị trễ hoặc mất dữ liệu)

**Liên kết với Chương 10 (Sharding):**
- Một hệ thống sharded thường được thiết kế là AP
- Nếu một shard (ví dụ: Shard 5) bị sập mạng (P), hệ thống vẫn hoạt động (A) cho tất cả các shards khác
- Nó chỉ thất bại khi truy cập Shard 5
- Nó hy sinh tính nhất quán toàn cục (global consistency) (ví dụ: không thể thực hiện transaction ACID trên Shard 5 và Shard 6)

**Liên kết với Chương 1 (ACID):**
- ACID với thuộc tính "C" (Consistency) mạnh mẽ, là đặc trưng của các hệ thống CA (RDBMS truyền thống)
- Khi các hệ thống (thường là NoSQL) chọn mô hình AP để đạt được quy mô và tính sẵn sàng, họ thường phải hy sinh các đảm bảo ACID nghiêm ngặt
- Điều này dẫn đến một mô hình thay thế gọi là **BASE** (Basically Available, Soft state, Eventual consistency)—một mô hình chấp nhận tính nhất quán cuối cùng để đổi lấy tính sẵn sàng cao

#### So sánh Hệ thống CP và AP theo CAP

| Đặc điểm | Hệ thống CP (Ưu tiên Consistency) | Hệ thống AP (Ưu tiên Availability) |
|----------|-----------------------------------|-----------------------------------|
| Ưu tiên khi có lỗi mạng (P) | Tính nhất quán (Consistency) | Tính sẵn sàng (Availability) |
| Hành vi khi có lỗi mạng (P) | Từ chối GHI (hoặc ĐỌC) ở phía bị ảnh hưởng để tránh dữ liệu không nhất quán | Vẫn chấp nhận Gi "sức khỏe" của Primary

Khi Primary được xác định là "failed" (thất bại), Fault Detector sẽ "tự động... chuyển traffic" đi vào hệ thống Secondary, biến nó thành Primary mới.

**So sánh Restore và Failover:**

Restore và Failover giải quyết hai vấn đề khác nhau:

- **Failover** là một chiến lược chủ động (proactive) để đạt được "High Availability" (Tính sẵn sàng cao - HA). Nó giải quyết **RTO (Recovery Time Objective)**—mất bao lâu để hệ thống hoạt động trở lại? (Với failover, câu trả lời là vài giây đến vài phút)

- **Restore** là một chiến lược phản ứng (reactive) để "Disaster Recovery" (Phục hồi thảm họa - DR). Nó giải quyết **RPO (Recovery Point Objective)**—mất bao nhiêu dữ liệu? (Với restore, câu trả lời là vài phút đến vài giờ, tùy thuộc vào tần suất backup log)

**Lưu ý quan trọng:**

Một hệ thống có tính sẵn sàng cao (dùng Failover) vẫn cần một chiến lược phục hồi thảm họa (dùng Backups) để phòng trường hợp toàn bộ cụm (cluster) (cả Primary và Secondary) bị phá hủy (ví dụ: hỏa hoạn trung tâm dữ liệu).

---

### 8. Database Migration

Migration là một thuật ngữ rộng, bao gồm hai khái niệm rất khác nhau: Schema Migration và Data Migration.

#### 8.1. Phân loại Migration: Schema vs Data

##### 1. Schema Migration (Di chuyển Lược đồ)

Schema Migration đề cập đến việc quản lý các thay đổi cấu trúc database một cách "có phiên bản" (version-controlled), "tăng dần" (incremental) và đôi khi "có thể đảo ngược" (reversible). Các thay đổi này bao gồm `ALTER TABLE`, `CREATE INDEX`, v.v.

Schema Migration là một phần thiết yếu, diễn ra hàng ngày của quy trình DevOps và CI/CD. Các công cụ như Flyway, Alembic, hay golang-migrate được thiết kế để chạy mỗi khi ứng dụng được triển khai (deploy). Chúng so sánh phiên bản hiện tại của database với các file migration trong mã nguồn và tự động áp dụng các thay đổi cần thiết, đảm bảo rằng mã ứng dụng và lược đồ database luôn khớp phiên bản với nhau.

##### 2. Data Migration (Di chuyển Dữ liệu)

Data Migration là "quá trình... chuẩn bị, trích xuất và chuyển đổi dữ liệu" và "chuyển vĩnh viễn" chúng từ hệ thống lưu trữ này sang hệ thống lưu trữ khác.

**Ví dụ bao gồm:**
- Di chuyển từ database on-premises (tại chỗ) lên "đám mây" (Cloud Migration)
- Chuyển đổi giữa các hệ quản trị database khác nhau (ví dụ: từ Oracle sang PostgreSQL, hoặc từ SQL sang NoSQL)

**Sự khác biệt:**

Không giống như Schema Migration (diễn ra hàng ngày), Data Migration thường là một dự án lớn, một lần (hoặc rất ít thường xuyên), đòi hỏi lập kế hoạch cẩn thận, chuẩn bị môi trường đích, và kiểm tra toàn diện.

#### 8.2. Thách thức lớn nhất: Zero-Downtime Migration

Đối với cả hai loại migration, thách thức lớn nhất trong các hệ thống quan trọng là thực hiện chúng mà không gây gián đoạn dịch vụ (Zero Downtime). Downtime có thể xảy ra do "khối lượng dữ liệu" quá lớn (trong Data Migration) hoặc do "thay đổi cấu trúc" database (trong Schema Migration).

**Các nguyên tắc chính:**

Để đạt được Zero-Downtime Migration, các nguyên tắc chính cần tuân thủ là:
- "Tương thích ngược" (backward compatibility)
- "Đảm bảo toàn vẹn dữ liệu" (data integrity)
- "Tối ưu hiệu suất"

**Các chiến lược thường được sử dụng:**
- Blue-green deployments
- Canary releases

##### Tương thích ngược: Chìa khóa tuyệt đối

"Tương thích ngược" là chìa khóa tuyệt đối cho Zero-Downtime Schema Migration. Nó đòi hỏi một quy trình "expand-and-contract" (mở rộng và thu hẹp) gồm nhiều giai đoạn, cho phép "nhiều phiên bản của ứng dụng chạy đồng thời".

**Ví dụ: Đổi tên cột username thành email**

**Cách làm sai (gây downtime):**
- Triển khai mã mới (dùng `email`) và chạy migration (đổi tên cột) cùng lúc
- Sẽ có một khoảng thời gian (downtime) mà code cũ (tìm `username`) hoặc code mới (tìm `email`) bị lỗi

**Cách làm đúng (Zero Downtime "expand-and-contract"):**

1. **Giai đoạn 1 (Mở rộng):** Deploy migration thêm cột `email` (với giá trị `NULL`)

2. **Giai đoạn 2 (Deploy Code v1):** Triển khai mã ứng dụng mới (phiên bản 1) ghi vào cả `username` và `email`, nhưng vẫn đọc từ `username`. (Mã này tương thích ngược với cả schema cũ và mới)

3. **Giai đoạn 3 (Backfill):** Chạy một tiến trình nền để sao chép dữ liệu từ `username` sang `email` cho tất cả các bản ghi cũ (`UPDATE users SET email = username WHERE email IS NULL`)

4. **Giai đoạn 4 (Deploy Code v2):** Triển khai mã ứng dụng (phiên bản 2) bắt đầu đọc từ `email` thay vì `username` (vẫn ghi vào cả hai)

5. **Giai đoạn 5 (Thu dọn):** Deploy mã (phiên bản 3) ngừng ghi vào `username`. Cuối cùng, chạy một migration mới để xóa cột `username`

Đây là một quy trình phức tạp, nhưng nó là cách duy nhất để đảm bảo tính tương thích ngược và không gây gián đoạn dịch vụ.

---

### 9. Data Replication

#### 9.1. Mục tiêu: High Availability và Read Scale

**Replication** (Nhân bản) là quá trình "duy trì nhiều bản sao của dữ liệu" trên nhiều máy chủ khác nhau. Mục tiêu chính của replication là để "cải thiện tính sẵn sàng (availability), khả năng chịu lỗi (fault-tolerance)... và hiệu suất (performance)".

**Lợi ích chính:**

1. **Tính sẵn sàng / Chịu lỗi:** Nếu máy chủ chính (Master) bị hỏng, một bản sao (Slave) có thể được đôn lên làm Master mới (đây chính là cơ chế Failover ở Chương 7)

2. **Hiệu suất:** Các truy vấn ĐỌC (SELECT) có thể được phân phối đến nhiều máy chủ Slave, giảm tải cho máy chủ Master

#### 9.2. Mô hình Master-Slave

Mô hình phổ biến nhất là Master-Slave.

**Các thành phần:**

1. **Master (Chủ):**
   - Là database "chính", "có tất cả quyền hạn"
   - Đây là nơi duy nhất nhận các thao tác GHI (INSERT, UPDATE, DELETE)

2. **Slave (Tớ):**
   - Là các database "chịu sự điều khiển"
   - Sao chép (đồng bộ hóa) dữ liệu từ Master

**Luồng hoạt động:**

Trong một hệ thống điển hình, "mọi request [ghi] sẽ được đưa vào MySQL master". Các máy chủ Slave được sử dụng để xử lý các request đọc hoặc để dự phòng khi "MySQL Master gặp sự cố".

**Ưu điểm và hạn chế:**

Mô hình Master-Slave giải quyết xuất sắc vấn đề "mở rộng đọc" (Read Scalability). Bạn có thể có 1 Master và 100 Slaves để xử lý lưu lượng đọc gấp 100 lần.

Tuy nhiên, nó **không giải quyết vấn đề "mở rộng ghi" (Write Scalability)**. Tất cả các lượt ghi vẫn phải đi qua một nút Master duy nhất. Nếu ứng dụng của bạn bị giới hạn bởi hiệu suất ghi (ví dụ: một mạng xã hội có hàng ngàn lượt đăng bài mỗi giây), mô hình Master-Slave là không đủ.

#### 9.3. Đánh đổi cốt lõi: Synchronous vs Asynchronous

Cách thức Master sao chép dữ liệu cho Slave quyết định các đặc tính cốt lõi của hệ thống.

##### Synchronous Replication (Sao chép Đồng bộ)

**Cách thức:**

Dữ liệu được ghi vào Primary (Master) và Replica (Slave) "đồng thời" (simultaneously). Khi ứng dụng gửi một lệnh GHI, Master sẽ GHI vào đĩa của mình, sau đó gửi cho Slave, và chỉ báo cáo thành công cho ứng dụng sau khi cả Slave cũng xác nhận đã GHI thành công.

**Ưu điểm:**
- Đảm bảo "Strong Consistency" (Tính nhất quán mạnh)
- Dữ liệu trên Master và Slave luôn giống hệt nhau
- "RPO (Mục tiêu điểm phục hồi) bằng không"

**Nhược điểm:**
- "Gây ra độ trễ (latency)"
- Thao tác GHI của ứng dụng bây giờ phải chờ đợi round-trip mạng đến Slave, làm chậm ứng dụng chính
- Thường chỉ hoạt động hiệu quả ở khoảng cách ngắn (dưới 300 km)

##### Asynchronous Replication (Sao chép Bất đồng bộ)

**Cách thức:**

Dữ liệu được ghi vào Primary (Master) trước, và Master báo cáo thành công cho ứng dụng ngay lập tức. Sau đó, ở chế độ nền, Master mới gửi các thay đổi đó cho Replica (Slave). (Replication mặc định của MySQL là bất đồng bộ).

**Ưu điểm:**
- Độ trễ GHI cực thấp (low latency), vì ứng dụng không phải chờ Slave
- Hoạt động tốt ở khoảng cách xa

**Nhược điểm:**
- "Delayed" (bị trễ)
- Chỉ đạt được "Eventual Consistency" (Tính nhất quán cuối cùng)
- Có "rủi ro mất dữ liệu": nếu Master bị hỏng ngay sau khi báo cáo thành công cho ứng dụng nhưng trước khi kịp gửi thay đổi đó cho Slave, thay đổi đó sẽ bị mất vĩnh viễn

##### Liên kết với CAP Theorem

Sự lựa chọn giữa Đồng bộ và Bất đồng bộ là một ví dụ hoàn hảo về sự đánh đổi trong Định lý CAP (sẽ thảo luận ở Chương 11).

**Replication Đồng bộ** là một hệ thống **CP** (Consistency, Partition Tolerance):
- Khi có sự cố mạng (Partition - P), Master không thể nhận xác nhận từ Slave
- Để đảm bảo Consistency (C) (dữ liệu trên Master và Slave giống hệt nhau), Master phải từ chối GHI
- Nó đã hy sinh Availability (A) (khả năng GHI của hệ thống)

**Replication Bất đồng bộ** là một hệ thống **AP** (Availability, Partition Tolerance):
- Khi có sự cố mạng (Partition - P), Master vẫn tiếp tục nhận GHI (ưu tiên Availability (A)) và báo cáo thành công
- Nó hy sinh Consistency (C) (vì Slave sẽ bị tụt hậu) và có nguy cơ mất dữ liệu

#### So sánh Replication Đồng bộ và Bất đồng bộ

| Đặc điểm | Replication Đồng bộ | Replication Bất đồng bộ |
|----------|---------------------|-------------------------|
| Luồng Ghi dữ liệu | Ghi vào Master → Ghi vào Slave → Báo cáo thành công | Ghi vào Master → Báo cáo thành công → Ghi vào Slave (sau) |
| Độ trễ khi Ghi (Write Latency) | Cao (bị ảnh hưởng bởi round-trip mạng) | Rất thấp (chỉ phụ thuộc vào Master) |
| Tính nhất quán (Consistency) | Mạnh (Strong Consistency) | Cuối cùng (Eventual Consistency) |
| Rủi ro mất dữ liệu (Data Loss) | Không (Zero RPO) | Có (Nếu Master hỏng trước khi sao chép) |
| Liên kết với CAP | Ưu tiên Consistency (CP) | Ưu tiên Availability (AP) |

---

### 10. Sharding Strategies

#### 10.1. Sharding là gì: Vượt qua giới hạn Write Scale

**Sharding** (Phân mảnh) là "công việc tách Database thành nhiều Database khác nhau", mỗi database (được gọi là một shard hay phân mảnh) "sẽ chứa 1 phần dữ liệu". Đây là một kỹ thuật "phân vùng ngang" (horizontal partition).

**Ví dụ:**

Thay vì có 1 bảng `Users` khổng lồ với 1 tỷ người dùng, Sharding sẽ chia nó thành 1000 bảng `Users` nhỏ hơn (mỗi bảng 1 triệu người dùng), và mỗi bảng này nằm trên một máy chủ database riêng biệt.

**Khi nào cần Sharding?**

Sharding là bước đi logic tiếp theo khi Replication (Chương 9) không còn đủ. Như đã phân tích, Replication Master-Slave giải quyết "mở rộng đọc", nhưng vẫn có một điểm nghẽn (bottleneck) là một Master duy nhất phải xử lý tất cả các lượt ghi.

**Ví dụ thực tế:**

Trong ví dụ của Instagram, với hàng ngàn bài đăng mỗi giây, một Master duy nhất không thể xử lý nổi khối lượng GHI đó. Sharding giải quyết điều này bằng cách chia 1 tỷ người dùng ra 1000 shards. Giả sử lưu lượng GHI được phân bổ đều, mỗi shard bây giờ chỉ phải xử lý 1/1000 lưu lượng GHI ban đầu. **Đây là cách duy nhất để mở rộng quy mô GHI (Write Scalability) gần như vô hạn.**

#### 10.2. Các chiến lược Sharding và Thách thức

**Hai chiến lược phổ biến nhất:**

1. **Key-based (Algorithmic) Sharding:**
   - Sử dụng một "shard key" (ví dụ: `user_id`)
   - Và một hàm băm (ví dụ: `hash(user_id) % N_shards`) để quyết định dữ liệu sẽ nằm ở shard nào

2. **Range-based Sharding:**
   - Chia theo phạm vi (ví dụ: User A-D ở Shard 1, E-H ở Shard 2)

**Sự phức tạp của Sharding:**

Sharding là một giải pháp cực kỳ mạnh mẽ nhưng cũng vô cùng phức tạp. Nó "đòi hỏi một cách tiếp cận 'tự làm'" và "tài liệu... rất khó tìm". Đó là lý do đề xuất các giải pháp thay thế đơn giản hơn trước (như "thực hiện caching" hoặc "nâng cấp lên server lớn hơn" – còn gọi là vertical scaling), ngụ ý sharding là giải pháp cuối cùng.

**Các thách thức chính:**

Sharding biến database của bạn từ một thực thể đơn giản thành một hệ thống phân tán phức tạp, và lập trình viên (hoặc lớp hạ tầng) phải gánh chịu sự phức tạp đó:

1. **Routing (Định tuyến):**
   - Lớp ứng dụng của bạn bây giờ phải có một "Routing Layer" đủ thông minh
   - Biết `user_id = 500` thì truy vấn Shard 5, nhưng `user_id = 1050` thì truy vấn Shard 11

2. **Cross-shard JOINs / Transactions:**
   - Đây là vấn đề lớn nhất
   - Làm thế nào để JOIN bảng `Users` (ở Shard 1) với `Posts` (ở Shard 2)?
   - Hoặc thực hiện một transaction ACID (Chương 1) trên cả hai shards?
   - Hầu hết các database sharded không hỗ trợ điều này
   - Các thao tác này phải được thực hiện ở cấp độ ứng dụng (Application-level JOIN/Transaction) – rất phức tạp và khó đảm bảo tính nhất quán

3. **Rebalancing (Tái cân bằng):**
   - Điều gì xảy ra khi Shard 1 bị đầy (ví dụ: "hot shard") trong khi Shard 2 vẫn trống?
   - Việc di chuyển dữ liệu giữa các shards (rebalancing) là một hoạt động cực kỳ nguy hiểm và phức tạp
   - Có nguy cơ làm mất dữ liệu hoặc gây downtime

---

### 11. CAP Theorem

Định lý CAP, do Giáo sư Eric Brewer phát biểu, là lý thuyết nền tảng giải thích cho tất cả các đánh đổi mà chúng ta đã thảo luận trong Phần III.

#### 11.1. Giải thích CAP: C-A-P

Định lý CAP phát biểu rằng trong một "hệ thống lưu trữ phân tán", không thể đồng thời đảm bảo cả ba tính chất sau đây cùng một lúc:

**C - Consistency (Tính nhất quán):**
- Tính nhất quán trong CAP khác với C trong ACID
- Ở đây, nó có nghĩa là "mọi lượt đọc đều nhận được nội dung mới nhất" hoặc lỗi
- Tất cả các clients "thấy cùng một dữ liệu tại cùng một thời điểm", bất kể họ kết nối đến node nào

**A - Availability (Tính sẵn sàng):**
- Mọi yêu cầu (request) gửi đến một node đang hoạt động đều phải nhận được phản hồi (không phải lỗi)
- Hệ thống luôn sẵn sàng cho cả ĐỌC và GHI

**P - Partition Tolerance (Khả năng chịu lỗi phân vùng):**
- Hệ thống "tiếp tục hoạt động" bất chấp "trục trặc mạng giữa các nodes"
- "Phân vùng" (Partition) là một sự cố truyền thông (mất gói tin, mạng chậm) làm các nodes không thể liên lạc được với nhau

#### 11.2. Đánh đổi thực tế: CP vs AP

Trong một hệ thống phân tán (bao gồm nhiều nodes), lỗi mạng (P) là không thể tránh khỏi và là một điều "bắt buộc" (must) phải có khả năng xử lý. Do đó, **sự đánh đổi thực sự không phải là chọn 2 trong 3, mà là: Khi một phân vùng mạng (P) xảy ra, bạn phải chọn hy sinh Consistency (C) hay Availability (A).**

Điều này chia các hệ thống phân tán làm hai loại chính:

##### Hệ thống CP (Consistent and Partition Tolerant)

**Đặc điểm:**
- Khi có lỗi mạng (P), hệ thống ưu tiên Consistency (C)
- Để đảm bảo mọi lượt đọc đều nhận được dữ liệu mới nhất (C), hệ thống phải ngừng chấp nhận các thao tác GHI (hoặc thậm chí cả ĐỌC) ở phía bị phân vùng
- Nó hy sinh Availability (A) để đảm bảo tính nhất quán

**Ví dụ:**
- Các hệ thống database quan hệ dùng Replication Đồng bộ (Chương 9)
- Các hệ thống yêu cầu giao dịch tài chính chặt chẽ

##### Hệ thống AP (Available and Partition Tolerant)

**Đặc điểm:**
- Khi có lỗi mạng (P), hệ thống ưu tiên Availability (A)
- Các nodes ở mỗi bên của phân vùng vẫn tiếp tục chấp nhận các thao tác ĐỌC và GHI
- Nó hy sinh Consistency (C). Dữ liệu trên hệ thống sẽ trở nên không nhất quán (ví dụ: một node có dữ liệu cũ hơn node kia) cho đến khi phân vùng mạng được giải quyết và các nodes có thể đồng bộ hóa lại (đạt được "Eventual Consistency")

**Ví dụ:**
- Cassandra, HBase
- Các hệ thống NoSQL
- Mạng xã hội (thà hiển thị một "like count" cũ còn hơn là không hiển thị gì cả)

##### Thế còn Hệ thống CA?

Hệ thống CA (Consistent and Available) cung cấp C và A, nhưng không thể chịu lỗi phân vùng (P). Trong thực tế, đây chính là các database chạy trên một instance độc lập (single-node). Một database chạy trên một máy chủ duy nhất thì không có "phân vùng mạng" (P) để mà chịu lỗi. Nó hoàn hảo về C (ACID) và A (miễn là nó không sập), nhưng nó không thể mở rộng quy mô.

#### 11.3. CAP trong thực tế: Kết nối toàn bộ Phần III

Định lý CAP không có ý nghĩa trong một database đơn (Chương 1, 2, 3). Nó chỉ áp dụng khi bạn bắt đầu phân tán hệ thống (Chương 9, 10). **CAP là lý thuyết nền tảng giải thích cho tất cả các đánh đổi kiến trúc trong Phần III.**

**Liên kết với Chương 9 (Replication):**
- **Sync Replication** là một thiết kế CP. Nó ưu tiên C (Master và Slave giống hệt nhau) và hy sinh A (Master phải chặn GHI nếu Slave mất kết nối)
- **Async Replication** là một thiết kế AP. Nó ưu tiên A (Master luôn GHI) và hy sinh C (Slave có thể bị trễ hoặc mất dữ liệu)

**Liên kết với Chương 10 (Sharding):**
- Một hệ thống sharded thường được thiết kế là AP
- Nếu một shard (ví dụ: Shard 5) bị sập mạng (P), hệ thống vẫn hoạt động (A) cho tất cả các shards khác
- Nó chỉ thất bại khi truy cập Shard 5
- Nó hy sinh tính nhất quán toàn cục (global consistency) (ví dụ: không thể thực hiện transaction ACID trên Shard 5 và Shard 6)

**Liên kết với Chương 1 (ACID):**
- ACID với thuộc tính "C" (Consistency) mạnh mẽ, là đặc trưng của các hệ thống CA (RDBMS truyền thống)
- Khi các hệ thống (thường là NoSQL) chọn mô hình AP để đạt được quy mô và tính sẵn sàng, họ thường phải hy sinh các đảm bảo ACID nghiêm ngặt
- Điều này dẫn đến một mô hình thay thế gọi là **BASE** (Basically Available, Soft state, Eventual consistency)—một mô hình chấp nhận tính nhất quán cuối cùng để đổi lấy tính sẵn sàng cao

#### So sánh Hệ thống CP và AP theo CAP

| Đặc điểm | Hệ thống CP (Ưu tiên Consistency) | Hệ thống AP (Ưu tiên Availability) |
|----------|-----------------------------------|-----------------------------------|
| Ưu tiên khi có lỗi mạng (P) | Tính nhất quán (Consistency) | Tính sẵn sàng (Availability) |
| Hành vi khi có lỗi mạng (P) | Từ chối GHI (hoặc ĐỌC) ở phía bị ảnh hưởng để tránh dữ liệu không nhất quán | Vẫn chấp nhận GHI (và ĐỌC), chấp nhận dữ liệu có thể trở nên không nhất quán tạm thời |
| Tính nhất quán | Mạnh (Strong), Tuyến tính (Linearizable) | Yếu (Weak), Cuối cùng (Eventual) |
| Tính sẵn sàng (GHI) | Thấp (khi có lỗi mạng) | Cao (luôn sẵn sàng GHI) |
| Ví dụ hệ thống | Hệ thống Ngân hàng, Giao dịch tài chính, RDBMS với Sync Replication | Mạng xã hội, Hệ thống phân tích, Cassandra, RDBMS với Async Replication |

---

## Kết luận: Tổng hợp các Khái niệm

Tài liệu này đã thực hiện một hành trình xuyên suốt 12 chủ đề cơ sở dữ liệu nâng cao, bắt đầu từ các khối xây dựng cơ bản của một database đơn lẻ và kết thúc bằng các lý thuyết phức tạp của hệ thống phân tán quy mô lớn.

### Các chủ đề liên kết chặt chẽ với nhau

**Từ Phần I đến Phần II:**

- **ACID và Normalization** (Phần I) cung cấp một nền tảng lý thuyết về tính toàn vẹn dữ liệu, nhưng chúng đánh đổi bằng hiệu suất ĐỌC (do JOIN) và tính linh hoạt

- **Denormalization** (Phần I) và **Indexes** (Phần I) là các kỹ thuật tối ưu hóa ĐỌC đầu tiên, nhưng chúng lại đánh đổi bằng chi phí GHI (bảo trì index, vô hiệu hóa cache phi chuẩn hóa)

- **ORMs** (Phần II) cố gắng che giấu sự phức tạp này khỏi lập trình viên, nhưng sự "leaky abstraction" của chúng lại tạo ra thảm họa N+1 (Phần II) nếu không được kiểm soát

- **SQLAlchemy** (Phần II) cung cấp các công cụ (như `selectinload`) để kiểm soát sự trừu tượng hóa đó, và **Profiling/EXPLAIN** (Phần II) là kính hiển vi cho phép chúng ta chẩn đoán chính xác những gì ORM đang làm

**Từ Phần II đến Phần III:**

- Khi một node không còn đủ, **Replication** (Phần III) giải quyết vấn đề mở rộng ĐỌC, và **Sharding** (Phần III) giải quyết vấn đề mở rộng GHI

- Những chiến lược mở rộng này (cùng với **Failure Modes** và **Migration**) đưa chúng ta vào thế giới của các hệ thống phân tán, nơi **Định lý CAP** (Phần III) trở thành quy luật vật lý tối cao, buộc chúng ta phải lựa chọn giữa Tính nhất quán (CP) hoặc Tính sẵn sàng (AP)

### Nguyên tắc chính: Không có "kiến trúc tốt nhất"

Cuối cùng, **không có "kiến trúc tốt nhất" – chỉ có "kiến trúc phù hợp"**. Mọi quyết định được thảo luận, từ Normalization vs Denormalization, B-Tree vs Hash, Đồng bộ vs Bất đồng bộ, đến CP vs AP, đều là một sự đánh đổi dựa trên yêu cầu nghiệp vụ cụ thể của ứng dụng.

### Các câu hỏi quan trọng khi thiết kế hệ thống

Khi thiết kế một hệ thống database, bạn cần tự hỏi:

1. **Về tải (Workload):**
   - Hệ thống của tôi là Read-Heavy hay Write-Heavy?
   - Tôi cần mở rộng đọc (Replication) hay mở rộng ghi (Sharding)?

2. **Về tính nhất quán:**
   - Tôi có thể chấp nhận Eventual Consistency không?
   - Hay tôi cần Strong Consistency bất kể giá nào?

3. **Về tính sẵn sàng:**
   - RTO (Recovery Time Objective) của tôi là gì? (Failover)
   - RPO (Recovery Point Objective) của tôi là gì? (Backup strategy)

4. **Về hiệu suất:**
   - Tôi có thể hy sinh tính nhất quán để đổi lấy độ trễ thấp không?
   - Tôi có thể hy sinh hiệu suất ghi để đổi lấy hiệu suất đọc không? (Indexes, Denormalization)

5. **Về phức tạp:**
   - Tôi có đủ năng lực để quản lý một hệ thống sharded phức tạp không?
   - Hay tôi nên bắt đầu với vertical scaling và caching đơn giản hơn?

### Lời kết

Kiến trúc database là một lĩnh vực đầy những đánh đổi tinh tế. Không có giải pháp "bạc đạn" nào phù hợp với mọi tình huống. Sự hiểu biết sâu sắc về các khái niệm cơ bản—từ ACID đến CAP, từ Indexes đến Sharding—cho phép bạn đưa ra những quyết định sáng suốt dựa trên yêu cầu cụ thể của hệ thống mà bạn đang xây dựng.

Hy vọng tài liệu này đã cung cấp cho bạn một nền tảng vững chắc để hiểu và áp dụng các khái niệm database nâng cao trong thực tế.

---

## Tài liệu tham khảo

Tài liệu này được biên soạn dựa trên nhiều nguồn tham khảo uy tín về cơ sở dữ liệu, bao gồm:

- Các tài liệu chính thức về Transactions, ACID, và Database Design
- Tài liệu hướng dẫn về SQLAlchemy và ORM patterns
- Các bài viết và nghiên cứu về Database Indexing (B-Tree, Hash)
- Tài liệu về Data Migration, Replication, và Sharding strategies
- Nghiên cứu học thuật về CAP Theorem và distributed systems

Để có hiểu biết sâu hơn về từng chủ đề, bạn nên tham khảo các nguồn gốc được liệt kê trong phần trích dẫn của tài liệu gốc.