"""Công cụ của bài toán — nhóm Siuu. Khớp bảng công cụ ở spec.md §4.

Chỉ có công cụ ĐỌC, không công cụ nào tác động ra ngoài (không gửi tin, không chấm điểm, không sửa dữ liệu).

Dữ liệu: data/lesson/segments.json (Hải soạn, mô tả ở data/DATA_CARD.md Dataset 2), dạng:
    [{"segment_id": "d01-r1-v01#S1", "video_id": "d01-r1-v01", "start_s": 0, "end_s": 120, "content": "..."}]
Chưa có segments.json thì tạm đọc data/lesson/segments.sample.json (bản nháp synthetic, chỉ để chạy thử luồng)
và ghi rõ trong trace. Có segments.json rồi thì file mẫu bị bỏ qua.
"""
import json
import math
import os
import re
import sys
import unicodedata

from tracing import tool, note, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSON_FILE = os.path.join(ROOT, "data", "lesson", "segments.json")
SAMPLE_FILE = os.path.join(ROOT, "data", "lesson", "segments.sample.json")

# Từ quá chung (đã bỏ dấu), không giúp phân biệt đoạn bài
STOPWORDS = set("""
la cua va co khong thi ma nao gi sao the nay kia do day nhe a oi minh ban em anh chi
duoc cho voi trong tren duoi khi neu vi nen de mot cac nhung nhieu it hon rat qua lam
hoi giai thich noi y doan bai video giay phut cai con o tai den tu ra vao lai roi
nghia hieu chua biet can phai muon xem gium giup toi tui ak ha hay thay
khac nhau giong cung luc vay dung sai tot nhu
""".split())
MIN_SCORE = 1.5   # tổng trọng số từ khoá chung tối thiểu để coi là đoạn khớp


def _fold(s: str) -> str:
    """Chữ thường, bỏ dấu tiếng Việt — để 'Chatbot', 'chatbot', 'chất' so khớp được khi gõ không dấu."""
    s = unicodedata.normalize("NFD", (s or "").lower()).replace("đ", "d")
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def words(s: str) -> list:
    out = []
    for w in re.findall(r"[a-z0-9\-]+", _fold(s)):
        out += [w] + (w.split("-") if "-" in w else [])   # 'chain-of-thought' khớp cả 'chain of thought'
    return [w for w in out if len(w) > 1 and w not in STOPWORDS]


def _load():
    path = LESSON_FILE if os.path.exists(LESSON_FILE) else SAMPLE_FILE
    if not os.path.exists(path):
        print("⚠️ Chưa có data/lesson/segments.json — find_segments sẽ luôn trả rỗng.", file=sys.stderr)
        return [], ""
    with open(path, encoding="utf-8-sig") as f:
        data = json.load(f)
    if isinstance(data, dict):           # chấp nhận cả {"segments": [...]}
        data = data.get("segments", [])
    segs = [s for s in data if isinstance(s, dict) and s.get("segment_id") and s.get("content")]
    if path == SAMPLE_FILE:
        print("⚠️ Đang dùng data/lesson/segments.sample.json (bản nháp synthetic) — chờ Hải nạp segments.json.",
              file=sys.stderr)
    return segs, os.path.basename(path)


SEGMENTS, SOURCE_FILE = _load()
BY_ID = {s["segment_id"]: s for s in SEGMENTS}
_DF = {}
for _s in SEGMENTS:
    for _w in set(words(_s["content"])):
        _DF[_w] = _DF.get(_w, 0) + 1
IDF = {w: math.log((len(SEGMENTS) + 1) / df) for w, df in _DF.items()}   # từ hiếm thì nặng hơn


def fmt_time(sec) -> str:
    sec = int(sec or 0)
    return "%02d:%02d" % (sec // 60, sec % 60)


def moc(seg: dict) -> str:
    """Mốc hiển thị cho học viên bấm: 'd01-r1-v01 @ 01:15–02:40'."""
    return "%s @ %s–%s" % (seg.get("video_id", "?"), fmt_time(seg.get("start_s")), fmt_time(seg.get("end_s")))


def _view(seg: dict, score: float) -> dict:
    return {"segment_id": seg["segment_id"], "video_id": seg.get("video_id", ""),
            "start_s": seg.get("start_s"), "end_s": seg.get("end_s"),
            "moc": moc(seg), "content": seg["content"], "score": round(score, 2)}


@tool
def find_segments(query: str, video_id: str = "", k: int = 3) -> list:
    """find_segments — tìm đoạn bài pre-class khớp câu hỏi.
    Input: query (str) câu hỏi · video_id (str, tuỳ chọn) video học viên đang xem · k (int) số đoạn tối đa.
    Output: danh sách ≤k đoạn {"segment_id", "video_id", "start_s", "end_s", "moc", "content", "score"},
            xếp theo điểm giảm dần. Điểm = tổng trọng số (idf) của từ khoá chung, +1 nếu cùng video đang xem.
            Rỗng nếu không đoạn nào đạt MIN_SCORE.
    Tác động ra ngoài: không (chỉ đọc data/lesson/segments.json)."""
    q = set(words(query))
    out = []
    for seg in SEGMENTS:
        common = q & set(words(seg["content"]))
        score = sum(IDF.get(w, 0) for w in common)
        if video_id and seg.get("video_id") == video_id and common:
            score += 1.0
        if score >= MIN_SCORE:
            out.append(_view(seg, score))
    out.sort(key=lambda s: -s["score"])
    if SOURCE_FILE != "segments.json":
        note("find_segments đọc %s (chưa có segments.json)" % (SOURCE_FILE or "— không có file nào"))
    return out[:k]


def segments_of_video(video_id: str) -> list:
    """Mọi đoạn của một video (không phải công cụ cho model — luồng dùng khi câu hỏi viết tắt / không có từ khoá khớp)."""
    return [_view(s, 0) for s in SEGMENTS if s.get("video_id") == video_id]