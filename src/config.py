"""Configuration management for MarketplaceScraper."""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Config:
    """Application configuration from environment variables."""

    DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN")
    FREE_WANTED_CHANNEL_ID: int = int(os.getenv("FREE_WANTED_CHANNEL_ID", None))
    FREE_MISC_CHANNEL_ID: int = int(os.getenv("FREE_MISC_CHANNEL_ID", None))
    FREE_HOME_CHANNEL_ID: int = int(os.getenv("FREE_HOME_CHANNEL_ID", None))
    FREE_UNWANTED_CHANNEL_ID: int = int(os.getenv("FREE_UNWANTED_CHANNEL_ID", None))
    FACEBOOK_MARKETPLACE_LOCATION_ID: str = os.getenv("FACEBOOK_MARKETPLACE_LOCATION_ID")
    MARKETPLACE_FREE_SEARCH_URL: str = (
        f"https://www.facebook.com/marketplace/{FACEBOOK_MARKETPLACE_LOCATION_ID}/free/?sortBy=creation_time_descend"
    )
    MAX_PREVIOUS_LISTINGS: int = 1000
    SCRAPE_INTERVAL_MINUTES: int = 5
    GECKODRIVER_PATH: str = "/usr/local/bin/geckodriver"
    FIREFOX_BINARY_PATHS: list = None

    # Browser and scraping configuration
    BROWSER_VERSION_CHECK_TIMEOUT: int = 10
    BROWSER_PAGE_LOAD_TIMEOUT: int = 180
    BROWSER_SCRIPT_TIMEOUT: int = 180
    BROWSER_IMPLICIT_WAIT: int = 10
    BROWSER_POPUP_CLOSE_TIMEOUT: int = 3
    BROWSER_SEE_MORE_TIMEOUT: int = 10
    BROWSER_LISTING_LOAD_TIMEOUT: int = 30
    GECKODRIVER_LOG_PATH: str = "/tmp/geckodriver.log"
    BROWSER_USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
    REQUESTS_TIMEOUT: int = 30
    SLEEP_DELAY: int = 2

    def __post_init__(self):
        """Set default Firefox binary paths."""
        if self.FIREFOX_BINARY_PATHS is None:
            self.FIREFOX_BINARY_PATHS = [
                "/usr/lib/firefox/firefox",  # Alpine
                "/usr/bin/firefox",  # Alpine symlink
                "/usr/bin/firefox-esr",  # Debian
            ]

    def validate(self):
        """Validate required configuration values."""
        if not self.DISCORD_TOKEN:
            raise ValueError("DISCORD_TOKEN is required")
        if not self.FACEBOOK_MARKETPLACE_LOCATION_ID:
            raise ValueError("FACEBOOK_MARKETPLACE_LOCATION_ID is required")
        if self.FREE_WANTED_CHANNEL_ID is None:
            raise ValueError("FREE_WANTED_CHANNEL_ID is required")
        if self.FREE_MISC_CHANNEL_ID is None:
            raise ValueError("FREE_MISC_CHANNEL_ID is required")
        if self.FREE_HOME_CHANNEL_ID is None:
            raise ValueError("FREE_HOME_CHANNEL_ID is required")
        if self.FREE_UNWANTED_CHANNEL_ID is None:
            raise ValueError("FREE_UNWANTED_CHANNEL_ID is required")


config = Config()
config.validate()
