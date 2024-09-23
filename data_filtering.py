import re

UNWANTED_WORDS = ['offre', 'offer', 'offres', 'offers',
                  'sale', 'sales', 'vente', 'ventes',
                  'achete', 'achète', 'achetes', 'achètes', 'acheter', 'buy', 'buying',
                  'échange', 'echange', 'échanger', 'echanger', 'trade', 'trades', 'trading', 
                  'vendre', 'sell', 'selling', 
                  'price', 'prices', 'prix', 
                  'cash',
                  'recherche']


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
    stringToCheck = stringToCheck.lower().replace('\n', ' ').strip()

    # check if contains $ in string
    checkDollarSign = re.compile(r"\$").search(stringToCheck)
    if checkDollarSign != None:
        return True

    for word in UNWANTED_WORDS:
        checks = r"\b(?:"+word+r")\b"
        pattern = re.compile(checks, re.IGNORECASE)
        matched = pattern.search(stringToCheck)
        if matched != None:
            return True
        
    # TODO maybe if find unwanted, check if contains "give away" or "a donner" and keep the listing

    return False
