#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import json
import os
import re
import sqlite3
import sys
import time
import unicodedata
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable
from zoneinfo import ZoneInfo

import requests


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


MLB_API = "https://statsapi.mlb.com/api/v1"
TG_API = "https://api.telegram.org"

MONTHS_RU = {
    1: "января",
    2: "февраля",
    3: "марта",
    4: "апреля",
    5: "мая",
    6: "июня",
    7: "июля",
    8: "августа",
    9: "сентября",
    10: "октября",
    11: "ноября",
    12: "декабря",
}

TEAM_RU_BY_ABBR = {
    "ARI": "Даймондбэкс",
    "ATH": "Атлетикс",
    "ATL": "Брэйвз",
    "BAL": "Ориолс",
    "BOS": "Ред Сокс",
    "CHC": "Кабс",
    "CIN": "Редс",
    "CLE": "Гардианс",
    "COL": "Рокиз",
    "CWS": "Уайт Сокс",
    "DET": "Тайгерс",
    "HOU": "Астрос",
    "KC": "Роялс",
    "LAA": "Энджелс",
    "LAD": "Доджерс",
    "MIA": "Марлинс",
    "MIL": "Брюэрс",
    "MIN": "Твинс",
    "NYM": "Метс",
    "NYY": "Янкис",
    "OAK": "Атлетикс",
    "PHI": "Филлис",
    "PIT": "Пайрэтс",
    "SD": "Падрес",
    "SEA": "Маринерс",
    "SF": "Джайентс",
    "STL": "Кардиналс",
    "TB": "Рейс",
    "TEX": "Рейнджерс",
    "TOR": "Блю Джейс",
    "WSH": "Нэшионалс",
}

TEAM_RU_BY_NAME = {
    "Arizona Diamondbacks": "Даймондбэкс",
    "Athletics": "Атлетикс",
    "Atlanta Braves": "Брэйвз",
    "Baltimore Orioles": "Ориолс",
    "Boston Red Sox": "Ред Сокс",
    "Chicago Cubs": "Кабс",
    "Chicago White Sox": "Уайт Сокс",
    "Cincinnati Reds": "Редс",
    "Cleveland Guardians": "Гардианс",
    "Colorado Rockies": "Рокиз",
    "Detroit Tigers": "Тайгерс",
    "Houston Astros": "Астрос",
    "Kansas City Royals": "Роялс",
    "Los Angeles Angels": "Энджелс",
    "Los Angeles Dodgers": "Доджерс",
    "Miami Marlins": "Марлинс",
    "Milwaukee Brewers": "Брюэрс",
    "Minnesota Twins": "Твинс",
    "New York Mets": "Метс",
    "New York Yankees": "Янкис",
    "Oakland Athletics": "Атлетикс",
    "Philadelphia Phillies": "Филлис",
    "Pittsburgh Pirates": "Пайрэтс",
    "San Diego Padres": "Падрес",
    "San Francisco Giants": "Джайентс",
    "Seattle Mariners": "Маринерс",
    "St. Louis Cardinals": "Кардиналс",
    "Tampa Bay Rays": "Рейс",
    "Texas Rangers": "Рейнджерс",
    "Toronto Blue Jays": "Блю Джейс",
    "Washington Nationals": "Нэшионалс",
}

# Seeded from the requested example. The bot can learn/override more with /fix.
PLAYER_RU_DEFAULTS = {
    "Aaron Bummer": "Аарон Баммер",
    "Aaron Civale": "Аарон Сивале",
    "Aaron Judge": "Аарон Джадж",
    "Adrian Del Castillo": "Адриан дель Кастийо",
    "Andrew Morris": "Эндрю Моррис",
    "Ben Rice": "Бен Райс",
    "Brant Hurter": "Брэнт Хёртер",
    "Brian Abreu": "Брайан Абреу",
    "Bryson Stott": "Брайсон Стотт",
    "Caleb Kilian": "Калеб Килиан",
    "Chase DeLauter": "Чейз Делотер",
    "Chris Bubic": "Крис Бубич",
    "Chris Paddack": "Крис Пэддак",
    "Clay Holmes": "Клей Холмс",
    "Colby Thomas": "Колби Томас",
    "Daniel Lynch": "Дэниел Линч",
    "Derek Hill": "Дерек Хилл",
    "Drew Romo": "Дрю Ромо",
    "Dustin May": "Дастин Мэй",
    "Esteury Ruiz": "Эстеури Руис",
    "Fernando Cruz": "Фернандо Круз",
    "Gabriel Moreno": "Габриэль Морено",
    "Grant Wolfram": "Грант Вулфрэм",
    "Gregory Soto": "Грегори Сото",
    "Ian Seymour": "Иэн Сеймур",
    "Jack Kochanowicz": "Джек Кохановиц",
    "Jack Leiter": "Джек Лайтер",
    "Jarren Duran": "Джаррен Дюран",
    "Jason Adam": "Джейсон Адам",
    "Jason Dominguez": "Джейсон Домингес",
    "Jasson Domínguez": "Джейсон Домингес",
    "Jesús Luzardo": "Хесус Лусардо",
    "Jesus Luzardo": "Хесус Лусардо",
    "Jonah Heim": "Джона Хайм",
    "Jorge Mateo": "Хорхе Матео",
    "Justin Topa": "Джастин Топа",
    "Justin Wrobleski": "Джастин Вроблески",
    "Kazuma Okamoto": "Кадзума Окамото",
    "Kris Bubic": "Крис Бубич",
    "Kyle Freeland": "Кайл Фриленд",
    "Logan Henderson": "Логан Хендерсон",
    "Luis Castillo": "Луис Кастийо",
    "Manny Machado": "Мэнни Мачадо",
    "Mark Vientos": "Марк Виентос",
    "Mason Miller": "Мейсон Миллер",
    "Matthew Boyd": "Мэттью Бойд",
    "Merrill Kelly": "Меррилл Келли",
    "Mickey Moniak": "Микки Мониак",
    "Miguel Andujar": "Мигель Андухар",
    "Miguel Andújar": "Мигель Андухар",
    "Moises Ballesteros": "Мойсес Байестерос",
    "Moisés Ballesteros": "Мойсес Байестерос",
    "Parker Messick": "Паркер Мессик",
    "Richard Lovelady": "Ричард Лавледи",
    "Spencer Torkelson": "Спенсер Торкелсон",
    "Tanner Scott": "Таннер Скотт",
    "T.J. Rumfield": "Ти Джей Рамфилд",
    "TJ Rumfield": "Ти Джей Рамфилд",
    "Tony Santillan": "Тони Сантийян",
    "Trey Yesavage": "Трей Йесаведж",
    "Tyler Davis": "Тайлер Дэвис",
    "Tyler Soderstrom": "Тайлер Содерстром",
    "Tyler Soderström": "Тайлер Содерстром",
    "Zack Gelof": "Зак Гелоф",
    "Zack Kelly": "Зак Келли",
}

