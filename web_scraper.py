from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import re
import asyncio
from data_filtering import is_unwanted_string
from listing import Listing

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

LISTING_DESCRIPTION_CLASS_NAME = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u'
LISTING_CLASS_NAME = 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv'
    
SCRIPT_OPEN_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[1].click();'
SCRIPT_SELECT_RADIUS_OPTIONS = 'document.getElementsByClassName("xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xzsf02u x78zum5 x1jchvi3 x1fcty0u x132q4wb xdj266r x11i5rnm xat24cr x1mh8g0r x1a2a7pz x9desvi x1pi30zi x1a8lsjc x1swvt13 x1n2onr6 x16tdsg8 xh8yej3 x1ja2u2z")[0].click();'
SCRIPT_SELECT_20KM_RADIUS = 'document.getElementsByClassName("html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x6s0dn4 x78zum5 x1q0g3np x1iyjqo2 x1qughib xeuugli")[4].click();'
SCRIPT_CLOSE_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[6].click();'

SCRIPT_SCROLL_BOTTOM_PAGE = 'window.scrollTo(0, document.body.scrollHeight);'

async def open_chrome_to_marketplace_free_items_page():

    chrome_install = ChromeDriverManager().install()

    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.page_load_strategy = 'eager'
    options.timeouts = { 'pageLoad': 10000 }

    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Initialize Chrome WebDriver
    browser = webdriver.Chrome(
        options=options,
        service = Service(chromedriver_path),
    )

    url = f"https://www.facebook.com/marketplace/{os.getenv("FACEBOOK_MARKETPLACE_LOCATION_ID")}/free/?sortBy=creation_time_descend"

    browser.get(url)

    return browser

async def close_log_in_popup(browser):

    try:
        await asyncio.sleep(1)
        close_button = browser.find_element(By.XPATH, '//div[@aria-label="Close" and @role="button"]')
        close_button.click()

    except Exception as e:
        print(f"Could not find or click the close button! Error : {e}")
        pass

async def change_location_radius(browser):

    try:
        browser.execute_script(SCRIPT_OPEN_LOCATION_MENU)
        await asyncio.sleep(1) 

        browser.execute_script(SCRIPT_SELECT_RADIUS_OPTIONS)
        await asyncio.sleep(1) 

        browser.execute_script(SCRIPT_SELECT_20KM_RADIUS)
        await asyncio.sleep(1) 

        browser.execute_script(SCRIPT_CLOSE_LOCATION_MENU)
        await asyncio.sleep(1) 

    except Exception as e:
        print(f"Could not change location radius! Error : {e}")
        pass

async def scroll_bottom_page(browser):

    try:
        browser.execute_script(SCRIPT_SCROLL_BOTTOM_PAGE)
        await asyncio.sleep(0.3)

    except Exception as e:
        print(f"An error occurred: {e}")
        pass

def extract_listings_informations(listing_links):

    listing_data = []

    for listing_link in listing_links:
        url = listing_link.get('href')
        text = '\n'.join(listing_link.stripped_strings)
        #image = listing_link.find('img')["src"]
        listing_data.append({'text': text, 'url': url})

    extracted_data = []

    for item in listing_data:
        lines = item['text'].split('\n')
        title = lines[-2]
        location = lines[-1]
        url = "https://www.facebook.com" + re.sub(r'\?.*', '', item['url'])

        listing = Listing(title, location, url)

        extracted_data.append(listing)

    return extracted_data

async def extract_description_listings(listings, browser):

    for listing in listings:
        try:

            browser.get(listing.url)

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            # TODO find more reliable way of getting description (sometimes, not the right one...)
            descriptions = soup.find_all('span', {"class": LISTING_DESCRIPTION_CLASS_NAME})
            description = descriptions[1].text

            # trying to fix unfound descriptions (usually happen with car listings and other special listings)
            for item in descriptions:
                if item.next_element == item.text and item.text != 'Condition' and item.text != 'Used - Good' and item.text != 'Used - Fair' and item.text != 'New' and item.text != 'Used - like new' :
                    description = item.text
                    break

            listing.description = description
        except Exception as e:
            print(f"Description error : {e}")
            pass


    browser.close()

    return listings

async def extract_wanted_listings(previousListings) :
    browser = await open_chrome_to_marketplace_free_items_page()

    await close_log_in_popup(browser)
    await change_location_radius(browser)
    await scroll_bottom_page(browser)
    
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', {"class": LISTING_CLASS_NAME})

    listings = extract_listings_informations(links)

    # remove listings from previous listings or that have titles containing unwanted words...
    for listing in listings:
        if is_unwanted_string(listing.title) or any(listingsUrl in listing.url for listingsUrl in previousListings):
                # only add if not from previous ones
                listings.remove(listing)

    listings = await extract_description_listings(listings, browser)

    # remove listings with description that contain unwanted words...
    for listing in listings:
        if is_unwanted_string(listing.description):
            listings.remove(listing)

    # check if furniture
    for listing in listings:
        listing.is_furniture()

    return listings


