FROM python:3.10 AS builder

ENV PYTHONUNBUFFERED=1

WORKDIR /ml_api

COPY pyproject.toml poetry.lock /ml_api/

RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

FROM python:3.10-slim AS final

ENV PYTHONUNBUFFERED=1

WORKDIR /ml_api

COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . /ml_api/

COPY entrypoint.sh /ml_api/entrypoint.sh

ENTRYPOINT ["/ml_api/entrypoint.sh"]
