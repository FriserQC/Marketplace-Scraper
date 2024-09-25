import re

UNWANTED_WORDS = ['offre', 'offer', 'offres', 'offers',
                  'sale', 'sales', 'vente', 'ventes',
                  'vendre', 'sell', 'selling', 
                  'price', 'prices', 'prix', 
                  'cash',
                  'échange', 'echange', 'échanger', 'echanger', 'trade', 'trades', 'trading', 
                  'achete', 'achète', 'achetes', 'achètes', 'acheter', 'buy', 'buying',
                  'recherche']

WANTED_WORDS = ['free', 'gratuit', 
                'donner', 'à donner', 'donné', 'donne', 'give away', 'giving away']


def extract_listings_information(links, previousListings):

    # Remove listings that are not free based on list of words
    listing_links = [link for link in links if not is_unwanted_string(link.text)]

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

        # only add if not from previous ones
        if not any(listingsUrl in url for listingsUrl in previousListings):
            extracted_data.append([title, location, url])

    return extracted_data

def is_unwanted_string(stringToCheck):
    remove = False

    stringToCheck = stringToCheck.lower().replace('\n', ' ').strip()

    # Check if contains $ in string
    checkDollarSign = re.compile(r"\$").search(stringToCheck)
    if checkDollarSign != None:
        remove = True

    # Check if contains unwanted word
    for word in UNWANTED_WORDS:
        remove = word_is_in_string(word, stringToCheck)
        if remove == True:
            break

    # Check if contains wanted word
    if remove == True:
        for word in WANTED_WORDS:
            remove = not word_is_in_string(word, stringToCheck)
            if remove == False:
                break

    return remove

def word_is_in_string(word, stringToCheck):
    checks = r"\b(?:"+word+r")\b"
    pattern = re.compile(checks, re.IGNORECASE)
    matched = pattern.search(stringToCheck)
    if matched != None:
        return True
    
    return False
