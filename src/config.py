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
    MAX_PREVIOUS_LISTINGS: int = 1000
    SCRAPE_INTERVAL_MINUTES: int = 5
    GECKODRIVER_PATH: str = "/usr/local/bin/geckodriver"
    FIREFOX_BINARY_PATHS: list = None

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
