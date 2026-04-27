# Câu 2.2 (PER-4332) — Thang đo (Stevens) & đối chiếu W₁…W₆ với V

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

## Bốn thang đo (Stevens) — nắm nhanh

1. **Định danh (nominal):** chỉ phân **loại tên**; số nếu có chỉ là mã, **không** nói a < b theo nghĩa “hơn/kém về bậc” trừ khi cùng tên.
2. **Thứ tự (ordinal):** thứ tự A < B < … **có ý nghĩa**; khoảng cách số trên mã **chưa chắc** tương đương.
3. **Khoảng (interval):** thứ tự **và** chênh lệch (hiệu) **có ý nghĩa**; **tỷ lệ** (a/b) **chưa** nhất thiết; thường **không** có số 0 tuyệt đối “vắng mặt” theo nghĩa vật lý. Phép tương đương thường: **W = aV + b** với **a > 0** (phép afin tăng).
4. **Tỷ lệ (ratio):** có thêm **gốc 0** tuyệt đối; tỷ số b có ý. Phép tương đương hẹp: **W = aV**, **a > 0** (nhân tỷ lệ **qua gốc** — không cộng hằng, trừ trường hợp đổi đơn vị vẫn về dạng aV).

Bài tập: V = 1,2,3,4,5, **bước 1** — **có thứ tự**; **bước 2** — hiệu giữa hai cột cách 1 cùng 1, nên mã cách **đều 1** thường xử lý như cho phép tính **chênh lệch** trên bảng → **(3) thang khoảng (interval)** phù hợp hơn hẳn “chỉ tên” hoặc “chỉ hạng”.  
Mã **1…5** **không** có 0, và đề **không** mô tả nghĩa “gấp đôi 2 bằng 1 + 1” theo tỷ lệ vật lý → thường **không** gọi V là **(4) tỷ lệ** trong cùng dạng bài sách giáo trình dụng tạo.

**Kết luận cho PER-4333 — thang đo của V(.) (đáp án ôn thường dùng):** **(3) thang khoảng (interval)**.

Nếu giảng viên chấm theo cách *chỉ* xem V là mã hạng (không tính hiệu), có thể giải thích **(2) thứ tự**; khi đó cùng thứ tự bậc tăng ở dưới sẽ **rộng** hơn (gồm cả W₄) — ghi ở mục “Ghi chú bài tập thứ tự”.

---

## Cùng thang **khoảng** (interval) với V: phép afin tăng

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

## Ghi chú: nếu V được coi là thang **thứ tự (ordinal)**

Phép cho phép: **bảo toàn thứ tự** nghiệm (đơn điệu **tăng** nghiêm nếu V tăng theo cột A→E).  

- **Cùng thứ tự** với V: W₁, W₂, W₄, W₅, W₆.  
- **Không** cùng: **W₃** (thứ tự cột theo mã V không còn tăng theo cùng cách).

Nếu thầy yêu cầu **cùng thang tỷ lệ (ratio)** thuần (chỉ W = aV): chỉ xét **W₁, W₆** (và so với bản thân khi gọi V là tỷ lệ — ở đây bảng 1..5 nhiều tài liệu **vẫn gọi V là khoảng, không tỷ lệ**).

---

## Mã Linear (sub-issues) — ánh xạ câu trả lời


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

## Kiểm tra bằng code

Từ thư mục `review_on_tap`:

```bash
python cau2_2_per4332.py
```

Script kiểm tra công thức, thử ánh xạ afin, và in từng dòng ứng với **PER-4333 … PER-4339**.

[Linear PER-4332](https://linear.app/bancie/issue/PER-4332/cau-22)