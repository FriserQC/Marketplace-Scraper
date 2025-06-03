import re
from typing import List

UNWANTED_WORDS = [
    # Offers and Sales
    'offre', 'offer', 'offres', 'offers', 'vente', 'ventes', 'vendre', 'vends', 'vendons', 'vendez', 'vendent',
    'sale', 'sales', 'liquidation', 'liquidations', 'solde', 'soldes', 'clearance', 'clearances', 'clearout', 'clearouts', 'clearing', 'clearings',
    'rabais', 'deal', 'promotion', 'promotions', 'promo', 'promos', 'discount', 'discounts', 'savings', 'save', 'saves', 'saving', 
    'économie', 'économies', 'économiser', 'économisez', 'économisant', 'économisants',

    # Buying and Selling
    'buy', 'buying', 'achete', 'achète', 'achetes', 'achètes', 'achetons', 'achetez', 'achètent', 'achetent',
    'sell', 'selling', 'sells', 'vend', 'purschase', 'purschases', 'purschasing', 

    # Renting
    'louer', 'rent', 'location', 'locations', 'rental', 'rentals', 'renting', 'rentings', 'loue', 'loues', 'louons', 'louez', 'louent',

    # Pricing and Costs
    'price', 'prices', 'prix', 'pricing', 'tarif', 'tarifs', 'cost', 'costs', 'coût', 'coûts', 

    # Payments
    'cash', 'paiement', 'paiements', 'payment', 'payments', 'pay', 'pays', 'paying', 'payez', 'payable', 'payables', 

    # Taxes
    'taxes', 'taxe', 'tax', 'taxation', 'taxations', 'taxable', 'taxables',

    # Rates
    'rate', 'rates', 'taux', 'interest', 'interests', 'intérêt', 'intérêts',

    # Free and Refunds
    'not free', 'pas gratuit', 'pas gratuits', 'not for free', 'not giveaway', 'not giveaways', 
    'remboursable', 'remboursables', 'remboursement', 'remboursements', 'refund', 'refunds', 'refundable', 'refundables',
    'free trial', 'essai gratuit', 'essais gratuits', 'free trials', 

    # Financing and Credit
    'financement', 'financing', 'finance', 'finances', 'financé', 'financés', 'financée', 'financées', 
    'credit', 'crédit', 'crédits', 'credits', 'mortgage', 'hypothèque', 'hypothèques', 'loan', 'loans',

    # Shipping and Delivery
    'free shipping', 'fast shipping', 'free delivery', 'fast delivery', 'delivery available', 'quality delivery', 'home delivery', 'home shipping',
    'we deliver', 'we ship', 'livraison disponible', 'livraison de qualité', 'livraison à domicile', 'livraison à la maison', 'livraison gratuite', 'livraison rapide', 
    'expédition gratuite', 'expédition rapide', 'expédition à domicile', 'expédition à la maison', 'nous livrons', 'nous expédions',

    # Services and Installation
    'installation', 'installations', 'service', 'services', 'technicien', 'techniciens', 'technicians', 'technician', 'installateur', 'installateurs', 'installers',

    # Orders
    'commande', 'commandes', 'order', 'orders', 'ordering', 'commandez', 'inquiries', 'inquiry', 'enquiry', 'enquiries',

    # Warranty
    'lifetime warranty', 'garantie à vie', 'garantie de satisfaction', 'satisfaction guarantee', 'warrantied',
    'insurance', 'assurance', 'assurances',

    # Negotiation
    'negotiable', 'negociable', 'négociable', 'négociables', 'negotiables', 'negotiate', 'negotiates', 'negotiating', 'negociate', 'negociates', 'negociating', 'négociation', 
    'négociations', 'negotiation', 'negotiations', 

    # Search
    'recherche', 'recherches', 'recherchons', 'recherchez', 'recherchent', 'search', 'searches', 'searching', 'searched',
    'looking for', 'looking to buy', 'looking to sell', 'looking to trade', 'looking to exchange', 'looking for a', 'looking for an', 'looking for some', 'looking for any',
    'looking for someone', 'looking for something', 'looking for somewhere', 'looking for a place', 'looking for a person', 'looking for a company', 'looking for a business',

    # Exchange and Trade
    'échange', 'echange', 'échanges', 'echanges', 'échanger', 'echanger', 'échangent', 'echangent',
    'exchange', 'exchanges', 'trade', 'trades', 'trading', 'traded', 'trader', 'traders',

    # Quotes and Estimates
    'soumission', 'quote', 'estimé', 'estimés', 'estimée', 'estimées', 'estimation', 'estimations', 'free estimate', 'free estimates',
    'soumettre', 'soumet', 'soumettez', 'soumettant', 'soumettent', 'soumissionner', 'soumissionnez', 'soumissionnant', 'soumissionnent',
    'en stock', 'in stock', 'stock', 'stocks',

    # Custom
    'custom', 'personnalisé', 'personnalisée', 'personnalisés', 'personnalisées', 'personnaliser', 'personnalisez',
    'customized', 'customisation', 'customisations', 'customizable', 'customisables', 'customization', 'customizations',
    'sur mesure', 'sur mesures', 'tailored', 

    # Miscellaneous
    'most demanding', 'plus offrant'
]

