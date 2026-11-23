# Собрал Глеб, «у меня работает»
# FROM python:3.12-slim
#
# WORKDIR /app
# COPY . .
# RUN pip install -r requirements.txt
#
# EXPOSE 8000
# ENV HOST=0.0.0.0
# CMD python -m app.api


# Собрал я для 8ого задания
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

RUN useradd --uid 10001 --user-group --no-create-home app \
    && install -d -o app -g app /app/var
USER app

EXPOSE 8000
ENV HOST=0.0.0.0
CMD ["python", "-m", "app.api"]

