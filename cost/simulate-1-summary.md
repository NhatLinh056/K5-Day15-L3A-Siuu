# Tóm tắt mô phỏng simulate-1@20261128-105736

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dung_it | 15 | 1 | 1053 | 891 | 0.8 | 0.9 |
| dung_vua | 12 | 1 | 974 | 930 | 0.8 | 0.8 |
| dung_nhieu | 23 | 2 | 2081 | 1783 | 1.6 | 1.7 |

Tỉ lệ đạt dùng để tính: 23/23 (100%) — lượt run-2@20261128-004110

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (145 người) | Chi phí / tháng — cơ sở (436 người) | Chi phí / tháng — cao (721 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gemini-2.0-flash (vào 0.1 · ra 0.4 $/1M) | $0.00068 | $0.00068 | $0.00046 | $1.30 | $3.92 | $6.49 | $0.0090 |
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.0010 | $0.0010 | $0.00069 | $1.96 | $5.88 | $9.73 | $0.0135 |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.5) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-5-mini. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
