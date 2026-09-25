# 1. Lightweight Python base
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# 2. Install database connector dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Install packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

# 🔒 EXPOSE PORT 8005 FOR THE TASK MANAGER INSTANCE
EXPOSE 8005

# 4. Boot via Gunicorn production server bound to all local container interfaces
CMD ["gunicorn", "--bind", "0.0.0.0:8005", "app.main:app"]