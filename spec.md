# AI SPEC — Trả lời kèm mốc đoạn bài · Nhóm Siuu · Phòng [XXX] · Zone [X]

> Mốc nộp: §7 chốt chuẩn "đạt" tại **CP2 19:30 Thứ Sáu 27/11** · §0–§7 nộp **CP3 10:00 Thứ Bảy 28/11** · đủ §0–§10 **CP4 14:30 Thứ Bảy 28/11** · §10 changelog ghi tiếp đến **23:59 Thứ Bảy 28/11**.
> Đầu mỗi mục ghi bước guide (`02-guide.md` trong repo đề) chỉ cách điền. Mỗi mục ngắn, có số và nguồn; chi tiết để ở file được trỏ tới. Xoá dòng hướng dẫn trong ngoặc vuông khi điền xong.

Track: [x] A · [ ] B · [ ] C · [ ] D · [ ] E — bài toán: hướng A1 (tutor cho trang pre-class) — tối ưu một điểm: trả lời câu hỏi dưới video kèm mốc đoạn trong bài, hoặc nói rõ "không có trong bài"
Data BTC cấp đã dùng (nếu có — không commit nguyên file): `data/preclass/` (events, answers, chat, completed_items, learners · 05/11–25/11/2026) — chỉ số tổng hợp, đếm bằng `evidence/count.py`

## §0. Hiện tại việc này diễn ra thế nào *(guide 1.1)*
- Luồng hiện tại: (1) học viên mở bài trên trang pre-class, xem video → (2) gặp ý chưa hiểu → (3) tua lùi xem lại, hoặc gõ câu hỏi / bôi đen chữ trên slide để hỏi trợ giảng AI dưới video → (4) đọc câu trả lời, có khi kèm mốc giây trong bài → (5) xem tiếp, hoặc bỏ dở. *(Ảnh chụp màn hình: bổ sung từ tài khoản của thành viên, đã che thông tin.)*
- Công cụ / AI đang được dùng: trợ giảng AI dưới video của trang pre-class (`agent_id = teaching_assistant` trong `chat.csv`), dùng ngữ cảnh "đoạn quanh lúc hỏi" hoặc "lời giảng cả ngày" (`ngu_canh`), từ 13/11 có ghi các mốc giây được dẫn (`moc_trich_dan`). Prompt và model cụ thể: chưa kiểm.

## §1. Người dùng & bằng chứng *(guide 1.1, 1.2)*
- Người dùng chính: học viên L3 khoá AI20K đang tự xem video pre-class trước buổi học, gặp một đoạn chưa hiểu mà lúc đó không có trợ giảng người trực.
- Việc họ cố làm xong: *hiểu một ý trong video pre-class trước buổi học trên lớp.*
- Hôm nay họ giải bằng gì, hỏng ở đâu, vì sao chưa bỏ: tua lùi để xem lại (38,3% người xem có làm), hỏi trợ giảng dưới video (33,3% học viên có hoạt động), hỏi bạn / ChatGPT riêng *(chưa kiểm, hỏi ở phỏng vấn)*. Chỗ hỏng: tua là dò thủ công; 41,1% câu trả lời của trợ giảng không chỉ ra đoạn nào trong bài để kiểm lại; 25,5% tin nhắn là lần hỏi lại cùng câu. Vì sao chưa bỏ: *(hỏi ở phỏng vấn)*.
- Pain (KHÔNG chữ AI): học viên L3 đang xem video pre-class, gặp ý chưa hiểu thì phải tua dò lại để tìm đúng đoạn giảng, và câu trả lời nhận được thường không chỉ ra đoạn nào trong bài để kiểm lại — mất thời gian, bỏ dở video (57,0% lượt mở video chưa xem tới cuối), lên lớp vẫn hổng ý đó.
- Bằng chứng — số chính + kết luận (chi tiết: `evidence/summary.md`): đào data đã có số (`evidence/data-mining.md`); phỏng vấn ≥3 người đang làm. **Một phần ngược giả thuyết:** chỉ 30,5% lượt mở video vào 19:00–01:00, đỉnh lớn nhất là 09:00 → bỏ ý "tối mới xem", giữ ý "tự xem, không có người trực".

## §2. Impact & quyết định chọn *(guide 1.3)*

Cửa sổ data: 21 ngày (05/11–25/11/2026) → quy ra tháng × 30/21.

