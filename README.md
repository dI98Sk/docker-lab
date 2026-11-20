# hh-tools

Утилиты для анализа вакансий hh.ru.

- `app/api.py` — HTTP API (`python -m app.api`), настройки в `app/settings.py`
- `app/worker.py` — ночной пересчёт по полной выгрузке `data/dump_2019.csv`
- `report/` — консольный отчёт `hh-report`
- `Dockerfile`, `compose.yaml` — запуск в контейнерах

Локально без Docker:

```bash
pip install -r requirements.txt
HOST=0.0.0.0 python -m app.api
```
