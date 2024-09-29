FROM python:3.12-slim-bookworm AS base
WORKDIR /app
COPY poetry.lock pyproject.toml ./
RUN python -m pip install --no-cache-dir poetry \
    && poetry config virtualenvs.in-project true \
    && poetry install --without dev --no-interaction --no-ansi --no-root

FROM python:3.12-slim-bookworm
COPY --from=base /app /app
WORKDIR /app
RUN mkdir -p /app/logs
COPY ./src /app/src
ENV PYTHONPATH=/app

CMD [".venv/bin/python", "src/main.py"]
