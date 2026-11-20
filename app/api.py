"""hh-api: HTTP-сервис над выгрузкой вакансий hh.ru.

GET  /health              состояние сервиса и Redis
GET  /stats               сколько вакансий загружено, счётчик визитов (нужен Redis)
GET  /vacancies?skill=go  число вакансий и медианная зарплата по навыку
GET  /favorites           избранные вакансии (SQLite)
POST /favorites?id=123    добавить вакансию в избранное

Настройки берутся из переменных окружения, см. app/settings.py.
"""
import json
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from app import settings
from app.data import ensure_dir, load_vacancies, median

VACANCIES = []
REDIS = None

# Внесли этот коментарий ради экспиримента с докером


def connect_redis():
    """Redis нужен только для счётчика визитов. Если REDIS_HOST не задан, работаем без него."""
    if not settings.REDIS_HOST:
        return None
    import redis
    client = redis.Redis(host=settings.REDIS_HOST, port=6379, password=settings.REDIS_PASSWORD or None,
                         socket_connect_timeout=1, socket_timeout=1)
    client.ping()   # одна попытка: если Redis ещё не поднялся, сервис падает
    return client


def db():
    ensure_dir(settings.DB_PATH)
    conn = sqlite3.connect(settings.DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS favorites (id INTEGER PRIMARY KEY)")
    return conn


def redis_state():
    if REDIS is None:
        return "off"
    try:
        REDIS.ping()
        return "ok"
    except Exception:
        return "error"


class Handler(BaseHTTPRequestHandler):
    def reply(self, code, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        url = urlparse(self.path)
        query = parse_qs(url.query)
        if url.path == "/health":
            return self.reply(200, {"status": "ok", "version": settings.VERSION, "redis": redis_state()})
        if url.path == "/stats":
            visits = REDIS.incr("hh:visits") if REDIS is not None else None
            return self.reply(200, {"file": settings.DATA_FILE, "vacancies": len(VACANCIES), "visits": visits})
        if url.path == "/vacancies":
            skill = query.get("skill", [""])[0].lower()
            salaries = [v["salary"] for v in VACANCIES if v["skill"] == skill]
            return self.reply(200, {"skill": skill, "count": len(salaries),
                                    "median_salary": median(salaries) if salaries else None})
        if url.path == "/favorites":
            with db() as conn:
                ids = [r[0] for r in conn.execute("SELECT id FROM favorites ORDER BY id")]
            return self.reply(200, {"favorites": ids})
        self.reply(404, {"error": "not found"})

    def do_POST(self):
        url = urlparse(self.path)
        if url.path != "/favorites":
            return self.reply(404, {"error": "not found"})
        try:
            vid = int(parse_qs(url.query)["id"][0])
        except (KeyError, ValueError):
            return self.reply(400, {"error": "нужен параметр id=<число>"})
        with db() as conn:
            conn.execute("INSERT OR IGNORE INTO favorites (id) VALUES (?)", (vid,))
            ids = [r[0] for r in conn.execute("SELECT id FROM favorites ORDER BY id")]
        self.reply(201, {"favorites": ids})


def main():
    global VACANCIES, REDIS
    VACANCIES = load_vacancies(settings.DATA_FILE)
    db().close()
    try:
        REDIS = connect_redis()
    except Exception as e:
        print(f"hh-api: Redis {settings.REDIS_HOST} недоступен: {e}", flush=True)
        sys.exit(1)
    server = ThreadingHTTPServer((settings.HOST, settings.PORT), Handler)
    print(f"hh-api {settings.VERSION}: {len(VACANCIES)} вакансий, слушаю {settings.HOST}:{settings.PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
