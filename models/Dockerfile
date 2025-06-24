# hadolint ignore=DL3007
FROM ghcr.io/astral-sh/uv:latest 

WORKDIR /models

COPY models /models
COPY database /database

RUN uv pip install --system --no-deps

CMD ["uv", "pip", "run", "python", "-m", "models"]