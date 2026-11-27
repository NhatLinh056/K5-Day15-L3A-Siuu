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

## Dataset 2 · Lời giảng bài pre-class, chia đoạn có mã mốc (nguồn cho công cụ tìm đoạn)

| | |
|---|---|
| Dùng để làm gì | File `data/lesson/segments.json`: nguồn cho công cụ tìm đoạn bài trong `codebase/tools.py`; mọi mã đoạn AI dẫn ra phải có trong file này (metric `moc_dung_doan`, `khong_vuot_tham_quyen`) |
| Từ đâu | **Chưa có.** Data BTC chỉ ghi tên file lời giảng (`Day01/d01-r1-v01.txt`…), không kèm nội dung. Cần chốt: xin transcript từ BTC, hoặc nhóm viết lại đoạn ngắn từ video Day01 và Day04 |
| Xử lý những bước gì | Dự kiến: chia mỗi video thành đoạn ngắn, gán mã `<video>#S<n>` (vd `d01-r1-v01#S1`) kèm mốc giây bắt đầu và kết thúc · chỉ chép đoạn trích ngắn hoặc viết lại, không chép nguyên bài |
| Số dòng / số đoạn | __ (điền khi có) |
| Phiên bản / ngày lấy | __ |
| Nhãn | thật (trích) hoặc `synthetic` (viết lại); ghi rõ từng dòng |
| Giới hạn | Bộ câu thử hiện dựa vào Day01 (d01-r1-v01, d01-r1-v05) và Day04 (d04-r3-v01), nên **ít nhất phải có các video này**. Không được đưa vào data những chủ đề mà câu thử `tu_choi` hay `kho` coi là "không có trong bài" (RAG, transformer: B12, B16, B17) |

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

**Data `synthetic` (nhóm tự sinh):** hiện chưa có. Nếu sinh thì ghi cách sinh (prompt hoặc script), seed, người kiểm, số dòng đã kiểm tay. Data tự dựng **không phải bằng chứng pain**.
