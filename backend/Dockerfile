# hadolint ignore=DL3007
FROM ghcr.io/astral-sh/uv:latest 

WORKDIR /app

COPY backend/app /app
COPY backend/uv.lock backend/pyproject.toml /app/
COPY database /database

RUN uv pip install --system --no-deps

CMD ["uv", "run", "uvicorn", "app.__init__:app", "--host", "0.0.0.0", "--port", "8000"]