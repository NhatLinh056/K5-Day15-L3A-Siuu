# Đào data — cách đếm và kết quả

> Guide bước 1.2. Script: [`evidence/count.py`](count.py) — chạy `python evidence/count.py data-btc/preclass` (đặt thư mục `data/preclass` của bộ đề vào `data-btc/`, không commit). Người khác chạy lại phải ra cùng số.
> Repo chỉ chứa số đã tổng hợp và vài mã dòng ví dụ — không chép lại nguyên file data.

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Data dùng:** `data/preclass/` BTC cấp — `events.csv`, `answers.csv`, `chat.csv`, `completed_items.csv`, `learners.csv` · 05/11 → 25/11/2026 (Day01–Day13).
- **Mẫu số gốc:** **436 học viên có hoạt động** (≥1 dòng `actor = learner` trong `events.csv`), không phải 721 tài khoản. Từng chỉ số ghi rõ mẫu số riêng bên dưới.
- **Đếm gì:**
  1. *Xem lại một đoạn:* lượt `video_seeked` có `from − to ≥ 10` giây (tua lùi). Đếm số học viên có ≥1 lượt, trên số học viên đã mở ≥1 video.
  2. *Bỏ dở video:* cặp (học viên, video) có `video_opened` nhưng chưa từng có `video_ended`, trên mọi cặp đã mở.
  3. *Giờ học:* giờ VN (UTC+7) của `video_opened`.
  4. *Bài mở mà không xong mục nào:* cặp (học viên, `lesson_id`) có `lecture_opened`/`video_opened` mà không có dòng nào trong `completed_items.csv`.
  5. *Hiểu bài:* `answers.csv`, `lan_thu = 1`, `was_correct` đúng/sai, theo `nguon` và `kc_code` (chỉ xét ý có ≥20 lượt).
  6. *Hỏi trợ giảng:* `chat.csv` `channel = video_question`, nối `agent_replied` qua `ref_id` để lấy `missing_context`, `moc_trich_dan` (mốc giây trong bài AI dẫn ra), `ask_count`.
- **Lọc:** chỉ `actor = learner` cho hành vi học viên. Trường `moc_trich_dan` chỉ được ghi từ **13/11/2026** → mẫu số của chỉ số "không dẫn mốc" là các trả lời có trường này (562), không phải toàn bộ 1.108.

## 2. Đọc trước, đếm sau

Đã đọc `column_dictionary.csv`, `event_types.csv` và các dòng đầu từng file. Các *kiểu* hành vi thấy được:
- Mở video → xem từng quãng (`video_segments_flushed`) → tua (`video_seeked`) → có/không xem tới cuối (`video_ended`).
- Câu hỏi giữa video bật lên → trả lời / đóng (`quiz_item_*`). Gần như không ai bỏ qua (1%).
- Hỏi trợ giảng dưới video (gõ câu hỏi hoặc bôi đen chữ trên slide) → trợ giảng trả lời, có khi kèm mốc giây trong bài.
- Ôn tập cuối ngày (`pre_post_post`) chỉ có 77 học viên làm.
- Mini lab: mở → làm từng bước → xong, hoặc bấm "bỏ qua".

## 3. Kết quả

| Đếm gì | x / N | % | Ghi chú |
|---|---|---|---|
| Học viên đã mở video có ≥1 lần **tua lùi ≥10s** | 165 / 431 | 38,3% | 1.870 lượt tua lùi / 4.322 lượt tua |
| Cặp (học viên, video) **mở mà chưa xem tới cuối** | 2.224 / 3.900 | 57,0% | Có thể xem phần còn lại ở LMS — chưa kiểm |
| Cặp (học viên, bài) mở mà **0 mục đánh dấu xong** | 1.047 / 1.563 | 67,0% | "Xong" là học viên tự bấm — có thể quên bấm |
| **Người xem video theo ngày học** | Day01: 416 → Day05: 134 → Day09: 75 → Day13: 50 | | Người xem giảm ~8 lần trong 13 ngày |
| Lượt mở video lúc **19:00–00:59** giờ VN | 2.210 / 7.254 | 30,5% | **Ngược giả thuyết "tối mới xem":** đỉnh lớn nhất 09:00 (1.156 lượt), đỉnh thứ hai 22–23h |
| Học viên **hỏi trợ giảng** dưới video ≥1 lần | 145 / 436 | 33,3% | 1.108 câu hỏi |
| Tỉ lệ người hỏi / người xem theo ngày | 14–24% (Day01–Day09) | | Ổn định → lượt hỏi giảm là do người xem giảm |
| Trả lời của trợ giảng **không dẫn mốc giây nào trong bài** | 231 / 562 | 41,1% | Chỉ tính trả lời từ 13/11 (lúc bắt đầu ghi trường này) |
| Trả lời bị gắn `missing_context` (thiếu ngữ cảnh) | 100 / 1.108 | 9,0% | |
| Tin nhắn là **lần hỏi lại** cùng câu (`ask_count ≥ 1`) | 35 / 137 | 25,5% | Chỉ trên tin có ghi `ask_count` |
| Câu hỏi rất ngắn (<15 ký tự) | 114 / 1.108 | 10,3% | Dễ mơ hồ |
| Ôn tập cuối ngày: đúng lần đầu | 1.569 / 1.968 | 79,7% | 77 học viên · **7/40 ý kiến thức <70%** (xem bảng dưới) |
| Mini lab "xong" bằng nút **bỏ qua** | 102 / 453 | 22,5% | |

