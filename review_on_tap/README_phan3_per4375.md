# Phần 3 (PER-4375) — Ma trận nhầm lẫn & độ đo: Câu 3.1 – 3.4

Lời giải **làm tay** (thi trên giấy). Code kiểm tra: `[cau3_phan3_per4375.py](cau3_phan3_per4375.py)` (`python cau3_phan3_per4375.py`).


| Linear                                               | Câu                        |
| ---------------------------------------------------- | -------------------------- |
| [PER-4340](https://linear.app/bancie/issue/PER-4340) | 3.1 — đa lớp A, B, C       |
| [PER-4346](https://linear.app/bancie/issue/PER-4346) | 3.2 — nhị phân P / N       |
| [PER-4356](https://linear.app/bancie/issue/PER-4356) | 3.3 — decision list (play) |
| [PER-4364](https://linear.app/bancie/issue/PER-4364) | 3.4 — 10 chỉ số từ ma trận |


Ký hiệu: ma trận **hàng = nhãn thực tế, cột = nhãn dự đoán** (thống nhất với `sklearn` / Weka; trên bài bạn nên ghi rõ hàng/cột bạn dùng).

---

## Câu 3.1 — 10 mẫu, lớp A, B, C

- **Nhãn thực:** A B C A B C A B C A  
- **Nhãn dự:** A C C B B A A B C C

### Bước 1 — Lập ma trận 3×3 (đếm từng cặp)

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

### Bước 2 — Accuracy


\mathrm{Accuracy} = \frac{6}{10} = 0{,}6.


### Bước 3 — Precision, Recall, F1 theo từng lớp

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

## Câu 3.2 — 10 mẫu, positive = P, negative = N

- **Thực:** P N P P N N P N P N  
- **Dự:**  P N N P P N P N N P

### Bảng 2×2 (hàng = thực, cột = dự; hàng 1: P, hàng 2: N; cột 1: P, cột 2: N)


|            | Dự P   | Dự N   |
| ---------- | ------ | ------ |
| **Thực P** | 3 (TP) | 2 (FN) |
| **Thực N** | 2 (FP) | 3 (TN) |


Cách đếm: duyệt 10 cặp; mỗi cặp (P,P) → TP+1, (N,N) → TN+1, (P,N) → FN+1, (N,P) → FP+1.

### Số tóm tắt

- TP=3, FP=2, FN=2, TN=3, tổng 10.


\mathrm{Acc} = \frac{3+3}{10} = 0{,}6, \quad
P = \frac{3}{3+2} = 0{,}6, \quad
R = \frac{3}{3+2} = 0{,}6, \quad
F1 = \frac{2\cdot 0{,}6 \cdot 0{,}6}{1{,}2} = 0{,}6.


---

## Câu 3.3 — 14 mẫu, decision list, positive = *play* = *yes*

### Quy tắc (thứ tự if–else, **dừng ở rule trúng**)

1. Nếu `outlook = overcast` → **play = yes**
2. Nếu không, và `windy = TRUE` → **play = no**
3. Nếu không, và `outlook = sunny` → **play = no**
4. **Ngược lại** (thường *rainy* và *không* gió) → **play = yes**

*Lưu ý: dòng* **overcast** *luôn đi tới rule 1, không cần xem gió. Dòng* **sunny** *và không gió → rule 3 nói* **no** *(mẫu 9, 8 khớp* **no** *như thực, mẫu 9 thực* **yes** *→ sai theo bộ quy tắc này). Dòng* **sunny** *+ gió* **TRUE** *→ rule 2* **no** *(mẫu 11: thực* **yes** *→ sai nếu nộp đúng quy tắc trên bài).*

### Cách làm bài: bảng 14 dòng

Với từng mẫu, viết: outlook, windy, rồi thử 1 → 2 → 3 → 4, ghi dựa đoán, so với cột *play* thật. Sau cùng điền ma trận 2×2 (thực yes/no × dự yes/no, positive = yes).

Kết quả cùng code (nếu cùng dữ liệu đề): **12/14** đúng, ma trận (thực hàng, dự cột): yes–yes=7, yes–no=2, no–yes=0, no–no=5, tức **TP=7, FN=2, FP=0, TN=5**.


\mathrm{Acc} = \frac{12}{14}, \quad
P = \frac{7}{7+0} = 1, \quad
R = \frac{7}{7+2} = \frac{7}{9} \ \text{(sensitivity)}, \quad
\mathrm{Spec} = \frac{5}{5+0} = 1, \quad
F1 = \frac{2PR}{P+R} = 0{,}875\ (\text{chính xác: }7/8).


---

## Câu 3.4 — Từ ma trận cho sẵn: TP, FP, TN, FN

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