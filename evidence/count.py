"""Đếm bằng chứng pain trên data pre-class BTC cấp (05/11–25/11/2026).

Chạy:  python evidence/count.py data-btc/preclass
(data-btc/ không commit — đặt nguyên thư mục data/preclass của bộ đề vào đó.)
Chỉ dùng thư viện chuẩn. In ra số đã tổng hợp + vài mã dòng ví dụ; không in nội dung cá nhân.
Cách đếm (viết trước khi chạy) ở evidence/data-mining.md §1.
"""
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")  # Windows console mặc định cp1252
D = Path(sys.argv[1] if len(sys.argv) > 1 else "data-btc/preclass")


def rows(name):
    with open(D / name, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def js(e):
    try:
        return json.loads(e["data"] or "{}")
    except json.JSONDecodeError:
        return {}


def vn_hour(ts):
    return (datetime.fromisoformat(ts) + timedelta(hours=7)).hour


def pct(x, n):
    return f"{x}/{n} ({100 * x / n:.1f}%)" if n else f"{x}/0"


ev = rows("events.csv")
ans = rows("answers.csv")
chat = rows("chat.csv")
done = rows("completed_items.csv")
learners = rows("learners.csv")

learner_ev = [e for e in ev if e["actor"] == "learner" and e["hv"]]
active = {e["hv"] for e in learner_ev}
print("== Quy mô ==")
print("Tài khoản:", len(learners), "· có hoạt động (≥1 event actor=learner):", len(active))

# --- 1. Video: mở, xem hết, tua lùi ---------------------------------------
print("\n== 1. Video ==")
opened = defaultdict(set)  # hv -> {video}
ended = defaultdict(set)
for e in learner_ev:
    if e["type"] == "video_opened" and e["video"]:
        opened[e["hv"]].add(e["video"])
    if e["type"] == "video_ended" and e["video"]:
        ended[e["hv"]].add(e["video"])
pairs_open = {(h, v) for h, vs in opened.items() for v in vs}
pairs_end = {(h, v) for h, vs in ended.items() for v in vs}
print("Học viên mở ≥1 video:", pct(len(opened), len(active)))
print("Cặp (học viên, video) đã mở mà chưa từng xem tới cuối:",
      pct(len(pairs_open - pairs_end), len(pairs_open)))

BACK = 10  # tua lùi ≥10 giây = xem lại một đoạn
back = [e for e in learner_ev if e["type"] == "video_seeked"
        and (js(e).get("to") is not None and js(e).get("from") is not None)
        and js(e)["from"] - js(e)["to"] >= BACK]
back_by_pair = Counter((e["hv"], e["video"]) for e in back)
print(f"Lượt tua lùi ≥{BACK}s:", len(back), "/", sum(e["type"] == "video_seeked" for e in learner_ev), "lượt tua")
print("Học viên (đã mở video) có ≥1 lần tua lùi ≥10s:",
      pct(len({h for h, _ in back_by_pair}), len(opened)))
print("Cặp (học viên, video) tua lùi ≥3 lần:", pct(sum(c >= 3 for c in back_by_pair.values()), len(pairs_open)))

# --- 2. Giờ học (giờ VN) ----------------------------------------------------
print("\n== 2. Giờ mở video (giờ VN = UTC+7) ==")
hours = Counter(vn_hour(e["occurred_at"]) for e in learner_ev if e["type"] == "video_opened")
tot = sum(hours.values())
evening = sum(c for h, c in hours.items() if h >= 19 or h < 1)
print("Lượt mở video 19:00–00:59:", pct(evening, tot))
print("Theo giờ:", " ".join(f"{h:02d}:{hours[h]}" for h in range(24)))

# --- 3. Bài mở mà không xong mục nào -------------------------------------------
print("\n== 3. Bài mở nhưng không xong mục nào ==")
lesson_open = {(e["hv"], e["lesson_id"]) for e in learner_ev
               if e["type"] in ("lecture_opened", "video_opened") and e["lesson_id"]}
lesson_done = {(r["hv"], r["lesson_id"]) for r in done}
stuck = lesson_open - lesson_done
print("Cặp (học viên, bài) mở mà 0 mục xong:", pct(len(stuck), len(lesson_open)))
print("Học viên có ≥1 bài như vậy:", pct(len({h for h, _ in stuck}), len({h for h, _ in lesson_open})))

# --- 4. Câu hỏi giữa video: đúng lần đầu ---------------------------------------
print("\n== 4. Câu hỏi giữa video (video_quiz) & ôn tập cuối ngày (pre_post_post), lần đầu ==")
for src in ("video_quiz", "pre_post_post"):
    first = [a for a in ans if a["nguon"] == src and a["lan_thu"] == "1" and a["was_correct"] in ("True", "False")]
    ok = sum(a["was_correct"] == "True" for a in first)
    print(f"{src}: đúng lần đầu", pct(ok, len(first)), "· học viên:", len({a['hv'] for a in first}))
    by_kc = defaultdict(list)
    for a in first:
        by_kc[a["kc_code"]].append(a["was_correct"] == "True")
    hard = sorted(((sum(v) / len(v), k, len(v)) for k, v in by_kc.items() if len(v) >= 20))
    low = [x for x in hard if x[0] < 0.7]
    print(f"  ý kiến thức có ≥20 lượt: {len(hard)} · trong đó đúng lần đầu <70%: {len(low)}")
    for r, k, n in low:
        print(f"    {k}: {round(r * n)}/{n} ({r:.0%})")

skipped = [e for e in learner_ev if e["type"] == "quiz_item_dismissed" and js(e).get("skipped_stop") is True]
print("Câu hỏi giữa video bị đóng không trả lời:",
      pct(len(skipped), sum(e["type"] == "quiz_item_dismissed" for e in learner_ev)))

# --- 5. Hỏi trợ giảng AI dưới video -----------------------------------------------
print("\n== 5. Hỏi trợ giảng AI ==")
vq = [c for c in chat if c["channel"] == "video_question"]
print("Lượt hỏi dưới video:", len(vq), "· học viên hỏi ≥1 lần:", pct(len({c['hv'] for c in vq}), len(active)))
print("  trong số học viên đã mở video:", pct(len({c['hv'] for c in vq} & set(opened)), len(opened)))
rep = {e["ref_id"]: js(e) for e in ev if e["type"] == "agent_replied"}
vq_rep = [rep[c["id"]] for c in vq if c["id"] in rep]
miss = sum(r.get("missing_context") is True for r in vq_rep)
print("Trả lời bị đánh dấu thiếu ngữ cảnh (missing_context):", pct(miss, len(vq_rep)))
has_field = [r for r in vq_rep if "moc_trich_dan" in r]
no_cite = sum(not r.get("moc_trich_dan") for r in has_field)
print("Trả lời không dẫn mốc giây nào trong bài (trên dòng có ghi trường này):", pct(no_cite, len(has_field)))
short_q = sum(int(c["do_dai_cau_hoi"] or 0) < 15 for c in vq)
print("Câu hỏi < 15 ký tự:", pct(short_q, len(vq)))
day_q = Counter(c["transcript"].split("/")[0] for c in vq if c["transcript"])
print("Theo ngày học:", dict(sorted(day_q.items())))
cs = [e for e in learner_ev if e["type"] == "chat_sent"]
again = [e for e in cs if (js(e).get("ask_count") or 0) >= 1]
print("Tin nhắn là lần hỏi lại (ask_count ≥1) trên tin có ghi ask_count:",
      pct(len(again), sum(js(e).get("ask_count") is not None for e in cs)))

# --- 6. Mini lab ---------------------------------------------------------------
print("\n== 6. Mini lab ==")
lo = [e for e in learner_ev if e["type"] == "lab_opened"]
lc = [e for e in learner_ev if e["type"] == "lab_completed"]
print("Lab hoàn thành bằng nút bỏ qua:", pct(sum(js(e).get("skipped") is True for e in lc), len(lc)))
lo_pairs = {(e["hv"], js(e).get("lab_key")) for e in lo}
lc_pairs = {(e["hv"], js(e).get("lab_key")) for e in lc}
print("Cặp (học viên, lab) mở mà chưa có lab_completed:", pct(len(lo_pairs - lc_pairs), len(lo_pairs)))

# --- Ví dụ (mã đã ẩn danh) ------------------------------------------------------
print("\n== Ví dụ ==")
for (h, v), c in back_by_pair.most_common(3):
    print(f"  {h} · video {v}: tua lùi ≥10s {c} lần, xem tới cuối: {'có' if (h, v) in pairs_end else 'không'}")
for c in vq:
    r = rep.get(c["id"], {})
    if r.get("missing_context") is True:
        print(f"  chat {c['id']} · {c['transcript']} · câu hỏi {c['do_dai_cau_hoi']} ký tự · missing_context=True")
        break
for h, l in sorted(stuck)[:2]:
    print(f"  {h} · {l}: mở bài, 0 mục xong")

# Nguồn data_that cho bộ câu thử: câu hỏi rất ngắn, thiếu ngữ cảnh, trả lời không dẫn mốc.
# Chỉ in mã dòng + video + độ dài (data không có nội dung câu hỏi).
print("\n== Ví dụ cho bộ câu thử (data_that) ==")
print("Câu hỏi dưới video <15 ký tự (10 dòng đầu theo thời gian):")
for c in sorted((c for c in vq if int(c["do_dai_cau_hoi"] or 0) < 15), key=lambda c: c["asked_at"])[:10]:
    print(f"  {c['id']} · {c['transcript']} · {c['do_dai_cau_hoi']} ký tự")
print("Câu hỏi <15 ký tự dưới video d04-r3-v01 (video của câu thử B02, B05, B07):")
for c in sorted((c for c in vq if c["transcript"] == "Day04/d04-r3-v01.txt" and int(c["do_dai_cau_hoi"] or 0) < 15), key=lambda c: c["asked_at"]):
    print(f"  {c['id']} · {c['transcript']} · {c['do_dai_cau_hoi']} ký tự")
print("Trả lời bị gắn missing_context (5 dòng đầu):")
for c in [c for c in vq if rep.get(c["id"], {}).get("missing_context") is True][:5]:
    print(f"  {c['id']} · {c['transcript']} · câu hỏi {c['do_dai_cau_hoi']} ký tự")
print("Trả lời không dẫn mốc nào trong bài (5 dòng đầu, từ 13/11):")
for c in [c for c in vq if "moc_trich_dan" in rep.get(c["id"], {}) and not rep[c["id"]]["moc_trich_dan"]][:5]:
    print(f"  {c['id']} · {c['transcript']} · câu hỏi {c['do_dai_cau_hoi']} ký tự · trả lời {c['do_dai_tra_loi']} ký tự")

# Persona chi phí (spec §2, §8): phân bố số câu hỏi dưới video / học viên trong 21 ngày.
print("\n== Số câu hỏi dưới video / học viên (145 người có hỏi) ==")
per = Counter(c["hv"] for c in vq)
bins = {"1 câu": 0, "2–5 câu": 0, "6–15 câu": 0, ">15 câu": 0}
for n in per.values():
    bins["1 câu" if n == 1 else "2–5 câu" if n <= 5 else "6–15 câu" if n <= 15 else ">15 câu"] += 1
for k, v in bins.items():
    print(f"  {k}: {pct(v, len(per))}")
print(f"  trung vị: {sorted(per.values())[len(per) // 2]} câu · nhiều nhất: {max(per.values())} câu")

# Ý kiến thức làm chủ đề câu thử data_that (eval/benchmark.csv): đúng lần đầu ở ôn tập cuối ngày.
print("\n== Ý kiến thức dùng cho câu thử (pre_post_post, lần đầu) ==")
first = [a for a in ans if a["nguon"] == "pre_post_post" and a["lan_thu"] == "1" and a["was_correct"] in ("True", "False")]
for k in ("chatbot_is_app_around_model", "cot_task_fit", "system_prompt_contract", "token_generation_loop_count",
          "temperature_stability_not_truth", "zero_one_few_shot_selection", "agentic_fit_scoring_decision"):
    v = [a["was_correct"] == "True" for a in first if a["kc_code"] == k]
    print(f"  {k}: {pct(sum(v), len(v))}")
