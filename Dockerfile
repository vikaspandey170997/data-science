FROM python:3.13-slim

WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH" \
    UV_PROJECT_ENVIRONMENT="/opt/venv" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install uv for dependency management.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Install dependencies first so Docker can cache this layer.
COPY api_project/pyproject.toml api_project/uv.lock ./
RUN uv sync --frozen --no-dev

# Copy the FastAPI application.
COPY api_project/ ./

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
