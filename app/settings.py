"""Настройки hh-api. Всё задаётся переменными окружения."""
import os

VERSION = "1.0"
HOST = os.environ.get("HOST", "127.0.0.1")       # на каком адресе слушать
PORT = int(os.environ.get("PORT", "8000"))
DATA_FILE = os.environ.get("DATA_FILE", "data/vacancies.csv")
DB_PATH = os.environ.get("DB_PATH", "var/hh.db")
REDIS_HOST = os.environ.get("REDIS_HOST", "")
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "")
HH_API_TOKEN = os.environ.get("HH_API_TOKEN", "")
