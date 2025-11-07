# pylint: disable=too-few-public-methods,import-error
"""Tests for data filtering functionality."""

import unittest

from listing import Listing
from src import data_filtering


class TestDataFiltering(unittest.TestCase):
    """Test cases for data filtering functions."""

    def test_is_unwanted_string_with_iso(self):
        """Test that ISO string is unwanted."""
        self.assertTrue(data_filtering.is_unwanted_string("ISO: some item"))
        self.assertTrue(data_filtering.is_unwanted_string("iso something"))

    def test_is_unwanted_string_with_wtb(self):
        """Test that WTB string is unwanted."""
        self.assertTrue(data_filtering.is_unwanted_string("WTB: gaming console"))
        self.assertTrue(data_filtering.is_unwanted_string("wtb laptop"))

    def test_is_unwanted_string_with_wanted(self):
        """Test that 'wanted' string is unwanted."""
        self.assertTrue(data_filtering.is_unwanted_string("wanted: furniture"))
        self.assertTrue(data_filtering.is_unwanted_string("Wanted bike"))

    def test_is_unwanted_string_normal_title(self):
        """Test that normal titles are not unwanted."""
        self.assertFalse(data_filtering.is_unwanted_string("Free couch"))
        self.assertFalse(data_filtering.is_unwanted_string("Table for sale"))

    def test_determine_categories_with_electronics(self):
        """Test electronics category detection."""
        listing = Listing(
            title="laptop",
            location="Montreal",
            url="http://test.com",
            img_url="",
        )
        listing.description = "old laptop"
        listing.general_category = "Electronics"
        listing.specific_category = "Computers"

        listings = data_filtering.determine_categories([listing])
        self.assertTrue(listings[0].is_wanted)

    def test_determine_categories_with_furniture(self):
        """Test furniture category detection."""
        listing = Listing(
            title="chair",
            location="Montreal",
            url="http://test.com",
            img_url="",
        )
        listing.description = "wooden chair"
        listing.general_category = "Furniture"
        listing.specific_category = "Chairs"

        listings = data_filtering.determine_categories([listing])
        self.assertTrue(listings[0].is_home)

    def test_determine_categories_with_misc(self):
        """Test miscellaneous category detection."""
        listing = Listing(
            title="random item",
            location="Montreal",
            url="http://test.com",
            img_url="",
        )
        listing.description = "some random thing"
        listing.general_category = "Other"
        listing.specific_category = "Miscellaneous"

        listings = data_filtering.determine_categories([listing])
        self.assertFalse(listings[0].is_wanted)
        self.assertFalse(listings[0].is_home)


if __name__ == "__main__":
    unittest.main()
