class Listing:
    # Represents a facebook marketplace listing with title, location, URL, category, description, etc.

    def __init__(self, title: str, location: str, url: str):
        self.title: str = title
        self.location: str = location
        self.url: str = url
        self.general_category: str = ""
        self.specific_category: str = ""
        self.description: str = ""
        self.is_unwanted: bool = False
        self.is_wanted: bool = False
        self.is_home: bool = False
        self.is_previous: bool = False