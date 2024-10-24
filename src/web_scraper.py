from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
from bs4 import BeautifulSoup
import re
import asyncio
from data_filtering import is_unwanted_string, is_furniture
from listing import Listing

import os
from dotenv import load_dotenv 
load_dotenv() 

LISTING_DESCRIPTION_CLASS_NAME = 'xz9dl7a x4uap5 xsag5q8 xkhd6sd x126k92a'
LISTING_CLASS_NAME = 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv'
    
SCRIPT_OPEN_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[1].click();'
SCRIPT_SELECT_RADIUS_OPTIONS = 'document.getElementsByClassName("xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xzsf02u x78zum5 x1jchvi3 x1fcty0u x132q4wb xdj266r x11i5rnm xat24cr x1mh8g0r x1a2a7pz x9desvi x1pi30zi x1a8lsjc x1swvt13 x1n2onr6 x16tdsg8 xh8yej3 x1ja2u2z")[0].click();'
SCRIPT_SELECT_20KM_RADIUS = 'document.getElementsByClassName("html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x6s0dn4 x78zum5 x1q0g3np x1iyjqo2 x1qughib xeuugli")[4].click();'
SCRIPT_CLOSE_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[6].click();'

SCRIPT_SCROLL_BOTTOM_PAGE = 'window.scrollTo(0, document.body.scrollHeight);'

FACEBOOK_MARKETPLACE_LOCATION_ID = os.getenv("FACEBOOK_MARKETPLACE_LOCATION_ID")

async def open_chrome_to_marketplace_free_items_page():

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    options.page_load_strategy = 'eager'
    options.timeouts = { 'pageLoad': 30000 }

    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Initialize Chrome WebDriver
    browser = webdriver.Chrome(
        options=options,
        service=Service(ChromeDriverManager().install()),
    )

    url = f"https://www.facebook.com/marketplace/{FACEBOOK_MARKETPLACE_LOCATION_ID}/free/?sortBy=creation_time_descend"

    browser.get(url)

    return browser

async def close_log_in_popup(browser):

    try:
        await asyncio.sleep(2)
        close_button = browser.find_element(By.XPATH, '//div[@aria-label="Close" and @role="button"]')
        close_button.click()

    except Exception as e:
        print(f"Could not find or click the close button, gonna retry! Error : {e}")
        await asyncio.sleep(10)
        browser.quit()
        browser = await open_chrome_to_marketplace_free_items_page()
        await close_log_in_popup(browser)
        pass

    return browser

async def change_location_radius(browser):

    try:
        await asyncio.sleep(2)

        browser.execute_script(SCRIPT_OPEN_LOCATION_MENU)
        await asyncio.sleep(2) 

        browser.execute_script(SCRIPT_SELECT_RADIUS_OPTIONS)
        await asyncio.sleep(2) 

        browser.execute_script(SCRIPT_SELECT_20KM_RADIUS)
        await asyncio.sleep(2) 

        browser.execute_script(SCRIPT_CLOSE_LOCATION_MENU)
        await asyncio.sleep(2) 

    except Exception as e:
        print(f"Could not change location radius! Error : {e}")
        pass

async def scroll_bottom_page(browser):

    try:
        browser.execute_script(SCRIPT_SCROLL_BOTTOM_PAGE)
        await asyncio.sleep(2)

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

        # get all segments of title (if used \n in it)
        # only keep useful sections of title, discard the rest...
        title = ''
        for line in lines:
            if line != "Free" and line != "Pending" and line != '·' and "CA$" not in line and line != lines[-1]:
                title = title + line + " "

        location = lines[-1]
        url = "https://www.facebook.com" + re.sub(r'\?.*', '', item['url'])

        listing = Listing(title, location, url)

        extracted_data.append(listing)

    return extracted_data

async def extract_description_listings(listings, browser):

    for listing in listings:
        if listing.isPrevious == True :
            continue

        try:
            browser.get(listing.url)

            html = browser.page_source
            soup = BeautifulSoup(html, 'html.parser')
            description = soup.find('div', {"class": LISTING_DESCRIPTION_CLASS_NAME}).text

            listing.description = description
        except Exception as e:
            print(f"Description not found : {e}")
            pass

    browser.quit()

    return listings

async def extract_wanted_listings(previousListings) :
    browser = await open_chrome_to_marketplace_free_items_page()

    browser = await close_log_in_popup(browser)
    await change_location_radius(browser)
    await scroll_bottom_page(browser)
    
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', {"class": LISTING_CLASS_NAME})

    listings = extract_listings_informations(links)

    # mark listings from previous listings or that have titles containing unwanted words...
    for listing in listings:
        if is_unwanted_string(listing.title):
            listing.isUnwanted = True
        if any(listingsUrl in listing.url for listingsUrl in previousListings):
            listing.isPrevious = True

    listings = await extract_description_listings(listings, browser)

    # mark listings with description that contain unwanted words...
    for listing in listings:
        if is_unwanted_string(listing.description):
            listing.isUnwanted = True

    # check if furniture
    for listing in listings:
        if is_furniture(listing.title, listing.description):
            listing.isFurniture = True

    return listings