**Ôn tập cuối ngày — 7 ý kiến thức đúng lần đầu <70%** (≥20 lượt, `lan_thu = 1`):

| Ý kiến thức (`kc_code`) | Đúng lần đầu |
|---|---|
| `agentic_fit_scoring_decision` | 8/20 (40%) |
| `cot_task_fit` | 16/27 (59%) |
| `chatbot_is_app_around_model` | 25/41 (61%) |
| `complete_ai_problem_statement` | 15/23 (65%) |
| `select_rule_workflow_agent_level` | 15/23 (65%) |
| `system_prompt_contract` | 18/27 (67%) |
| `construct_eval_plan` | 16/23 (69,6%) |

**Số câu hỏi dưới video / học viên** (145 người có hỏi, trong 21 ngày) — dùng cho persona chi phí (`spec.md` §2, §8):

| Kiểu | Số người |
|---|---|
| Hỏi 1 câu | 40/145 (27,6%) |
| Hỏi 2–5 câu | 42/145 (29,0%) |
| Hỏi 6–15 câu | 47/145 (32,4%) |
| Hỏi >15 câu | 16/145 (11,0%) — nhiều nhất 72 câu |

Trung vị: 4 câu / người / 21 ngày.

## 4. ≥5 ví dụ cụ thể (mã đã ẩn danh, không đoán ai là ai)

1. `L0271` · video `d01-r1-v02`: tua lùi ≥10s **48 lần** trong một video (vẫn xem tới cuối).
2. `L0271` · video `d02-r2-v05`: tua lùi ≥10s 26 lần.
3. Chat `C00983` · `Day01/d01-r1-v05.txt`: câu hỏi 29 ký tự, trả lời bị gắn `missing_context = True`.
4. Chat `C00218` · `Day01/d01-r1-v03.txt`: câu hỏi 28 ký tự, trả lời 266 ký tự **không dẫn mốc nào** trong bài.
5. Chat `C01187` · `Day06/d06-r1-v01.txt`: câu hỏi 92 ký tự, trả lời 600 ký tự không dẫn mốc nào.
6. Chat `C01056`, `C00962` · `Day01/d01-r1-v01.txt`: câu hỏi chỉ **2 ký tự**.
7. `L0002` · `program-day01:ai-llm-foundation`: mở bài, 0 mục xong.

## 4b. Nguồn `data_that` cho bộ câu thử (cấp cho người viết `eval/benchmark.csv`)

Data **không có nội dung câu hỏi**, chỉ có mã dòng, video, độ dài. Nên câu thử ghi nguồn `data_that` thì câu chữ do nhóm viết; data quyết định **chủ đề / kiểu câu**, phải ghi rõ trong cột `source`. Tất cả mã dưới đây in ra bằng `evidence/count.py` (mục "Ví dụ cho bộ câu thử").

| Kiểu câu thử | Căn cứ trong data | Mã dòng ví dụ |
|---|---|---|
| Câu mơ hồ, rất ngắn → phải hỏi lại | 114/1.108 câu <15 ký tự | `C01056` (2 ký tự, d01-r1-v01) · `C00048` (6, d01-r1-v01) · `C00370` (11, d04-r3-v03) · `C00321` (2, d04-r3-v01) |
| Câu thiếu ngữ cảnh | 100/1.108 trả lời gắn `missing_context` | `C00983` (d01-r1-v05) · `C00992`, `C00837` (d02-r2-v01) |
| Câu dễ bị trả lời không dẫn nguồn | 231/562 trả lời không dẫn mốc | `C00218`, `C00955`, `C00951` (d01-r1-v03) · `C00882` (d05-r2-v06) |
| Câu về ý học viên hay sai | 7 ý kiến thức <70% ở bảng trên | ví dụ `chatbot_is_app_around_model` 25/41 · `cot_task_fit` 16/27 · `system_prompt_contract` 18/27 |

## 5. Giới hạn của data

- Data cho biết học viên **làm gì**, không cho biết **vì sao**: tua lùi có thể là do không hiểu, cũng có thể là do bị gián đoạn; bỏ dở có thể là do thiếu thời gian.
- Không có nội dung câu hỏi và câu trả lời (chỉ có độ dài), nên **không biết câu trả lời đúng hay sai** về kiến thức.
- "Không dẫn mốc" chưa chắc là sai: câu hỏi chung chung có thể không cần mốc.
- Chỉ có trang pre-class; học viên có thể học trên LMS, YouTube hoặc tài liệu khác.
- Ôn tập cuối ngày chỉ có 77/436 người làm, nên lệch về nhóm học chăm.

→ **Kiểm lại bằng phỏng vấn ≥3 học viên L3 ngoài nhóm** (chiều 27/11): lần gần nhất tua lại một đoạn là vì sao, mất bao lâu, câu trả lời của trợ giảng có giúp tìm đúng đoạn không, vì sao các ngày sau ít xem trang pre-class.
