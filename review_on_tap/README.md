# Tài liệu ôn tập — `review_on_tap`

Giải tay (thi trên giấy) kèm script Python để đối chiếu số. **Mục lục:** Câu 2.1 · Câu 2.2 · Phần 3.

| Nội dung | Linear | Script |
| -------- | ------ | ------ |
| Câu 2.1 — thống kê mô tả (tuổi) | [PER-4322](https://linear.app/bancie/issue/PER-4322/cau-21) | `cau2_1_per4322.py` |
| Câu 2.2 — thang đo Stevens | [PER-4332](https://linear.app/bancie/issue/PER-4332/cau-22) | `cau2_2_per4332.py` |
| Phần 3 — ma trận nhầm lẫn & độ đo | [PER-4375](https://linear.app/bancie/issue/PER-4375/checklist-on-phan-3) | `cau3_phan3_per4375.py` |

---

## Câu 2.1 (PER-4322) — Giải tay (thi trên giấy) và kiểm tra bằng code

Tài liệu này trình bày **cách làm truyền thống từng bước** cho bài ôn tập về thuộc tính **tuổi**; file `cau2_1_per4322.py` dùng để **đối chiếu đáp án** sau khi bạn tự tính.

---

### Dữ liệu (đã sắp tăng dần)

n = 27

```
13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33,
35, 35, 35, 35, 36, 40, 45, 46, 52, 70
```

Đánh số thứ tự từ **1** đến **27** (trên giấy bạn có thể ghi số thứ tự dưới mỗi giá trị để khỏi nhầm vị trí).

---

### Phần (a): Trung bình, trung vị, mode

#### Bước 1 — Tổng các giá trị (chia nhóm cho dễ cộng)


| Nhóm      | Giá trị                | Tổng                                |
| --------- | ---------------------- | ----------------------------------- |
| 10 số đầu | 13…22, 22              | 13+15+16+16+19+20+20+21+22+22 = 184 |
| Bốn số 25 | 25×4                   | 100                                 |
| 30        |                        | 30                                  |
| Hai số 33 |                        | 66                                  |
| Bốn số 35 | 35×4                   | 140                                 |
| Còn lại   | 36, 40, 45, 46, 52, 70 | 36+40+45+46+52+70 = 289             |


**Tổng:** 184 + 100 + 30 + 66 + 140 + 289 = 809.

#### Bước 2 — Trung bình (mean)

\bar{x} = \frac{809}{27} \approx 29{,}963 \quad \text{(trên giấy thường ghi } 29{,}96 \text{ hoặc phân số } \frac{809}{27}\text{).}

#### Bước 3 — Trung vị (median)

n = 27 lẻ → trung vị là **giá trị ở vị trí giữa**:

\text{vị trí} = \frac{n+1}{2} = \frac{28}{2} = 14.

Đếm trên dãy đã sắp: phần tử thứ **14** (kể từ 1) là **25**.

**Trung vị = 25.**

#### Bước 4 — Mode (mốt)

Đếm tần số từng giá trị (có thể lập bảng tần số gọn):

- 25 xuất hiện **4** lần  
- 35 xuất hiện **4** lần  
- Các giá trị khác **≤ 2** lần

Vậy có **hai mode**: **25** và **35** (tập **đa mốt**).

---

### Phần (b): Tứ phân vị Q1 và Q3 (đề cho phép xấp xỉ)

Có **hai cách** tài liệu hay dùng; nếu thầy dạy theo cách nào thì bạn dùng đúng cách đó. Trên thi, **ghi rõ công thức bạn dùng** là ổn.

#### Cách 1 — Vị trí phần tử theo tỷ lệ (n+1) (dễ tính tay)

- **Q1** ứng với **25%** dưới: vị trí (theo 1-based)

v_1 = \frac{1}{4}(n+1) = \frac{28}{4} = 7.

Phần tử thứ **7** trong dãy tăng dần là **20** → **Q1 = 20** (khi thầy dùng “lấy đúng phần tử tại vị trí nguyên”).

- **Q3** ứng với **75%**: vị trí

v_3 = \frac{3}{4}(n+1) = 21.

Phần tử thứ **21** là **35** → **Q3 = 35**.

- **IQR** (khoảng tứ phân vị):  \mathrm{IQR} = 35 - 20 = 15 .

#### Cách 2 — Tứ phân vị nội suy tuyến tính (gần với hàm `quantile` / Excel)

Công thức thường dùng: vị trí tứ phân vị ở mức p (0,25 hoặc 0,75) theo 1-based là  
L = 1 + p \times (n - 1).

- **Q1** (p = 0{,}25):  
L = 1 + 0{,}25 \times 26 = 7{,}5  
→ nằm **giữa** phần tử 7 (20) và 8 (21):

\mathrm{Q1} = \frac{20+21}{2} = 20{,}5.

- **Q3** (p = 0{,}75):  
L = 1 + 0{,}75 \times 26 = 20{,}5  
→ nằm **giữa** phần tử 20 (35) và 21 (35):

\mathrm{Q3} = \frac{35+35}{2} = 35.

- **IQR (cách 2)**: 35 - 20{,}5 = 14{,}5.

**Gợi ý khi thi:** Nếu đề nói *“xấp xỉ nếu cần”*, bạn có thể nội suy (20,5; 35) **hoặc** lấy nguyên (20; 35) — quan trọng là trình tự **công bố công thức** cho điểm thẳng.

---

### Phần (c): Vẽ boxplot và nhận xét (trên giấy)

#### Bước 1 — Năm số tóm tắt (five-number summary)

- **Min** = 13  
- **Q1** = 20 (cách 1) hoặc 20,5 (cách 2)  
- **Median** = 25  
- **Q3** = 35  
- **Max** = 70

(Trong boxplot, trục tung là thang tuổi: vẽ hộp từ Q1 đến Q3, đường giữa hộp là median, “râu” xuống min và lên max **theo quy ước môn học** — thường **giới hạn bởi 1,5·IQR**; giá trị nằm ngoài bằng **điểm** hoặc “râu kéo đến giá trị hợp lệ lớn nhất trong khoảng”).

#### Bước 2 — Rào 1,5·IQR (dùng IQR đã tính)

- Với **IQR = 15** (Q1=20, Q3=35):  
Cận trên: 35 + 1{,}5 \times 15 = 35 + 22{,}5 = 57{,}5.  
Vì **70 > 57,5** → **70 thường xem là ngoại lai (outlier)** phía trên; trên hình có thể vẽ 70 bằng *chấm* riêng, râu dừng tại 52 (hoặc theo cách bài tập/WeMooc của lớp).
- Với **IQR = 14,5** (Q1=20,5, Q3=35):  
Cận trên: 35 + 1{,}5 \times 14{,}5 = 56{,}75 → **70** vẫn **> 56,75** → vẫn ngoài rào.

#### Bước 3 — Nhận xét phân bố (viết 2–3 câu)

- **Trung bình (≈ 29,96) > trung vị (25)** → phân bố **lệch phải** (đuôi dài về phía lớn).  
- Có **giá trị rất lớn (70)** kéo mean lên, trong khi phần lớn dữ liệu tập trung ở khoảng 15–40.  
- (Tuỳ trình bày) **Độ tập trung** của phần 50% giữa: hộp từ Q1 đến Q3 (khoảng 20–35).

---

### Phần (d): Rời rạc hóa với k = 4

Cần nêu rõ: **chia độ rộng đều** (equal-width) **hoặc** **chia tần số đều** (equal-frequency / equal-depth).

#### Dạng 1 — Chia độ rộng đều (4 khoảng cùng độ dài trên trục giá trị)

1. **Min** = 13, **max** = 70.
2. **Độ dài từng khoảng**
  w = \frac{70-13}{4} = \frac{57}{4} = 14{,}25.
3. Các mốc:
  - L_0 = 13  
  - L_1 = 13 + 14{,}25 = 27{,}25  
  - L_2 = 27{,}25 + 14{,}25 = 41{,}5  
  - L_3 = 41{,}5 + 14{,}25 = 55{,}75  
  - L_4 = 70
4. Các lớp (dạng bán mở thường dùng):
  (13, 27{,}25\rbrack,\ (27{,}25, 41{,}5\rbrack,\ (41{,}5, 55{,}75\rbrack,\ (55{,}75, 70\rbrack  
   (cách mở/đóng cạnh: **ghi đúng** theo tài liệu lớp; quan trọng là cách bạn gán từng số trùng mốc).
5. **Đếm số mẫu từng lớp** (đối chiếu từng giá trị trong bảng):


| Lớp (ý niệm)                                                            | Số mẫu (đếm)  |
| ----------------------------------------------------------------------- | ------------- |
| Lớn nhất: (12{,}99\cdots, 27{,}25] tương ứng khoảng từ 13 lên tới 27,25 | **14**        |
| Kế tiếp: đến 41,5                                                       | **9**         |
|                                                                         | **3**         |
| Lớp chứa 70 (đến 70)                                                    | **1**         |
|                                                                         | **Cộng = 27** |


#### Dạng 2 — Chia tần số đều (4 nhóm, mỗi nhóm số mẫu gần bằng nhau)

- 27 \div 4 = 6{,}75 → có thể chia **7 + 7 + 7 + 6** mẫu (tổng 27), số mẫu mỗi lớp **gần bằng** nhau.
- Xếp dãy đã tăng dần, **cắt** theo thứ tự:


| Lớp | Các mẫu (position 1–7, 8–14, …) | Số mẫu |
| --- | ------------------------------- | ------ |
| 1   | 13, 15, 16, 16, 19, 20, 20      | 7      |
| 2   | 21, 22, 22, 25, 25, 25, 25      | 7      |
| 3   | 30, 33, 33, 35, 35, 35, 35      | 7      |
| 4   | 36, 40, 45, 46, 52, 70          | 6      |


- **Ranh giới lớp** (để mô tả: “Lớp 1: tuổi từ … đến …; Lớp 2: từ …”): theo cách **bài giải**, có thể nêu: ranh ở khoảng (20, 21), (25, 30), (35, 36) — nghĩa là tách theo thứ tự **giữa** 20 và 21, 25 và 30, 35 và 36.

---

### Kiểm tra bằng code (cùng thư mục)

Từ thư mục `review_on_tap`:

```bash
cd review_on_tap
python cau2_1_per4322.py
```

Script sẽ:

- in lại (a)–(d) tương ứng với các bước tay;  
- lưu hình `boxplot_tuoi_cau2_1.png` (để xem dạng boxplot tự động, **không thay thế cách vẽ tay trên bài thi**).

Bạn dùng output để **so khớp từng số** sau khi đã tự tính trên giấy.

---

### Tóm tắt số cần nhớ nhanh


| Chỉ số                     | Giá trị (theo tính tay / code thống nhất) |
| -------------------------- | ----------------------------------------- |
| n, tổng                    | 27; 809                                   |
| Trung bình                 | 809/27 \approx 29{,}96                    |
| Trung vị                   | 25                                        |
| Mode                       | 25 và 35                                  |
| Q1, Q3 (cách vị trí 7, 21) | 20; 35                                    |
| Q1, Q3 (nội suy tuyến)     | 20,5; 35                                  |
| Chia rộng đều k=4, bước w  | 14,25; mẫu: 14, 9, 3, 1                   |
| Chia tần số tương đương    | 7, 7, 7, 6                                |


---

## Câu 2.2 (PER-4332) — Thang đo (Stevens) & đối chiếu W₁…W₆ với V

Giải **trên giấy**; file `cau2_2_per4332.py` dùng để **kiểm tra công thức** và cùng thang theo từng định nghĩa.

Bảng dữ liệu (5 cột A…E, theo hàng):


|          | A   | B   | C   | D   | E   |
| -------- | --- | --- | --- | --- | --- |
| **V(.)** | 1   | 2   | 3   | 4   | 5   |
| **W₁**   | 100 | 200 | 300 | 400 | 500 |
| **W₂**   | 10  | 11  | 12  | 13  | 14  |
| **W₃**   | 8   | 13  | 45  | 6   | 7   |
| **W₄**   | 1   | 4   | 9   | 16  | 25  |
| **W₅**   | −10 | −8  | −6  | −4  | −2  |
| **W₆**   | 3   | 6   | 9   | 12  | 15  |


Câu hỏi: (1) V được đo theo **thang nào** trong bốn thang: định danh, thứ tự, khoảng, tỷ lệ? (2) Wᵢ nào **cùng thang** với V(.)?

**Ánh xạ tuyến tính/afin từ V** (kiểm tra từng cột, v ∈ {1,2,3,4,5}):

- W₁(v) = **100v**
- W₂(v) = **v + 9**
- W₄(v) = **v²**
- W₅(v) = **2v − 12**
- W₆(v) = **3v**
- W₃: dãy **8, 13, 45, 6, 7** theo cùng thứ tự cột V = 1,2,3,4,5 **không** tăng dần (8 < 13 < 45 nhưng 45 > 6), nên **không cùng thứ tự** với thứ tự của V, và **không** tồn tại a, b với W = av + b cho cả 5 cột (hệ phương trình mâu thuẫn nếu cố gắng từ hai cặp điểm).

---

### Bốn thang đo (Stevens) — nắm nhanh

1. **Định danh (nominal):** chỉ phân **loại tên**; số nếu có chỉ là mã, **không** nói a < b theo nghĩa “hơn/kém về bậc” trừ khi cùng tên.
2. **Thứ tự (ordinal):** thứ tự A < B < … **có ý nghĩa**; khoảng cách số trên mã **chưa chắc** tương đương.
3. **Khoảng (interval):** thứ tự **và** chênh lệch (hiệu) **có ý nghĩa**; **tỷ lệ** (a/b) **chưa** nhất thiết; thường **không** có số 0 tuyệt đối “vắng mặt” theo nghĩa vật lý. Phép tương đương thường: **W = aV + b** với **a > 0** (phép afin tăng).
4. **Tỷ lệ (ratio):** có thêm **gốc 0** tuyệt đối; tỷ số b có ý. Phép tương đương hẹp: **W = aV**, **a > 0** (nhân tỷ lệ **qua gốc** — không cộng hằng, trừ trường hợp đổi đơn vị vẫn về dạng aV).

Bài tập: V = 1,2,3,4,5, **bước 1** — **có thứ tự**; **bước 2** — hiệu giữa hai cột cách 1 cùng 1, nên mã cách **đều 1** thường xử lý như cho phép tính **chênh lệch** trên bảng → **(3) thang khoảng (interval)** phù hợp hơn hẳn “chỉ tên” hoặc “chỉ hạng”.  
Mã **1…5** **không** có 0, và đề **không** mô tả nghĩa “gấp đôi 2 bằng 1 + 1” theo tỷ lệ vật lý → thường **không** gọi V là **(4) tỷ lệ** trong cùng dạng bài sách giáo trình dụng tạo.

**Kết luận cho PER-4333 — thang đo của V(.) (đáp án ôn thường dùng):** **(3) thang khoảng (interval)**.

Nếu giảng viên chấm theo cách *chỉ* xem V là mã hạng (không tính hiệu), có thể giải thích **(2) thứ tự**; khi đó cùng thứ tự bậc tăng ở dưới sẽ **rộng** hơn (gồm cả W₄) — ghi ở mục “Ghi chú bài tập thứ tự”.

---

### Cùng thang **khoảng** (interval) với V: phép afin tăng

Hai ánh xạ từ V lên cùng một “bậc thang khoảng” là **tương đương** nếu tồn tại số **a > 0** và **b** sao cho mọi cột: **W = a·V + b**.

- **Bước 1 — Thử 2 cột bất kỳ** (ví dụ A, B) để tìm a, b.  
- **Bước 2 — Thay v vào 3 cột còn lại**; nếu **đúng cả 5 cột** → cùng thang khoảng.  
- **Bước 3** — Nếu **không tồn tại** a, b, hoặc a ≤ 0 → **không** cùng thang khoảng.

Tính toán **tay** từng hàng:


| Biến | Công thức từ V | Dạng aV + b?                                                                                                            | a > 0? | Cùng thang khoảng với V? |
| ---- | -------------- | ----------------------------------------------------------------------------------------------------------------------- | ------ | ------------------------ |
| W₁   | 100V           | 100V + 0                                                                                                                | Có     | **Có** (PER-4334)        |
| W₂   | V + 9          | 1·V + 9                                                                                                                 | Có     | **Có** (PER-4335)        |
| W₃   | —              | Không tuyến tính theo cột; dãy không đơn điệu cùng V                                                                    | —      | **Không** (PER-4336)     |
| W₄   | V²             | Hệ số tăng giữa các bước không thẳng (W(2)−W(1)=3, W(3)−W(2)=5, …); **không** dạng aV+b với a, b cố định trên toàn bảng | —      | **Không** (PER-4337)     |
| W₅   | 2V − 12        | 2V + (−12)                                                                                                              | Có     | **Có** (PER-4338)        |
| W₆   | 3V             | 3V + 0                                                                                                                  | Có     | **Có** (PER-4339)        |


**Viết tối thiểu trên bài nộp:**

- **W₁, W₅, W₆:** tìm a, b từ hai giá trị (ví dụ tại v=1, v=2), rồi thử v=3,4,5.  
- **W₂:** W₂ = V + 9 rõ.  
- **W₄:** V = 1,2,3,4,5 thì (W₄(2)−W₄(1))/(2−1) = 3, (W₄(3)−W₄(2))/(1) = 5 **khác** nhau → **không** afin.  
- **W₃:** Thứ tự W₃ theo cột: D = 6 < E = 7 < A = 8 < B = 13 < C = 45 **khác** thứ tự V, hoặc liệt kê: v tăng, W₃: 8,13,45,6,7 — **không** tăng dần → **không** afin, **không** cùng thang khoảng.

**Tổng hợp câu (2) — cùng thang (interval) với V:** **W₁, W₂, W₅, W₆**. **Không:** **W₃, W₄**.

---

### Ghi chú: nếu V được coi là thang **thứ tự (ordinal)**

Phép cho phép: **bảo toàn thứ tự** nghiệm (đơn điệu **tăng** nghiêm nếu V tăng theo cột A→E).  

- **Cùng thứ tự** với V: W₁, W₂, W₄, W₅, W₆.  
- **Không** cùng: **W₃** (thứ tự cột theo mã V không còn tăng theo cùng cách).

Nếu thầy yêu cầu **cùng thang tỷ lệ (ratio)** thuần (chỉ W = aV): chỉ xét **W₁, W₆** (và so với bản thân khi gọi V là tỷ lệ — ở đây bảng 1..5 nhiều tài liệu **vẫn gọi V là khoảng, không tỷ lệ**).

---

### Mã Linear (sub-issues) — ánh xạ câu trả lời


| Issue        | Nội dung          | Tóm tắt trả lời                                             |
| ------------ | ----------------- | ----------------------------------------------------------- |
| **PER-4333** | Thang đo của V(.) | **(3) Thang khoảng (interval)** — theo cách môn học ở trên. |
| **PER-4334** | W₁ vs V           | Cùng: **W₁ = 100V**.                                        |
| **PER-4335** | W₂ vs V           | Cùng: **W₂ = V + 9**.                                       |
| **PER-4336** | W₃ vs V           | Không: thứ tự/không afin.                                   |
| **PER-4337** | W₄ vs V           | Không: **V²** không afin.                                   |
| **PER-4338** | W₅ vs V           | Cùng: **W₅ = 2V − 12**.                                     |
| **PER-4339** | W₆ vs V           | Cùng: **W₆ = 3V**.                                          |


---

### Kiểm tra bằng code

Từ thư mục `review_on_tap`:

```bash
python cau2_2_per4332.py
```

Script kiểm tra công thức, thử ánh xạ afin, và in từng dòng ứng với **PER-4333 … PER-4339**.

[Linear PER-4332](https://linear.app/bancie/issue/PER-4332/cau-22)
---

## Phần 3 (PER-4375) — Ma trận nhầm lẫn & độ đo: Câu 3.1 – 3.4

Lời giải **làm tay** (thi trên giấy). Code kiểm tra: chạy `python cau3_phan3_per4375.py` (cùng thư mục `review_on_tap`).


| Linear                                               | Câu                        |
| ---------------------------------------------------- | -------------------------- |
| [PER-4340](https://linear.app/bancie/issue/PER-4340) | 3.1 — đa lớp A, B, C       |
| [PER-4346](https://linear.app/bancie/issue/PER-4346) | 3.2 — nhị phân P / N       |
| [PER-4356](https://linear.app/bancie/issue/PER-4356) | 3.3 — decision list (play) |
| [PER-4364](https://linear.app/bancie/issue/PER-4364) | 3.4 — 10 chỉ số từ ma trận |


Ký hiệu: ma trận **hàng = nhãn thực tế, cột = nhãn dự đoán** (thống nhất với `sklearn` / Weka; trên bài bạn nên ghi rõ hàng/cột bạn dùng).

---

### Câu 3.1 — 10 mẫu, lớp A, B, C

- **Nhãn thực:** A B C A B C A B C A  
- **Nhãn dự:** A C C B B A A B C C

#### Bước 1 — Lập ma trận 3×3 (đếm từng cặp)

Duyệt 10 mẫu theo thứ tự:


| #   | Thực | Dự  |
| --- | ---- | --- |
| 1   | A    | A   |
| 2   | B    | C   |
| 3   | C    | C   |
| 4   | A    | B   |
| 5   | B    | B   |
| 6   | C    | A   |
| 7   | A    | A   |
| 8   | B    | B   |
| 9   | C    | C   |
| 10  | A    | C   |


Gộp vào bảng (hàng = thực, cột = dự):


|            | Dự: A | B   | C   |
| ---------- | ----- | --- | --- |
| **Thực A** | 2     | 1   | 1   |
| **Thực B** | 0     | 2   | 1   |
| **Thực C** | 1     | 0   | 2   |


Tổng đúng trên đường chéo: 2+2+2=6.

#### Bước 2 — Accuracy


\mathrm{Accuracy} = \frac{6}{10} = 0{,}6.


#### Bước 3 — Precision, Recall, F1 theo từng lớp

Với mỗi lớp *k*:

- **TP_k** = ô (k,k).  
- **FN_k** = tổng hàng *k* trừ TP_k.  
- **FP_k** = tổng cột *k* trừ TP_k.


P_k = \frac{\mathrm{TP}_k}{\mathrm{TP}_k+\mathrm{FP}_k}, \quad
R_k = \frac{\mathrm{TP}_k}{\mathrm{TP}_k+\mathrm{FN}_k}, \quad
F1_k = \frac{2 P_k R_k}{P_k+R_k}.


**Kết quả (làm tròn):**

- **A:** TP=2, FP=1, FN=2 → P=2/3, R=2/4=0{,}5, F1≈0,571.  
- **B:** TP=2, FP=1, FN=1 → P=2/3, R=2/3, F1≈0,667.  
- **C:** TP=2, FP=2, FN=1 → P=0{,}5, R=2/3, F1≈0,571.

---

### Câu 3.2 — 10 mẫu, positive = P, negative = N

- **Thực:** P N P P N N P N P N  
- **Dự:**  P N N P P N P N N P

#### Bảng 2×2 (hàng = thực, cột = dự; hàng 1: P, hàng 2: N; cột 1: P, cột 2: N)


|            | Dự P   | Dự N   |
| ---------- | ------ | ------ |
| **Thực P** | 3 (TP) | 2 (FN) |
| **Thực N** | 2 (FP) | 3 (TN) |


Cách đếm: duyệt 10 cặp; mỗi cặp (P,P) → TP+1, (N,N) → TN+1, (P,N) → FN+1, (N,P) → FP+1.

#### Số tóm tắt

- TP=3, FP=2, FN=2, TN=3, tổng 10.


\mathrm{Acc} = \frac{3+3}{10} = 0{,}6, \quad
P = \frac{3}{3+2} = 0{,}6, \quad
R = \frac{3}{3+2} = 0{,}6, \quad
F1 = \frac{2\cdot 0{,}6 \cdot 0{,}6}{1{,}2} = 0{,}6.


---

### Câu 3.3 — 14 mẫu, decision list, positive = *play* = *yes*

#### Quy tắc (thứ tự if–else, **dừng ở rule trúng**)

1. Nếu `outlook = overcast` → **play = yes**
2. Nếu không, và `windy = TRUE` → **play = no**
3. Nếu không, và `outlook = sunny` → **play = no**
4. **Ngược lại** (thường *rainy* và *không* gió) → **play = yes**

*Lưu ý: dòng* **overcast** *luôn đi tới rule 1, không cần xem gió. Dòng* **sunny** *và không gió → rule 3 nói* **no** *(mẫu 9, 8 khớp* **no** *như thực, mẫu 9 thực* **yes** *→ sai theo bộ quy tắc này). Dòng* **sunny** *+ gió* **TRUE** *→ rule 2* **no** *(mẫu 11: thực* **yes** *→ sai nếu nộp đúng quy tắc trên bài).*

#### Cách làm bài: bảng 14 dòng

Với từng mẫu, viết: outlook, windy, rồi thử 1 → 2 → 3 → 4, ghi dựa đoán, so với cột *play* thật. Sau cùng điền ma trận 2×2 (thực yes/no × dự yes/no, positive = yes).

Kết quả cùng code (nếu cùng dữ liệu đề): **12/14** đúng, ma trận (thực hàng, dự cột): yes–yes=7, yes–no=2, no–yes=0, no–no=5, tức **TP=7, FN=2, FP=0, TN=5**.


\mathrm{Acc} = \frac{12}{14}, \quad
P = \frac{7}{7+0} = 1, \quad
R = \frac{7}{7+2} = \frac{7}{9} \ \text{(sensitivity)}, \quad
\mathrm{Spec} = \frac{5}{5+0} = 1, \quad
F1 = \frac{2PR}{P+R} = 0{,}875\ (\text{chính xác: }7/8).


---

### Câu 3.4 — Từ ma trận cho sẵn: TP, FP, TN, FN

**Đã cho (YES = lớp dương):** TP=100, FP=10, TN=50, FN=5 → N=165.


| Ký hiệu                      | Công thức (đề)                   | Tính số (thay số)            |
| ---------------------------- | -------------------------------- | ---------------------------- |
| Accuracy                     | (TP+TN) / N                      | 150/165 = **10/11** ≈ 0,9091 |
| Misclass. rate               | (FP+FN) / N = 1 − acc            | 15/165 = **1/11** ≈ 0,0909   |
| TPR (= Recall = Sensitivity) | TP / (TP+FN)                     | 100/105 = **20/21** ≈ 0,9524 |
| FPR                          | FP / (FP+TN)                     | 10/60 = **1/6** ≈ 0,1667     |
| TNR (= Specificity)          | TN / (TN+FP)                     | 50/60 = **5/6** ≈ 0,8333     |
| Precision                    | TP / (TP+FP)                     | 100/110 = **10/11** ≈ 0,9091 |
| Prevalence                   | (TP+FN) / N (tỷ lệ “thực” dương) | 105/165 = **7/11** ≈ 0,6364  |


*Sensitivity = Recall = TPR; Specificity = TNR.*

---

*Issue gốc: [PER-4375](https://linear.app/bancie/issue/PER-4375/checklist-on-phan-3).*