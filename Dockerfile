
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libc-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apt-get purge -y --auto-remove \
        gcc \
        libc-dev && \
    rm -rf /var/lib/apt/lists/*

COPY . .

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

VOLUME /app/data

RUN adduser --disabled-password --gecos '' appuser
USER appuser

CMD ["python", "-u", "main.py"]