# Facebook Marketplace Scraper for free items in your city

## Description
This program scrapes Facebook Marketplace for free items in your area and sends the listings to a Discord server.
You need a Discord bot that can send messages to channels.

## Prerequisites
- Docker and Docker Compose
- Discord Bot Token
- Facebook Marketplace location ID

---

## Setup Instructions

### 1. Create your `.env` file

Copy the `.env.example` file to `.env` and fill in your values:

```bash
cp .env.example .env
```

**Where to find these values:**
- **DISCORD_TOKEN**: Create a Discord bot at [Discord Developer Portal](https://discord.com/developers/applications)
- **Channel IDs**: Right-click on Discord channels → "Copy Channel ID" (enable Developer Mode in Discord settings)
- **FACEBOOK_MARKETPLACE_LOCATION_ID**: See instructions below

### 2. Find your Facebook Marketplace City ID

1. Go to Facebook Marketplace in your browser
2. Select your city from the location dropdown
3. Copy the location string from the URL (see image below):

![Example](docs/MarketplaceLocationStringExemple.png)

Example: `https://www.facebook.com/marketplace/montreal/search/` → use `montreal`

---

## Running with Docker Compose (Recommended)

**Best for production deployment and Raspberry Pi**

### Build and run:
```bash
docker compose up -d --build
```

### View logs in real-time:
```bash
docker compose logs -f
```

### Stop the container:
```bash
docker compose down
```

### Rebuild after code changes:
```bash
docker compose build --no-cache
docker compose up -d
```

---

## Running with Docker (Without Compose)

### Build the image:
```bash
docker build -t marketplace-scraper:latest .
```

### Run the container:
```bash
docker run -d --env-file .env --name marketplace-scraper --restart unless-stopped --shm-size=1gb marketplace-scraper:latest
```

### View logs:
```bash
docker logs -f marketplace-scraper
```

### Stop and remove:
```bash
docker stop marketplace-scraper
docker rm marketplace-scraper
```

---

## Raspberry Pi Deployment

This project is fully compatible with Raspberry Pi (ARM64/aarch64 architecture).

### Requirements:
- Raspberry Pi 3/4/5 with ARM64 OS
- Docker and Docker Compose installed

**The Dockerfile automatically detects ARM architecture and installs the correct Firefox + geckodriver versions.**

### Performance on Raspberry Pi:
- Initial build: ~5-10 minutes
- Docker image size: ~150-200MB (Alpine-based)
- Memory usage: ~200-400MB during scraping
- Recommended: Raspberry Pi 4 with 2GB+ RAM

---

## Technical Details

### Docker Image
- **Base**: `python:3.13-alpine` for minimal size
- **Architecture support**: AMD64 (x86_64), ARM64 (aarch64), ARMv7
- **Size**: ~150-200MB (vs ~300-400MB with Debian-based images)
- **Browser**: Firefox ESR (headless)
- **Driver**: Geckodriver v0.35.0

### Python Dependencies
- **Python 3.13** with Alpine compatibility
- **discord.py 2.4.0** - Discord bot framework
- **selenium 4.27.1** - Web scraping automation
- **beautifulsoup4 4.12.3** - HTML parsing
- **audioop-lts 0.2.1** - Python 3.13 compatibility for discord.py

---

### Common Issues

**"Improper token has been passed"**
- Check your `DISCORD_TOKEN` in `.env` is correct
- Ensure no extra spaces or quotes around the token
- Verify the token is valid at [Discord Developer Portal](https://discord.com/developers/applications)

**"binary is not a Firefox executable"**
- This is automatically handled in the Dockerfile
- If issues persist, check Firefox installation: `docker exec marketplace-scraper which firefox`

**"Unable to locate element" (Selenium)**
- Facebook may have changed their page structure
- Check logs for specific error details
- The scraper will retry failed listings

**Container exits immediately**
- Check logs: `docker logs marketplace-scraper`
- Verify all required environment variables are set in `.env`
- Ensure Discord token has proper permissions

**Out of memory on Raspberry Pi**
- Ensure `shm-size: '1gb'` is set in `docker-compose.yml`
- Close other applications to free up RAM
- Consider using Raspberry Pi 4 with 4GB+ RAM

**Slow build times on Raspberry Pi**
- Normal for ARM devices (5-10 minutes)
- Compiling Python packages with C extensions takes longer
- Use `--no-cache` only when necessary

### Pre-commit hook

A pre-commit hook is included to help keep code quality consistent before commits. It runs checks/formatters locally (examples: black, isort, mypy, flake8) as configured in .pre-commit-config.yaml.

Install and enable the hook (Windows / local dev):

```bash
python -m pip install --upgrade pip
pip install pre-commit
pre-commit install
```

Run the hooks against all files (useful on first setup):

```bash
pre-commit run --all-files
```

---

## Future Potential Features
<ol>
  <li>Reverse image finder on Google, and find price of product (send message to different channel when profit is high)</li>
  <li>Add filtering options for specific item categories</li>
  <li>Web dashboard for configuration</li>
  <li>Price history tracking</li>
  <li>Multi-location support</li>
</ol>

---

## License
MIT License - feel free to use and modify for your own projects.

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.
