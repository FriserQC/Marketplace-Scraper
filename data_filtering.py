import re

UNWANTED_WORDS = ['offre', 'offer', '$', 'sale', 'vente', 'achete', 'échange', 'echange', 'vendre' 
                 'achète', 'buy', 'sell', 'price', 'prix', 'trade', 'trading', 'recherche']


def extract_listings_information(links, previousListings):

    # Remove listings that are not free based on list of words
    listing_links = [link for link in links if not is_unwanted_string(link.text)]

    listing_data = []

    # Store the items url and text into a list of dictionaries
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
    contains = False

    stringToCheck = stringToCheck.lower().replace('\n', ' ').strip()

    for word in UNWANTED_WORDS:
        if word in stringToCheck:
            contains = True
            break

    return contains
