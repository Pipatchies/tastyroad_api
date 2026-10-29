# 1. Base Build Stage
FROM python:3.15-slim-trixie AS builder

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System dependencies for GeoDjango and netcat for PostgreSQL wait loop
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils \
        libproj-dev \
        gdal-bin \
        netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# 2. Development Stage
FROM builder AS development

COPY . .

# Hot-reload and verbose request logging for development
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--reload", "--access-logfile", "-"]

# 3. Production Stage
FROM builder AS production

# Security: create dedicated non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

# Optimized production mode without reload
    CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]