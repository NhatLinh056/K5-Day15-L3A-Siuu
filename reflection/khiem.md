# Reflection — Hoàng Gia Khiêm

1. **Vai trò + phần mình làm (trỏ tới file / commit):** Thành viên, phụ trách bản chạy thử và phần đánh giá sau lượt 1.
   - CP2: `eval/metric_spec.yaml` (4 metric, cách chấm, ngưỡng số) và 3 câu thử B12, B16, B17.
   - CP3: nối model thật trong `codebase/ai.py` (token lấy từ `usage`, thử lại khi lỗi mạng / 429), công cụ `find_segments` trong `codebase/tools.py`, luồng 6 bước trong `codebase/agent.py`, 3 câu thử K01–K03 — commit `5d9141e`.
   - CP4: một lần cải tiến trong `codebase/agent.py` (bước 5b), lượt 2 `eval/run-2.csv` + `traces/run-2.jsonl` (23/23), `eval/report.md` mục 1 (lượt 2), 3, 4 — commit `fb0165e`.

2. **AI hỗ trợ mình thế nào (việc gì, công cụ gì, chỗ nào phải sửa lại output AI):** Mình dùng Claude (Claude Opus 5.5) viết bản chính của code, prompt `SYSTEM`, metric, câu thử, nháp chấm lượt 2 và nháp báo cáo; khai đủ ở `docs/ai-usage.md`. Phần mình làm là chạy, đọc kết quả và đưa lỗi thật về cho AI sửa:
   - `tools.py` bản đầu chọn sai đoạn vì đếm cả từ phổ biến → đổi sang trọng số từ hiếm (idf).
   - Luồng đọc tiền tố `[d01-r1-v01 @ mm:ss]` nhưng bộ câu thử viết `[video d01-r1-v01]` → sửa cho đọc được cả hai.
   - `simulate --try` lỗi `WinError 10054` (mất kết nối) → thêm thử lại tối đa 2 lần.
   - Trước lượt 2, cho chạy lại đúng 23 câu trả lời model ở lượt 1 qua luồng mới để chắc chỉ 4 câu đích (B04, B05, B16, K03) thay đổi.
   - Chỗ mình làm sai: lượt 2 chạy `gpt-5-mini` trong khi lượt 1 chạy `openai/gpt-oss-120b` vì đổi `.env` giữa chừng, nên không tách được phần tăng do code hay do model — đã ghi rõ trong `eval/report.md` mục 1.

3. **Một câu thử trượt của nhóm và mình học được gì:** B04 — `[video d01-r1-v05] Cái ví dụ lúc nãy là ý gì vậy?`. Ở lượt 1 model chọn đúng loại `hoi_lai`, nhưng hỏi lại **hai** câu, liệt kê hai ví dụ (thiếu ví dụ ở `#S3`) và không hỏi phút nào, nên trượt `hoi_lai_khi_mo_ho` và kéo cả lượt xuống "chưa đạt". Prompt lúc đó đã ghi "hỏi lại đúng MỘT câu" mà model vẫn không theo. Bài học: luật nào kiểm được bằng code (đếm dấu "?", có chữ "phút") thì kiểm bằng code sau model, không chỉ dặn trong prompt. Và chọn đúng loại quyết định chưa đủ — học viên nhìn thấy hình thức câu trả lời, nên hình thức cũng phải nằm trong metric. Sửa xong lại sinh tác dụng phụ: dòng "luôn xưng mình" làm `gpt-5-mini` mở câu bằng "Mình:" ở B01, B05, B06 — mỗi lần sửa prompt cần chạy lại cả bộ câu thử, không chỉ câu bị trượt.