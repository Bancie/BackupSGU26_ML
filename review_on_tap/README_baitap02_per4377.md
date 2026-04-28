# Bài tập 02 (PER-4377) — EDA & tiền xử lý — giải tay (chi tiết kiểu bài thi)

Code đối chiếu: [`bai_tap02_per4377.py`](bai_tap02_per4377.py) (chạy từ repo: `python review_on_tap/bai_tap02_per4377.py`).

Issue: [PER-4377](https://linear.app/bancie/issue/PER-4377)

---

## Khung trả lời “như trong phòng thi”

Mỗi câu lớp nên chia rõ (có thể ghi tay số trong ngoặc ngay bên đề nhỏ):

| Bước | Ghi vào đề làm |
|------|----------------|
| **Cho biết** | Trích những gì được hỏi (có giả định thì nhắn ngắn 1 dòng). |
| **Dữ liệu dùng** | Viết các giá trị quan trắc sẽ vào biểu đồ/phép tính (ID, chỉ các ô không NaN làm được). |
| **Làm từng bước** | Viết $\sum$, sắp xếp, bảng trung gian… — **không bỏ bước trung vị.** |
| **Đáp số** | Viết một câu chốt: số, ID, nhận xét theo nhận định của đề/tổ sư phạm. |

**Lưu ý ôn đồ:** cách định nghĩa **phân vị / whisker của boxplot** và **Pearson đã ghi** dưới đây. Nếu giảng/thi ép định nghĩa khác, trình bày và ghi một dòng đối chiếu “máy tính công cụ XYZ cho $\pm\varepsilon$ không trừ ý học”; **quyết định chấp nhận theo luật lớp**.

---

## Quy ước ôn và đồng bộ máy đối chiếu

- **`?` trong đề** → ô thiếu (**NaN** trong code/pandas).
- **Khoảng tứ phân (${Q_1,Q_3}$)** — toàn README + script **`bai_tap02_per4377.py`** dùng **`pandas.quantile(0{.}25)`, `quantile(0{.}75)`** (**nội suy mạch tuyến tính** giữa hai quan sát kề). Nếu mô hình ôn thầy chỉ Thukey hinges (khác $1\text{–}2\%$ ở bảng nhỏ): ghi tay theo ôn, so với bảng dưới đây nếu cần.
- **Pearson:** trên các cặp **đồng thời đầy đủ** Tuổi–Lương ⇒ **mẫu con $n=8$**, bảng tay dưới **khớp** `numpy.corrcoef` và script.
- **Skew của Tuổi:** báo là **skew mẫu** theo **`pandas.Series.skew()`** (= thị hiếu của biểu đồ; trình bày không cần công thức tay nếu đề chỉ nhận xét nhìn histogram).
- **Câu 2** — **`mean/median`** trên chỉ các ô không thiếu; **mode** khi không có đỉnh tần ($m_{\max}$ chẳng hạn) thì không có mode “chuẩn thống kê”: **pandas** trả một **danh sách các mode** và code lần lại lấy `iloc[0]` — thi tay nên nêu hai hướng: “**không có mode**” / “code lấy phần tử đầu danh sách của pandas”).
- **Câu 6**: trước khi học \(\bar{x}\)/median có hiệu lực cột-wise, **`Lương < 0` → NaN** (**giống `SimpleImputer` trong script**) để **−2000 không kéo** trị mean/median cột điền vào chỗ ô thiếu.
- **Câu 7–10:** sau median-impute của Câu 6, **−2000 (ID 5)** được thể hiện bằng **median các lương dương** trên các ô có số không thiếu ($=8100$, xem chứng minh bên dưới) ⇒ bảng số của Câu 9–10 **khớp** `cleaned_for_later` trong script.

---

## Dữ liệu (10 mẫu)

