# Câu 2.1 (PER-4322) — Giải tay (thi trên giấy) và kiểm tra bằng code

Tài liệu này trình bày **cách làm truyền thống từng bước** cho bài ôn tập về thuộc tính **tuổi**; file `cau2_1_per4322.py` dùng để **đối chiếu đáp án** sau khi bạn tự tính.

---

## Dữ liệu (đã sắp tăng dần)

n = 27

```
13, 15, 16, 16, 19, 20, 20, 21, 22, 22, 25, 25, 25, 25, 30, 33, 33,
35, 35, 35, 35, 36, 40, 45, 46, 52, 70
```

Đánh số thứ tự từ **1** đến **27** (trên giấy bạn có thể ghi số thứ tự dưới mỗi giá trị để khỏi nhầm vị trí).

---

## Phần (a): Trung bình, trung vị, mode

### Bước 1 — Tổng các giá trị (chia nhóm cho dễ cộng)


| Nhóm      | Giá trị                | Tổng                                |
| --------- | ---------------------- | ----------------------------------- |
| 10 số đầu | 13…22, 22              | 13+15+16+16+19+20+20+21+22+22 = 184 |
| Bốn số 25 | 25×4                   | 100                                 |
| 30        |                        | 30                                  |
| Hai số 33 |                        | 66                                  |
| Bốn số 35 | 35×4                   | 140                                 |
| Còn lại   | 36, 40, 45, 46, 52, 70 | 36+40+45+46+52+70 = 289             |


**Tổng:** 184 + 100 + 30 + 66 + 140 + 289 = 809.

### Bước 2 — Trung bình (mean)

\bar{x} = \frac{809}{27} \approx 29{,}963 \quad \text{(trên giấy thường ghi } 29{,}96 \text{ hoặc phân số } \frac{809}{27}\text{).}

### Bước 3 — Trung vị (median)

n = 27 lẻ → trung vị là **giá trị ở vị trí giữa**:

\text{vị trí} = \frac{n+1}{2} = \frac{28}{2} = 14.

Đếm trên dãy đã sắp: phần tử thứ **14** (kể từ 1) là **25**.

**Trung vị = 25.**

### Bước 4 — Mode (mốt)

Đếm tần số từng giá trị (có thể lập bảng tần số gọn):

- 25 xuất hiện **4** lần  
- 35 xuất hiện **4** lần  
- Các giá trị khác **≤ 2** lần

Vậy có **hai mode**: **25** và **35** (tập **đa mốt**).

---

## Phần (b): Tứ phân vị Q1 và Q3 (đề cho phép xấp xỉ)

Có **hai cách** tài liệu hay dùng; nếu thầy dạy theo cách nào thì bạn dùng đúng cách đó. Trên thi, **ghi rõ công thức bạn dùng** là ổn.

### Cách 1 — Vị trí phần tử theo tỷ lệ (n+1) (dễ tính tay)

- **Q1** ứng với **25%** dưới: vị trí (theo 1-based)

v_1 = \frac{1}{4}(n+1) = \frac{28}{4} = 7.

Phần tử thứ **7** trong dãy tăng dần là **20** → **Q1 = 20** (khi thầy dùng “lấy đúng phần tử tại vị trí nguyên”).

- **Q3** ứng với **75%**: vị trí

v_3 = \frac{3}{4}(n+1) = 21.

Phần tử thứ **21** là **35** → **Q3 = 35**.

- **IQR** (khoảng tứ phân vị):  \mathrm{IQR} = 35 - 20 = 15 .

### Cách 2 — Tứ phân vị nội suy tuyến tính (gần với hàm `quantile` / Excel)

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

## Phần (c): Vẽ boxplot và nhận xét (trên giấy)

### Bước 1 — Năm số tóm tắt (five-number summary)

- **Min** = 13  
- **Q1** = 20 (cách 1) hoặc 20,5 (cách 2)  
- **Median** = 25  
- **Q3** = 35  
- **Max** = 70

(Trong boxplot, trục tung là thang tuổi: vẽ hộp từ Q1 đến Q3, đường giữa hộp là median, “râu” xuống min và lên max **theo quy ước môn học** — thường **giới hạn bởi 1,5·IQR**; giá trị nằm ngoài bằng **điểm** hoặc “râu kéo đến giá trị hợp lệ lớn nhất trong khoảng”).

### Bước 2 — Rào 1,5·IQR (dùng IQR đã tính)

- Với **IQR = 15** (Q1=20, Q3=35):  
Cận trên: 35 + 1{,}5 \times 15 = 35 + 22{,}5 = 57{,}5.  
Vì **70 > 57,5** → **70 thường xem là ngoại lai (outlier)** phía trên; trên hình có thể vẽ 70 bằng *chấm* riêng, râu dừng tại 52 (hoặc theo cách bài tập/WeMooc của lớp).
- Với **IQR = 14,5** (Q1=20,5, Q3=35):  
Cận trên: 35 + 1{,}5 \times 14{,}5 = 56{,}75 → **70** vẫn **> 56,75** → vẫn ngoài rào.

### Bước 3 — Nhận xét phân bố (viết 2–3 câu)

- **Trung bình (≈ 29,96) > trung vị (25)** → phân bố **lệch phải** (đuôi dài về phía lớn).  
- Có **giá trị rất lớn (70)** kéo mean lên, trong khi phần lớn dữ liệu tập trung ở khoảng 15–40.  
- (Tuỳ trình bày) **Độ tập trung** của phần 50% giữa: hộp từ Q1 đến Q3 (khoảng 20–35).

---

## Phần (d): Rời rạc hóa với k = 4

Cần nêu rõ: **chia độ rộng đều** (equal-width) **hoặc** **chia tần số đều** (equal-frequency / equal-depth).

### Dạng 1 — Chia độ rộng đều (4 khoảng cùng độ dài trên trục giá trị)

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


### Dạng 2 — Chia tần số đều (4 nhóm, mỗi nhóm số mẫu gần bằng nhau)

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

## Kiểm tra bằng code (cùng thư mục)

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

## Tóm tắt số cần nhớ nhanh


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

*Tài liệu ôn theo cùng bài: Linear [PER-4322](https://linear.app/bancie/issue/PER-4322/cau-21).*

*Câu 2.2 (thang đo Stevens): [README_cau2_2.md](README_cau2_2.md) — [PER-4332](https://linear.app/bancie/issue/PER-4332/cau-22).*

*Phần 3 (ma trận nhầm lẫn / độ đo): [README_phan3_per4375.md](README_phan3_per4375.md) — [PER-4375](https://linear.app/bancie/issue/PER-4375/checklist-on-phan-3).*