HOME_WORDS = [
    # General Furniture
    'meuble', 'meubles', 'furniture', 'furnitures',
    'ameublement', 'ameublements', 'mobilier', 'mobiliers', 'furnishing', 'furnishings',
    'décoration', 'decorations', 'décor', 'decor', 'decors', 

    # Office Furniture
    'bureau', 'bureaux', 'desk', 'desks', 'table', 'tables', 'office', 'offices',

    # Storage Furniture
    'tiroir', 'tiroirs', 'drawer', 'drawers',
    'dresser', 'dressers', 'commode', 'commodes',
    'armoire', 'armoires', 'cabinet', 'cabinets', 'wardrobe', 'wardrobes',
    'classeur', 'classeurs', 'file cabinet', 'file cabinets',
    'buffet', 'buffets', 'hutch', 'hutches',
    'tablette', 'tablettes', 'étagères', 'étagère', 'shelf', 'shelves',
    'bibliothèque', 'bibliotheque', 'bibliothèques', 'bibliotheques', 'bookshelf', 'bookshelves',
    'bookcase', 'bookcases', 'book case', 'book cases',
    'coffre', 'coffres', 'chest', 'chests',
    'caisson', 'caissons', 'cubby', 'cubbies',
    'panier', 'paniers', 'basket', 'baskets',
    'boîte', 'boîtes', 'box', 'boxes',
    'rangement', 'rangements', 'storage', 'storages',

    # Seating Furniture
    'chaise', 'chaises', 'chair', 'chairs', 'armchair', 'armchairs',
    'ottoman', 'ottomans',
    'sofa', 'sofas', 'divan', 'divans',
    'fauteuil', 'fauteuils', 'futon', 'futons', 'recliner', 'recliners',
    'causeuse', 'causeuses', 'loveseat', 'loveseats',
    'canapé', 'canapés', 'canape',
    'sectionnelle', 'sectionnelles', 'sectional', 'sectionals',
    'couch', 'couches', 
    'tabouret', 'tabourets', 'stool', 'stools',
    'pouf', 'poufs', 'pouffe', 'pouffes',
    'banquette', 'banquettes', 'bench', 'benches',

    # Bedroom
    'lit', 'lits', 'bed', 'beds', 'mattress', 'mattresses',
    'sommier', 'sommeiler', 'matelas',
    'oreiller', 'oreillers', 'pillow', 'pillows', 'pillowcase', 'pillowcases',
    'couette', 'couettes', 'duvet', 'duvets',
    'couverture', 'couvertures', 'coverlet', 'coverlets',
    'drap', 'draps', 'sheet', 'sheets',
    'taie', 'taies', 'sham', 'shams',
    'literie', 'bedding',
    'table de nuit', 'table de nuits', 'nightstand', 'nightstands',
    'vanité', 'vanités', 'vanity', 'vanities',
    'coiffeuse', 'coiffeuses', 'dressing table', 'dressing tables',
    'penderie', 'penderies', 'closet', 'closets',
    'garde-robe', 'garde-robes', 'garde robe', 'garde robes', 'wardrobe', 'wardrobes',
    'coffre-fort', 'coffres-forts', 'safe', 'safes',

    # Lighting
    'lampe', 'lampes', 'lamp', 'lamps', 'lumière', 'lumieres', 'light', 'lights',
    'luminaire', 'luminaires', 'lighting', 
    'plafonnier', 'plafonniers',
    'lustre', 'lustres', 'chandelier', 'chandeliers',
    'lampadaire', 'lampadaires',
    'applique', 'appliques', 'sconce', 'sconces',
    'abat-jour', 'abat-jours', 'lampshade', 'lampshades',
    'ampoule', 'ampoules', 'bulb', 'bulbs',
    'projecteur', 'projecteurs', 'projector', 'projectors',
    'spotlight', 'spotlights',
    'veilleuse', 'veilleuses', 'nightlight', 'nightlights',

    # Kitchen and Appliances
    'cuisine', 'cuisines', 'kitchen', 'kitchens', 'kitchenette', 'kitchenettes',
    'lavabo', 'lavabos', 'évier', 'evier', 'éviers', 'eviers', 'sink', 'sinks',
    'laveuse', 'washer', 'sècheuse', 'dryer', 'laveuse-sécheuse', 'washer-dryer',
    'frigo', 'frigos', 'frigidaire', 'frigidaires', 'réfrigérateur', 'réfrigérateurs',
    'fridge', 'fridges', 'refrigerator', 'refrigerators', 'refrigerateur', 'refrigerateurs',
    'congélateur', 'congélateurs', 'congelateur', 'congelateurs', 'freezer', 'freezers',
    'cuisinière', 'cuisiniere', 'cuisinières', 'cuisinieres', 'stove', 'stoves', 'range', 'ranges',
    'micro-onde', 'microonde', 'micro onde', 'micro-ondes',
    'microondes', 'micro ondes', 'microwave', 'microwaves', 'oven', 'ovens', 
    'lave-vaisselle', 'lave vaisselle', 'lave-vaisselles', 'lave vaisselles', 'dishwasher', 'dishwashers',
    'hotte', 'hottes', 'hood', 'hoods',
    'mixeur', 'mixeurs', 'blender', 'blenders',
    'grille-pain', 'grille pain', 'grille-pains', 'grille pains', 'toaster', 'toasters',
    'cafetière', 'cafetieres', 'coffee maker', 'coffee makers',
    'bouilloire', 'bouilloires', 'kettle', 'kettles',
    'robot culinaire', 'robot culinaires', 'food processor', 'food processors',
    'batteur', 'batteurs', 'beater', 'beaters',
    'mélangeur', 'melangeur', 'mélangeurs', 'melangeurs', 'mixer', 'mixers',
    'cuiseur', 'cuiseurs', 'cooker', 'cookers',
    'grill', 'grills', 'grille', 'grilles',
    'friteuse', 'friteuses', 'fryer', 'fryers',
    'crockpot', 'crockpots', 'slow cooker', 'slow cookers',
    'cuisinart', 'cuisinarts',
    'garde-manger', 'garde-mangers', 'pantry', 'pantries',
    'vaisselier', 'vaisseliers', 'china cabinet', 'china cabinets',

    # Dining and Utensils
    'ustensile', 'ustensiles', 'utensil', 'utensils',
    'vaisselle', 'vaisselles', 'dinnerware', 'tableware', 'dishware',
    'poêle', 'poêles', 'poêlon', 'poêlons', 'pan', 'pans',
    'casserole', 'casseroles', 'pot', 'pots',
    'plat', 'plats', 'dish', 'dishes',
    'assiette', 'assiettes', 'plate', 'plates',
    'bol', 'bols', 'bowl', 'bowls', 'saladier', 'saladiers',
    'verre', 'verres', 'glass', 'glasses',
    'tasse', 'tasses', 'cup', 'cups',
    'couvert', 'couverts', 'cutlery', 'cutleries',
    'couteau', 'couteaux', 'knife', 'knives',
    'fourchette', 'fourchettes', 'fork', 'forks',
    'cuillère', 'cuillères', 'spoon', 'spoons',

    # Miscellaneous
    'foyer', 'foyers', 'fireplace', 'fireplaces', 'cheminée', 'cheminées',
    'rideau', 'rideaux', 'curtain', 'curtains', 'drapery', 'draperies',
    'coussin', 'coussins', 'cushion', 'cushions',
    'toilette', 'toilettes', 'toilet', 'toilets',
    'porte', 'portes', 'door', 'doors',
    'fenêtre', 'fenetres', 'window', 'windows',
    'tapis', 'carpet', 'carpets', 'rug', 'rugs',
    'tableau', 'tableaux', 'tableau', 'tableaux', 'table', 'tables',
    'miroir', 'miroirs', 'mirror', 'mirrors',
    'vitre', 'vitres', 'glass', 'glasses', 'verre', 'verres',
    'cadre', 'cadres', 'frame', 'frames',
    'piscine', 'piscines', 'pool', 'pools',
    'spa', 'spas', 'jacuzzi', 'jacuzzis',
    'sauna', 'saunas', 'sauna',
    'patio', 'patios', 'terrasse', 'terrasses', 'terrace', 'terraces',
    'balcon', 'balcons', 'balcony', 'balconies',
    'jardin', 'jardins', 'garden', 'gardens', 'courtyard', 'courtyards',
    'garage', 'garages', 'parking', 'parkings', 'stationnement', 'stationnements',
    'entrée', 'entrées', 'entrance', 'entrances',
    'escalier', 'escaliers', 'stair', 'stairs',
    'chambre', 'chambres', 'room', 'rooms',
    'salle', 'salles', 'salon', 'salons',
    'bathroom', 'bathrooms',
    'cuisine', 'cuisines', 'kitchen', 'kitchens'
]

