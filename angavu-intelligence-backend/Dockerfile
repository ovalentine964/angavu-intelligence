# ============================================
# Angavu Intelligence Backend — Production Image
# Multi-process Gunicorn + Uvicorn workers
# Python 3.12 (upgraded from 3.11)
# ============================================

# ---- Build stage ----
FROM python:3.12-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install .

# ---- Production stage ----
FROM python:3.12-slim

LABEL maintainer="Angavu Intelligence <valentine@angavu.ai>"
LABEL description="Angavu Intelligence Backend — FastAPI multi-process production server"

# Runtime dependencies only
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq5 curl && \
    rm -rf /var/lib/apt/lists/* && \
    groupadd -r appuser && \
    useradd -r -g appuser -d /app -s /sbin/nologin appuser

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY . .

# Create directories for logs
RUN mkdir -p /app/logs && chown -R appuser:appuser /app

USER appuser

# ---- Environment ----
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WEB_CONCURRENCY=4 \
    GUNICORN_TIMEOUT=120 \
    GUNICORN_GRACEFUL_TIMEOUT=30

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

# ---- Multi-process entrypoint ----
# Gunicorn manages 4 Uvicorn async workers for concurrent request handling.
# Each worker runs a full async event loop (uvloop via UvicornWorker).
# Workers are recycled after 2000 requests to prevent memory leaks.
CMD ["gunicorn", \
     "app.main:app", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--workers", "4", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "120", \
     "--graceful-timeout", "30", \
     "--max-requests", "2000", \
     "--max-requests-jitter", "200", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info"]
