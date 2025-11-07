"""Constants for Facebook Marketplace scraping."""

FIREFOX_BINARY_PATHS = [
    "/usr/lib/firefox/firefox",  # Alpine
    "/usr/bin/firefox",  # Alpine symlink
    "/usr/bin/firefox-esr",  # Debian
]

FACEBOOK_BASE_URL = "https://www.facebook.com"
MARKETPLACE_URL_TEMPLATE = f"{FACEBOOK_BASE_URL}/marketplace/{{location}}/free/?sortBy=creation_time_descend"

# Selenium timeouts
DEFAULT_WAIT_TIMEOUT = 10
SCROLL_WAIT_TIME = 2
POPUP_CLOSE_TIMEOUT = 3
