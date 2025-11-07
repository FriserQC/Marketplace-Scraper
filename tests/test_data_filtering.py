import unittest

from src import data_filtering
from src.listing import Listing


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
        self.assertFalse(data_filtering.is_unwanted_string("Completely free item!"))

    def test_determine_categories_unwanted(self):
        listing = Listing(description="This is for sale", general_category="Vehicles", specific_category="")
        listings = [listing]
        data_filtering.determine_categories(listings)
        self.assertTrue(listing.is_unwanted)
        self.assertFalse(listing.is_wanted)
        self.assertFalse(listing.is_home)

    def test_determine_categories_wanted(self):
        listing = Listing(
            description="Brand new CPU", general_category="Electronics", specific_category="CPUs/Processors"
        )
        listings = [listing]
        data_filtering.determine_categories(listings)
        self.assertTrue(listing.is_wanted)
        self.assertFalse(listing.is_unwanted)
        self.assertFalse(listing.is_home)

    def test_determine_categories_home(self):
        listing = Listing(
            title="Beautiful sofa",
            description="Comfortable and stylish",
            general_category="Home Goods",
            specific_category="",
        )
        listings = [listing]
        data_filtering.determine_categories(listings)
        self.assertTrue(listing.is_home)
        self.assertFalse(listing.is_unwanted)
        self.assertFalse(listing.is_wanted)

    # --- New tests added below ---

    def test_word_is_in_string_boundaries_and_case(self):
        self.assertTrue(data_filtering.word_is_in_string("Sale", "Huge SALE now"))
        self.assertFalse(data_filtering.word_is_in_string("sale", "raisesales"))
        self.assertFalse(data_filtering.word_is_in_string("table", "vegetable"))

    def test_is_unwanted_string_iso_wtb_wanted_variations(self):
        self.assertTrue(data_filtering.is_unwanted_string("ISO: looking for a bike"))
        self.assertTrue(data_filtering.is_unwanted_string("wtb gaming console"))
        self.assertTrue(data_filtering.is_unwanted_string("Wanted: old textbooks"))
        self.assertTrue(data_filtering.is_unwanted_string("isolation sale"))
        self.assertFalse(data_filtering.is_unwanted_string("eagerlywtbought"))

    def test_listing_defaults_and_mutation(self):
        listing = Listing()
        # defaults
        self.assertEqual(listing.title, "")
        self.assertEqual(listing.description, "")
        self.assertFalse(listing.is_unwanted)
        # mutation
        listing.description = "WTB: monitor"
        self.assertEqual(listing.description, "WTB: monitor")

    def test_determine_categories_marks_iso_wtb_as_unwanted(self):
        listing1 = Listing(description="ISO for a laptop", general_category="Electronics", specific_category="")
        listing2 = Listing(description="WTB: sofa", general_category="Home Goods", specific_category="")
        listings = [listing1, listing2]
        data_filtering.determine_categories(listings)
        self.assertTrue(listing1.is_unwanted)
        self.assertTrue(listing2.is_unwanted)
        self.assertFalse(listing1.is_wanted)
        self.assertFalse(listing2.is_wanted)

    def test_title_triggers_unwanted_even_if_description_clean(self):
        title = "$25 Office Chair"
        desc = "Lightly used, no smoke"
        self.assertTrue(data_filtering.is_unwanted_string(title))
        listing = Listing(title=title, description=desc, general_category="Home Goods", specific_category="")
        data_filtering.determine_categories([listing])
        self.assertTrue(listing.is_unwanted)
        self.assertFalse(listing.is_wanted)

    def test_description_triggers_unwanted_even_if_title_clean(self):
        title = "Cozy couch"
        desc = "WTB: replacement cushions"
        self.assertTrue(data_filtering.is_unwanted_string(desc))
        listing = Listing(title=title, description=desc, general_category="Home Goods", specific_category="")
        data_filtering.determine_categories([listing])
        self.assertTrue(listing.is_unwanted)
        self.assertFalse(listing.is_wanted)

    def test_zero_amount_in_title_not_unwanted(self):
        title = "Free table $0"
        desc = "Pick up only"
        # zero amount should not be flagged as unwanted
        self.assertFalse(data_filtering.is_unwanted_string(title))
        listing = Listing(title=title, description=desc, general_category="Home Goods", specific_category="")
        data_filtering.determine_categories([listing])
        self.assertFalse(listing.is_unwanted)

    def test_embedded_currency_like_text_not_unwanted(self):
        title = "Great deal on dollar store items"
        desc = "Many $ signs but no numeric price"
        # Should not be flagged because no standalone price number
        self.assertTrue(data_filtering.is_unwanted_string(title))
        self.assertTrue(data_filtering.is_unwanted_string(desc))


if __name__ == "__main__":
    unittest.main()