WORD_RU = {
    "aaron": "Аарон",
    "adam": "Адам",
    "adrian": "Адриан",
    "alejandro": "Алехандро",
    "andrew": "Эндрю",
    "anthony": "Энтони",
    "austin": "Остин",
    "ben": "Бен",
    "brandon": "Брэндон",
    "brant": "Брэнт",
    "brian": "Брайан",
    "bryan": "Брайан",
    "bryce": "Брайс",
    "caleb": "Калеб",
    "carlos": "Карлос",
    "chris": "Крис",
    "christopher": "Кристофер",
    "clay": "Клей",
    "daniel": "Дэниел",
    "david": "Дэвид",
    "derek": "Дерек",
    "dominguez": "Домингес",
    "dylan": "Дилан",
    "fernando": "Фернандо",
    "francisco": "Франсиско",
    "gabriel": "Габриэль",
    "george": "Джордж",
    "gregory": "Грегори",
    "ian": "Иэн",
    "jack": "Джек",
    "jake": "Джейк",
    "jarren": "Джаррен",
    "jason": "Джейсон",
    "jasson": "Джейсон",
    "jesus": "Хесус",
    "josh": "Джош",
    "juan": "Хуан",
    "justin": "Джастин",
    "kyle": "Кайл",
    "logan": "Логан",
    "luis": "Луис",
    "manny": "Мэнни",
    "marcus": "Маркус",
    "mark": "Марк",
    "mason": "Мейсон",
    "matt": "Мэтт",
    "matthew": "Мэттью",
    "max": "Макс",
    "michael": "Майкл",
    "miguel": "Мигель",
    "nick": "Ник",
    "nolan": "Нолан",
    "parker": "Паркер",
    "paul": "Пол",
    "pete": "Пит",
    "richard": "Ричард",
    "robert": "Роберт",
    "ryan": "Райан",
    "sam": "Сэм",
    "sean": "Шон",
    "spencer": "Спенсер",
    "tanner": "Таннер",
    "tony": "Тони",
    "trey": "Трей",
    "tyler": "Тайлер",
    "will": "Уилл",
    "william": "Уильям",
    "zack": "Зак",
    "zac": "Зак",
    "zach": "Зак",
}


def env_str(name: str, default: str = "") -> str:
    value = os.getenv(name)
    return default if value is None else value.strip()


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or not value.strip():
        return default
    try:
        return int(value.strip())
    except ValueError:
        return default


def parse_chat_ids(raw: str) -> set[int]:
    out: set[int] = set()
    for part in re.split(r"[,\s]+", raw.strip()):
        if not part:
            continue
        try:
            out.add(int(part))
        except ValueError:
            continue
    return out


