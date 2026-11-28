# Reflection — Đặng Thanh Hải

> Làm ở guide bước 5.3. Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.
> *(Bản nháp do Claude soạn từ lịch sử repo — Hải đọc lại, sửa câu 3 bằng lời của mình trước khi push.)*

1. **Vai trò + phần mình làm:** Thành viên 2 (TV2), phụ trách bằng chứng từ data, dữ liệu bài giảng và chi phí.
   - CP1–CP2: đào data pre-class bằng `evidence/count.py` → `evidence/data-mining.md` (38,3% người xem tua lùi · 41,1% câu trả lời không dẫn mốc · 114/1.108 câu <15 ký tự); viết câu thử B01–B05 và ghép `eval/benchmark.csv`; bản đầu `data/DATA_CARD.md` · commit `3522d35`, `8476b1d`.
   - CP3: viết 16 đoạn bài `synthetic` `data/lesson/segments.json` cho 4 video Day01, Day04; Dataset 2 trong `DATA_CARD.md`; 5 câu thử H01–H05 · commit `7e84dd9`.
   - CP4: `cost/cost-estimate.md` (persona so với data, 3 kịch bản người dùng, so với impact, bảng độ nhạy) và lượt mô phỏng `cost/simulate-1.csv` (50 phiên, đo trên `gpt-5-mini`) · commit `e58e026`, `d5ab54c`; nháp §9 Rủi ro & an toàn gửi Linh ghép vào `spec.md`.

2. **AI hỗ trợ mình thế nào:** Dùng Claude Code (Claude Opus 5.5) để viết script đếm, soạn nháp câu thử, 16 đoạn bài và khung `cost-estimate.md`; khai ở `docs/ai-usage.md`.
   - Phải kiểm / sửa lại: kiểm tay 3 số đào data bằng Excel lọc cột (khớp 3/3); script có lần lỗi cú pháp do chuỗi `"\n"` bị đổi thành xuống dòng thật; checker báo câu B04 còn chữ "(ví dụ" như dòng mẫu → viết lại.
   - Số AI đưa vào phải đối chiếu nguồn: giá `gemini-2.0-flash` không có trong bảng giá của đề → ghi cảnh báo thay vì dùng như số chắc; persona `dung_nhieu` hỏi gấp ~2 lần data → ghi rõ chi phí mục 2 là mức cao; dòng giá `gpt-5-mini` tự tính thêm thì kiểm bằng cách tính lại đúng số simulate in ra cho `gpt-4o-mini`.

3. **Một câu thử trượt của nhóm và mình học được gì:** B05 — câu mình viết: `[video d04-r3-v02] System prompt nên ghi những phần gì ạ?`. Lượt 1 trả lời đủ ý, đọc qua thấy đúng, nhưng câu cuối lấy ý từ đoạn `#S4` mà danh sách mốc chỉ dẫn `#S1–#S3` → trượt `moc_dung_doan` khi chấm chặt. Mình học được: câu hỏi trải qua cả 4 đoạn của video là câu dễ sót mốc nhất, dù nó là câu "thường"; người đọc lướt không thấy lỗi, chỉ chấm theo từng câu ↔ từng mốc mới thấy. Vì mình viết cả đoạn bài lẫn câu thử, lần sau cần ghi trong `pass_criterion` câu này cần dẫn những đoạn nào, để lỗi sót mốc không phụ thuộc người chấm có đọc kỹ hay không.
