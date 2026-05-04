from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        payload = {
            "ok": True,
            "telegram_token": bool(os.getenv("TELEGRAM_BOT_TOKEN", "").strip()),
            "target_chat_id": os.getenv("TARGET_CHAT_ID", "-1003643946438"),
            "state": "redis" if (os.getenv("KV_URL") or os.getenv("REDIS_URL")) else "sqlite",
        }
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

