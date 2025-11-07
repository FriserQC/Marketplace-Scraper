"""Listing data class for Facebook Marketplace items."""


class Listing:
    """Represents a facebook marketplace listing with title, location, URL, category, description, etc."""

    def __init__(
        self,
        title: str = "",
        location: str = "",
        url: str = "",
        img_url: str = "",
        general_category: str = "",
        specific_category: str = "",
        description: str = "",
    ):
        self.title = title
        self.location = location
        self.url = url
        self.img_url = img_url
        self.general_category = general_category
        self.specific_category = specific_category
        self.description = description
        self.is_previous = False
        self.is_unwanted = False
        self.is_wanted = False
        self.is_home = False
