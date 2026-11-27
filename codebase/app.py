"""Giao diện web demo cục bộ (và chế độ CLI `--cli`) cho bản chạy thử — nhóm Siuu.

Chạy bằng: python run.py   (mặc định mở web demo tại http://127.0.0.1:8765)
Chạy dòng lệnh cũ: python codebase/app.py --cli
Chỉ dùng thư viện chuẩn Python; gọi trực tiếp answer(text) trong codebase/agent.py.
"""
import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import re
import sys
import threading
import time
import webbrowser

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

CODEBASE_DIR = os.path.dirname(os.path.abspath(__file__))
if CODEBASE_DIR not in sys.path:
    sys.path.insert(0, CODEBASE_DIR)

UI_PATH = os.path.join(CODEBASE_DIR, "ui.html")
CODE_RE = re.compile(r"d\d{2}-r\d+-v\d+#S\d+", re.I)
TRACE_LOCK = threading.Lock()


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    base = os.path.dirname(CODEBASE_DIR)
    return os.path.relpath(p, base).replace(os.sep, "/") if p.startswith(base) else path


def load_runtime():
    """Nạp các module codebase dùng chung cho cả web và CLI."""
    import ai
    import tools
    import tracing
    from agent import answer
    return ai, tools, tracing, answer


def extract_cited_segments(output: str, by_id: dict) -> list:
    """Trích các mã đoạn hợp lệ xuất hiện trong output theo thứ tự xuất hiện."""
    lower_map = {k.lower(): v for k, v in by_id.items()}
    seen = set()
    cited = []
    for raw_code in CODE_RE.findall(output or ""):
        seg = by_id.get(raw_code) or lower_map.get(raw_code.lower())
        if not seg:
            continue
        sid = seg["segment_id"]
        if sid in seen:
            continue
        seen.add(sid)
        cited.append({
            "segment_id": sid,
            "video_id": seg.get("video_id", ""),
            "start_s": seg.get("start_s", 0),
            "end_s": seg.get("end_s", 0),
            "moc": tools_moc(seg),
            "content": seg.get("content", ""),
        })
    return cited


def tools_moc(seg: dict) -> str:
    s0 = int(seg.get("start_s") or 0)
    s1 = int(seg.get("end_s") or 0)
    return "%s @ %02d:%02d–%02d:%02d" % (seg.get("video_id", "?"), s0 // 60, s0 % 60, s1 // 60, s1 % 60)


def run_cli() -> int:
    try:
        _, _, tracing, answer = load_runtime()
    except Exception as e:
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1
    print("Bản chạy thử (CLI) — gõ đầu vào rồi Enter. Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống).")
    blank = 0
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0
        with TRACE_LOCK:
            tracing.begin("app")
            try:
                result = answer(text)
            except NotImplementedError as e:
                tracing.end()
                print("Chưa nối model: %s" % e)
                return 1
            except Exception as e:
                tracing.end()
                print("[lỗi] %s: %s" % (type(e).__name__, e))
                continue
            s, _ = tracing.end()
        print(result.get("output", "") if isinstance(result, dict) else result)
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(s["models"]) or "—", s["model_calls"], s["tool_calls"], s["tokens_in"], s["tokens_out"]))


