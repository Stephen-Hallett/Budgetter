# hadolint ignore=DL3007
FROM python:3.13-slim-bookworm

WORKDIR /

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
COPY models /models
COPY models/uv.lock .
COPY models/pyproject.toml .
COPY database /database

RUN uv sync --frozen

CMD ["uv", "run", "python", "-m", "models"]