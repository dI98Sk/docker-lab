"""hh-report: сводка по вакансиям из командной строки.

    python -m hh_report --top 5          топ навыков по медианной зарплате
    python -m hh_report --skill python   число вакансий и медиана по навыку
    python -m hh_report --file other.csv --top 3
"""
import argparse
import csv
import io
import sys
from importlib import resources

from hh_report.stats import median


def read(path):
    if path:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    else:
        text = resources.files("hh_report").joinpath("vacancies.csv").read_text(encoding="utf-8")
    by_skill = {}
    for r in csv.DictReader(io.StringIO(text)):
        by_skill.setdefault(r["skill"], []).append(int(r["salary"]))
    return by_skill


def money(x):
    return f"{int(x):,} ₽".replace(",", " ")


def main(argv=None):
    p = argparse.ArgumentParser(prog="hh-report")
    p.add_argument("--file", help="CSV с вакансиями (по умолчанию встроенный)")
    p.add_argument("--skill", help="сводка по одному навыку")
    p.add_argument("--top", type=int, help="топ-N навыков по медианной зарплате")
    args = p.parse_args(argv)
    if not args.skill and not args.top:
        p.error("укажите --skill или --top")
    by_skill = read(args.file)
    if args.skill:
        values = by_skill.get(args.skill, [])
        if not values:
            print(f"{args.skill}: вакансий нет")
            return 1
        print(f"{args.skill}: {len(values)} вак., медиана {money(median(values))}")
        return 0
    med = {s: median(v) for s, v in by_skill.items()}
    top = sorted(med, key=lambda s: (-med[s], s))[:args.top]
    print(f"Топ-{args.top} навыков по медианной зарплате:")
    for i, s in enumerate(top, 1):
        print(f"{i}. {s:<11} {len(by_skill[s]):>3} вак.  медиана {money(med[s])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
