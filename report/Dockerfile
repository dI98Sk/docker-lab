# Сборка для задания 9
FROM python:3.12-slim AS build
WORKDIR /src
COPY . .
RUN python -m unittest discover -s tests -t .
RUN mkdir /pkg && cp -r hh_report /pkg/
RUN python -m zipapp /pkg -m "hh_report.__main__:main" -o /hh-report.pyz

# Сборка для второго этапа задания 9
FROM python:3.12-alpine
COPY --from=build /hh-report.pyz /app/hh-report.pyz
ENTRYPOINT ["python", "/app/hh-report.pyz"]
CMD ["--top", "5"]