WANTED_CATEGORIES = ['Electronics', 'Musical Instruments', 'Sporting Goods', 'Audio Equipment']
WANTED_SPECIFIC_CATEGORIES = ['DVD & Blu-ray Players', 'Desktop Computers', 'Smart Watches', 'CPUs/Processors', 'Pro Audio Equipment', 'Video Games', 'Networking & Servers', 'Tablets & eBook Readers', 'Drums', 'Camping & Hiking']
UNWANTED_CATEGORIES = ['Vehicles', 'Property Rentals', 'Home Sales', 'Rentals']
UNWANTED_SPECIFIC_CATEGORIES = ['Cars & Trucks', 'Commercial Trucks', 'Commercial Vehicles']
HOME_CATEGORIES = ['Home Goods', 'Home Improvement Supplies', 'Garden & Outdoor', 'Pet Supplies', 'Office Supplies', 'Family', 'Toys & Games']

def word_is_in_string(word: str, string_to_check: str) -> bool:
    pattern = re.compile(rf"\b{re.escape(word)}\b", re.IGNORECASE)
    return bool(pattern.search(string_to_check))

def is_unwanted_string(string_to_check: str) -> bool:
    string_to_check = string_to_check.lower().replace('\n', ' ').strip()

    matches = re.finditer(r"(?:\d+(?:\.\d+)?\s*\$|\$\s*\d+(?:\.\d+)?|\$)", string_to_check)
    for match in matches:
        text = match.group()

        if text.strip() == "$":
            return True

        number_match = re.search(r"\d+(?:\.\d+)?", text)
        if number_match:
            value = float(number_match.group())
            if value != 0:
                return True
        
    return any(word_is_in_string(word, string_to_check) for word in UNWANTED_WORDS)

def determine_categories(listings: List) -> List:
    for listing in listings:
        if (
            is_unwanted_string(listing.description) or 
            listing.general_category in UNWANTED_CATEGORIES or 
            listing.specific_category in UNWANTED_SPECIFIC_CATEGORIES
        ):
            listing.is_unwanted = True
        elif (
            listing.general_category in WANTED_CATEGORIES or 
            listing.specific_category in WANTED_SPECIFIC_CATEGORIES
        ):
            listing.is_wanted = True
        elif (
            any(word_is_in_string(word, listing.title) for word in HOME_WORDS) or 
            any(word_is_in_string(word, listing.description) for word in HOME_WORDS) or 
            any(word_is_in_string(word, listing.general_category) for word in HOME_WORDS) or 
            any(word_is_in_string(word, listing.specific_category) for word in HOME_WORDS) or 
            listing.general_category in HOME_CATEGORIES
        ):
            listing.is_home = True
    return listings
