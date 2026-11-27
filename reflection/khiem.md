# Reflection — Hoàng Gia Khiêm

> Làm ở guide bước 5.3. Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.
> *(Bản nháp do Claude soạn từ lịch sử repo — Khiêm đọc lại, sửa câu 3 bằng lời của mình trước khi push.)*

1. **Vai trò + phần mình làm:** Thành viên, phụ trách bản chạy thử và đánh giá.
   - CP2: `eval/metric_spec.yaml` (4 metric, cách chấm, ngưỡng) và 3 câu thử B12, B16, B17.
   - CP3: nối model thật trong `codebase/ai.py` (lấy token từ `usage`, thử lại khi lỗi mạng / 429), công cụ `find_segments` trong `codebase/tools.py`, luồng 6 bước trong `codebase/agent.py`, 3 câu thử K01–K03 · commit `5d9141e`.
   - CP4: một lần cải tiến trong `codebase/agent.py` (bước 5b), lượt 2 `eval/run-2.csv` + `traces/run-2.jsonl`, `eval/report.md` mục 1 (lượt 2), 3, 4.

2. **AI hỗ trợ mình thế nào:** Dùng Claude để soạn nháp metric, code `ai.py` / `tools.py` / `agent.py`, câu thử và phần báo cáo; khai ở `docs/ai-usage.md`.
   - Phải sửa / kiểm lại: bản đầu của `tools.py` chọn sai đoạn vì đếm cả từ phổ biến → đổi sang trọng số từ hiếm; luồng đọc tiền tố `[d01-r1-v01 @ mm:ss]` nhưng bộ câu thử viết `[video d01-r1-v01]` → sửa cho đọc được cả hai; `simulate --try` lỗi `WinError 10054` → thêm thử lại.
   - Trước khi chạy lượt 2, mình cho chạy lại đúng 23 câu trả lời model ở lượt 1 qua luồng mới để chắc chỉ 4 câu đích thay đổi.

3. **Một câu thử trượt của nhóm và mình học được gì:** B04 — `[video d01-r1-v05] Cái ví dụ lúc nãy là ý gì vậy?`. Model chọn đúng là phải hỏi lại, nhưng hỏi **hai** câu và đưa hai lựa chọn thiếu, không hỏi phút nào.
   *(Nháp — viết lại bằng lời của bạn)* Mình học được: viết luật trong prompt ("hỏi lại đúng MỘT câu") không bảo đảm model làm đúng; luật nào kiểm được bằng code (đếm dấu "?") thì nên kiểm bằng code sau model. Và chọn đúng *loại* quyết định chưa đủ — người dùng thấy *hình thức* câu trả lời, nên hình thức cũng phải nằm trong metric.