| ID | Tuổi | Lương | Điểm | Giới tính | Mua hàng |
|----|------|-------|------|-----------|----------|
| 1 | 25 | 8000 | 7.5 | Nam | Yes |
| 2 | 30 | ? | 8.0 | Nữ | No |
| 3 | 22 | 5000 | 6.5 | Nam | Yes |
| 4 | 40 | 15000 | 9.0 | Nữ | Yes |
| 5 | 35 | **−2000** | 7.0 | Nam | No |
| 6 | ? | 7000 | 6.0 | Nữ | Yes |
| 7 | 29 | 8500 | 8.5 | Nam | Yes |
| 8 | 50 | 30000 | 9.5 | Nữ | Yes |
| 9 | 27 | 8200 | ? | Nam | No |
| 10 | 31 | 7800 | 7.8 | Nữ | Yes |

---

### Câu 1 — Số hàng/cột, định loại thuộc tính

**Cho biết:** Bảng khảo sát mẫu bao nhiêu hàng, **không** nhắc quy ước mã `ID` thì xem `ID` chỉ là chỉ số dòng.

**Dữ liệu dùng:** Cả bảng dưới; $N=10$ ô hàng (mỗi hàng là một quan trắc).

**Làm từng bước.**

- Kích thước bảng dạng pandas: `df.shape` ⇒ **10 dòng** $\times$ **6 cột** ⇒ kí hiệu **$(10,\,6)$**. Có $6$ cột mô tả (**ID** + 5 thuộc tính khảo sát).
- Nếu chỉ nói “số đặc trưng cho mô hình (học có giám sát)”, thường **không nhét `ID` vào** (vì là mã thứ tự, không phải độ đo thật) ⇒ còn **5** thuộc tính: Tuổi, Lương, Điểm (**định lượng**), Giới tính (**định tính** 2 thể), Mua hàng (**nhị phân**/nhãn nhắm dự đoán).
- `dtypes` tay: Tuổi / Lương / Điểm ⇒ số thực (**float** nếu có thiếu), Giới tính / Mua hàng ⇒ **danh mục** (chuỗi).

**Đáp số:** Có **10** quan trắc, **6** cột trong file; **5** thuộc tính học máy thường dùng (**bỏ ID** nếu đề hỏi “thuộc tính predictor”).

---

### Câu 2 — Mean / median / mode (Tuổi, Lương, Điểm)

**Giả định:** Mỗi biến tính tay trên chỉ các ô **ghi số** (bỏ các ô `?` của bảng gốc).

**Công thức trung bình mẫu (bỏ ô thiếu):**

$$
\bar{x} = \frac{1}{n_{\mathrm{đủ}}}\sum_{\text{ô có số}} x
$$

#### Tuổi

- Các quan trắc **có tuổi** (theo ID cho dễ nhìn): $\{1{:}25,\,2{:}30,\,3{:}22,\,4{:}40,\,5{:}35,\,7{:}29,\,8{:}50,\,9{:}27,\,10{:}31\}$ (ID 6 thiếu).
- $n_{\mathrm{đủ}}=9$. Tổng $25+30+22+40+35+29+50+27+31=\mathbf{289}$.
- **Mean** $\bar{x}_{\mathrm{Tuổi}}=289/9=\mathbf{32{.}111\dots}\approx 32{,}11$ (năm).
- Sắp tăng $(n=9$ lẻ)$: $22,25,27,29,30,31,35,40,50$. Vị trí trung vị thứ $\tfrac{9+1}{2}=5$: **median** $=\mathbf{30}$.
- **Mode:** mọi giá trị xuất hiện đúng **1** lần ⇒ **không có mode** cổ điển — nếu bắt buộc nêu một số như máy: `pandas.mode().iloc[0]` trên bảng được sắp theo giá trị thường trả **nhỏ nhất** của nhiều “đồng tần”: **22** (đối chiếu `mode=22` của script).

#### Lương

