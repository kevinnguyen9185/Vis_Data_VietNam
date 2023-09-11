# DataVietNam
# Vis_Data_VietNam
# DataVietNam
Trong Project này có 2 phần chính:
    
+ Crawl (Kéo dữ liệu từ các nguồn)
+ Transform (Biến đối và compare)

Để dễ tiếp cận đọc và chính sửa code thì tài liệu này sẽ giải thích chi tiết các hàm trong hệ thống, về flow data sẽ chạy theo 2 phần chính như kia:
# Crawl
- Nhìn chung các tool hiện tại đang sử dụng đều có thể đáp ứng được 80-90% các nguồn dữ liệu trên mạng (Hiện chưa có chức năng xử lý capcha):

| Công nghệ | Chức năng | Áp dụng | Ký hiệu |
|-----------|-----------|---------|---------|
| BeatifulSoup | Phân tích cú pháp HTML | Khi có source HTML | BS4_ |
| Request | Gửi yêu cầu đến máy chủ để lấy dữ liệu về | Khi phát hiện được API của trang web để public | R_ |
| Selenium | Tương tác nhưng người thật với máy để lấy được Source HTML của trang web | Khi không thể dùng request để lấy | S_ |
## Base
- Trong quá trình làm thì để tạo ra những công việc chung nhất sau này tiện cho việc tái sử dụng code thì hệ thống có cung cấp các hàm cơ bản để tương tác và hiện nó được lưu trữ và được để trong thư mục

    ![image](https://user-images.githubusercontent.com/35418790/236776337-138eac38-1834-4885-a5e1-f4e62a2407f8.png)
- Cần quan tâm những file sau:

| Tên file | Nhiệm vụ |
|-----------|-----------|
| setup.py | Lưu trữ các hàm cơ bản để tương tác với trang web. Đọc chi tiết ở phần dưới đây. [API](#api_setup) |
| URL.py | Nơi lưu trữ các đường dẫn của các nguồn khác nhau, Có tài khoản của VietStock |

## Source Data

![image](https://user-images.githubusercontent.com/35418790/236780765-e8138d16-1aa6-4154-baac-957602f7c9ce.png)

- Cần quan tâm những file sau:

| Tên file | API | Trạng Thái | Công nghệ |
|-----------|-----------|-----------|----------|
| CafeF.py |  [API](#CafeF) | Kéo hàng ngày | BS4, R_, S_ |
| SSI.py | [API](#SSI) | Kéo 1 lần | R_ |
| StockBiz.py | [API](#StockBiz) | Kéo 1 lần | BS4, R_ |
| TVSI.py | [API](#TVSI) | Kéo 1 lần | BS4, R_ |
| VietStock.py | [API](#VietStock) | Kéo hàng ngày |  BS4, R_, S_ |
| Web68.py | [API](#Web68) | Kéo 1 lần | BS4, R_, S_ |

## Crawl main
Đây là thư mục lưu trữ phần kéo data:

![image](https://github.com/dangthevang/DataVietNam/assets/35418790/858c72f2-512b-48f9-851b-0996dbde1b8e)

| Data | Tên file | Trạng Thái | Source | Mô tả |
|-----------|-----------|-----------|-----------|------------------------------|
| ListCompany | crawl_list_company.py | Running | VietStock| Kéo danh sách những công ty bình thường trên 3 sàn chính |
| Price | crawl_price.py | Stop | CafeF | Lấy giá 6 tháng gần nhất |
| Price Day | crawl_price_day.py | Running | Iboard_SSI | Lấy giá hàng ngày từ bảng giá giao dịch|
| Financial | crawl_financail.py | Running | CafeF, VietStock | Lấy báo cáo tài chính thời điểm gần nhất từ 2 nguồn Source |
| Volume | craw_volume.py | Running | CafeF, VietStock | Lấy khối lượng giao dịch hiện tại từ 2 nguồn Source |
| Dividend | crawl_dividend.py | Running | CafeF, VietStock | Lấy cổ tức thời điểm gần nhất 2 nguồn Source |

<a name="api"></a>
# API
<a name="api_setup"></a>
## Setup.py
| Feature | Argument Default | Type | Description |
|---------|----------|---------|----------|
| Setup(type_tech,source) | type_tech="Selenium", source="CF" | Class | Nơi khai báo các thuộc tính cần có của các trang web: user = USER,password = PASSWORD,year = 0, quater = 0, day = 0, symbol = "", form_data = {}, HEADERS |
| turn_off_drive() | None | None | Tắt driver (hiện tại Selenium) hệ thống |
| reset_colab()    | None | None | Thiết lập cài đặt ban đầu của selenium trên google colab |
| reset_driver()   | None | None | Thiết lập driver (hiện tại Selenium) trên máy local |
| request_link(link, time) | link, time | None | Request đường link bằng selenium |
| find_element_by_xpath(something) | something | None | Tìm kiếm phần tử HTML bằng xpath |
| find_element_by_other(something, other) | something | None | Tìm kiếm phần tử HTML bằng phần tử By(ID,Class,..) |
| click_something_by_xpath(something) | something | None | Click phần tử HTML bằng phần tử By(ID,Class,..) |
| click_something_by_id(something) | something | None | Click phần tử HTML bằng phần tử ID |
| click_something_by_other(something, other) | something, other | None | Click phần tử HTML bằng phần tử By(ID,Class,..) |
| send_something_by_id(id, somthing) | something | None | Điển vào input theo ID |
| send_something_by_other(somthing, other_txt, other) | somthing, other_txt, other | None |  Điền vào input phần tử HTML bằng phần tử By(ID,Class,..) |
| r_get(url) | url | string | request bằng link theo phương thức get |
| r_post(url, data, cookie, headers) | data, cookie, headers | string | request bằng link theo phương thức post, data là payload, header mặc định theo thuộc tính của Setup |
| click_select(name, value) | name, value | None | Chọn seletion trong HTML |
| download_batch_get_post(url, dict_) | url, dict_ | DataFrame | Tải bảng theo post, url là đường link, dict_ là thuộc tính của bảng |
| download_batch_selenium(url, dict_) | url, dict_ | DataFrame | Tải bảng theo selenium, url là đường link, dict_ là thuộc tính của bảng  |
| download_batch_get_request(url, dict_) | url, dict_ | DataFrame | Tả bảng theo get, url là đường link, dict_ là thuộc tính của bảng  |

<a name="api_url"></a>
## URL.py
| Argument Default | Description |
|---------|----------|
| URL_STOCK_BIZ | link Stock Biz |
| URL_TVSI | link TVSI |
| URL_VIETSTOCK | link Viet Stock |
| URL_68 | link 68 |
| USER | Tài khoản Viet Stock |
| PASSWORD | Mật khẩu Viet Stock |
| URL_CAFE | link CafeF |


<a name="Transform"></a>
# Transform 
- Tổng hợp các file để từ thư mục Ingestion để Transform lại thành file chính.
- Transform chia làm 3 phần chính:
   + Transform: Base, run
   + Merge: Merge
   + Ghép file tổng, export: Các file export 
 Để hiểu được flow data người đọc cần hiều quy trình theo từng bước:
    + Bước 1: [Detail](#Step_1) Tạo folder, lấy danh sách company 
    + Bước 2: [Detail](#Step_2) Lấy file raw từ folder Data Ingestion: Hiện tại có 3 thành phần sẽ lấy file Financial, Dividend, Volumn. Price sẽ lấy trực tiếp từ Realday
    + Bước 3: [Detail](#Step_3) Lấy biến đổi xuất file compare ra để so sánh với các quy ước và phương pháp ban đầu
    + Bước 4: [Detail](#Step_4) Tổng hợp file từng thành phần. Ví dụ: Dividend riêng file Dividend, Financial riêng file Financial,...
    + Bước 5: [Detail](#Step_5) Xử lý bằng tay
    + Bước 6: [Detail](#Step_6) Merge từng thành phần.
    + Bước 7: [Detail](#Step_7) Export data từ những file nhỏ

<a name="Base"></a>
## Base.py

| Tên file | Mô tả | Lưu ý |
|-----------|-----------|-----------|
| Compare.py | Tổng hợp thành phần compare dùng để so sánh trong hệ thống | Khi cần xem lại quy ước, logic compare thì có thể xem ở đây |
| Dividend.py | Tổng hợp các thành phần xử lý, trích xuất các file Dividend | Hiện đang có VS, CafeF |
| Financial.py | Tổng hợp các thành phần xử lý, trích xuất các file Financail | Ở đây có 2 đối tượng: VS, CafeF và chứa đầy đủ các bước biến đổi |
| ListSymbol.py | Tổng hợp xử lý file Symbol đầu vào | Hiện chưa có gì cần xử lý |
| PATH_UPDATE.py | Các thành phần đường dẫn cơ bản cần có | Trong dây cần chú ý 2 thư mục chính FC(đối tượng folder Crawl) và FU(Đối tượng folder Update) |
| Price.py | Tổng hợp các hàm xử lý giá | Chú yếu các hàm xử lý giai đoạn crawl giá 2 ngày 1 lần |
| Setup.py | Nơi khởi tạo những yêu cầu cơ bản khi bắt đầu chạy Tranform | Cần chú ý đến các tham số SYMBOL(Mã công ty), F_START(Tên thư mục bắt đầu), F_END(Tên thư mục kết thúc), F_RANGE(List thư mục chạy qua)|
| Volume.py | Tổng hợp các hàm xử lý Volume |  |

## VAR_GLOBAL_CONFIG.py
Đây là nơi cấu hình cơ bản các biến số khi chạy trasform vào một thời điểm nào đấy
| Argument Default | Description |
|---------|----------|
| START_DAY_UPDATE | Ngày bắt đầu lấy khi quét file update |
| START_DAY_LIST_UPDATE | Ngày lấy danh sách mã công ty cụ thể |
| END_DAY_UPDATE | Ngày dừng khi lấy khi quét file update |
| QUARTER_KEY | Quý tạo báo cáo tài chính VD: 4/2023,1/2022 |
| YEAR_KEY | Năm tạo báo cáo tài chính VD: 2021,2022 |
| TYPE_TIME | Loại báo cáo tài chính theo thời gian ,True là Năm, Flase là Quý |
| FILE_FEATURE | Tên file nhãn, tên cột sau khi được dịch cần có |
| QUARTER_FINANCAIL_FIX_FILE | Tên file financial sau khi được quyết định |
| QUARTER_FINANCAIL_FIX_FILE_BY_HUMAN | Tên file data được người fix tay(Cái này sử dụng khi phải chỉnh sửa bằng tay phần nhỏ) |
| PATH_DISTILLATION_VIETNAM_ALLREAL | Thư mục lưu trữ file trong Storage |
| PATH_DISTILLATION_VIETNAM_ADDITIONALDATA | Thư mục lưu trữ tạm thời file trong Storage |
| COMPANY_ACTIVE | Danh sách những công ty quyết định là sàn có tồn tại hay đang hoạt động hay không, check xem ngày nào là ngày giao dịch |

<a name="Step_1"></a>
## Step 1
Bước này chỉ đơn thuần là tại thư mục trong Raw VIS, Cần chú ý các tham khởi tạo ngày trong VAR_GLOBAL_CONFIG.py:
    + START_DAY_UPDATE
    + START_DAY_LIST_UPDATE
    + END_DAY_UPDATE
Sau khi chỉnh sửa chỉ cần chạy 0_CreateFolder.py trong run

<a name="Step_2"></a>
## Step 2
Bước này lấy danh sách mã công ty để vào trong thư mục vừa được tạo từ bước trên.
Cần chú ý Check kỹ lại dữ liệu được ghi vào xem có đúng file cần lấy theo thư mục START_DAY_LIST_UPDATE

<a name="Step_3"></a>
## Step 3
Quét qua các file ở Ingestion để cho vào RawVIS tương ứng, Hiện có 3 thành phần sẽ support:
+ Financial
+ Dividend
+ Volume
- Price theo đợt kéo theo batch(Kéo đồng loại trên CafeF) không cần chạy nữa. Nhưng nếu cần vẫn còn hàm để đọc phần này
- Chạy file _2_Choose_file.py để có thể quan tâm.
- Đọc kỹ comment để biết được các tham số

<a name="Step_4"></a>
## Step 4
- Tuyển tập code chạy các transform và compare các thành phần riêng biệt, cần phần nào chạy phần đấy không ảnh hưởng đến nhau
Quy ước chung:

| Value | Mean |
|-------|------|
| 1 | 2 giá trị bằng nhau |
| 0 | 2 giá trị khác nhau |
| N | cả 2 giá trị đều là NaN |
| 2 | có 1 trong 2 giá trị là NaN |

- Các file code trong bước này:
  
| Component | Description | Note |
|---------|----------|------------|
| _4_Price.py | Trasform file Price từ bước 3 | Hiện đang không sử dụng |
| _4_Value_ARG.py | Transform giá trị giao dịch từ bước 3 | Hiện đang không sử dụng |
| _5_Volume.py | Trasform và compare giá trị Volume của 2 nguồn CF, VS | |
| _6_Dividend.py | Trasform và compare giá trị Dividend của 2 nguồn CF, VS | |
| _3_Financial.py | Trasform và compare giá trị Financial của 2 nguồn CF, VS | |

- Sau khi chạy xong các thành phần thì chạy file tổng hợp nhưng so sánh các giá trị của 2 nguồn để gom file lại làm 1 cho bước tiếp theo xử lý. Chính là file Total_Compare.py

## Step 5
Bước này xử lý bằng tay để xử lý những so sánh nên không có gì để comment
Có một lưu ý nhỏ với quy ước đặt tên trường dữ liệu:
+ Chữ trường dữ liệu phải là chữ in hoa
+ Dữ liệu chốt được đặt tên là FIX
+ Không được phép sửa các trường dữ liệu ở những file ở bước trước đấy

## Step 6
Sau khi nhận được file thì ta sẽ cần xuất thành nhưng file quyết định cuối cùng riêng rẽ. Ở bước này cần quan tâm đến folder merge nhé.
![image](https://github.com/dangthevang/DataVietNam/assets/35418790/b2e55c1f-51a7-4ca7-ae1b-f3ae1bf03251)
Nhìn chung ở bước này thường thì chỉ đơn thuần là chạy file tương ứng với dữ liệu đầu vào.

## Step 7
Bước này chính là bước cuối cùng trong việc ghép một file data hoàn chỉnh.
Lưu ý khi chạy file
- Với bản update mối thì Price sẽ được chạy trong đây, Nên cần chắc chắn check lại file giá giao dịch gần nhất.
- File code chính để thấy được mindset ghép data là ExportFileTemp.py
- Chạy từng bước một để check data đầu vào đầu ra.
- Hiện có 2 dạng yêu cầu của team DA, DS đó là:
    + Ghép giá bán cho quý cũ: Khi làm task này cần chú ý đến Dividend và Giá giao dịch
    + Ghép giá mua cho quý mới: Khi làm task này cần chú ý Financial, volume, giá giao dịch.
-------------------------------------------------------------------------------------------------
## Conclusion
- Tài liệu này với mục đích cho người dùng thấy tổng quan được code và các lưu ý trong quá trình xử lý data chứ không phải là một tài liệu toàn năng giúp bạn tìm được mọi vấn đề sẽ có trong quá trình làm.
- Để hiểu được bạn cần tự đọc code và hiểu chúng.
- Trong quá trình làm có bất kỳ thay đổi và lưu ý bạn có thể tiếp tục chỉnh sửa file readme này để người đọc hiểu hơn nhé.
  Good luck!!!  

