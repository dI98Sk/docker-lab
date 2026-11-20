import csv
import os


def load_vacancies(path):
    with open(path, encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["salary"] = int(r["salary"])
    return rows


def median(values):
    values = sorted(values)
    mid = len(values) // 2
    return values[mid] if len(values) % 2 else (values[mid - 1] + values[mid]) / 2


def ensure_dir(path):
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
