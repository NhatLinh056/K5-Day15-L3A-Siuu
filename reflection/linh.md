# Reflection — Lê Nhật Linh

> Làm ở guide bước 5.3. Hạn: **23:59 Thứ Bảy 28/11**. Mỗi câu 3–6 dòng.

1. **Vai trò + phần mình làm:** Đội trưởng (`TEAMS.md`), phụ trách mạch Pain → Impact, thiết kế giải pháp và điều phối/nộp checkpoint.
   - CP2: chốt lát cắt, chuẩn "đạt" và hồ sơ đánh giá ban đầu tại `canvas.md`, `spec.md` §0–§4, §7, `eval/README.md` (commit `e2a5ebe`).
   - CP3: hoàn thiện `spec.md`, bổ sung retry/`User-Agent` ở `codebase/ai.py` và tách JSON ở `codebase/agent.py`, chấm tay 23/23 câu lượt 1 (`eval/run-1.csv`, commit `422fe1a`), làm giao diện demo `codebase/app.py` + `codebase/ui.html` (commit `2000172`).
   - CP4: đồng bộ hồ sơ (`spec.md`, `cost/cost-estimate.md`, `eval/README.md`, `docs/ai-usage.md`), hoàn thiện slide `demo-slides.html` / `demo-slides.pdf` và cập nhật link video dự phòng (commits `c2d3984`, `694bc29`, `c90a5bb`).

2. **AI hỗ trợ mình thế nào:** Dùng Antigravity để rà cấu trúc `spec.md`, ghép `eval/benchmark.csv`, thêm xử lý lỗi mạng/JSON trong `codebase/ai.py` và `codebase/agent.py`, dựng giao diện `codebase/ui.html`; dùng Codex đồng bộ hồ sơ CP4 và dựng `demo-slides.html` từ số liệu đã có (`docs/ai-usage.md`).
   - Chỗ phải kiểm và sửa lại: đối chiếu thủ công số liệu từ `evidence/data-mining.md` và `evidence/summary.md` vào `spec.md`; kiểm đủ 16/16 đoạn `data/lesson/segments.json` khớp `expected` và không lẫn khái niệm ngoài bài (RAG, transformer, embedding, agentic fit, LoRA).
   - Ở `eval/run-1.csv`, mình tự chấm tay 23/23 câu theo `eval/metric_spec.yaml` (chốt phương án chấm chặt 21/23, không dùng LLM chấm) và luôn kiểm diff + chạy `python run.py check` trước khi commit.

3. **Một câu thử trượt của nhóm và mình học được gì:** Câu `B05` (`[video d04-r3-v02] System prompt nên ghi những phần gì ạ?`) ở lượt 1 (`eval/run-1.csv`, `eval/report.md` mục 2): model lấy ý cuối từ đoạn `#S4` nhưng danh sách mốc chỉ dẫn `#S1, #S2, #S3`, bỏ sót `#S4`.
   - Khi chấm chặt `moc_dung_doan`, nếu chỉ đọc lướt xem câu trả lời có đúng ý không thì rất dễ bỏ qua lỗi sót mốc, trong khi thiếu mốc để mở lại đúng chỗ chính là pain gốc của học viên (41,1% câu trả lời thiếu mốc).
   - Mình rút ra rằng không thể chỉ trông vào prompt để model tự gắn đủ mốc cho từng ý, mà cần hậu kiểm bằng code sau model và giữ tiêu chí chấm chặt ngay từ lượt 1 để lỗi lộ ra rõ ràng trước khi sửa cho CP4.
