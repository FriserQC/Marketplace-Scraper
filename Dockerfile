FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install Firefox ESR, geckodriver and dependencies in a single layer
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    wget \
    firefox-esr \
    libgtk-3-0 \
    libdbus-1-3 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxshmfence1 \
    && ARCH=$(dpkg --print-architecture) \
    && if [ "$ARCH" = "arm64" ] || [ "$ARCH" = "aarch64" ]; then \
        GECKO_ARCH="linux-aarch64"; \
    elif [ "$ARCH" = "armhf" ] || [ "$ARCH" = "armv7l" ]; then \
        GECKO_ARCH="linux32"; \
    else \
        GECKO_ARCH="linux64"; \
    fi \
    && wget -q https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-$GECKO_ARCH.tar.gz \
    && tar -xzf geckodriver-v0.35.0-$GECKO_ARCH.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.35.0-$GECKO_ARCH.tar.gz \
    && apt-get purge -y --auto-remove wget gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Copy application code
COPY src/ ./src/
COPY .env* ./

CMD ["python", "src/main.py"]