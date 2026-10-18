# Multi-stage Dockerfile for Water Potability & Underwater Environmental Monitor
FROM python:3.11-slim AS builder

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

RUN useradd -m -u 1001 appuser

COPY --from=builder /root/.local /home/appuser/.local
COPY . /app

ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health').read()"

CMD ["python", "-m", "uvicorn", "src.serving.api:app", "--host", "0.0.0.0", "--port", "8000"]
