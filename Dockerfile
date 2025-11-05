FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install Firefox ESR and geckodriver (ARM-compatible)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    ca-certificates \
    wget \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    firefox-esr \
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

# Install geckodriver (download latest ARM-compatible version)
RUN ARCH=$(dpkg --print-architecture) && \
    if [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ]; then \
        GECKO_ARCH="linux-aarch64"; \
    elif [ "$ARCH" = "armhf" ] || [ "$ARCH" = "armv7l" ]; then \
        GECKO_ARCH="linux32"; \
    else \
        GECKO_ARCH="linux64"; \
    fi && \
    wget -q https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-$GECKO_ARCH.tar.gz && \
    tar -xzf geckodriver-v0.35.0-$GECKO_ARCH.tar.gz -C /usr/local/bin && \
    chmod +x /usr/local/bin/geckodriver && \
    rm geckodriver-v0.35.0-$GECKO_ARCH.tar.gz

# Install python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

CMD ["python", "src/main.py"]