| Hướng | Bao nhiêu người gặp | Bao nhiêu lần / tháng | Mỗi lần tốn gì | Impact / tháng | Làm kịp không | Chọn? |
|---|---|---|---|---|---|---|
| **A1 · Trả lời câu hỏi dưới video kèm mốc đoạn trong bài / nói "không có trong bài"** | 145/436 học viên hỏi dưới video; 165/431 người xem tua lùi ≥10s *(data)* | ~1.580 câu hỏi (1.108 × 30/21) · ~2.670 lượt tua lùi ≥10s *(data)* | 3–5 phút dò lại đoạn bài mỗi lần *(tự ước tính, kiểm ở phỏng vấn)* | ~1.580 × 4 phút ≈ **105 giờ học viên / tháng** (chỉ tính lượt hỏi) | Kịp: một quyết định, data bài tự dựng từ đoạn trích ngắn | **Chọn** |
| A1' · Báo cáo "lớp đang kẹt ý gì" cho giảng viên trước buổi | Giảng viên mỗi buổi LEC *(tự ước tính ~1 người / buổi)* | ~12 buổi / tháng *(tự ước tính)* | ~30 phút tự đoán / tự gom câu hỏi *(tự ước tính)* | ~6 giờ / tháng; hưởng lợi gián tiếp: 7/40 ý kiến thức đúng lần đầu <70% *(data, n=77 học viên)* | Kịp, nhưng khó gặp giảng viên để kiểm | Loại |
| A1'' · Tóm tắt / nhắc học bù cho người bỏ dở bài | Người xem giảm từ 416 (Day01) xuống 50 (Day13); 1.047/1.563 cặp (học viên, bài) mở mà 0 mục xong *(data)* | Chưa rõ | Chưa rõ: có thể do thiếu thời gian, không do không hiểu | Chưa tính được | Khó đo "học được" trong 10 giờ | Loại (giữ dự phòng) |
| A5 · Soạn thông báo phòng lab cho key coach | Key coach mỗi tối trước buổi lab *(chưa có nguồn)* | Chưa rõ | Chưa rõ | Chưa tính được | Kịp | Loại: chưa có bằng chứng thật (data training-ops là giả lập) |

- **Impact / tháng** của hướng chọn = 145 người hỏi → ~1.580 câu hỏi / tháng × ~4 phút = **~105 giờ / tháng**. Nguồn: số câu hỏi và số người lấy từ `data/preclass/chat.csv` (đếm bằng `evidence/count.py`); số phút mỗi lần là *(tự ước tính)*, thay bằng số phỏng vấn trước CP3.
- Hướng ĐÃ LOẠI + vì sao: A1' (người dùng là giảng viên, ít người, khó gặp trong 2 ngày, impact nhỏ hơn) · A1'' (chưa biết vì sao học viên bỏ dở, có thể không phải chỗ AI giúp được) · A5 (không có bằng chứng thật, chỉ có data giả lập).
- Số lần / tháng của từng kiểu người dùng (dùng cho persona ở §8): *(đếm phân bố câu hỏi / học viên trước CP3: hỏi ít · hỏi vừa · hỏi dồn trước buổi học)*

## §3. Giải pháp tương tự *(guide 2.1)*
- [sản phẩm / tính năng gần giống]: một điều đáng học · một điều đáng né · mình khác gì

## §4. Thiết kế *(guide 2.2, 3.2)*
- **Lát cắt MỘT CÂU** (1 người dùng · 1 việc · 1 quyết định AI · 1 kết quả):
- Không làm (≥3 điều):
- **Sơ đồ** (ảnh / Mermaid / draw.io): [chèn ở đây]
- **Hình dạng:** [ ] workflow cố định · [ ] một agent · [ ] nhiều agent — 2 dòng lý do, và vì sao **không** chọn hình dạng phức tạp hơn:
- **AI dựa vào đâu** — mỗi công cụ (khớp `codebase/tools.py`):

  | Công cụ | Input | Output | Tác động ra ngoài? |
  |---|---|---|---|
  |  |  |  |  |

- **Mức tự động:** [ ] AI gợi ý, người quyết · [ ] AI tự làm khi chắc, chuyển người khi không · [ ] AI tự làm — lý do (sai thì ai chịu gì, sửa đắt hay rẻ):
- **Chỗ chặn rủi ro** (rủi ro lớn nhất của lát cắt bị chặn ở đâu, bằng gì):
- **Chỗ người duyệt** (việc AI không được tự làm):
- **Nguyên tắc thiết kế** (≥3, bắt buộc G10):

  | Nguyên tắc | Chỗ cụ thể trên sơ đồ / trong bản chạy thử |
  |---|---|
  | G10 — thu hẹp phạm vi khi không chắc |  |
  |  |  |
  |  |  |

