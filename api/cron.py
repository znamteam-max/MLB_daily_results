from __future__ import annotations

import json
import os
import sys
from datetime import date
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import parse_qs, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mlb_daily_results_bot import make_app, parse_optional_date


class handler(BaseHTTPRequestHandler):
    def send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def provided_secret(self, query: dict[str, list[str]]) -> str:
        auth = self.headers.get("authorization", "")
        if auth.lower().startswith("bearer "):
            return auth[7:].strip()
        return (query.get("secret") or [""])[0].strip()

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)
        expected_secret = os.getenv("CRON_SECRET", "").strip()
        if not expected_secret:
            self.send_json(500, {"ok": False, "error": "CRON_SECRET is not set"})
            return
        if self.provided_secret(query) != expected_secret:
            self.send_json(401, {"ok": False, "error": "unauthorized"})
            return

        try:
            app = make_app()
        except Exception as exc:
            self.send_json(500, {"ok": False, "error": str(exc)})
            return
        try:
            raw_date = (query.get("date") or [""])[0]
            target_date = parse_optional_date(raw_date)
            if target_date:
                result = self.check_single_date(app, target_date)
                self.send_json(200, {"ok": True, "results": [result]})
                return
            self.send_json(200, {"ok": True, "results": app.cron_check_once()})
        except Exception as exc:
            self.send_json(500, {"ok": False, "error": str(exc)})
        finally:
            app.store.close()

    def check_single_date(self, app, target_date: date) -> str:
        if app.store.get_post(target_date):
            return f"{target_date.isoformat()}: already posted"
        games = app.client.games(target_date)
        if not app.formatter.all_done(games):
            final = sum(1 for game in games if app.formatter.is_final_game(game))
            return f"{target_date.isoformat()}: not ready ({final}/{len(games)} final)"
        text = app.formatter.build_results(target_date, include_pending=False)
        return app.send_or_edit_channel_post(target_date, text)
