from data_filtering import word_is_in_string

FURNITURE_WORDS = ['meuble', 'meubles', 'furniture', 'furnitures',
                   'bureau', 'bureaux', 'desk', 'desks', 
                   'chaise', 'chaises', 'chair', 'chairs',
                   'commode', 'commodes', 'ottoman', 
                   'sofa', 'sofas', 'divan', 'divans', 'fauteuil', 'fauteuils', 'canapé', 'canapés', 'sectionnelle', 'sectionnelles', 'couch', 'couchs',
                   'bed', 'beds', 'lit', 'lits', 
                   'table', 'tables', 
                   'lampe', 'lampes', 'lamp', 'lamps']

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


    