- Phần nào còn giả (công cụ trả dữ liệu giả, model chế độ giả…) — ghi rõ, không giả làm thật:

## §5. Chỗ khó — 4 lớp + ≥6 kịch bản + 2 tấn công *(guide 2.3)*

| Kịch bản | Lớp (1–4) | Hành vi mong muốn (nói gì, hiện gì, cho làm gì tiếp) | Câu thử |
|---|---|---|---|
|  |  |  |  |
| *(tấn công)* |  |  |  |
| *(tấn công)* |  |  |  |

(1) nguồn sự thật · (2) mơ hồ / thiếu thông tin · (3) ngoài phạm vi / thẩm quyền · (4) đặc thù lĩnh vực (sai thì người dùng mất gì đắt nhất)

## §6. Bốn đường đi của trải nghiệm
- Mọi thứ suôn sẻ: · Không chắc (lớp 2): · Không có căn cứ (lớp 1): · Người dùng sửa:
- Bị đòi ngoài phạm vi (lớp 3): · Trường hợp đặc thù lĩnh vực (lớp 4):

## §7. Đánh giá & chuẩn "đạt" *(guide 2.4, 4.1)*
- Data card: `data/DATA_CARD.md` · bộ câu thử: `eval/benchmark.csv` — __ câu (thuong __ · kho __ · tu_choi __) · metric: `eval/metric_spec.yaml` (__ metric)
- **Chuẩn "đạt"** (chốt **trước 19:30 Thứ Sáu 27/11**, giữ nguyên đến 23:59 Thứ Bảy 28/11): "Đạt khi ≥ __% câu qua, và __"
- Kết quả: lượt 1 __/__ (__%) · lượt 2 __/__ (__%) — run ID: __ / __ → chi tiết `eval/report.md`, hồ sơ `eval/README.md`

## §8. Chi phí khi dùng thật *(guide 4.2)*
- Persona + giá: `cost/personas.yaml` · lượt mô phỏng: `cost/simulate-__.csv` (__ phiên)
- Chi phí / task thành công: __ (model __) · __ (model __)
- Chi phí / tháng ở quy mô thật: thấp __ · cơ sở __ · cao __ → chi tiết `cost/cost-estimate.md`
- So với impact / người / tháng (§2): đáng làm không, vì sao:

## §9. Rủi ro & an toàn
- Dữ liệu: đã ẩn danh gì, không thu gì, không đưa gì vào model gói miễn phí:
- AI **không được** làm gì kể cả khi người dùng yêu cầu:
- Ai có thể bị hại nếu AI sai, và nhóm chặn thế nào:

## §10. Phân công & changelog
- Phân công có tên (theo chặng, chia cặp — guide "Cách chia việc"): Lê Nhật Linh (đội trưởng) — §0–§2, §4, canvas, nộp checkpoint · Đặng Thanh Hải — đào data, kịch bản phỏng vấn · Hoàng Gia Khiêm — `codebase/`, `eval/`, `data/DATA_CARD.md` · Lê Hải Bắc — phỏng vấn P1–P3, `evidence/summary.md`. Cặp: Hải + Bắc (bằng chứng), Linh + Khiêm (thiết kế → bản chạy thử)
- Dùng AI vào việc gì (2–3 dòng; chi tiết `docs/ai-usage.md`):
- Nhật ký thay đổi — **mọi thay đổi sau CP2 19:30 Thứ Sáu 27/11 phải có dòng ở đây**:

**CP2 → CP4** (vd thu hẹp lát cắt, hỏi thêm người dùng, lần cải tiến trước lượt 2)

| Thời điểm | Đổi gì | Vì sao (trỏ về câu thử / lỗi / bằng chứng nào) |
|---|---|---|
|  |  |  |

**Sau CP4 (đến 23:59 Thứ Bảy 28/11)** (sửa theo góp ý — không sửa chuẩn "đạt", câu thử, số bằng chứng, kết quả các lượt đã chạy)

| Thời điểm | Đổi gì | Vì sao |
|---|---|---|
|  |  |  |