import os
import re
import asyncio
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from data_filtering import is_unwanted_string, is_furniture
from listing import Listing

load_dotenv()

LISTING_CLASS_NAME = 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv'

SCRIPT_OPEN_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[1].click();'
SCRIPT_SELECT_RADIUS_OPTIONS = 'document.getElementsByClassName("xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xzsf02u x78zum5 x1jchvi3 x1fcty0u x132q4wb xdj266r x11i5rnm xat24cr x1mh8g0r x1a2a7pz x9desvi x1pi30zi x1a8lsjc x1swvt13 x1n2onr6 x16tdsg8 xh8yej3 x1ja2u2z")[0].click();'
SCRIPT_SELECT_20KM_RADIUS = 'document.getElementsByClassName("html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x6s0dn4 x78zum5 x1q0g3np x1iyjqo2 x1qughib xeuugli")[4].click();'
SCRIPT_CLOSE_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[6].click();'

SCRIPT_SCROLL_BOTTOM_PAGE = 'window.scrollTo(0, document.body.scrollHeight);'

FACEBOOK_MARKETPLACE_LOCATION_ID = os.getenv("FACEBOOK_MARKETPLACE_LOCATION_ID")

async def open_chrome_to_marketplace_free_items_page():
    # Open Chrome browser to the Facebook Marketplace free items page
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.page_load_strategy = 'eager'
    options.timeouts = {'pageLoad': 30000}
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    browser = webdriver.Chrome(
        options=options,
        service=Service(ChromeDriverManager().install()),
    )

    url = f"https://www.facebook.com/marketplace/{FACEBOOK_MARKETPLACE_LOCATION_ID}/free/?sortBy=creation_time_descend"
    browser.get(url)

    return browser

async def close_log_in_popup(browser):
    # Close the login popup if it appears
    await asyncio.sleep(2)
    try:
        close_button = browser.find_element(By.XPATH, '//div[@aria-label="Close" and @role="button"]')
        close_button.click()
    except Exception as e:
        print(f"Could not find or click the close button, retrying. Error: {e}")
        await asyncio.sleep(10)
        browser.quit()
        browser = await open_chrome_to_marketplace_free_items_page()
        return await close_log_in_popup(browser)

    return browser

async def change_location_radius(browser):
    # Change the location radius in marketplace settings
    await asyncio.sleep(2)
    try:
        browser.execute_script(SCRIPT_OPEN_LOCATION_MENU)
        await asyncio.sleep(2)
        browser.execute_script(SCRIPT_SELECT_RADIUS_OPTIONS)
        await asyncio.sleep(2)
        browser.execute_script(SCRIPT_SELECT_20KM_RADIUS)
        await asyncio.sleep(2)
        browser.execute_script(SCRIPT_CLOSE_LOCATION_MENU)
        await asyncio.sleep(2)
    except Exception as e:
        print(f"Could not change location radius! Error: {e}")

async def scroll_bottom_page(browser):
    # Scroll to the bottom of the page
    try:
        browser.execute_script(SCRIPT_SCROLL_BOTTOM_PAGE)
        await asyncio.sleep(2)
    except Exception as e:
        print(f"An error occurred: {e}")

def extract_listings_informations(browser):
    # Extract listing's informations from the page
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', {"class": LISTING_CLASS_NAME})

    listing_data = [
        {'text': '\n'.join(listing_link.stripped_strings), 'url': listing_link.get('href')}
        for listing_link in links
    ]

    extracted_data = []
    for item in listing_data:
        lines = item['text'].split('\n')
        title = ' '.join(line for line in lines if line not in ["Free", "Pending", '·'] and "CA$" not in line)
        location = lines[-1]
        url = "https://www.facebook.com" + re.sub(r'\?.*', '', item['url'])
        extracted_data.append(Listing(title, location, url))

    return extracted_data

async def extract_listings_description_and_category(listings, browser):
    # Extract descriptions and categories from the listings pages
    for listing in listings:
        if listing.is_previous:
            continue

        browser.get(listing.url)
        html = browser.page_source
        soup = BeautifulSoup(html, 'html.parser')

        try:
            description = soup.find('meta', attrs={'name':'description'})['content']
            listing.description = description
        except Exception as e:
            print(f"Description not found or not existing: {e}")

        if listing.category is None or listing.category == "":
            try:
                title = soup.find('title').text
                last_index = title.rfind(' - ')
                first_index = title.rfind(' - ', None, last_index) + 3
                if first_index > 0 and last_index > first_index:
                    category = title[first_index:last_index]
                    listing.category = category
            except Exception as e:
                print(f"Category not found: {e}")

    browser.quit()
    return listings

async def scrape_wanted_listings(previous_listings):
    # Scrape listings that are wanted from marketplace
    browser = await open_chrome_to_marketplace_free_items_page()
    browser = await close_log_in_popup(browser)
    await change_location_radius(browser)
    await scroll_bottom_page(browser)

    listings = extract_listings_informations(browser)

    for listing in listings:
        if is_unwanted_string(listing.title):
            listing.is_unwanted = True
        if any(previous_url in listing.url for previous_url in previous_listings):
            listing.is_previous = True

    listings = await extract_listings_description_and_category(listings, browser)

    for listing in listings:
        if is_unwanted_string(listing.description):
            listing.is_unwanted = True
        if is_furniture(listing.title, listing.description):
            listing.is_furniture = True

    return listings
