class Listing:
    # Represents a facebook marketplace listing with title, location, URL, category, description, etc.

    def __init__(self, title, location, url):
        self.title = title
        self.location = location
        self.url = url
        self.category = ""
        self.description = ""
        self.is_furniture = False
        self.is_unwanted = False
        self.is_previous = False