def remove_accents(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def norm_key(value: str) -> str:
    value = remove_accents(value or "").casefold()
    value = re.sub(r"[^a-zа-яё0-9]+", " ", value, flags=re.I)
    return re.sub(r"\s+", " ", value).strip()


def clean_player_source(name: str) -> str:
    name = re.sub(r"\s+", " ", (name or "").strip())
    return re.sub(r"\s+(Jr\.?|Sr\.?|II|III|IV|V)$", "", name, flags=re.I).strip()


def ru_date(d: date) -> str:
    return f"{d.day} {MONTHS_RU[d.month]}"


def int_or_zero(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def load_dotenv(path: Path = Path(".env")) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


class Store:
    def __init__(self, db_path: str):
        self.path = Path(db_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.conn = sqlite3.connect(self.path)
        self.conn.row_factory = sqlite3.Row
        self.init()

    def init(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS translations (
                kind TEXT NOT NULL,
                source TEXT NOT NULL,
                source_norm TEXT NOT NULL,
                target TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                PRIMARY KEY (kind, source_norm)
            );

            CREATE TABLE IF NOT EXISTS posts (
                game_date TEXT PRIMARY KEY,
                chat_id TEXT NOT NULL,
                message_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                posted_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS meta (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            );
            """
        )
        self.conn.commit()

    def close(self) -> None:
        self.conn.close()

    def get_meta(self, key: str, default: str = "") -> str:
        row = self.conn.execute("SELECT value FROM meta WHERE key = ?", (key,)).fetchone()
        return str(row["value"]) if row else default

    def set_meta(self, key: str, value: str) -> None:
        self.conn.execute(
            "INSERT INTO meta(key, value) VALUES(?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, value),
        )
        self.conn.commit()

    def put_translation(self, kind: str, source: str, target: str) -> None:
        self.conn.execute(
            """
            INSERT INTO translations(kind, source, source_norm, target, updated_at)
            VALUES(?, ?, ?, ?, ?)
            ON CONFLICT(kind, source_norm) DO UPDATE SET
                source = excluded.source,
                target = excluded.target,
                updated_at = excluded.updated_at
            """,
            (kind, source.strip(), norm_key(source), target.strip(), datetime.now(timezone.utc).isoformat()),
        )
        self.conn.commit()

    def get_translation(self, kind: str, source: str) -> str | None:
        keys = [kind]
        if kind != "any":
            keys.append("any")
        for k in keys:
            row = self.conn.execute(
                "SELECT target FROM translations WHERE kind = ? AND source_norm = ?",
                (k, norm_key(source)),
            ).fetchone()
            if row:
                return str(row["target"])
        return None

    def list_translations(self, query: str = "", limit: int = 30) -> list[sqlite3.Row]:
        if query:
            like = f"%{norm_key(query)}%"
            return list(
                self.conn.execute(
                    """
                    SELECT kind, source, target, updated_at
                    FROM translations
                    WHERE source_norm LIKE ? OR lower(target) LIKE lower(?)
                    ORDER BY updated_at DESC
                    LIMIT ?
                    """,
                    (like, f"%{query}%", limit),
                )
            )
        return list(
            self.conn.execute(
                """
                SELECT kind, source, target, updated_at
                FROM translations
                ORDER BY updated_at DESC
                LIMIT ?
                """,
                (limit,),
            )
        )

    def save_post(self, game_date: date, chat_id: int | str, message_id: int, text: str) -> None:
        now = datetime.now(timezone.utc).isoformat()
        self.conn.execute(
            """
            INSERT INTO posts(game_date, chat_id, message_id, text, posted_at, updated_at)
            VALUES(?, ?, ?, ?, ?, ?)
            ON CONFLICT(game_date) DO UPDATE SET
                chat_id = excluded.chat_id,
                message_id = excluded.message_id,
                text = excluded.text,
                updated_at = excluded.updated_at
            """,
            (game_date.isoformat(), str(chat_id), message_id, text, now, now),
        )
        self.conn.commit()

    def get_post(self, game_date: date) -> sqlite3.Row | None:
        return self.conn.execute("SELECT * FROM posts WHERE game_date = ?", (game_date.isoformat(),)).fetchone()

    def latest_post(self) -> sqlite3.Row | None:
        return self.conn.execute("SELECT * FROM posts ORDER BY game_date DESC LIMIT 1").fetchone()

    def update_post_text(self, game_date: date, text: str) -> None:
        self.conn.execute(
            "UPDATE posts SET text = ?, updated_at = ? WHERE game_date = ?",
            (text, datetime.now(timezone.utc).isoformat(), game_date.isoformat()),
        )
        self.conn.commit()


class MlbClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "MLB Daily Results Telegram Bot/1.0",
                "Accept": "application/json",
            }
        )
        self._pitcher_logs: dict[tuple[int, int], list[dict[str, Any]]] = {}

    def get_json(self, url: str, tries: int = 3, timeout: int = 30) -> Any:
        last_error: Exception | None = None
        for attempt in range(tries):
            try:
                response = self.session.get(url, timeout=timeout)
                response.raise_for_status()
                return response.json()
            except Exception as exc:
                last_error = exc
                if attempt + 1 < tries:
                    time.sleep(0.75 * (2**attempt))
        raise RuntimeError(f"GET failed: {url}: {last_error}") from last_error

    def schedule(self, d: date) -> dict[str, Any]:
        url = (
            f"{MLB_API}/schedule?sportId=1&date={d.isoformat()}"
            "&hydrate=team,linescore,decisions,homeRuns"
        )
        return self.get_json(url)

    def games(self, d: date) -> list[dict[str, Any]]:
        data = self.schedule(d)
        dates = data.get("dates") or []
        if not dates:
            return []
        return list(dates[0].get("games") or [])

    def pitcher_game_log(self, player_id: int, season: int) -> list[dict[str, Any]]:
        key = (player_id, season)
        if key in self._pitcher_logs:
            return self._pitcher_logs[key]
        url = f"{MLB_API}/people/{player_id}/stats?stats=gameLog&group=pitching&season={season}"
        data = self.get_json(url)
        splits = []
        for group in data.get("stats") or []:
            splits.extend(group.get("splits") or [])
        self._pitcher_logs[key] = splits
        return splits

    def pitcher_record_through(self, player_id: int, season: int, through_date: date) -> tuple[int, int, int] | None:
        try:
            splits = self.pitcher_game_log(player_id, season)
        except Exception:
            return None
        wins = losses = saves = 0
        for split in splits:
            raw_date = split.get("date")
            if not raw_date:
                continue
            try:
                split_date = date.fromisoformat(str(raw_date)[:10])
            except ValueError:
                continue
            if split_date > through_date:
                continue
            stat = split.get("stat") or {}
            wins += int_or_zero(stat.get("wins"))
            losses += int_or_zero(stat.get("losses"))
            saves += int_or_zero(stat.get("saves"))
        return wins, losses, saves


class Translator:
    def __init__(self, store: Store):
        self.store = store
        self.default_players = {norm_key(k): v for k, v in PLAYER_RU_DEFAULTS.items()}
        self.default_teams = {norm_key(k): v for k, v in TEAM_RU_BY_NAME.items()}
        self.default_teams.update({norm_key(k): v for k, v in TEAM_RU_BY_ABBR.items()})

    def team(self, team: dict[str, Any]) -> str:
        candidates = [
            str(team.get("abbreviation") or ""),
            str(team.get("teamName") or ""),
            str(team.get("clubName") or ""),
            str(team.get("name") or ""),
            str(team.get("shortName") or ""),
        ]
        for candidate in candidates:
            if not candidate:
                continue
            override = self.store.get_translation("team", candidate)
            if override:
                return override
            default = self.default_teams.get(norm_key(candidate))
            if default:
                return default
        return self.words_ru(str(team.get("teamName") or team.get("name") or "Team"))

    def player(self, name: str) -> str:
        name = re.sub(r"\s+", " ", (name or "").strip())
        if not name:
            return ""
        override = self.store.get_translation("player", name)
        if override:
            return override
        clean_name = clean_player_source(name)
        if clean_name != name:
            override = self.store.get_translation("player", clean_name)
            if override:
                return override
        default = self.default_players.get(norm_key(name))
        if default:
            return default
        default = self.default_players.get(norm_key(clean_name))
        if default:
            return default
        return self.words_ru(clean_name)

    def any_phrase(self, value: str) -> str:
        override = self.store.get_translation("any", value)
        return override if override else value

    def words_ru(self, value: str) -> str:
        tokens = re.split(r"(\s+|-|')", remove_accents(value))
        out: list[str] = []
        for token in tokens:
            if not token:
                continue
            if token.isspace() or token in {"-", "'"}:
                out.append(token)
                continue
            if "." in token and len(token.replace(".", "")) <= 3:
                letters = [LETTER_NAMES.get(ch.lower(), ch) for ch in token if ch.isalpha()]
                out.append(" ".join(letters))
                continue
            mapped = WORD_RU.get(token.casefold())
            out.append(mapped if mapped else transliterate_word(token))
        return re.sub(r"\s+", " ", "".join(out)).strip()


LETTER_NAMES = {
    "a": "Эй",
    "b": "Би",
    "c": "Си",
    "d": "Ди",
    "e": "И",
    "f": "Эф",
    "g": "Джи",
    "h": "Эйч",
    "i": "Ай",
    "j": "Джей",
    "k": "Кей",
    "l": "Эл",
    "m": "Эм",
    "n": "Эн",
    "o": "Оу",
    "p": "Пи",
    "q": "Кью",
    "r": "Ар",
    "s": "Эс",
    "t": "Ти",
    "u": "Ю",
    "v": "Ви",
    "w": "Дабл-ю",
    "x": "Экс",
    "y": "Уай",
    "z": "Зи",
}


def transliterate_word(word: str) -> str:
    src = remove_accents(word).lower()
    replacements = [
        ("sch", "ш"),
        ("tch", "ч"),
        ("ch", "ч"),
        ("sh", "ш"),
        ("ph", "ф"),
        ("th", "т"),
        ("ck", "к"),
        ("qu", "кв"),
        ("ee", "и"),
        ("oo", "у"),
        ("ai", "эй"),
        ("ay", "эй"),
        ("ei", "ей"),
        ("ey", "ей"),
        ("ea", "и"),
        ("ou", "ау"),
        ("ow", "оу"),
        ("au", "о"),
        ("ie", "и"),
        ("ia", "иа"),
        ("io", "ио"),
        ("ll", "лл"),
    ]
    out = ""
    i = 0
    while i < len(src):
        matched = False
        for latin, cyr in replacements:
            if src.startswith(latin, i):
                out += cyr
                i += len(latin)
                matched = True
                break
        if matched:
            continue
        ch = src[i]
        out += {
            "a": "а",
            "b": "б",
            "c": "к",
            "d": "д",
            "e": "е",
            "f": "ф",
            "g": "г",
            "h": "х",
            "i": "и",
            "j": "дж",
            "k": "к",
            "l": "л",
            "m": "м",
            "n": "н",
            "o": "о",
            "p": "п",
            "q": "к",
            "r": "р",
            "s": "с",
            "t": "т",
            "u": "у",
            "v": "в",
            "w": "в",
            "x": "кс",
            "y": "и" if i else "й",
            "z": "з",
        }.get(ch, ch)
        i += 1
    if not out:
        return word
    return out[:1].upper() + out[1:]


@dataclass(frozen=True)
class Config:
    token: str
    target_chat_id: int
    admin_chat_ids: set[int]
    state_db: str
    local_tz: ZoneInfo
    mlb_tz: ZoneInfo
    auto_post: bool
    auto_check_seconds: int
    auto_lookback_days: int
    team_emoji: str
    dry_run: bool

    @classmethod
    def from_env(cls) -> "Config":
        target_chat_id = int(env_str("TARGET_CHAT_ID", "-1003643946438"))
        admin_chat_ids = parse_chat_ids(env_str("ADMIN_CHAT_IDS", ""))
        if not admin_chat_ids:
            admin_chat_ids.add(target_chat_id)
        return cls(
            token=env_str("TELEGRAM_BOT_TOKEN"),
            target_chat_id=target_chat_id,
            admin_chat_ids=admin_chat_ids,
            state_db=env_str("STATE_DB", "state/mlb_daily_results.db"),
            local_tz=ZoneInfo(env_str("LOCAL_TZ", "Europe/Moscow")),
            mlb_tz=ZoneInfo(env_str("MLB_TZ", "America/New_York")),
            auto_post=env_bool("AUTO_POST", True),
            auto_check_seconds=env_int("AUTO_CHECK_SECONDS", 300),
            auto_lookback_days=env_int("AUTO_LOOKBACK_DAYS", 2),
            team_emoji=env_str("TEAM_EMOJI", "😀") or "😀",
            dry_run=env_bool("DRY_RUN", False),
        )


class Formatter:
    def __init__(self, client: MlbClient, translator: Translator, config: Config):
        self.client = client
        self.tr = translator
        self.cfg = config

    def build_results(self, d: date, include_pending: bool = True) -> str:
        games = self.client.games(d)
        header = f"⚾️ МЛБ • {self.series_title(games)} • {ru_date(d)}"
        if not games:
            return f"{header}\n\nМатчей нет."

        blocks = [header]
        for game in sorted(games, key=self.game_sort_key):
            if self.is_final_game(game):
                blocks.append(self.final_game_block(game, d))
            elif include_pending:
                blocks.append(self.pending_game_block(game))
        return "\n\n".join(block for block in blocks if block).strip()

    def build_schedule(self, d: date) -> str:
        games = self.client.games(d)
        count = len(games)
        word = plural_ru(count, "матч", "матча", "матчей")
        lines = [f"⚾️ МЛБ • Расписание • {ru_date(d)}", f"{count} {word}"]
        if not games:
            return "\n".join(lines)
        lines.append("")
        for game in sorted(games, key=self.game_sort_key):
            home = self.team_line_name(game, "home")
            away = self.team_line_name(game, "away")
            start = self.game_local_time(game)
            state = self.status_ru(game)
            suffix = state if state else start
            lines.append(f"{home} — {away} • {suffix}")
        return "\n".join(lines).strip()

    def status_summary(self, d: date, posted: bool) -> str:
        games = self.client.games(d)
        total = len(games)
        final = sum(1 for game in games if self.is_final_game(game))
        active = sum(1 for game in games if self.is_active_game(game))
        pending = max(0, total - final - active)
        ready = total > 0 and final == total
        return (
            f"MLB {d.isoformat()}\n"
            f"Всего: {total}\n"
            f"Завершено: {final}\n"
            f"В игре: {active}\n"
            f"Ожидают: {pending}\n"
            f"Готово к публикации: {'да' if ready else 'нет'}\n"
            f"Опубликовано: {'да' if posted else 'нет'}"
        )

    def unknown_players(self, d: date) -> list[tuple[str, str]]:
        games = self.client.games(d)
        names: set[str] = set()
        for game in games:
            decisions = game.get("decisions") or {}
            for key in ("winner", "loser", "save"):
                person = decisions.get(key) or {}
                if person.get("fullName"):
                    names.add(str(person["fullName"]))
            for hr in game.get("homeRuns") or []:
                batter = ((hr.get("matchup") or {}).get("batter") or {}).get("fullName")
                if batter:
                    names.add(str(batter))

        out = []
        for name in sorted(names, key=norm_key):
            if self.tr.store.get_translation("player", name):
                continue
            if norm_key(name) in self.tr.default_players:
                continue
            out.append((name, self.tr.player(name)))
        return out

    def final_game_block(self, game: dict[str, Any], d: date) -> str:
        home = self.team_score_line(game, "home")
        away = self.team_score_line(game, "away")
        decisions = self.decisions_line(game, d)
        homers = self.home_runs_line(game)
        parts = [home, away, "", decisions, homers]
        return "\n".join(part for part in parts if part is not None).strip()

    def pending_game_block(self, game: dict[str, Any]) -> str:
        home = self.team_line_name(game, "home")
        away = self.team_line_name(game, "away")
        return f"{home}: —\n{away}: —\n{self.status_ru(game) or self.game_local_time(game)}"

    def team_score_line(self, game: dict[str, Any], side: str) -> str:
        team_data = ((game.get("teams") or {}).get(side) or {})
        team = team_data.get("team") or {}
        name = self.tr.team(team)
        score = int_or_zero(team_data.get("score"))
        rec = team_data.get("leagueRecord") or {}
        record = f"{int_or_zero(rec.get('wins'))}-{int_or_zero(rec.get('losses'))}"
        return f"{self.cfg.team_emoji} {name}: {score} ({record})"

    def team_line_name(self, game: dict[str, Any], side: str) -> str:
        team = ((((game.get("teams") or {}).get(side) or {}).get("team")) or {})
        return f"{self.cfg.team_emoji} {self.tr.team(team)}"

    def decisions_line(self, game: dict[str, Any], d: date) -> str:
        decisions = game.get("decisions") or {}
        parts: list[str] = []
        winner = decisions.get("winner")
        loser = decisions.get("loser")
        save = decisions.get("save")
        if winner:
            parts.append(f"Победа: {self.pitcher_with_record(winner, game, d, 'wl')}")
        if loser:
            parts.append(f"поражение: {self.pitcher_with_record(loser, game, d, 'wl')}")
        if save:
            parts.append(f"сейв: {self.pitcher_with_record(save, game, d, 'save')}")
        return "; ".join(parts) if parts else "Победа/поражение: —"

    def pitcher_with_record(self, person: dict[str, Any], game: dict[str, Any], d: date, mode: str) -> str:
        name = self.tr.player(str(person.get("fullName") or ""))
        player_id = int_or_zero(person.get("id"))
        season = int_or_zero(game.get("season")) or d.year
        record = self.client.pitcher_record_through(player_id, season, d) if player_id else None
        if not record:
            return name
        wins, losses, saves = record
        if mode == "save":
            return f"{name} ({saves})"
        return f"{name} ({wins}-{losses})"

    def home_runs_line(self, game: dict[str, Any]) -> str:
        by_side: dict[str, dict[str, dict[str, Any]]] = {"home": {}, "away": {}}
        for hr in game.get("homeRuns") or []:
            half = str(((hr.get("about") or {}).get("halfInning") or "")).lower()
            side = "away" if half == "top" else "home"
            batter = ((hr.get("matchup") or {}).get("batter") or {})
            raw_name = str(batter.get("fullName") or "").strip()
            if not raw_name:
                continue
            key = norm_key(raw_name)
            item = by_side[side].setdefault(
                key,
                {
                    "name": self.tr.player(raw_name),
                    "count": 0,
                    "season_total": None,
                },
            )
            item["count"] += 1
            total = self.hr_total(hr)
            if total is not None:
                item["season_total"] = total

        home = self.format_hr_items(by_side["home"].values())
        away = self.format_hr_items(by_side["away"].values())
        if home and away:
            value = f"{home} — {away}"
        else:
            value = home or away or "—"
        return f"Хоум-раны: {value}"

    @staticmethod
    def format_hr_items(items: Iterable[dict[str, Any]]) -> str:
        parts: list[str] = []
        for item in items:
            count = int_or_zero(item.get("count"))
            total = item.get("season_total")
            if count > 1 and total is not None:
                parts.append(f"{item['name']} {count} ({total})")
            elif total is not None:
                parts.append(f"{item['name']} ({total})")
            else:
                parts.append(str(item["name"]))
        return ", ".join(parts)

    @staticmethod
    def hr_total(hr: dict[str, Any]) -> int | None:
        desc = str(((hr.get("result") or {}).get("description") or ""))
        match = re.search(r"homers\s+\((\d+)\)", desc, flags=re.I)
        if not match:
            return None
        return int(match.group(1))

    @staticmethod
    def series_title(games: list[dict[str, Any]]) -> str:
        game_types = {str(game.get("gameType") or "") for game in games}
        if game_types == {"R"} or not game_types:
            return "Регулярный чемпионат"
        if "P" in game_types:
            return "Плей-офф"
        if "S" in game_types:
            return "Предсезонка"
        return "Матчи"

    @staticmethod
    def game_sort_key(game: dict[str, Any]) -> tuple[str, str, int]:
        return (
            str(game.get("gameDate") or ""),
            str(((((game.get("teams") or {}).get("home") or {}).get("team") or {}).get("name")) or ""),
            int_or_zero(game.get("gamePk")),
        )

    @staticmethod
    def is_final_game(game: dict[str, Any]) -> bool:
        status = game.get("status") or {}
        return (
            str(status.get("abstractGameState") or "").lower() == "final"
            or str(status.get("statusCode") or "").upper() in {"F", "O"}
            or str(status.get("codedGameState") or "").upper() in {"F", "O"}
        )

    @staticmethod
    def is_active_game(game: dict[str, Any]) -> bool:
        status = game.get("status") or {}
        return str(status.get("abstractGameState") or "").lower() == "live"

    @staticmethod
    def is_closed_nonfinal(game: dict[str, Any]) -> bool:
        status = game.get("status") or {}
        detailed = str(status.get("detailedState") or "").lower()
        return any(word in detailed for word in ("postponed", "cancelled", "suspended"))

    def all_done(self, games: list[dict[str, Any]]) -> bool:
        return bool(games) and all(self.is_final_game(game) or self.is_closed_nonfinal(game) for game in games)

    def game_local_time(self, game: dict[str, Any]) -> str:
        raw = str(game.get("gameDate") or "")
        if not raw:
            return ""
        try:
            dt_utc = datetime.fromisoformat(raw.replace("Z", "+00:00"))
            return dt_utc.astimezone(self.cfg.local_tz).strftime("%H:%M МСК")
        except ValueError:
            return raw

    @staticmethod
    def status_ru(game: dict[str, Any]) -> str:
        status = game.get("status") or {}
        detailed = str(status.get("detailedState") or "")
        abstract = str(status.get("abstractGameState") or "")
        if abstract.lower() == "final":
            return "завершён"
        if abstract.lower() == "live":
            return "идёт"
        if detailed and detailed.lower() not in {"scheduled", "pre-game"}:
            mapping = {
                "postponed": "перенесён",
                "cancelled": "отменён",
                "suspended": "приостановлен",
                "delayed": "задержка",
            }
            low = detailed.lower()
            for key, value in mapping.items():
                if key in low:
                    return value
        return ""


class Telegram:
    def __init__(self, config: Config):
        self.cfg = config
        self.base = f"{TG_API}/bot{config.token}" if config.token else ""
        self.session = requests.Session()

    def request(self, method: str, payload: dict[str, Any]) -> Any:
        if self.cfg.dry_run:
            print(f"[DRY_RUN] Telegram {method}: {json.dumps(payload, ensure_ascii=False)}")
            if method == "sendMessage":
                return {"ok": True, "result": {"message_id": 0}}
            return {"ok": True, "result": True}
        if not self.cfg.token:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
        response = self.session.post(f"{self.base}/{method}", json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram API error: {data}")
        return data

    def send_message(self, chat_id: int | str, text: str) -> int:
        data = self.request(
            "sendMessage",
            {
                "chat_id": chat_id,
                "text": text,
                "disable_web_page_preview": True,
            },
        )
        return int_or_zero((data.get("result") or {}).get("message_id"))

    def edit_message(self, chat_id: int | str, message_id: int, text: str) -> None:
        self.request(
            "editMessageText",
            {
                "chat_id": chat_id,
                "message_id": message_id,
                "text": text,
                "disable_web_page_preview": True,
            },
        )

    def get_updates(self, offset: int | None, timeout: int = 25) -> list[dict[str, Any]]:
        payload: dict[str, Any] = {
            "timeout": timeout,
            "allowed_updates": ["message", "edited_message", "channel_post", "edited_channel_post"],
        }
        if offset is not None:
            payload["offset"] = offset
        data = self.request("getUpdates", payload)
        return list(data.get("result") or [])


class BotApp:
    def __init__(self, config: Config, store: Store, client: MlbClient, formatter: Formatter, telegram: Telegram):
        self.cfg = config
        self.store = store
        self.client = client
        self.formatter = formatter
        self.telegram = telegram
        self.next_auto_check = 0.0

    def current_game_date(self) -> date:
        now_mlb = datetime.now(self.cfg.mlb_tz)
        if now_mlb.hour < 12:
            return now_mlb.date() - timedelta(days=1)
        return now_mlb.date()

    def send_or_edit_channel_post(self, d: date, text: str) -> str:
        if len(text) > 4096:
            raise RuntimeError(f"Telegram message is too long: {len(text)} chars")
        existing = self.store.get_post(d)
        if existing:
            self.telegram.edit_message(existing["chat_id"], int(existing["message_id"]), text)
            self.store.save_post(d, existing["chat_id"], int(existing["message_id"]), text)
            return f"Обновил пост за {d.isoformat()}."
        message_id = self.telegram.send_message(self.cfg.target_chat_id, text)
        self.store.save_post(d, self.cfg.target_chat_id, message_id, text)
        return f"Опубликовал пост за {d.isoformat()}."

    def refresh_post(self, d: date) -> str:
        existing = self.store.get_post(d)
        if not existing:
            return f"За {d.isoformat()} ещё нет сохранённого поста. Используй /post {d.isoformat()}."
        text = self.formatter.build_results(d, include_pending=False)
        self.telegram.edit_message(existing["chat_id"], int(existing["message_id"]), text)
        self.store.save_post(d, existing["chat_id"], int(existing["message_id"]), text)
        return f"Перегенерировал и обновил пост за {d.isoformat()}."

    def auto_check(self) -> None:
        if not self.cfg.auto_post:
            return
        now = time.monotonic()
        if now < self.next_auto_check:
            return
        self.next_auto_check = now + max(30, self.cfg.auto_check_seconds)

        today = datetime.now(self.cfg.mlb_tz).date()
        for delta in range(self.cfg.auto_lookback_days):
            d = today - timedelta(days=delta)
            if self.store.get_post(d):
                continue
            try:
                games = self.client.games(d)
                if not self.formatter.all_done(games):
                    continue
                text = self.formatter.build_results(d, include_pending=False)
                result = self.send_or_edit_channel_post(d, text)
                print(f"[auto] {result}", flush=True)
            except Exception as exc:
                print(f"[auto] failed for {d.isoformat()}: {exc}", flush=True)

    def run_polling(self) -> None:
        if not self.cfg.token and not self.cfg.dry_run:
            raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
        offset_raw = self.store.get_meta("telegram_offset", "")
        offset = int(offset_raw) if offset_raw.isdigit() else None
        print("MLB daily results bot started", flush=True)
        while True:
            try:
                updates = self.telegram.get_updates(offset=offset, timeout=25)
                for update in updates:
                    offset = int(update["update_id"]) + 1
                    self.store.set_meta("telegram_offset", str(offset))
                    self.handle_update(update)
                self.auto_check()
            except KeyboardInterrupt:
                raise
            except Exception as exc:
                print(f"[loop] {exc}", flush=True)
                time.sleep(5)

    def handle_update(self, update: dict[str, Any]) -> None:
        message = (
            update.get("message")
            or update.get("edited_message")
            or update.get("channel_post")
            or update.get("edited_channel_post")
            or {}
        )
        chat = message.get("chat") or {}
        chat_id = chat.get("id")
        text = str(message.get("text") or "").strip()
        if chat_id is None or not text.startswith("/"):
            return
        if not self.is_allowed_chat(int(chat_id), str(chat.get("type") or "")):
            return
        try:
            answer = self.handle_command(text)
        except Exception as exc:
            answer = f"Ошибка: {exc}"
        if answer:
            self.telegram.send_message(chat_id, answer)

    def is_allowed_chat(self, chat_id: int, chat_type: str) -> bool:
        if chat_id in self.cfg.admin_chat_ids:
            return True
        # Handy for first setup: private owner chat can configure/check the bot.
        return chat_type == "private"

    def handle_command(self, raw: str) -> str:
        cmd, _, rest = raw.partition(" ")
        cmd = cmd.split("@", 1)[0].lower()
        rest = rest.strip()
        if cmd in {"/start", "/help"}:
            return HELP_TEXT
        if cmd == "/today":
            d = parse_optional_date(rest) or self.current_game_date()
            return self.formatter.build_results(d, include_pending=True)
        if cmd == "/schedule":
            d = parse_optional_date(rest) or self.current_game_date()
            return self.formatter.build_schedule(d)
        if cmd == "/status":
            d = parse_optional_date(rest) or self.current_game_date()
            return self.formatter.status_summary(d, posted=self.store.get_post(d) is not None)
        if cmd == "/post":
            d = parse_optional_date(rest) or self.current_game_date()
            text = self.formatter.build_results(d, include_pending=False)
            return self.send_or_edit_channel_post(d, text)
        if cmd == "/refresh":
            d = parse_optional_date(rest) or self.current_game_date()
            return self.refresh_post(d)
        if cmd in {"/fix", "/player", "/name"}:
            source, target = split_assignment(rest)
            self.store.put_translation("player", source, target)
            message = f"Запомнил: {source} → {target}"
            latest = self.store.latest_post()
            if latest:
                message += "\n" + self.refresh_post(date.fromisoformat(str(latest["game_date"])))
            return message
        if cmd == "/team":
            source, target = split_assignment(rest)
            self.store.put_translation("team", source, target)
            message = f"Запомнил команду: {source} → {target}"
            latest = self.store.latest_post()
            if latest:
                message += "\n" + self.refresh_post(date.fromisoformat(str(latest["game_date"])))
            return message
        if cmd == "/replace":
            source, target = split_assignment(rest)
            latest = self.store.latest_post()
            if not latest:
                return "Нет сохранённых постов для правки."
            d = date.fromisoformat(str(latest["game_date"]))
            text = str(latest["text"])
            if source not in text:
                return f"Не нашёл в последнем посте: {source}"
            text = text.replace(source, target)
            self.telegram.edit_message(latest["chat_id"], int(latest["message_id"]), text)
            self.store.update_post_text(d, text)
            return f"Заменил в посте за {d.isoformat()}: {source} → {target}"
        if cmd == "/dict":
            rows = self.store.list_translations(rest)
            if not rows:
                return "Словарь правок пока пуст."
            return "\n".join(f"{row['kind']}: {row['source']} → {row['target']}" for row in rows)
        if cmd == "/unknown":
            d = parse_optional_date(rest) or self.current_game_date()
            unknown = self.formatter.unknown_players(d)
            if not unknown:
                return "Новых имён без ручной правки не нашёл."
            lines = [f"Имена без ручной правки за {d.isoformat()}:"]
            lines.extend(f"{src} → {guess}" for src, guess in unknown[:40])
            return "\n".join(lines)
        return HELP_TEXT


HELP_TEXT = """Команды MLB-бота:
/today [YYYY-MM-DD] - показать пост результатов
/schedule [YYYY-MM-DD] - расписание и количество матчей
/status [YYYY-MM-DD] - статус игрового дня
/post [YYYY-MM-DD] - отправить/обновить пост в канале
/refresh [YYYY-MM-DD] - перегенерировать уже опубликованный пост
/fix English Name = Русское Имя - запомнить имя игрока
/team Twins = Твинс - запомнить название команды
/replace старый текст = новый текст - поправить последний пост
/dict [поиск] - показать словарь правок
/unknown [YYYY-MM-DD] - показать имена без ручной правки"""


def parse_optional_date(value: str) -> date | None:
    value = value.strip()
    if not value:
        return None
    match = re.search(r"\d{4}-\d{2}-\d{2}", value)
    if not match:
        return None
    return date.fromisoformat(match.group(0))


def split_assignment(value: str) -> tuple[str, str]:
    if "=" in value:
        left, right = value.split("=", 1)
    elif "->" in value:
        left, right = value.split("->", 1)
    elif "→" in value:
        left, right = value.split("→", 1)
    else:
        raise ValueError("Нужен формат: /fix English Name = Русское Имя")
    left = left.strip()
    right = right.strip()
    if not left or not right:
        raise ValueError("Слева и справа от '=' должен быть текст")
    return left, right


def plural_ru(n: int, one: str, few: str, many: str) -> str:
    n_abs = abs(n)
    if n_abs % 10 == 1 and n_abs % 100 != 11:
        return one
    if 2 <= n_abs % 10 <= 4 and not 12 <= n_abs % 100 <= 14:
        return few
    return many


def make_app() -> BotApp:
    load_dotenv()
    config = Config.from_env()
    store = Store(config.state_db)
    client = MlbClient()
    translator = Translator(store)
    formatter = Formatter(client, translator, config)
    telegram = Telegram(config)
    return BotApp(config, store, client, formatter, telegram)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", dest="target_date", default="")
    parser.add_argument("--schedule", action="store_true")
    parser.add_argument("--status", action="store_true")
    parser.add_argument("--post", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    if args.dry_run:
        os.environ["DRY_RUN"] = "true"

    app = make_app()
    d = date.fromisoformat(args.target_date) if args.target_date else app.current_game_date()
    try:
        if args.schedule:
            print(app.formatter.build_schedule(d))
            return 0
        if args.status:
            print(app.formatter.status_summary(d, posted=app.store.get_post(d) is not None))
            return 0
        if args.post:
            text = app.formatter.build_results(d, include_pending=False)
            print(app.send_or_edit_channel_post(d, text))
            return 0
        if args.refresh:
            print(app.refresh_post(d))
            return 0
        if args.target_date or args.dry_run:
            print(app.formatter.build_results(d, include_pending=True))
            return 0
        app.run_polling()
        return 0
    finally:
        app.store.close()


if __name__ == "__main__":
    sys.exit(main())
