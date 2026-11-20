"""Ночной пересчёт средней зарплаты по полной выгрузке data/dump_2019.csv.

    WORKER_MODE=full    (по умолчанию) читает файл целиком в память: быстро на ноутбуке
    WORKER_MODE=stream  читает построчно: память не растёт, сколько бы строк ни было
    DUMP=/data/dump_2019.csv
"""
import csv
import os

mode = os.environ.get("WORKER_MODE", "full")
path = os.environ.get("DUMP", "/data/dump_2019.csv")
print(f"worker: mode={mode}, file={path}", flush=True)

with open(path, encoding="utf-8", newline="") as f:
    if mode == "full":
        rows = list(csv.DictReader(f))
        print(f"worker: загружено {len(rows)} строк, считаю...", flush=True)
        total = sum(int(r["salary"]) for r in rows)
        count = len(rows)
    else:
        total = count = 0
        for r in csv.DictReader(f):
            total += int(r["salary"])
            count += 1

print(f"worker: processed {count} rows, avg salary {total // count}", flush=True)
