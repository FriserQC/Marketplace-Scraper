from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import os
import time
from bs4 import BeautifulSoup
import re
import pandas as pd
import asyncio

import os
from dotenv import load_dotenv, dotenv_values 
load_dotenv() 

UNWANTED_WORDS = [' offre', ' offer', '$', ' sale', ' vente', ' achete', 'échange', ' echange', 'vendre' 
                 ' achète', ' buy', ' sell', ' price', 'prix', 'trade', 'trading', 'recherche']

LISTING_DESCRIPTION_CLASS_NAME = 'x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u'
LISTING_CLASS_NAME = 'x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1sur9pj xkrqix3 x1lku1pv'
    
SCRIPT_OPEN_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[1].click();'
SCRIPT_SELECT_RADIUS_OPTIONS = 'document.getElementsByClassName("xjyslct xjbqb8w x13fuv20 xu3j5b3 x1q0q8m5 x26u7qi x972fbf xcfux6l x1qhh985 xm0m39n x9f619 xzsf02u x78zum5 x1jchvi3 x1fcty0u x132q4wb xdj266r x11i5rnm xat24cr x1mh8g0r x1a2a7pz x9desvi x1pi30zi x1a8lsjc x1swvt13 x1n2onr6 x16tdsg8 xh8yej3 x1ja2u2z")[0].click();'
SCRIPT_SELECT_20KM_RADIUS = 'document.getElementsByClassName("html-div xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x6s0dn4 x78zum5 x1q0g3np x1iyjqo2 x1qughib xeuugli")[4].click();'
SCRIPT_CLOSE_LOCATION_MENU = 'document.getElementsByClassName("x1i10hfl xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x972fbf xcfux6l x1qhh985 xm0m39n x1ypdohk xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x9f619 x3nfvp2 xdt5ytf xl56j7k x1n2onr6 xh8yej3")[6].click();'

SCRIPT_SCROLL_BOTTOM_PAGE = 'window.scrollTo(0, document.body.scrollHeight);'

async def OpenChromeToMarketplacePage():

    chrome_install = ChromeDriverManager().install()

    folder = os.path.dirname(chrome_install)
    chromedriver_path = os.path.join(folder, "chromedriver.exe")

    options = webdriver.ChromeOptions() 
    options.add_argument("start-maximized")
    # to supress the error messages/logs
    options.add_experimental_option('excludeSwitches', ['enable-logging'])

    # Initialize Chrome WebDriver
    browser = webdriver.Chrome(
        options=options,
        service = Service(chromedriver_path),
    )

    url = f"https://www.facebook.com/marketplace/{os.getenv("FACEBOOK_MARKETPLACE_LOCATION_STRING")}/free/?sortBy=creation_time_descend"

    browser.get(url)

    return browser

async def CloseLogInPopup(browser):

    # Locate the button for the login pop-up with aria-label="Close"
    try:
        close_button = browser.find_element(By.XPATH, '//div[@aria-label="Close" and @role="button"]')
        close_button.click()
        print("Close button clicked!")
        
    except:
        print("Could not find or click the close button!")
        pass

async def ChangeLocationRadius(browser):

    # Change location radius
    try:
        browser.execute_script(SCRIPT_OPEN_LOCATION_MENU)
        await asyncio.sleep(0.3)

        browser.execute_script(SCRIPT_SELECT_RADIUS_OPTIONS)
        await asyncio.sleep(0.3)  

        browser.execute_script(SCRIPT_SELECT_20KM_RADIUS)
        await asyncio.sleep(0.3) 

        browser.execute_script(SCRIPT_CLOSE_LOCATION_MENU)
        await asyncio.sleep(0.3) 
    except:
        print("Could not change location radius!")
        pass

async def ScrollBottomPage(browser):

    #Scroll down to load first two listings sections
    try:
        
        # Scroll down to the bottom of the page using JavaScript
        browser.execute_script(SCRIPT_SCROLL_BOTTOM_PAGE)
        await asyncio.sleep(0.3)

    except Exception as e:
        print(f"An error occurred: {e}")
        pass

def ExtractListingsInformation(html, previousListings):

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Find all link elements
    links = soup.find_all('a', {"class": LISTING_CLASS_NAME})

    # Only keep items where the text matches your search terms and desired location
    listing_links = [link for link in links if not any(ext in link.text.lower() for ext in UNWANTED_WORDS)]

    # Create empty list to store product data
    listing_data = []

    # Store the items url and text into a list of dictionaries
    for listing_link in listing_links:
        url = listing_link.get('href')
        text = '\n'.join(listing_link.stripped_strings)
        #image = listing_link.find('img')["src"]
        listing_data.append({'text': text, 'url': url})

    # Create an empty list to store product data
    extracted_data = []

    for item in listing_data:
        lines = item['text'].split('\n')

        # Extract title
        title = lines[-2]

        # Extract location
        location = lines[-1]

        url = "https://www.facebook.com" + re.sub(r'\?.*', '', item['url'])

        if not any(listingsUrl in url for listingsUrl in previousListings):
            extracted_data.append([title, location, url])

    return extracted_data

async def GetDescriptionListings(extracted_data, browser):

    # get description listing
    for data in extracted_data:
        url = data[2]
        browser.get(url)
        await asyncio.sleep(0.01)

        # Retrieve the HTML
        html = browser.page_source

        # Use BeautifulSoup to parse the HTML
        soup = BeautifulSoup(html, 'html.parser')

        desc = soup.find_all('span', {"class": LISTING_DESCRIPTION_CLASS_NAME})[1].text 

        if any(ext in desc.lower() for ext in UNWANTED_WORDS):
            extracted_data.remove(data)
        else:
            data.append(desc)

    browser.close()

    return extracted_data

async def GetMessage(previousListings) :
    browser = await OpenChromeToMarketplacePage()

    await CloseLogInPopup(browser)
    await ChangeLocationRadius(browser)
    await ScrollBottomPage(browser)
    
    html = browser.page_source

    extracted_data = ExtractListingsInformation(html, previousListings)

    extracted_data = await GetDescriptionListings(extracted_data, browser)

    return extracted_data


