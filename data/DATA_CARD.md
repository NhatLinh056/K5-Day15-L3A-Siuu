# Data card — dữ liệu bản chạy thử dùng

> Điền ở guide bước 2.4 (bản đầu ở CP2, đủ ở CP3). Ôn lại: ngày 6 · lab ngày 6. Chấm ở rubric R4.
> Không commit nguyên tài liệu khoá, dữ liệu cá nhân thật hay nguyên file data BTC cấp — chỉ đoạn trích ngắn, bản viết lại, hoặc số đã tổng hợp.
> **Bản đầu CP2** — người giữ: Đặng Thanh Hải.

## Dataset 1 · Nhật ký pre-class (BTC cấp)

| | |
|---|---|
| Dùng để làm gì | Đào bằng chứng pain ([evidence/data-mining.md](../evidence/data-mining.md)); chọn **chủ đề và kiểu** câu thử nguồn `data_that` trong `eval/benchmark.csv`. **Không** đưa vào bản chạy thử |
| Từ đâu | `data/preclass/` trong repo đề (BTC cấp), đặt ở `data-btc/preclass/` trên máy, **không commit** (đã có trong `.gitignore`) |
| Xử lý những bước gì | Chỉ đọc và đếm bằng [`evidence/count.py`](../evidence/count.py) · lọc `actor = learner` · mẫu số là 436 học viên có hoạt động · với "không dẫn mốc" chỉ tính trả lời từ 13/11 · BTC đã ẩn danh sẵn (mã `L…`, `C…`), nhóm không nối lại danh tính |
| Số dòng / số đoạn | `events.csv` 107.709 · `answers.csv` 3.776 · `chat.csv` 1.260 (1.108 câu hỏi dưới video) · `completed_items.csv` 2.472 · `learners.csv` 721 |
| Phiên bản / ngày lấy | Data 05/11 → 25/11/2026 (Day01–Day13) · nhóm nhận 27/11/2026 |
| Nhãn | thật (đã ẩn danh) |
| Giới hạn | **Không có câu chữ** học viên hỏi hay AI trả lời, chỉ có độ dài, nên câu thử `data_that` do nhóm viết lại theo kiểu câu/chủ đề · chỉ có trang pre-class (không có LMS, YouTube) · ôn tập cuối ngày chỉ 77/436 người làm, lệch về nhóm học chăm · trường `moc_trich_dan` chỉ có từ 13/11 · người xem giảm từ 416 (Day01) xuống 50 (Day13), nên câu hỏi dồn vào Day01 (339/1.108) |

## Dataset 2 · Lời giảng bài pre-class, chia đoạn có mã mốc — `data/lesson/segments.json`

| | |
|---|---|
| Dùng để làm gì | Nguồn cho công cụ tìm đoạn bài trong `codebase/tools.py`. File: **`data/lesson/segments.json`** — mọi mã đoạn AI dẫn ra phải có trong file này (metric `moc_dung_doan`, `khong_vuot_tham_quyen` trong `eval/metric_spec.yaml` kiểm đúng file này) |
| Từ đâu | **Nhóm viết lại** (track A cho phép: "tự dựng bài có mã đoạn… trích ngắn hoặc viết lại"). Data BTC chỉ ghi tên file lời giảng (`Day01/d01-r1-v01.txt`…), không kèm nội dung. Chủ đề từng đoạn lấy từ **tên ý kiến thức** của bài trong `answers.csv` (`kc_code` + mã câu ôn tập, vd `chatbot_is_app_around_model` / `d01-on-chatbot-la-ung-dung`, `system_prompt_contract` / `d04-on-phan-constraints`); câu chữ do nhóm viết, không chép tài liệu khoá |
| Xử lý những bước gì | Mỗi video 4 đoạn, mỗi đoạn một ý, 2–4 câu · mã `<video>#S<n>` (S1–S4) · trường: `segment_id`, `video_id`, `start_s`, `end_s`, `content`, `label` · **mốc giây do nhóm tự đặt** (đoạn liền nhau, 130–180 giây), chưa khớp video thật · script kiểm: không đoạn nào chứa "RAG", "transformer", "embedding" |
| Số dòng / số đoạn | 16 đoạn · 4 video: `d01-r1-v01` (ba yếu tố bùng nổ AI, sinh từng token, chatbot là ứng dụng bọc quanh model, trí nhớ ở ứng dụng) · `d01-r1-v05` (tự tin ≠ đúng, temperature, giới hạn đầu ra, chi phí token) · `d04-r3-v01` (zero/few-shot, khi nào dùng CoT, khi nào không, prompt cụ thể) · `d04-r3-v02` (system prompt: vai trò, ràng buộc, định dạng, lỗi hay gặp) |
| Phiên bản / ngày lấy | v1 · 27/11/2026 · người viết: Đặng Thanh Hải (nháp bằng Claude Code, xem `docs/ai-usage.md`) |
| Nhãn | `synthetic` — cả 16 đoạn (trường `label` từng dòng) |
| Giới hạn | **Không phải lời giảng thật**: nội dung là bản viết lại theo chủ đề, mốc giây tự đặt → bấm mốc trong bản chạy thử không mở đúng giây của video thật; khi có transcript thì thay và ghi phiên bản mới · chỉ 4/≈70 video, chỉ Day01 và Day04 → câu hỏi về ngày khác sẽ ra "không có trong bài" (câu thử H05 dựa vào điều này) · cố ý **không** có RAG, transformer, embedding, agentic fit (câu B12, B16, B17, H05) — thêm đoạn mới phải kiểm lại các câu này · đoạn `d01-r1-v05` có nhiều ví dụ → câu "ví dụ lúc nãy" (B04) phải hỏi lại |

## Dataset 3 · Bộ câu thử `eval/benchmark.csv`

| | |
|---|---|
| Dùng để làm gì | Chấm bản chạy thử (`python run.py eval`) |
| Từ đâu | `data_that`: câu chữ do nhóm viết, kiểu câu hoặc chủ đề lấy từ data (cột `source` ghi mã dòng hoặc `kc_code` và con số) · `tu_viet`: câu tấn công và câu ngoài bài · `nguoi_dung`: sẽ lấy từ phỏng vấn (câu 5b trong [GUIDE](../evidence/interviews/GUIDE.md)) |
| Xử lý những bước gì | Input có tiền tố `[video <mã>]` để báo học viên đang ở video nào · bỏ mọi thông tin cá nhân |
| Số dòng / số đoạn | 10 câu: thuong 3 · kho 5 · tu_choi 2 (2 câu tấn công B16, B17) · từ data thật 7/10 · B01–B04 Hải · B05–B07 Lê Hải Bắc · B12, B16, B17 Khiêm |
| Phiên bản / ngày lấy | 27/11/2026, bản CP2 |
| Nhãn | thật (chủ đề) + nhóm viết (câu chữ) |
| Giới hạn | Chưa có câu `nguoi_dung` · câu dồn vào Day01, Day04 · `expected` mô tả **hành vi và chủ đề**; `pass_criterion` ghi **phạm vi mã** (video hoặc ngày) thay vì mã cụ thể vì chưa có Dataset 2 |

**Data `synthetic` (nhóm tự sinh):** `data/lesson/segments.json` (16 đoạn). Cách sinh: Claude Code soạn nháp từng đoạn theo tên `kc_code` của bài, không dùng seed (viết tay, không sinh ngẫu nhiên); người kiểm: Đặng Thanh Hải, kiểm tay __/16 đoạn (đúng kiến thức, không lẫn chủ đề cấm). Data tự dựng **không phải bằng chứng pain**.