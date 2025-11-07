"""Web scraping functionality for Facebook Marketplace."""

import asyncio
import logging
import os
import re
from typing import List, Optional

from bs4 import BeautifulSoup, Tag
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from config import config
from data_filtering import determine_categories, is_unwanted_string
from listing import Listing

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def refresh_html_soup(browser: webdriver.Firefox) -> BeautifulSoup:
    """Refresh and parse the current page HTML."""
    html = browser.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup


def create_firefox_driver():
    """Create and configure Firefox webdriver."""
    options = Options()

    # Try to find Firefox binary location
    firefox_binary = None
    for path in config.FIREFOX_BINARY_PATHS:
        if os.path.exists(path):
            firefox_binary = path
            break

    if firefox_binary:
        options.binary_location = firefox_binary
        logger.info("Using Firefox binary: %s", firefox_binary)

    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--width=1920")
    options.add_argument("--height=1080")

    # Use system geckodriver
    service = Service(config.GECKODRIVER_PATH)
    driver = webdriver.Firefox(service=service, options=options)
    return driver


def open_firefox_to_marketplace_free_items_page() -> webdriver.Firefox:
    """Open Firefox to marketplace free items page."""
    browser = create_firefox_driver()
    marketplace_url = (
        f"https://www.facebook.com/marketplace/{config.FACEBOOK_MARKETPLACE_LOCATION_ID}/"
        f"free/?sortBy=creation_time_descend"
    )
    browser.get(marketplace_url)
    return browser


async def close_log_in_popup(browser: webdriver.Firefox):
    """Attempt to close Facebook login popup."""
    await asyncio.sleep(2)
    try:
        # Try multiple selectors for the close button
        selectors = [
            (By.XPATH, "//div[@aria-label='Close' and @role='button']"),
            (By.XPATH, "//div[contains(@aria-label, 'Close')]"),
            (By.CSS_SELECTOR, "div[aria-label='Close']"),
            (By.CSS_SELECTOR, "[aria-label*='Close']"),
        ]

        for by, selector in selectors:
            try:
                close_button = WebDriverWait(browser, 3).until(
                    expected_conditions.element_to_be_clickable((by, selector))
                )
                close_button.click()
                return
            except Exception:  # pylint: disable=broad-except
                continue

        logger.warning("No close button found, continuing anyway")
    except Exception as exc:
        logger.error("Could not close popup: %s", exc)


async def scroll_bottom_page(browser: webdriver.Firefox):
    """Scroll to bottom of page to load all listings."""
    await asyncio.sleep(2)
    try:
        last_height = browser.execute_script("return document.body.scrollHeight")

        while True:
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            await asyncio.sleep(2)

            new_height = browser.execute_script("return document.body.scrollHeight")

            if new_height == last_height:
                break

            last_height = new_height

    except Exception as exc:
        logger.error("A Scrolling Error occurred: %s", exc)


async def click_see_more_description(browser: webdriver.Firefox, first_time=True):
    """Click 'See more' button to expand description."""
    await asyncio.sleep(2)
    try:
        await close_log_in_popup(browser)
    except Exception as exc:
        logger.error("Could not close popup: %s", exc)

    try:
        see_more_div = browser.find_element(By.XPATH, "//div[@role='button' and contains(., 'See more')]")
        see_more_button = see_more_div.find_element(By.XPATH, ".//span")
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(see_more_button))
        try:
            see_more_button.click()
        except ElementClickInterceptedException:
            logger.info("Click intercepted, trying JavaScript click")
            browser.execute_script("arguments[0].click();", see_more_button)

    except ElementClickInterceptedException as exc:
        logger.info("Click intercepted by another element, retrying. Error: %s", exc)
        if first_time:
            # Scroll the element into view and try again
            try:
                see_more_div = browser.find_element(By.XPATH, "//div[@role='button' and contains(., 'See more')]")
                browser.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", see_more_div
                )
                await asyncio.sleep(2)
                await close_log_in_popup(browser)
                see_more_button = see_more_div.find_element(By.XPATH, ".//span")
                browser.execute_script("arguments[0].click();", see_more_button)
            except Exception as retry_error:
                logger.error("Click intercepted by another element after retrying. Error: %s", retry_error)
    except Exception as exc:
        logger.error("Could not click 'See more' button. Error: %s", exc)


def get_listings_full_description(soup: BeautifulSoup, description_text: str) -> Optional[Tag]:
    """Extract full description from page."""
    description = description_text[:-3]
    spans: List[Tag] = soup.find_all("span")
    for span in spans:
        if span.get_text() and description in span.get_text():
            return span
    return None


