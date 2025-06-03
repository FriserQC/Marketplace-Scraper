import unittest
from src import data_filtering

class DummyListing:
    def __init__(self, title="", description="", general_category="", specific_category=""):
        self.title = title
        self.description = description
        self.general_category = general_category
        self.specific_category = specific_category
        self.is_unwanted = False
        self.is_wanted = False
        self.is_home = False

class TestDataFiltering(unittest.TestCase):
    def test_word_is_in_string(self):
        self.assertTrue(data_filtering.word_is_in_string("sale", "Big sale today!"))
        self.assertFalse(data_filtering.word_is_in_string("sale", "Big sailing event!"))

    def test_is_unwanted_string(self):
        self.assertTrue(data_filtering.is_unwanted_string("Listing for $10!"))
        self.assertTrue(data_filtering.is_unwanted_string("12 Listing for $!"))
        self.assertTrue(data_filtering.is_unwanted_string("Listing for $! 12"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for $0!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for 0$!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for 0 $!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for $ 0!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for 0.0 $!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for $ 0.0!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for 0. 0 $!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for $ 0. 0!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for 0 .0 $!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for $ 0 .0!"))
        self.assertFalse(data_filtering.is_unwanted_string("12 Listing for 0 $!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for $ 0! 12"))
        self.assertFalse(data_filtering.is_unwanted_string("12 Listing for $ 0!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for 0 $! 12"))
        self.assertFalse(data_filtering.is_unwanted_string("12 Listing for $ 0nice!"))
        self.assertFalse(data_filtering.is_unwanted_string("Listing for0 $! 12"))
        self.assertFalse(data_filtering.is_unwanted_string("Completely free item!"))

    def test_determine_categories_unwanted(self):
        listing = DummyListing(description="This is for sale", general_category="Vehicles", specific_category="")
        listings = [listing]
        data_filtering.determine_categories(listings)
        self.assertTrue(listing.is_unwanted)
        self.assertFalse(listing.is_wanted)
        self.assertFalse(listing.is_home)

    def test_determine_categories_wanted(self):
        listing = DummyListing(description="Brand new CPU", general_category="Electronics", specific_category="CPUs/Processors")
        listings = [listing]
        data_filtering.determine_categories(listings)
        self.assertTrue(listing.is_wanted)
        self.assertFalse(listing.is_unwanted)
        self.assertFalse(listing.is_home)

    def test_determine_categories_home(self):
        listing = DummyListing(title="Beautiful sofa", description="Comfortable and stylish", general_category="Home Goods", specific_category="")
        listings = [listing]
        data_filtering.determine_categories(listings)
        self.assertTrue(listing.is_home)
        self.assertFalse(listing.is_unwanted)
        self.assertFalse(listing.is_wanted)

if __name__ == "__main__":
    unittest.main()