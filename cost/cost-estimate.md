# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Chấm ở rubric R6. Người phụ trách: Đặng Thanh Hải.
> Số **không điền tay**: `cost/personas.yaml` → `python run.py simulate --wait 12 --rate-from eval/run-2.csv` → chép bảng trong `cost/simulate-N-summary.md` vào mục 2.
> Lúc build dùng gói miễn phí vẫn tính theo **giá gói trả phí**: đây là chi phí khi đưa vào dùng thật.

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`), 3 kiểu, tỉ lệ lấy từ phân bố số câu hỏi dưới video / học viên trong 21 ngày (`evidence/data-mining.md` §3, n = 145 học viên có hỏi):

  | Persona | Tỉ lệ | Phiên / người / tháng | Lượt hỏi / phiên | Câu hỏi / người / tháng | Data (quy ra tháng × 30/21) |
  |---|---|---|---|---|---|
  | `dung_it` | 0,28 | 2 | 1 | 2 | 40/145 hỏi 1 câu / 21 ngày → ~1,4 câu / tháng |
  | `dung_vua` | 0,29 | 6 | 1 | 6 | 42/145 hỏi 2–5 câu → ~5 câu / tháng |
  | `dung_nhieu` | 0,43 | 20 | 2 | 40 | 63/145 hỏi ≥6 câu → ~20 câu / tháng (47 người 6–15 câu, 16 người >15 câu) |

  → Trung bình theo persona: **~19,5 câu / người / tháng**, còn data thật là 1.108 câu × 30/21 ÷ 145 người ≈ **10,9 câu / người / tháng**. Persona `dung_nhieu` đang hỏi gấp ~2 lần data, nên chi phí ở mục 2 là **mức cao (bảo thủ)**, chưa phải mức giữa.
- **Số người dùng thật**, 3 kịch bản: thấp **145** (học viên đã hỏi dưới video) · cơ sở **436** (học viên có hoạt động trên trang pre-class) · cao **721** (mọi tài khoản học viên). Nguồn: `data/preclass/` BTC cấp (`evidence/data-mining.md` §1, §3). Cả khoá có hơn 1.000 học viên (guide 4.2) → nếu mở cho cả khoá thì vượt mức cao.
  - Lưu ý: kịch bản cơ sở và cao giả định **mọi** người dùng hỏi theo persona; data cho thấy chỉ 145/436 (33,3%) người có hỏi → hai kịch bản này cũng là mức cao.
- **Giá** (USD / 1 triệu token, giá chuẩn, chưa thuế):

  | Model | Vào | Ra | Nguồn |
  |---|---|---|---|
  | `gpt-4o-mini` | 0,15 | 0,60 | `further-reading/model-prices.md` của repo đề (bảng OpenAI, đối chiếu 25/11/2026) · https://developers.openai.com/api/docs/pricing |
  | `gemini-2.0-flash` | 0,10 | 0,40 | ⚠️ **Không có trong bảng giá của đề** (bảng chỉ có Gemini 3.x / 4.x). Nguồn tự ghi trong `personas.yaml`: https://ai.google.dev/pricing, xem 25/11/2026 — người đã xem trang cần xác nhận lại, hoặc đổi sang model có trong bảng (vd `gpt-5-mini` 0,25 / 2,00 — model của lượt eval) |

- **Tỉ lệ đạt** dùng để tính: **23/23 (100%)**, lượt `run-2@20261128-004110` (`eval/run-2.csv`).
  - Lượt 2 đạt 100% sau khi sửa đúng 3 lỗi của lượt 1 trên **cùng bộ câu thử**, nên 100% có thể là lạc quan. Mục 4 tính thêm với tỉ lệ lượt 1 (21/23 = 91%) để thấy độ nhạy.
- **Đo token trên model** `openai/gpt-oss-120b` (theo phân công; ghi lại đúng tên model mà `simulate-N-summary.md` in ra), **tính giá model** `gemini-2.0-flash` và `gpt-4o-mini`.
  - ⚠️ Lượt 1 (`run-1@20261127-233051`, 21/23) chạy bằng `openai/gpt-oss-120b`; lượt 2 (23/23) chạy bằng `gpt-5-mini`. Mô phỏng đo trên `gpt-oss-120b` mà lấy tỉ lệ đạt của lượt 2 → bản tóm tắt sẽ ghi "khác model". Ghi rõ điều này khi trình bày; tỉ lệ cùng model với mô phỏng là lượt 1 (91%, mục 4).
  - Các model khác bộ tách token và khác độ dài câu trả lời, nên token đo trên `gpt-oss-120b` chỉ là **xấp xỉ** cho `gemini-2.0-flash` và `gpt-4o-mini`.

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-__.csv` · run ID __ · 50 phiên · seed 42 · token đo trên model __

