import re

UNWANTED_WORDS = ['offre', 'offer', 'offres', 'offers',
                  'sale', 'sales', 'wholesale', 'wholesales', 'vente', 'ventes',
                  'vendre', 'sell', 'selling', 
                  'price', 'prices', 'prix', 
                  'cash',
                  'échange', 'echange', 'échanger', 'echanger', 'trade', 'trades', 'trading', 
                  'achete', 'achète', 'achetes', 'achètes', 'acheter', 'buy', 'buying',
                  'recherche']

WANTED_WORDS = ['free', 'gratuit', 
                'donner', 'à donner', 'donné', 'donne', 'give away', 'giving away']

def is_unwanted_string(stringToCheck):

    remove = False
    stringToCheck = stringToCheck.lower().replace('\n', ' ').strip()

    # Check if contains $ in string
    checkDollarSign = re.compile(r"\$").search(stringToCheck)
    if checkDollarSign != None:
        remove = True

    # Check if contains unwanted word only if didn't find dollar sign $
    if remove == False:
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