- **Ô có số không rỗng:** $n_{\mathrm{đủ}}=9$ (ID **2** ô trống nên không tính). Giá trị theo ID: $\{1{:}8000,\,3{:}5000,\,4{:}15000,\,5\text{:}{\color{red}-2000},\,6{:}7000,\,7{:}8500,\,8{:}30000,\,9{:}8200,\,10{:}7800\}$.
- Tổng $\sum=\mathbf{87400}$ ⇒ $\bar{x}_{\mathrm{Lương}}=87400/9\approx \mathbf{9722{.}2222}$.
- **Sắp tăng** $n=9$ lẻ: $-2000,5000,7000,7800,8000,8200,8500,15000,30000$ ⇒ **median** $=\mathbf{8000}$ (**vị thứ 5**).
- **Mode tay:** không có mode thống kê học cổ điển (mọi tần như nhau). Tool `pandas`: `mode()` trả danh sách toàn bộ giá trị đã sắp tăng khi mọi điểm chỉ xuất hiện một lần — `iloc[0]` ghi **$-2000$** (**phần tử đầu**) — thi nên nêu rõ **không có mode** và **chỉ tham chiếu máy** nếu bắt buộc ôn.

#### Điểm

- Thiếu một ô (**ID 9**) ⇒ có **9** giá trị: $7{.}5,8{.}0,6{.}5,9{.}0,7{.}0,6{.}0,8{.}5,9{.}5,7{.}8$.
- $\sum=\mathbf{69{,}8000}$, $\bar{y}=69{.}8000/9\approx \mathbf{7{.}756}$.
- Đặt tăng: $6{.}0,6{.}5,7{.}0,7{.}5,7{.}8,8{.}0,8{.}5,9{.}0,9{.}5$. Trung vị vị $\tfrac{n+1}{2}=5$ ⇒ **median** $=\mathbf{7{.}8000}$.
- **Mode tay:** không mode cổ điển; `pandas.mode().iloc[0]` báo **`6{.}0`** (giá nhỏ nhất trong danh sách mode khi mọi tần như nhau).

---

### Câu 3 — Histogram Tuổi (skew) và boxplot Lương

**Giả định:** Histogram trên chỉ các tuổi **không thiếu** (9 ô); boxplot chỉ các lương **không thiếu** (bao gồm **−2000** vì chỉ báo ô rỗng).

**Đồ họa tay:** Vẽ trục $x$ chia khoảng $\approx[22,50]$; bin rộng (ví dụ 22–31, …) — chỉ học không bắt buộc màu trong thi tay.

**Số.**

- Theo `pandas.Series.skew()` trên 9 ô tuổi: skew $\approx \mathbf{1{,}20}$ ⇒ **léch phải** (đuôi về các tuổi lớn hơn 40).
- Theo `quantile(0{.}25)`, `quantile(0{.}75)` trên **9** ô không thiếu của Lương: $\mathbf{Q_1=7000}$, $\mathbf{Q_3=8500}$, $\mathbf{IQR=1500}$; median trùng ô thứ 5 của sắp trên ⇒ **median Lương** $=8000$. Whisker của `matplotlib`/Tukey học ôn vào các **min/max** không vượt ngoại lai của râu ⇒ hiểu rõ **−2000** và **30000** sẽ nằm **ngoài hộp** ⇒ **ngoại lai hình học và nội dung.**

**Đáp viết tay:** Histogram tuổi **hơi lệch phải**; Lương có **ngoại biên âm không thực tế**, đỉnh dương rất xa phần còn lại.

_(Lưu ý ôn có thêm trường hợp bỏ **−2000** trước khi vẽ — chốt ôn không trùng bảng dưới — ghi tay rằng bạn chỉ báo không vẽ giá âm vào ô thường thì phải nói được “chờ Câu 7”!)_


### Câu 4 — Scatter Tuổi–Lương

- Xu hướng: thường **tương quan dương** (tuổi tăng → lương tăng) nếu chỉ xét cặp không thiếu; trên bảng thật cần làm sạch **−2000** và **điền thiếu** trước khi kết luận mạnh.
- Tiền xử lý đề xuất: **impute**; **cắt/thay lỗi −2000**; có thể $\log$ sau khi làm dương và thêm hằng (nếu học phần biến đổi để giảm skew).

