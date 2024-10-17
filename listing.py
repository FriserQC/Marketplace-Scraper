from data_filtering import word_is_in_string

FURNITURE_WORDS = ['meuble', 'meubles', 'furniture', 'furnitures',
                   'bureau', 'bureaux', 'desk', 'desks', 
                   'tiroir', 'tiroirs', 'drawer', 'drawers',
                   'chaise', 'chaises', 'chair', 'chairs',
                   'commode', 'commodes', 'ottoman', 
                   'sofa', 'sofas', 'divan', 'divans', 'fauteuil', 'fauteuils', 'canapé', 'canapés', 'canape', 'sectionnelle', 'sectionnelles', 'sectional', 'couch', 'couchs',
                   'bed', 'beds', 'lit', 'lits', 
                   'table', 'tables', 
                   'lampe', 'lampes', 'lamp', 'lamps',
                   'sommier', 'sommeiler', 'matelas',
                   'laveuse', 'washer', 'sècheuse', 'dryer',
                   'frigo', 'frigidaire', 'fridge', 'refrigerator',
                   'bibliothèque', 'bibliotheque',
                   'foyer', 'fireplace',
                   'armoire', 'armoires',
                   'tablette', 'tablettes', 'étagères', 'étagère',
                   'rideau', 'rideaux', 'curtain', 'curtains',
                   'coffre', 
                   'miroir', 'mirror',
                   'piano',
                   'buffet']

class Listing():

    def __init__(self, title, location, url):
        self.title = title
        self.location = location
        self.url = url
        self.description = ""
        self.isFurniture = False
        self.isUnwanted = False
        self.isPrevious = False

    def is_furniture(self):
        for word in FURNITURE_WORDS:
            if word_is_in_string(word, self.description) or word_is_in_string(word, self.title):
                self.isFurniture = True


    
