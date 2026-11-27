# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | | | | |
| Prompt / thiết kế lời gọi mô hình | | | | |
| Đào data (viết script đếm, gợi ý nhãn) | Claude Code (Claude Opus 5.5) | Viết `evidence/count.py`, chạy và soạn `evidence/data-mining.md`; viết kịch bản phỏng vấn `evidence/interviews/GUIDE.md` | Kiểm tay 3 số bằng Excel lọc cột (1.108 câu hỏi dưới video · 114 câu <15 ký tự · chatbot_is_app_around_model 25/41), khớp 3/3 | Đặng Thanh Hải |
| Rà câu hỏi phỏng vấn / khảo sát | | Chỉ rà câu dẫn dắt | | |
| Viết câu thử (benchmark) | Claude Code (Claude Opus 5.5) | Tra `data-btc/preclass` lấy mã dòng / `kc_code` làm nguồn `data_that` và soạn nháp câu chữ B01–B04, B05 (câu thay); chỉnh `pass_criterion` B03, B04, B05–B07 cho khớp `eval/metric_spec.yaml`; ghép `eval/benchmark.csv`; soạn bản đầu `data/DATA_CARD.md` | Mỗi câu thử có `source` ghi mã dòng hoặc `kc_code` + số trong `evidence/data-mining.md`; đã đối chiếu mã C01056, C00983, C00899 trong `chat.csv`; nội dung `expected` (vd "chatbot là ứng dụng bọc quanh model") suy từ tên `kc_code`, **chưa đối chiếu lời giảng** — kiểm lại khi có `data/lesson/segments.json` · B12, B16, B17 do Khiêm viết · B06, B07 do Bắc viết | Đặng Thanh Hải (ghép) · Hoàng Gia Khiêm · Lê Hải Bắc |
| Sinh data `synthetic` (nếu có) | Claude Code (Claude Opus 5.5) | Soạn nháp 16 đoạn bài `data/lesson/segments.json` (4 video Day01, Day04) theo tên `kc_code` của bài; tự đặt mốc giây; soạn nháp 5 câu thử H01–H05 (`eval/cau-thu-Hai.csv`) | Không seed (viết tay, không sinh ngẫu nhiên) · kiểm tay __/16 đoạn (đúng kiến thức, khớp `expected` các câu thử, không có RAG / transformer / embedding / agentic fit) | Đặng Thanh Hải |
| Chấm cột `pass` bằng LLM (nếu có) | | | Kiểm tra thủ công __ câu thử, khớp __/__ | |
| Slide, văn bản | | | | |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
