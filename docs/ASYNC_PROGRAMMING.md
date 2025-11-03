# Asynchoronous Programming with Python

## Mục lục

[Phần I. Tư duy bất đồng bộ - Từ Blocking đến Non-blocking](#phần-i-tư-duy-bất-đồng-bộ---từ-blocking-đến-non-blocking)
 * [1.1 Tại sao `async` lại quan trọng đối với web server: Bài toán của các tác vụ I/O-bound](#11-tại-sao-async-lại-quan-trọng-đối-với-web-server-bài-toán-của-các-tác-vụ-io-bound)
 * [1.2. Các thành phần cốt lõi `async`, `await`, và **coroutine**](#12-các-thành-phần-cốt-lõi-async-await-và-coroutine)
 * [1.3. Nhạc trường của sự đồng thời: `asyncio` Event Loop](#13-nhạc-trường-của-sự-đồng-thời-asyncio-event-loop)

[Phần II. Làm chủ các thao tác đồng thời cho các endpoint phức tạp](#phần-ii-làm-chủ-các-thao-tác-đồng-thời-cho-các-endpoint-phức-tạp)
 * [2.1. Vượt ra ngoài `await`: Hiểu về các đối tượng `Task` và `Future`](#21-vượt-ra-ngoài-await-hiểu-về-các-đối-tượng-task-và-future)
 * [2.2. Thực thi song song: Sức mạnh của `asyncio.gather`](#22-thực-thi-song-song-sức-mạnh-của-asynciogather)

[Phần III. Xây dựng Logic bất đồng bộ với Sanic](#phần-iii-xây-dựng-logic-bất-đồng-bộ-với-sanic)
 * [3.1. Cấu trúc của một Handler `async` trong Sanic](#31-cấu-trúc-của-một-handler-async-trong-sanic)
 * [3.2. Can thiệp vào vòng đời yêu cầu với Middleware](#32-can-thiệp-vào-vòng-đời-yêu-cầu-với-middleware)
 * [3.3. Fire-and-Forge: Listeners và tác vụ nền](#33-fire-and-forge-listeners-và-tác-vụ-nền)

[Phần IV. Lớp dữ liệu bất đồng bộ - Hướng dẫn chuyên sâu cho API CRUD](#phần-iv-lớp-dữ-liệu-bất-đồng-bộ---hướng-dẫn-chuyên-sâu-cho-api-crud)
 * [4.1. Sai lầm lớn nhất: Tránh I/O chặn trong lớp dữ liệu](#41-sai-lầm-lớn-nhất-tránh-io-chặn-trong-lớp-dữ-liệu)
 * [4.2. Mẫu hình chuyên nghiệp: Quản lý connection pool với `asyncpg`](#42-mẫu-hình-chuyên-nghiệp-quản-lý-connection-pool-với-asyncpg)
 * [4.3. Tích hợp các ORM hiện đại: SQLAlchemy 2.0](#43-tích-hợp-các-orm-hiện-đại-sqlalchemy-20)
 * [4.4. Một phương pháp thay thế: Tortoise ORM](#44-một-phương-pháp-thay-thế-tortoise-orm)

[Phần V. Mã bất đồng bộ sẵn sàng cho production (Best Pactices)](#phần-v-mã-bất-đồng-bộ-sẵn-sàng-cho-production-best-pactices)
 * [5.1. Bảo vệ Event Loop](#51-bảo-vệ-event-loop)
 * [5.2. Cấu trúc dự án `Async` của bạn](#52-cấu-trúc-dự-án-async-của-bạn)
 * [5.3. Xử lý ngoại lệ nâng cao và huỷ tác vụ](#53-xử-lý-ngoại-lệ-nâng-cao-và-huỷ-tác-vụ)

[Kết luận](#kết-luận)

Mục tiêu của sổ tay này là cung cấp một nền tảng vững chắc về **lập trình bất đồng bộ (asynchronous programming)** sử dụng thư viện `asyncio` của Python, 
được tùy chỉnh để khai thác tối đa sức mạnh của Sanic Framework trong việc xây dựng các API CRUD hiệu năng cao.

## Phần I. Tư duy bất đồng bộ - Từ Blocking đến Non-blocking
Để sử dụng Sanic một cách hiệu quả, điều kiện tiên quyết quan trọng nhất là phải xây dựng được một mô hình tư duy theo hướng không chặn. 
Phần này sẽ thiết lập nền tảng "tại sao" đằng sau lập trình bất đồng bộ trong bối cảnh phát triển web.

### 1.1 Tại sao `async` lại quan trọng đối với web server: Bài toán của các tác vụ I/O-bound
Nền tảng của việc hiểu khi nào nên sử dụng asyncio nằm ở việc phân biệt rõ ràng giữa hai loại tác vụ: I/O-bound và CPU-bound.
- **Tác vụ I/O-bound (Input/Output-Bound):** Đây là những công việc mà thời gian thực thi chủ yếu bị chi phối bởi việc chờ đợi các hoạt động đầu vào/đầu ra hoàn tất. 
Một web server phục vụ API CRUD là một ví dụ điển hình, nó dành phần lớn thời gian để chờ đợi các hoạt động như: nhận yêu cầu mạng từ client, chờ phản hồi từ cơ sở dữ liệu, 
đọc/ghi file, hoặc gọi đến các API của bên thứ ba.
- **Tác vụ CPU-bound:** Đây là những công việc đòi hỏi bộ xử lý trung tâm (CPU) phải làm việc liên tục từ đầu đến cuối, ví dụ như các phép tính toán phức tạp, xử lý hình ảnh, 
hoặc các vòng lặp tính toán dày đặc. Đối với các tác vụ này, giải pháp thường là đa xử lý (multiprocessing) để tận dụng nhiều lõi CPU.

Trong một server đồng bộ truyền thống (ví dụ như Flask ở cấu hình mặc định), mỗi tiến trình worker xử lý các yêu cầu một cách tuần tự. Khi một request handler đang chờ một truy vấn cơ sở dữ liệu trả về kết quả, 
nó sẽ chặn (block) toàn bộ tiến trình worker đó, khiến cho không một yêu cầu nào khác có thể được xử lý. Điều này dẫn đến việc sử dụng tài nguyên không hiệu quả và khả năng mở rộng kém khi tải tăng cao.

`asyncio` giải quyết vấn đề này thông qua mô hình đồng thời (concurrency) đơn luồng,  đơn tiến trình, sử dụng cơ chế **đa nhiệm hợp tác (cooperative multitasking)**. 
Thay vì bị chặn, một tác vụ `async` có thể tự nguyện nhường quyền điều khiển cho **bộ điều phối trung tâm (event loop)** trong khi nó chờ một hoạt động I/O hoàn tất. 
Điều này cho phép một tác vụ khác được chạy, tạo ra cảm giác song song và tăng đáng kể thông lượng cho các ứng dụng I/O bound. 

Việc lựa chọn `asyncio` không chỉ là một tối ưu hóa hiệu năng; nó là một quyết định về mặt kiến trúc. 
Nó đòi hỏi toàn bộ ngăn xếp công nghệ liên quan đến I/O (HTTP client, driver cơ sở dữ liệu) phải có khả năng hợp tác, tức là không chặn. 
Chỉ một lệnh gọi blocking duy nhất trong một request handler cũng có thể làm đóng băng toàn bộ event loop, vô hiệu hóa mọi lợi ích của `asyncio`. 
Điều này lý giải tại sao việc áp dụng một framework `async` như Sanic mang tính chất "all-in" (phải tuân thủ hoàn toàn).   

### 1.2. Các thành phần cốt lõi `async`, `await`, và **coroutine**
- `async def`: Cú pháp này dùng để định nghĩa một hàm coroutine (coroutine function). Việc gọi một hàm coroutine không thực thi mã ngay lập tức, 
mà thay vào đó trả về một **đối tượng coroutine (coroutine object)**. Đây là một đối tượng "awaitable" (có thể được chờ), đại diện cho một tính toán 
có thể bị tạm dừng và tiếp tục sau đó. Một lỗi phổ biến của người mới là gọi một hàm coroutine mà không `await` nó, dẫn đến một `RuntimeWarning` vì 
đoạn mã đó không bao giờ được chạy. 
- `await`: Từ khoá này là động cơ của **đa nhiệm hợp tác (cooperative multitasking)**. Nó chỉ có thể được sử dụng bên trong một hàm `async def`. 
Khi chương trình gặp `await some_awaitable`, nó báo cho event loop rằng: "Tôi sẽ tạm dừng ở đây để chờ `some_awaitable` hoàn thành. 
Trong thời gian đó bạn có thể tự do chạy các tác vụ đã được lên lịch khác.". Khi đối tượng awaitable được giải quyết (resolved), event loop sẽ thực thi 
hàm từ chínhd điểm đó. 
- `Awaitables`: Một đối tượng được gọi là "awaitable" nếu nó có thể được sử dụng trong một biểu thức `await`. Ba loại awaitable chính là: coroutine, `Task`, `Future`.

### 1.3. Nhạc trường của sự đồng thời: `asyncio` Event Loop
Event Loop là trái tim của mọi ứng dụng `asyncio`. Nó là điều phối trung tâm, giống như một "nhạc trưởng giàn nhạc", quản lý và điều khiển việc thực thi các tác vụ `async`.
Nó duy trì một hàng đợi các tác vụ sẵn sàng chạy và thực thi chúng lần lượt. 

Mô hình hoạt động của event loop có thể được đơn giản hoá như sau:
1. Lấy một tác vụ từ hàng đợi sẵn sàng (ready queue).
2. Chạy mã của tác vụ đó cho đến khi nó gặp một lệnh `await`.
3. Tác vụ nhường quyền điều khiển lại cho `loop`.
4. Loop lên lịch cho các tác vụ sẵn sàng tiếp theo
5. Trong khi các tác vụ đang chờ I/O, loop sẽ giám sát hệ điều hành để phát hiện các sự kiện hoàn thành I/O (ví dụ: dữ liệu được nhận trên một socket).
6. Sau khi I/O được thực hiện xong, event loop sẽ chuyển tác vụ đang chờ I/O tương ứng trở lại hàng đợi sẵn sàng (ready queue). 

Khi bạn chạy một ứng dụng Sanic, chính Sanic sẽ khởi tạo và quản lý event loop này cho bạn. Mỗi request handler bạn viết là một coroutine được lên lịch như một `Task` trên event loop này. 
Do đó, bạn không bao giờ được gọi `asyncio.run()` từ bên trong một handler của Sanic, vì event loop đã và đang chạy—một lỗi phổ biến gây ra `RuntimeError`. 
Để tăng tốc hơn nữa, Sanic thường sử dụng `uvloop`, một phiên bản event loop hiệu năng cao được viết bằng C.   

#### Bảng 1. Các phép toán tương đương giữa Đồng bộ và Bất đồng bộ
Bảng này là một tài liệu tham khảo nhanh và thiết thực để chuyển đổi kiến thức **lập trình đồng bộ (sync programming)** hiện có sang thế giới **lập trình bất đồng bộ (async programming)**. 
Nó trực tiếp giải quyết "sai lầm lớn nhất" là sử dụng các thư viện blocking bên trong một ứng dụng `async` bằng cách cung cấp các giải pháp thay thế không chặn (non-blocking).

<table>
  <thead>
    <tr>
      <th>Thao tác Blocking</th>
      <th>Mã Đồng bộ</th>
      <th>Tương đương Bất đồng bộ Không chặn</th>
      <th>Thư viện yêu cầu</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Tạm dừng thực thi</td>
      <td><code>time.sleep(1)</code></td>
      <td><code>await asyncio.sleep(1)</code></td>
      <td>asyncio (tích hợp sẵn)</td>
    </tr>
    <tr>
      <td>Yêu cầu HTTP</td>
      <td><code>requests.get(url)</code></td>
      <td><code>async with session.get(url) as resp:</code></td>
      <td>aiohttp, httpx</td>
    </tr>
    <tr>
      <td>Truy vấn PostgreSQL</td>
      <td><code>cursor.execute()</code></td>
      <td><code>await conn.fetch(query)</code></td>
      <td>asyncpg</td>
    </tr>
    <tr>
      <td>Truy vấn MySQL</td>
      <td><code>cursor.execute()</code></td>
      <td><code>await cur.execute(query)</code></td>
      <td>aiomysql</td>
    </tr>
    <tr>
      <td>Đọc File</td>
      <td><code>with open(...)</code></td>
      <td><code>async with aiofiles.open(...)</code></td>
      <td>aiofiles</td>
    </tr>
  </tbody>
</table>

## Phần II. Làm chủ các thao tác đồng thời cho các endpoint phức tạp
Phần này chuyển từ những kiến thức cơ bản về một thao tác bất đồng bộ đơn lẻ sang nhu cầu thực tế là chạy nhiều thao tác đồng thời, 
một yêu cầu phổ biến để xây dựng các endpoint API phong phú.

### 2.1. Vượt ra ngoài `await`: Hiểu về các đối tượng `Task` và `Future`
Việc chỉ sử dụng `await` một cách tuần tự không đạt được sự đồng thời. `await Func1()` theo sau bởi `await Func2()` sẽ chỉ chạy `Func2()` sau khi `Func1()` 
được hoàn thành hoàn toàn, làm mất đi mục đích của `asyncio` đối với I/O song song. 
- `asyncio.Future`: Một `Future` là một đối tượng awaitable cấp thấp đại diện cho _kết quả cuối cùng_ của một hoạt động. Nó hoạt động giống như một vật giữ chỗ 
hoặc một lời hứa (promise). Mặc dù bạn hiếm khi tạo chúng trực tiếp trong mã ứng dụng, chúng là nền tảng cho cách `asyncio` hoạt động và được sử dụng để kết nối 
mã dựa trên callback với cú pháp `async/await`.
- `asyncio.Task`: Đây là một đối tượng quan trọng dành cho các nhà phát triển ứng dụng. Một `Task` là một lớp con của `Future`, được thiết kế đặc biệt để bao bọc và 
chạy một hàm coroutine trong nền. Hành động quan trọng là `asyncio.create_task(my_coro())`. Hàm này lên lịch cho coroutine chạy trên event loop "càng sớm càng tốt" và 
ngay lập tức trả về một đối tượng `Task`. Mã gốc có thể tiếp tục thực thi mà không cần chờ đợi. Sau đó bạn có. thể `await` đối tượng Task này để lấy kết quả của nó.

Sự khác biệt giữa `await my_coro()` và `task = asyncio.create_task(my_coro())` là rất tinh tế nhưng cực kỳ quan trọng. `await` tạm dừng hoạt đông hàm hiện tại cho đến khi 
coroutine được chờ hoàn thành. Ngược lại, `create_task` lên lịch cho coroutine và trả về quyền điều khiển ngay lập tức. Điều này có nghĩa là `create_task` là chỉ thị rõ ràng 
cho event loop để "bắt đầu công việc này ngay bây giờ, và tôi sẽ kiểm tra lại sau.". Đây là cơ chế cơ bản để đạt được sự đồng thời. Nếu không có `create_task` 
(hoặc một công cụ cấp cao hơn như `asyncio.gather` sử dụng nó bên trong), bạn không thể có hai hoạt động I/O chồng chéo về mặt thời gian. `await`là để lấy kết quả, 
trong khi `create_task` là để khởi tạo việc thực thi đồng thời. 

### 2.2. Thực thi song song: Sức mạnh của `asyncio.gather`
Đối với một API CRUD, việc cần lấy dữ liệu từ nhiều nguồn để xây dựng một phản hồi duy nhất là rất phổ biến (ví dụ: lấy chi tiết người dùng từ một bảng, 
các đơn hàng gần đây của họ từ bảng khác, và URL ảnh đại diện của họ từ một dịch vụ bên ngoài). `asyncio.gather` là một công cụ cấp cao hoàn hảo cho việc này. 

`asyncio.gather(*aws)` nhận vào một chuỗi các awaitable (coroutines, Tasks hoặc Futures), lên lịch cho tất cả chúng chạy đồng thời, và chờ cho đến khi tất cả hoàn thành. 
Sau đó, nó trả về một danh sách các kết quả của chúng, theo đúng thứ tự chúng được truyền vào. Việc này giúp giảm tổng thể thời gian thực thi xuống bằng thời gian của 
thao tác đơn lẻ duy nhất. 

Theo mặc định, nếu bất kỳ tác vụ nào trong `gather` gây ra một ngoại lệ, `gather` sẽ ngay lập tức huỷ các tác vụ đang chờ khác và lan truyền ngoại lệ đó. 
Cờ `return_exceptions=True` là một mẫu hình để xử lý các lỗi một phần một cách duyên dáng (gracefully). Với cờ này, các ngoại lệ được trả về như là kết quả trong danh sách 
thay vì được ném ra, cho phép ứng dụng xử lý các kết quả thành công. 

#### Bảng 2. So sánh các công cụ đồng thời của `asyncio`
Bảng này làm sáng tỏ các cách khác nhau để chạy và chờ đợi mã bất đồng bộ, cung cấp một khuôn khổ ra quyết định rõ ràng về việc khi nào nên sử dụng một `await` đơn giản, 
khi nào nên tạo một `Task` nền, và khi nào nên sử dụng mẫu hình `gather` mạnh mẽ.

<table>
  <thead>
    <tr>
      <th>Công cụ</th>
      <th>Trường hợp sử dụng</th>
      <th>Hành vi thực thi</th>
      <th>Giá trị trả về</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>await coro()</code></td>
      <td>Thực thi tuần tự; lấy kết quả của một bước tiếp theo duy nhất.</td>
      <td>Tạm dừng hàm hiện tại cho đến khi <code>coro</code> hoàn thành.</td>
      <td>Kết quả của <code>coro</code>.</td>
    </tr>
    <tr>
      <td><code>task = create_task(coro)</code></td>
      <td>Chạy một tác vụ trong nền; "fire-and-forget" hoặc lấy kết quả sau.</td>
      <td>Lên lịch cho <code>coro</code> chạy trên event loop ngay lập tức. KHÔNG tạm dừng hàm hiện tại.</td>
      <td>Một đối tượng <code>asyncio.Task</code>.</td>
    </tr>
    <tr>
      <td><code>results = await gather(*coros)</code></td>
      <td>Chạy nhiều hoạt động I/O độc lập đồng thời và chờ tất cả hoàn thành.</td>
      <td>Lên lịch cho tất cả các coroutine chạy đồng thời. Tạm dừng cho đến khi tất cả hoàn thành.</td>
      <td>Một danh sách các kết quả theo thứ tự ban đầu.</td>
    </tr>
    <tr>
      <td><code>result = await wait_for(coro, timeout)</code></td>
      <td>Chạy một hoạt động duy nhất với một thời hạn.</td>
      <td>Chạy coroutine nhưng ném ra <code>TimeoutError</code> nếu nó vượt quá thời gian chờ.</td>
      <td>Kết quả của <code>coro</code> nếu nó hoàn thành kịp thời.</td>
    </tr>
  </tbody>
</table>

## Phần III. Xây dựng Logic bất đồng bộ với Sanic
Phần này kết nối lý thuyết `asyncio` với việc triển khai thực tế trong framework Sanic, tận dụng cấu trúc dự án hiện có của bạn.

### 3.1. Cấu trúc của một Handler `async` trong Sanic
Mỗi request handler của Sanic được trang trí bằng `@app.get`, `@app.post`,...có thể (và nên) là một hàm `async def`. 
Khi một yêu cầu đến, Sanic lên lịch cho coroutine handler này như một `Task` trên event loop của nó. 

Để chứng minh sự khác biệt về hiệu năng, hãy xem xét hai endpoint:
- `/sync`: Sử dụng `time.sleep(0.1)` (blocking). Với bốn worker, endpoint này chỉ có thể xử lý khoảng 31.76 yêu cầu/giây.
- '/async': Sử dụng `await asyncio.sleep(0.1)` (non-blocking). Với cùng cấu hình, endpoint này có thể xử lý một con số đang kinh ngạc là `3,3843.17` yêu cầu/giây.

Sự khác biệt này cho thấy lợi ích to lớn của `async/await` trong thế giới web. Phiên bản bất đồng bộ hiệu quả hơn nhiều vì trong khi một yêu cầu đang "ngủ", 
nó có thể bắt đầu xử lý hàng ngàn yêu cầu khác. Sanic nhanh vì nó tận dụng tối đa các tài nguyên sẵn có để xử lý nhiều yêu cầu đồng thời. 

Đối tượng `request` được truyền vào làm đối số đầu tiên cho handler, cung cấp quyền truy cập không chặn vào dữ liệu như body (`request.json`), 
tham số truy vấn (`request.args`), và dữ liệu form (`request.form`).

### 3.2. Can thiệp vào vòng đời yêu cầu với Middleware
Middleware cho phép phạn chạy mã trước (request) hoặc sau (reponse) khi handler chính của bạn thực thi. 
Điều này hoàn hảo cho các mối quan tâm chung như xác thực, ghi log, thêm header, hoặc quản lý session cơ sở dữ liệu. 

Các middleware được tạo bằng decorator `@app.on_request` và `@app.on_response`. 
Các hàm middleware này cũng phải là `async` nếu chúng thực hiện bất kỳ hoạt động I/O nào. 

`request.ctx` là một không gian tên chuyên dụng để chuyển trạng thái từ middleware đến handler. 
Mỗi mẫu hình phổ biến là middleware xác thực sẽ xác minh token, lấy người dùng từ cơ sở dữ liệu, 
và gắn đối tượng người dùng vào `request.ctx.user` để handler sử dụng. 

Thứ tự thực thi rất quan trọng: middleware `request` chạy theo thứ tự được định nghĩa, trong khi middleware `response` chạy theo thứ tự **ngược lại.** 

### 3.3. Fire-and-Forge: Listeners và tác vụ nền
- **Listeners cho vòng đợi ứng dụng:** Các listener của Sanic (`@app.before_server_start`, `@app.after_server_start`,...) là các hook vào vòng đời của ứng dụng, 
không phải vòng đời của yêu cầu. Trường hợp sử dụng của chúng là thiết lập và dọn dẹp các tài nguyên được chia sẻ như connection pool của cơ sở dữ liệu. 

- **`app.add_task()` cho các công việc nền (background task)**: Sử dụng `app.add_task()` để lên lịch cho một coroutine chạy trong nền, 
độc lập với bất kỳ yêu cầu cụ thể nào. Đây là mẫu hình **"fire-and-forget"**.

Có một sự khác biệt quan trọng giữa `asyncio.create_task` trong một handler và `@app.add_task`. `asynio.create_task` tạo ra một tác vụ gắn liền với vòng đời của yêu cầu đó. 
Nếu handler kết thúc và tác vụ không được `await`, nó có thể bị thu gom rác hoặc ngoại lệ của nó có thể bị mất. Ngược lại, `app.add_task` gắn tác vụ vào event loop của ứng dụng, 
làm cho nó phù hợp với quy trình nền chạy dài hơn một yêu cầu duy nhất. Một mẫu hình phổ biến là một handler gọi `app.add_task(send_email_confirmation(user))` và ngay lập tức trả về 
phản hồi cho client, trong khi email được gửi trong nền. **Quy tắc:** sử dụng `asyncio.create_task` (hoặc `gather`) cho công việc cần thiết cho phản hồi, và `app.add_task` cho công việc xảy ra sau phản hồi. 

## Phần IV. Lớp dữ liệu bất đồng bộ - Hướng dẫn chuyên sâu cho API CRUD
Đây là phần quan trọng và thực tế nhất. Nó cung cấp các mẫu hình chi tiết, sẵn sàng để sao chép-dán để tích hợp các cơ sở dữ liệu `async` vào cấu trúc dự án hiện có của bạn.

### 4.1. Sai lầm lớn nhất: Tránh I/O chặn trong lớp dữ liệu
Việc sử dụng một driver cơ sở dữ liệu đòng bộ (như `psycopg2`, `pymysql`) hoặc một ORM đồng bộ bên trong một handler của Sanic là một sai lầm về hiệu năng phổ biến và nghiêm trọng nhất. 
Một lệnh gọi như vậy sẽ chặn toàn bộ event loop, làm cho server trở nên đồng bộ và vô hiệu hóa mọi lợi ích của `asyncio`. 
Yêu cầu này áp dụng cho tất cả các hoạt động I/O. Bất kỳ thư viện nào không hỗ trợ `async/await` phải được chạy trong một thread pool riêng biệt bằng cách sử dụng `loop.run_in_executor`, 
mặc dù giải pháp ưu tiên luôn là sử dụng một thư viện `async` gốc.   

### 4.2. Mẫu hình chuyên nghiệp: Quản lý connection pool với `asyncpg`
`asyncpg` là driver `asyncio` gốc, hiệu năng cao cho PostgreSQL. Nó được thiết kế từ đầu để đạt tốc độ cao và tích hợp hoàn hảo với event loop của `asyncio`. 
Việc tạo một kết nối cơ sở dữ liệu mới cho yêu cầu là không hiệu quả. Một connection pool duy trì một tập hợp các kết nối sẵn sàng sử dụng, giảm đáng kể độ trễ. 

Dưới đây là một mẫu hình kinh điển để quản lý `asyncpg` pool trong Sanic:
1. Sử dụng listener `@app.before_server_start` để khởi tạo connection pool (`@asyncpg.create_pool`) và lưu nó vào context của ứng dụng (`app.ctx.db_pool`).
2. Trong request handler, lấy một kết nối từ pool bằng cách sử dụng `async with app.ctx.db_pool.acquire() as connection`
3. Thực hiện các thao tác cơ sở dữ liệu bằng cách `await connection.fetch(...)`.
4. Khối `async with` sẽ tự động giải phóng kết nối trở lại pool.
5. Sử dụng listener `@app.after_server_stop` để đóng connection pool một cách duyên dáng (`await app.ctx.db_pool.close()`)

### 4.3. Tích hợp các ORM hiện đại: SQLAlchemy 2.0
SQLAlchemy 1.4+ đã giới thiệu hỗ trợ `asyncio` gốc, biến nó thành một công cụ hàng đầu trong thế giới `async`. 
Nó cung cấp sức mạnh và sự linh hoạt của SQLAlchemy Core và ORM với I/O không chặn. 

Hướng dẫn tích hợp từng bước:
1. **Dependencies**: Cài đặt `sqlalchemy` (>=1.4) và driver `asyn`c (`asyncpg` hoặc `aiomysql`).
2. **Tạo `AsyncEngine:`** Sử dụng `create_async_engine` từ `sqlalchemy.ext.asyncio` để tạo một engine cơ sở dữ liệu bất đồng bộ.
3. **Quản lý `AsyncSession` với Middleware**: Đây là mẫu hình chính:
   * Một middleware `@app.on_request` tạo một `AsyncSession` cho mỗi yêu cầu và gắn nó vào `request.ctx.session`
   * Một middleware `@app.on_response` đảm bảo `await request.ctx.session.close()` được gọi khi yêu cầu được xử lý, dọn dẹp kết nối. 
4. Viết truy vấn `Async`: Trong handler, truy cập session qua `request.ctx.session`. Sử dụng cú pháp truy vấn kiểu 2.0 hiện đại với các câu lệnh 
`select()` và `await session.execute(...)`, theo sau là `.scalar().all()` hoặc `.scalar_one_or_none()`.

`asyncpg` có tốc độ rất cao vì truy cập trực tiếp PostgreSQL mà không qua lớp trung gian.
ORM bất đồng bộ của SQLAlchemy chậm hơn do có thêm lớp trừu tượng và xử lý nội bộ giữa async/sync.
Tuy vậy, trong ứng dụng phức tạp, chi phí này là chấp nhận được để đổi lấy mã dễ bảo trì, an toàn và không chặn I/O.

### 4.4. Một phương pháp thay thế: Tortoise ORM
**Tortoise ORM** là một ORM *async-native* lấy cảm hứng từ **Django ORM**.  
Nó được thiết kế cho **asyncio** ngay từ đầu, nên API của nó hoạt động rất tự nhiên trong môi trường bất đồng bộ.  
So với **SQLAlchemy**, Tortoise thường được xem là **dễ bắt đầu hơn**, trong khi SQLAlchemy cung cấp **nhiều quyền kiểm soát chi tiết hơn**.

#### Hướng dẫn tích hợp từng bước

1. **Dependencies**  
   Cài đặt `tortoise-orm` và driver cần thiết (ví dụ: `asyncpg`).

2. **Định nghĩa Model**  
   Tạo các model bằng cách kế thừa từ `tortoise.Model`.

3. **Tiện ích `register_tortoise`**  
   Sử dụng hàm trợ giúp `register_tortoise`.  
   Hàm này tự động thiết lập các listener `before_server_start` và `after_server_stop` để khởi tạo và dọn dẹp kết nối cơ sở dữ liệu.

4. **Viết Truy vấn trong Handlers**  
   Thực hiện các thao tác CRUD như:  
   ```python
   await Users.all()
   await Users.create(...)
   
#### Bảng 3: Các Mẫu hình Tích hợp ORM Async trong Sanic

Bảng dưới đây so sánh chiến lược cấp cao giữa ba lựa chọn ORM async phổ biến, giúp bạn chọn hướng kiến trúc phù hợp.

<table>
  <thead>
    <tr>
      <th>Tính năng</th>
      <th>asyncpg thô</th>
      <th>SQLAlchemy 2.0</th>
      <th>Tortoise ORM</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>Kiểu API</strong></td>
      <td>Chuỗi SQL thô, trả về <code>tuple</code>/<code>dict</code>.</td>
      <td>Biểu thức <code>select()</code> Pythonic, dựa trên <code>Session</code>.</td>
      <td>Chuỗi phương thức kiểu Django (<code>.filter()</code>, <code>.all()</code>).</td>
    </tr>
    <tr>
      <td><strong>Tích hợp</strong></td>
      <td>Quản lý <em>connection pool</em> thủ công qua listeners.</td>
      <td>Tạo <code>AsyncEngine</code> và quản lý <code>Session</code> thủ công qua middleware.</td>
      <td>Hàm trợ giúp <code>register_tortoise</code> tự động hóa việc thiết lập listener.</td>
    </tr>
    <tr>
      <td><strong>Trừu tượng hóa</strong></td>
      <td>Không. Toàn quyền kiểm soát, nhưng phải viết SQL thủ công.</td>
      <td>Cao. Cung cấp đầy đủ khả năng ORM (quan hệ, unit of work).</td>
      <td>Cao. Cung cấp đầy đủ khả năng ORM với API đơn giản và trực quan hơn.</td>
    </tr>
    <tr>
      <td><strong>Phù hợp nhất cho...</strong></td>
      <td>Ứng dụng cần hiệu năng cao, truy vấn đơn giản; nhà phát triển quen viết SQL trực tiếp.</td>
      <td>Ứng dụng phức tạp cần kiểm soát chi tiết; nhóm có kinh nghiệm với SQLAlchemy.</td>
      <td>Phát triển nhanh; nhà phát triển quen Django ORM; dự án ưu tiên cú pháp async-native sạch sẽ.</td>
    </tr>
  </tbody>
</table>

## Phần V. Mã bất đồng bộ sẵn sàng cho production (Best Pactices)
Phần cuối cùng này tổng hợp các bài học thành lời khuyên có thể hành động để xây dựng một ứng dụng mạnh mẽ, dễ bảo trì và có thể kiểm thử.

### 5.1. Bảo vệ Event Loop
Luôn nhớ rằng bất kỳ công việc CPU-bound hoặc I/O Blocking nào cũng sẽ làm đình trệ event loop. Đối với mã blocking không thể tránh khỏi, 
`await loop.run_in_executor(None, blocking_function, *args)` có thể được sử dụng để chạy nó trong một thread pool riêng biệt, nhưng một thư viện 
`async` gốc luôn là giải pháp được ưu tiên. 

### 5.2. Cấu trúc dự án `Async` của bạn
Áp dụng cho cấu trúc dự án của bạn:
- `repositories`: Tất cả các phương thức trong lớp này chạm vào cơ sở dữ liệu phải trở thành `async def` và sử dụng mẫu hình truy cập dữ liệu `async` đã chọn. 
- `services`: Các phương thức của lớp service gọi đến repository cũng phải là `async def` và `await` các lệnh gọi đó. 
Nếu một phương thức service cần gọi nhiều phương thức repository, đó là nơi hoàn hảo để sử dụng `asyncio.gather` để chạy chúng đồng thời. 
- `views` **(Handlers):** Đây là các hàm `async def` cấp cao nhất `await` các lệnh gọi đến lớp service. 

Nguyên tắc "Async all the way down" (Bất đồng bộ từ trên xuống dưới) là rất quan trọng: việc biến một hàm cấp cao (như handler của Sanic) 
thành `async` đòi hỏi toàn bộ chuỗi lệnh gọi bên dưới nó cũng phải là `async` nếu nó liên quan đến I/O. 

Để kiểm thử mã `async`, `pytest-asyncio` là công cụ tiêu chuẩn, cung cấp các fixture event loop cần thiết để kiểm tra đúng các coroutine của bạn. 
`pytest-sanic` cũng hữu ích cho việc kiểm thử ở cấp độ cao hơn. 

### 5.3. Xử lý ngoại lệ nâng cao và huỷ tác vụ
- Xử lý ngoại lệ trong `gather`: Sử dụng mẫu hình `return_exceptions=True` và lặp qua các kết quả để xử lý cả các tác vụ thành công và thất bại một cách duyên dáng.
- **Huỷ tác vụ:** Các tác vụ có thể bị huỷ bằng `task.cancel()`. Điều này ném ra một `CancelledError` bên trong tác vụ, 
nên được bắt trong khối `try...finally` để thực hiện dọn dẹp (ví dụ: đóng kết nối)
- **Timeouts:** Sử dụng `asyncio.wait_for` để áp dụng một thời gian chờ cho bất kỳ awaitable nào, 
điều này rất cần thiết để ngăn các yêu cầu bị treo vô thời hạn khi chờ đợi một dịch vụ bên ngoài không phản hồi. 

## Kết luận
Việc chuyển đổi từ lập trình đồng bộ sang bất đồng bộ với Sanic là một sự thay đổi về tư duy cũng như về công cụ. Bằng cách nắm vững các khái niệm cốt lõi của asyncio—async/await, event loop, và các Task—bạn có thể mở khóa tiềm năng hiệu năng thực sự của Sanic, đặc biệt đối với các ứng dụng I/O-bound như API CRUD.

Lộ trình được đề xuất là:

1. **Xây dựng Tư duy:** Hiểu rõ sự khác biệt giữa I/O-bound và CPU-bound, và tại sao mô hình đa nhiệm hợp tác của asyncio lại vượt trội cho các máy chủ web.

2. **Làm chủ sự Đồng thời:** Vượt ra ngoài các `await` tuần tự và sử dụng `asyncio.create_task` và `asyncio.gather` để thực thi các hoạt động I/O song song, giảm đáng kể độ trễ của endpoint.

3. **Tích hợp Lớp Dữ liệu Async:** Đây là bước quan trọng nhất. Chọn một chiến lược truy cập dữ liệu không chặn—cho dù đó là asyncpg thô để có hiệu năng tối đa, 
SQLAlchemy 2.0 để có sức mạnh và sự quen thuộc, hay Tortoise ORM để phát triển nhanh chóng—và áp dụng nó một cách nhất quán.

4. **Áp dụng các Phương pháp Tốt nhất:** Bảo vệ event loop khỏi mã blocking, cấu trúc ứng dụng của bạn theo nguyên tắc "async all the way down", 
và triển khai xử lý lỗi và timeout mạnh mẽ để tạo ra một dịch vụ đáng tin cậy và có khả năng phục hồi.

Bằng cách tuân theo lộ trình này, bạn sẽ có đủ kiến thức nền tảng để không chỉ xây dựng các endpoint CRUD hoạt động, 
mà còn để kiến trúc các hệ thống backend hiệu năng cao, có khả năng mở rộng, tận dụng toàn bộ hệ sinh thái async mà Sanic cung cấp.








