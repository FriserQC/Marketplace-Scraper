FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    CHROME_BIN=/usr/bin/chromium \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install build deps and Chromium runtime libs (install system chromedriver to match Chromium)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    ca-certificates \
    wget \
    unzip \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libasound2 \
    libatk1.0-0 \
    libcups2 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libgbm1 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libxcb1 \
    libatk-bridge2.0-0 \
    libdbus-1-3 \
    libdrm2 \
    libexpat1 \
    libfontconfig1 \
    libgcc-s1 \
    libglib2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Install python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure system chromedriver is executable
RUN chmod +x /usr/bin/chromedriver || true

CMD ["python", "src/main.py"]