def make_handler(ai, tools, tracing, answer):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, format, *args):
            return  # giữ terminal gọn cho người dùng khi demo

        def _send_json(self, code: int, payload: dict):
            raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)

        def _send_html(self, code: int, html_bytes: bytes):
            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(html_bytes)))
            self.end_headers()
            self.wfile.write(html_bytes)

        def do_GET(self):
            path = self.path.split("?", 1)[0]
            if path == "/favicon.ico":
                self.send_response(204)
                self.end_headers()
                return
            if path in ("/", "/index.html"):
                try:
                    with open(UI_PATH, "rb") as f:
                        return self._send_html(200, f.read())
                except OSError as e:
                    return self._send_json(500, {"error": "Không đọc được codebase/ui.html: %s" % e})

            if path == "/api/segments":
                videos = list(dict.fromkeys(s.get("video_id", "") for s in tools.SEGMENTS if s.get("video_id")))
                segs = [
                    {
                        "segment_id": s["segment_id"],
                        "video_id": s.get("video_id", ""),
                        "start_s": s.get("start_s", 0),
                        "end_s": s.get("end_s", 0),
                        "moc": tools_moc(s),
                        "content": s.get("content", ""),
                        "label": s.get("label", ""),
                    }
                    for s in tools.SEGMENTS
                ]
                return self._send_json(200, {
                    "source_file": tools.SOURCE_FILE,
                    "model_provider": ai.MODEL_PROVIDER,
                    "model_name": ai.MODEL_NAME,
                    "videos": videos,
                    "segments": segs,
                })

            return self._send_json(404, {"error": "Không tìm thấy đường dẫn: " + path})

        def do_POST(self):
            path = self.path.split("?", 1)[0]
            if path != "/api/ask":
                return self._send_json(404, {"error": "Không tìm thấy đường dẫn: " + path})
            try:
                length = int(self.headers.get("Content-Length") or 0)
            except ValueError:
                return self._send_json(400, {"error": "Content-Length không hợp lệ"})
            raw_body = self.rfile.read(min(length, 1024 * 64))
            try:
                body = json.loads(raw_body.decode("utf-8"))
            except (UnicodeDecodeError, ValueError):
                return self._send_json(400, {"error": "JSON đầu vào không hợp lệ"})
            if not isinstance(body, dict):
                return self._send_json(400, {"error": "Đầu vào phải là đối tượng JSON"})

            question = str(body.get("question") or "").strip()
            video_id = str(body.get("video_id") or "").strip()
            if not question:
                return self._send_json(400, {"error": "Vui lòng nhập câu hỏi"})

            full_input = "[video %s] %s" % (video_id, question) if (video_id and not question.startswith("[")) else question

            with TRACE_LOCK:
                t0 = time.perf_counter()
                tracing.begin("app")
                try:
                    res = answer(full_input)
                except Exception as e:
                    tracing.end()
                    return self._send_json(500, {"error": "%s: %s" % (type(e).__name__, e)})
                summary, events = tracing.end()
                latency_s = round(time.perf_counter() - t0, 3)

            output = res.get("output", "") if isinstance(res, dict) else str(res)
            summary["latency_s"] = latency_s
            cited = extract_cited_segments(output, tools.BY_ID)
            return self._send_json(200, {
                "input": full_input,
                "output": output,
                "cited_segments": cited,
                "stats": summary,
                "latency_s": latency_s,
                "trace": events,
            })

    return Handler


def start_server(port: int, open_browser: bool = True):
    ai, tools, tracing, answer = load_runtime()
    handler = make_handler(ai, tools, tracing, answer)
    server = None
    chosen_port = port
    for p in range(port, port + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", p), handler)
            chosen_port = p
            break
        except OSError:
            continue
    if server is None:
        raise OSError("Không mở được cổng nào trong dải %d–%d" % (port, port + 19))

    url = "http://127.0.0.1:%d" % chosen_port
    print("Đang mở giao diện demo tại: %s" % url)
    print("Model: %s (%s) · Dữ liệu: %s (%d đoạn)"
          % (ai.MODEL_NAME or "fake", ai.MODEL_PROVIDER, tools.SOURCE_FILE or "—", len(tools.SEGMENTS)))
    print("Nhấn Ctrl+C để dừng (hoặc chạy `python codebase/app.py --cli` cho chế độ dòng lệnh).")
    sys.stdout.flush()
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    return server, url


def run_web(port: int, open_browser: bool) -> int:
    try:
        server, _ = start_server(port, open_browser=open_browser)
    except Exception as e:
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return 1
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng giao diện demo.")
    finally:
        server.server_close()
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Bản chạy thử Pre-class AI Tutor — Nhóm Siuu")
    parser.add_argument("--cli", action="store_true", help="Chạy ở chế độ dòng lệnh thay cho giao diện web")
    parser.add_argument("--port", type=int, default=8765, help="Cổng web cục bộ (mặc định 8765)")
    parser.add_argument("--no-browser", action="store_true", help="Không tự mở trình duyệt")
    args = parser.parse_args(argv)
    if args.cli:
        return run_cli()
    return run_web(args.port, open_browser=not args.no_browser)


if __name__ == "__main__":
    sys.exit(main())
