FROM python:3.12.3-alpine

RUN pip install poetry==2.2.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-ansi --no-root --no-cache

COPY . .

RUN adduser --disabled-password --gecos '' --uid 1000 baseuser
RUN chown -R baseuser:baseuser /app
USER baseuser
