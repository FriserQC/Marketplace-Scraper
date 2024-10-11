import re

UNWANTED_WORDS = ['offre', 'offer', 'offres', 'offers',
                  'sale', 'sales', 'wholesale', 'wholesales', 'liquidation', 'liquidations', 'vente', 'ventes', 'rabais', 'deal',
                  'vendre', 'vend', 'vends', 'vendons', 'vendez', 'vendent', 'sell', 'selling', 
                  'louer', 'rent', 'location', 'locations',
                  'price', 'prices', 'prix', 'cash',
                  'not free', 'pas gratuit', 'pas gratuits',
                  'negotiable', 'negotiables', 'négociable', 'negociable', 'négociables', 'negociables',
                  'échange', 'echange', 'échanges', 'echanges', 'échanger', 'echanger', 'trade', 'trades', 'trading', 'exchange', 'exchanges',
                  'achete', 'achète', 'achetes', 'achètes', 'acheter', 'buy', 'buying',
                  'échangeable', 'échangeables', 'echangeables', 'echangeable', 'remboursable', 'remboursables',
                  'credit', 'crédit',
                  'soumission', 'quote',
                  'free shipping', 'fast shipping', 'livraison gratuite', 'livraison rapide',
                  'financement', 'financing',
                  'paiement', 'paiements', 'payment', 'payments', 'pay', 
                  'cad', 'usd', 'taxes', 'taxe', 'tax',
                  'recherche', 'recherches', 'recherchons', 'recherchez', 'recherchent']

WANTED_WORDS = ['free', 'gratuit', 
                'donner', 'à donner', 'donné', 'donne', 'give away', 'giving away']

def is_unwanted_string(stringToCheck):

    stringToCheck = stringToCheck.lower().replace('\n', ' ').strip()

    # Check if contains $ in string
    checkDollarSign = re.compile(r"\$").search(stringToCheck)
    if checkDollarSign != None:
        return True

    # Check if contains unwanted word only if didn't find dollar sign $
    for word in UNWANTED_WORDS:
        remove = word_is_in_string(word, stringToCheck)
        if remove == True:
            return True

    # Check if contains wanted word             Too many false positives...
    # if remove == True:
    #     for word in WANTED_WORDS:
    #         remove = not word_is_in_string(word, stringToCheck)
    #         if remove == False:
    #             break

    return False

def word_is_in_string(word, stringToCheck):

    checks = r"\b(?:"+word+r")\b"
    pattern = re.compile(checks, re.IGNORECASE)
    matched = pattern.search(stringToCheck)
    if matched != None:
        return True
    
    return False