---

### Câu 5 — Missing data

- **Tuổi:** thiếu 1 ô (ID 6) → $\frac{1}{10} = 10\%$.
- **Lương:** thiếu ID 2 → $10\%$.
- **Điểm:** thiếu ID 9 → $10\%$.
- Ảnh hưởng: giảm độ chính xác mô tả; một số phương pháp không nhận NA; cần **impute** hoặc **xóa** có kiểm soát.

---

### Câu 6 — Hai cách imputation (mean vs median)

Phổ biến: **điền NaN bằng**:

- trung bình $\bar{x}$ của cột (**mean imputation**),
- hoặc **median** (bền outlier hơn).

Sau khi đánh lương âm là “missing logic” để −2000 không kéo mean trong bước học thống kê, hai cách trên **không giống nhau** ở Lương và Tuổi có thể khác — so bảng trong script.

**Chọn median** khi có skew/outlier nặng (vẫn có giá trị cực đại 30000).

---

### Câu 7 — Chất lượng dữ liệu

- **Lương −2000** cho ID 5: **không thực tế** → coi **lỗi nhập / ghi âm** → **NA rồi median**, hoặc **thay median lương > 0**, hoặc **phân tích riêng**.

---

### Câu 8 — Ngoại lai Lương: IQR và Z-score

**IQR:**

$$
\mathrm{IQR} = Q_3 - Q_1
$$

Ngoại lai Tukey thường dùng $k = 1{,}5$:

$$
x < Q_1 - k\cdot\mathrm{IQR} \quad \text{hoặc} \quad x > Q_3 + k\cdot\mathrm{IQR}
$$

**Z-score:**

$$
z_i = \frac{x_i - \mu}{\sigma}
$$

($\mu,\sigma$ trên **mẫu** hoặc tổng thể — ghi rõ trong bài).

Ngưỡng **$|z|>3$** (tùy lớp). −2000 và 30000 có thể được IQR gắn cờ; −2000 vẫn **sai nội dung** → cần kiểm tra **miền giá trị** (Câu 7).

---

### Câu 9 — Chuẩn hóa Z-score Lương

$$
z = \frac{x - \mu}{\sigma}
$$

Sau chuẩn hóa cột, trung bình $z$ của cột **$\approx 0$**, độ lệch chuẩn **$\approx 1$**.

**Nhận xét:** thang đo vô đơn vị tuyệt đối của Lương; so các mẫu theo số sigma.

---

### Câu 10 — Encoding

- **Giới tính — one-hot:** cột `{Nam, Nữ}` tương ứng bảng học đã giảng (đôi khi `drop_first=True` để tránh nhân một hệ số không xác định).
- **Mua:** $\mathrm{Yes} \to 1$, $\mathrm{No} \to 0$.

Ghép với các cột đã làm sạch — xem output script.

---

### Câu 11 — Feature selection

- **ID** thường **không** làm đặc trưng dự đoán Mua (trừ khi chuỗi thời gian) → **bỏ**.
- **Tuổi, Điểm, Lương** — liên quan; cần xử thiếu/lỗi.
- **Giới tính** — one-hot nếu giữ.
- Cột thiếu/lỗi nặng **không khắc phục được** → cân nhắc **bỏ** hoặc **giảm độ tin cậy**.

---

### Câu 12 — Giảm chiều

- **Xóa biến:** loại **ID**; đơn giản với bảng nhỏ.
- **PCA:** khi **nhiều** biến định lượng **tương quan cao**; cần **chuẩn hóa** trước PCA. Ở bài này **ít** biến định lượng + có biến danh mục → **ưu tiên** trình bày khi nào PCA phù hợp hơn là gắn vào bảng này.

---

## Hình do script tạo

- `hist_tuoi_boxplot_luong_baitap02.png`
- `scatter_age_luong_baitap02.png`