*(dán 2 bảng từ `cost/simulate-N-summary.md`: bảng persona và bảng chi phí)*

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (145) | / tháng — cơ sở (436) | / tháng — cao (721) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| gemini-2.0-flash | | | | | | |
| gpt-4o-mini | | | | | | |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt (lượt 2), **không coi như đạt 100%** — ở đây tỉ lệ đo được đúng là 23/23, xem cảnh báo ở mục 1.

## 3. So với impact

- **Impact / tháng** (`spec.md` §2): ~1.580 câu hỏi / tháng × ~4 phút dò lại đoạn bài ≈ **105 giờ học viên / tháng** (số câu từ data; 4 phút là mức bảo thủ trong khoảng 5–15 phút 7/10 người khảo sát kể).
- **Impact / người / tháng:** 105 giờ ÷ 145 người có hỏi ≈ **43 phút / người / tháng** (≈ 10,9 câu × 4 phút).
- **Chi phí / người / tháng** (cơ sở, model __): __ *(lấy từ mục 2)*
- **Chi phí cho 1 giờ học viên tiết kiệm:** chi phí / tháng (thấp, 145 người) ÷ 105 giờ = __ USD / giờ.
- **Kết luận một dòng — đáng làm không:** __ *(vd: "Đáng: ~__ USD / người / tháng để tiết kiệm ~43 phút dò bài; kể cả ở mức cao 721 người với persona hỏi gấp đôi data, tổng chỉ ~__ USD / tháng.")*

## 4. *(Muốn sâu hơn, không bắt buộc)*

**Bảng độ nhạy** — mỗi cần gạt đổi chi phí bao nhiêu (tính lại từ token đo được ở mục 2, không chạy thêm):

| Cần gạt | Thay đổi | Ảnh hưởng chi phí | Cách tính |
|---|---|---|---|
| Tỉ lệ đạt | 100% (lượt 2) → 91% (lượt 1, 21/23) | Chi phí / task thành công **+10%** | ÷ 0,91 thay vì ÷ 1,00 |
| Persona sát data | 19,5 → 10,9 câu / người / tháng | Chi phí / tháng **−44%** | × 10,9 / 19,5 |
| Người dùng thật | 436 → 145 (chỉ người có hỏi) | Chi phí / tháng **−67%** | = kịch bản thấp |
| Model rẻ hơn | gpt-4o-mini → gemini-2.0-flash | __ | đọc thẳng 2 dòng ở mục 2 |
| Cache phần cố định | system prompt (~__ token) lặp lại mỗi lượt; gpt-4o-mini cache vào 0,075 thay vì 0,15 | phần token vào lặp lại **−50%** | token system prompt × số lượt × (0,15 − 0,075) |
| Cắt ngữ cảnh | `MAX_CONTEXT = 8` đoạn → 3 đoạn (`codebase/agent.py`) | token vào giảm theo số đoạn bỏ | chưa đo — phải chạy lại để biết ảnh hưởng tới tỉ lệ đạt |
| Hỏi lại không gọi model | câu quá ngắn được code hỏi lại luôn, 0 lần gọi model | đã có: 3/23 câu lượt 2 (B03, H04, BAC2) tốn 0 token | `eval/run-2.csv` cột `model_calls` |

**Chi phí ngoài model:**
- Hosting: bản chạy thử chỉ là Python thư viện chuẩn + một file `segments.json`, chạy được trên máy chủ nhỏ sẵn có của khoá *(tự ước tính: ~0 USD thêm)*.
- Lưu trữ: 16 đoạn bài hiện tại vài chục KB; cả khoá (~70 video × 4 đoạn) vẫn dưới 1 MB *(tự ước tính)*.
- **Giờ công người**: (1) viết và cập nhật đoạn bài có mốc khi bài giảng đổi — đây là chi phí lớn nhất, hiện mới có 4 video *(tự ước tính, chưa đo)*; (2) trợ giảng người nhận các câu AI trả "không có trong bài" và gợi ý hỏi người.

**Quy mô nào thì còn đáng làm:** chi phí model tăng tuyến tính theo số câu hỏi, còn impact cũng tăng theo số câu hỏi (mỗi câu ~4 phút), nên tỉ lệ chi phí / giờ tiết kiệm gần như không đổi theo quy mô. Chỗ không tăng tuyến tính là **giờ công viết đoạn bài**: làm một lần cho mỗi video, càng nhiều người hỏi trên cùng video thì càng đáng. Video ít người xem (Day13 chỉ còn 50 người) là chỗ cân nhắc có nên viết đoạn bài không.
