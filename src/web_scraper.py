import os
import re
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementClickInterceptedException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from data_filtering import is_unwanted_string, determine_categories
from listing import Listing
from typing import List

load_dotenv()

FACEBOOK_MARKETPLACE_LOCATION_ID = os.getenv("FACEBOOK_MARKETPLACE_LOCATION_ID")

def refresh_html_soup(browser: webdriver.Chrome) -> BeautifulSoup:
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def open_headless_browser() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    # options.add_argument('--no-sandbox')
    # options.page_load_strategy = 'eager'

    options.add_argument('--headless')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument("start-maximized")
    options.add_argument("--window-size=2560,1440")
    options.timeouts = {'pageLoad': 30000}
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(
        options=options,
        service=Service(ChromeDriverManager().install()),
    )

    return browser

def open_chrome_to_marketplace_free_items_page() -> webdriver.Chrome:
    browser = open_headless_browser()

    url = f"https://www.facebook.com/marketplace/{FACEBOOK_MARKETPLACE_LOCATION_ID}/free/?sortBy=creation_time_descend"
    browser.get(url)

    return browser

def close_log_in_popup(browser: webdriver.Chrome):
    close_button = browser.find_element(By.XPATH, '//div[@aria-label="Close" and @role="button"]')
    close_button.click()

async def close_log_in_popup_first_time(browser: webdriver.Chrome):
    await asyncio.sleep(2)
    try:
        close_log_in_popup(browser)
    except Exception as e:
        print(f"Could not find or click the close button, retrying. Error: {e}")
        await asyncio.sleep(10)
        browser.quit()
        browser = await open_chrome_to_marketplace_free_items_page()
        await close_log_in_popup_first_time(browser)

async def scroll_bottom_page(browser: webdriver.Chrome):
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
        
    except Exception as e:
        print(f"A Scrolling Error occurred: {e}")

async def click_see_more_description(browser: webdriver.Chrome, first_time=True):
    await asyncio.sleep(2)
    try:
        close_log_in_popup(browser)
    except Exception as e:
        print(f"Could not find or click the close button. Error: {e}")
    
    try:
        see_more_div = browser.find_element(By.XPATH, "//div[@role='button' and contains(., 'See more')]")
        see_more_button = see_more_div.find_element(By.XPATH, ".//span")
        WebDriverWait(browser, 10).until(expected_conditions.element_to_be_clickable(see_more_button))
        see_more_button.click()
    except ElementClickInterceptedException as e:
        if first_time:
            print(f"Click intercepted by another element, retrying. Error: {e}")
            await click_see_more_description(browser, False)
        else:
            print(f"Click intercepted by another element after retrying. Error: {e}")
    except Exception as e:
        if first_time:
            print(f"Could not find or click the 'See more' button, retrying. Error: {e}")
            await click_see_more_description(browser, False)
        else:
            print(f"Could not find or click the 'See more' button after retrying. Error: {e}")

def get_listings_full_description(soup: BeautifulSoup, description_text: str) -> str:
    spans = soup.find_all('span')
    description = description_text[:-3]
    for span in spans:
        if span.get_text() and description in span.get_text():
            return span
    return None

def extract_listings_informations_from_home_page(browser: webdriver.Chrome) -> List[Listing]:
    soup = refresh_html_soup(browser)
    links = soup.find_all('a', attrs={'href': re.compile(r'\/marketplace\/item\/')})

    listing_data = [
        {'text': '\n'.join(listing_link.stripped_strings), 'url': listing_link.get('href'), 'img_url': listing_link.find('img')['src'] if listing_link.find('img').has_attr('src') else None}
        for listing_link in links
    ]

    extracted_data = []
    for item in listing_data:
        lines = item['text'].split('\n')
        title = ' '.join(line for line in lines if line not in ["Free", "Pending", '·'] and "CA$" not in line)
        location = lines[-1]
        url = "https://www.facebook.com" + re.sub(r'\?.*', '', item['url'])
        img_url = item['img_url'] if item['img_url'] else ""
        extracted_data.append(Listing(title, location, url, img_url))

    return extracted_data

def fill_listings_general_category(listing: Listing, soup: BeautifulSoup) -> Listing:
    try:
        category = soup.find('a', attrs={'href': re.compile(r'\/marketplace\/[0-9]+\/[\w-]+\/')})
        listing.general_category = category.text
    except Exception as e:
        pass
        # print(f"General category not found or not existing for this listing {listing.url} : {e}")

    return listing

def fill_listings_specific_category(listing: Listing, soup: BeautifulSoup) -> Listing:
    try:
        title = soup.find('title').text
        last_index = title.rfind(' - ')
        first_index = title.rfind(' - ', None, last_index) + 3
        if first_index > 0 and last_index > first_index:
            category = title[first_index:last_index]
            listing.specific_category = category
    except Exception as e:
        print(f"Specific category not found or not existing for this listing {listing.url} : {e}")

    return listing

async def fill_listings_description(listing: Listing, soup: BeautifulSoup, browser: webdriver.Chrome) -> Listing:
    try:
        description_text = ""
        description = soup.find('meta', attrs={'name': 'description'})['content']
        description_text = str(description).strip()

        if len(description_text) > 10 or description_text[-3:] == "...":
            complete_description = get_listings_full_description(soup, description_text)

            if complete_description is not None :
                # check if expand button is present
                expand_button = complete_description.find('div', attrs={'role': 'button'})

                if expand_button is not None:
                    await click_see_more_description(browser)
                    print(f"Clicking on 'See more' for listing {listing.url}")
                    soup = refresh_html_soup(browser)
                    complete_description = get_listings_full_description(soup, description_text)

                if len(complete_description.text) > len(description_text):
                    description_text = str(complete_description.text)

    except Exception as e:
        print(f"Description not found or not existing for this listing {listing.url} : {e}")
    finally:
        listing.description = description_text

    return listing

async def fill_listings_informations(listings: List[Listing], browser: webdriver.Chrome) -> List[Listing]:
    for listing in listings:
        print(f"\rProcessing listing number: {listings.index(listing) + 1} / {len(listings)} ", end="")
        if listing.is_previous:
            continue

        browser.get(listing.url)
        soup = refresh_html_soup(browser)

        listing = fill_listings_general_category(listing, soup)
        listing = fill_listings_specific_category(listing, soup)
        listing = await fill_listings_description(listing, soup, browser)

        # checks if the listing is a delivery (is not really free)
        delivery = soup.find(lambda tag: tag.name == "div" and "dropoff" in tag.get_text().lower())

        if not delivery is None:
            listing.is_unwanted = True

    print("\nAll listings processed.")

    return listings

def filter_previous_listings(previous_listings: List[str], listings: List[Listing]) -> List[Listing]:
    for listing in listings:
        if any(previous_url in listing.url for previous_url in previous_listings):
            listing.is_previous = True
        elif is_unwanted_string(listing.title):
            listing.is_unwanted = True
    return listings

async def scrape_marketplace_listings(previous_listings: List[str]) -> List[Listing]:
    browser = open_chrome_to_marketplace_free_items_page()
    await close_log_in_popup_first_time(browser)
    await scroll_bottom_page(browser)

    listings = extract_listings_informations_from_home_page(browser)
    listings = filter_previous_listings(previous_listings, listings)

    print(f"Number of new listings found: {len([x for x in listings if not x.is_previous])}")

    listings = await fill_listings_informations(listings, browser)
    browser.quit()
    listings = determine_categories(listings)

    return listings