def extract_listings_informations_from_home_page(browser: webdriver.Firefox) -> List[Listing]:
    """Extract listing information from marketplace home page."""
    soup = refresh_html_soup(browser)
    links = soup.find_all("a", attrs={"href": re.compile(r"\/marketplace\/item\/")})

    listing_data = [
        {
            "text": "\n".join(listing_link.stripped_strings),
            "url": listing_link.get("href"),
            "img_url": listing_link.find("img")["src"] if listing_link.find("img").has_attr("src") else None,
        }
        for listing_link in links
    ]

    extracted_data = []
    for item in listing_data:
        lines = item["text"].split("\n")
        title = " ".join(line for line in lines if line not in ["Free", "Pending", "·"] and "CA$" not in line)
        location = lines[-1]
        url = "https://www.facebook.com" + re.sub(r"\?.*", "", item["url"])
        img_url = item["img_url"] if item["img_url"] else ""
        extracted_data.append(Listing(title, location, url, img_url))

    return extracted_data


def fill_listings_general_category(listing: Listing, soup: BeautifulSoup) -> Listing:
    """Fill general category for listing."""
    try:
        category = soup.find("a", attrs={"href": re.compile(r"\/marketplace\/[0-9]+\/[\w-]+\/")})
        listing.general_category = category.text
    except Exception:  # pylint: disable=broad-except
        pass

    return listing


def fill_listings_specific_category(listing: Listing, soup: BeautifulSoup) -> Listing:
    """Fill specific category for listing."""
    try:
        title = soup.find("title").text
        last_index = title.rfind(" - ")
        first_index = title.rfind(" - ", None, last_index) + 3
        if 0 < first_index < last_index:
            category = title[first_index:last_index]
            listing.specific_category = category
    except Exception as exc:
        logger.error("Specific category not found or not existing for this listing %s : %s", listing.url, exc)

    return listing


async def fill_listings_description(listing: Listing, soup: BeautifulSoup, browser: webdriver.Firefox) -> Listing:
    """Fill description for listing."""
    try:
        description_text = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if isinstance(meta_tag, Tag):
            content = meta_tag.get("content")
            if isinstance(content, list):
                content = content[0] if content else ""
            if isinstance(content, str):
                description_text = content.strip()

        if len(description_text) > 10 or description_text[-3:] == "...":
            complete_description = get_listings_full_description(soup, description_text)

            if complete_description is not None:
                # check if expand button is present
                expand_button = complete_description.find("div", attrs={"role": "button"})

                if expand_button is not None:
                    await click_see_more_description(browser)
                    logger.info("Clicking on 'See more' for listing %s", listing.url)
                    soup = refresh_html_soup(browser)
                    complete_description = get_listings_full_description(soup, description_text)

                if len(complete_description.text) > len(description_text):
                    description_text = str(complete_description.text)

    except Exception as exc:
        logger.error("Description not found or not existing for this listing %s : %s", listing.url, exc)
    finally:
        listing.description = description_text

    return listing


async def fill_listings_informations(listings: List[Listing], browser: webdriver.Firefox) -> List[Listing]:
    """Fill detailed information for all listings."""
    for listing in listings:
        logger.info("Processing listing number: %d / %d", listings.index(listing) + 1, len(listings))
        if listing.is_previous or listing.is_unwanted:
            continue

        browser.get(listing.url)
        soup = refresh_html_soup(browser)

        listing = fill_listings_general_category(listing, soup)
        listing = fill_listings_specific_category(listing, soup)
        listing = await fill_listings_description(listing, soup, browser)

        # checks if the listing is a delivery (is not really free)
        delivery = soup.find(lambda tag: tag.name == "div" and "dropoff" in tag.get_text().lower())

        if delivery is not None:
            listing.is_unwanted = True

    logger.info("All listings processed.")

    return listings


def filter_previous_listings(previous_listings: List[Listing], listings: List[Listing]) -> List[Listing]:
    """Filter out previous and unwanted listings."""
    for listing in listings:
        if any(previous_url in listing.url for previous_url in previous_listings):
            listing.is_previous = True
        elif is_unwanted_string(listing.title):
            listing.is_unwanted = True
    return listings


async def scrape_marketplace_listings(previous_listings: List[Listing]) -> List[Listing]:
    """Main function to scrape marketplace listings."""
    browser = open_firefox_to_marketplace_free_items_page()
    listings: List[Listing] = []

    try:
        await close_log_in_popup(browser)
        await scroll_bottom_page(browser)

        listings = extract_listings_informations_from_home_page(browser)
        listings = await fill_listings_informations(listings, browser)
        listings = filter_previous_listings(previous_listings, listings)
        listings = determine_categories(listings)

        return listings
    finally:
        browser.quit()
