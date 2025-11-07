FROM python:3.13-alpine

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install Firefox ESR, geckodriver and dependencies in a single layer
RUN apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    libxml2-dev \
    libxslt-dev \
    wget \
    tar \
    firefox-esr \
    gtk+3.0 \
    dbus-libs \
    libxcomposite \
    libxdamage \
    libxrandr \
    mesa-gbm \
    alsa-lib \
    pango \
    at-spi2-core \
    cups-libs \
    libdrm \
    libxshmfence \
    && ARCH=$(uname -m) \
    && if [ "$ARCH" = "aarch64" ]; then \
        GECKO_ARCH="linux-aarch64"; \
    elif [ "$ARCH" = "armv7l" ]; then \
        GECKO_ARCH="linux32"; \
    else \
        GECKO_ARCH="linux64"; \
    fi \
    && wget -q https://github.com/mozilla/geckodriver/releases/download/v0.35.0/geckodriver-v0.35.0-$GECKO_ARCH.tar.gz \
    && tar -xzf geckodriver-v0.35.0-$GECKO_ARCH.tar.gz -C /usr/local/bin \
    && chmod +x /usr/local/bin/geckodriver \
    && rm geckodriver-v0.35.0-$GECKO_ARCH.tar.gz

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && rm requirements.txt

# Clean up build dependencies to reduce image size
RUN apk del wget tar gcc musl-dev libffi-dev libxml2-dev libxslt-dev

# Copy application code
COPY src/ ./src/
COPY .env* ./

CMD ["python", "src/main.py"]