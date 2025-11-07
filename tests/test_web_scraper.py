import unittest
from unittest.mock import MagicMock, call, patch

from bs4 import BeautifulSoup

from src import web_scraper
from src.listing import Listing


class TestWebScraper(unittest.IsolatedAsyncioTestCase):
    def test_refresh_html_soup_success(self):
        """Test refresh_html_soup with valid HTML."""
        mock_browser = MagicMock()
        mock_browser.page_source = "<html><body><h1>Test</h1></body></html>"
        soup = web_scraper.refresh_html_soup(mock_browser)
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.find("h1").text, "Test")

    def test_refresh_html_soup_fallback_to_lxml(self):
        """Test refresh_html_soup falls back to lxml on html.parser failure."""
        mock_browser = MagicMock()
        mock_browser.page_source = "<html><body><h1>Test</h1></body></html>"
        with patch("src.web_scraper.BeautifulSoup") as mock_bs:
            # Simulate html.parser failure
            mock_bs.side_effect = [Exception("html.parser failed"), BeautifulSoup("<html></html>", "html.parser")]
            web_scraper.refresh_html_soup(mock_browser)
            # Should call BeautifulSoup twice: once with html.parser, once with lxml
            self.assertEqual(mock_bs.call_count, 2)

    @patch("src.web_scraper.webdriver.Firefox")
    def test_create_firefox_driver(self, mock_firefox):
        """Test create_firefox_driver creates a Firefox driver."""
        driver = web_scraper.create_firefox_driver()
        mock_firefox.assert_called_once()
        self.assertIsNotNone(driver)

    @patch("src.web_scraper.webdriver.Firefox")
    def test_open_firefox_to_marketplace_free_items_page(self, mock_firefox):
        """Test open_firefox_to_marketplace_free_items_page navigates to URL."""
        mock_driver = MagicMock()
        mock_firefox.return_value = mock_driver
        with patch("src.web_scraper.create_firefox_driver", return_value=mock_driver):
            driver = web_scraper.open_firefox_to_marketplace_free_items_page()
            mock_driver.get.assert_called_with(
                "https://www.facebook.com/marketplace/montreal/free/?sortBy=creation_time_descend"
            )
            self.assertEqual(driver, mock_driver)

    async def test_close_log_in_popup(self):
        """Test close_log_in_popup uses WebDriverWait to find close button."""
        mock_browser = MagicMock()
        mock_element = MagicMock()

        with patch("src.web_scraper.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_element
            await web_scraper.close_log_in_popup(mock_browser)
            # Should have called WebDriverWait with browser
            mock_wait.assert_called()
            mock_element.click.assert_called_once()

    async def test_close_log_in_popup_no_popup(self):
        """Test close_log_in_popup logs warning if no popup found."""
        mock_browser = MagicMock()

        with patch("src.web_scraper.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.side_effect = Exception("No element found")
            with patch("src.web_scraper.logger") as mock_logger:
                await web_scraper.close_log_in_popup(mock_browser)
                # Should log warning when no popup found
                mock_logger.warning.assert_called()

    async def test_scroll_bottom_page(self):
        """Test scroll_bottom_page executes JavaScript."""
        mock_browser = MagicMock()
        await web_scraper.scroll_bottom_page(mock_browser)
        # Function calls execute_script multiple times; check that the scroll call is present
        self.assertIn(
            call("window.scrollTo(0, document.body.scrollHeight);"), mock_browser.execute_script.call_args_list
        )

    async def test_click_see_more_description(self):
        """Test click_see_more_description tries to find and click See more button."""
        mock_browser = MagicMock()
        mock_see_more_div = MagicMock()
        mock_span = MagicMock()
        mock_see_more_div.find_element.return_value = mock_span
        mock_browser.find_element.return_value = mock_see_more_div

        with patch("src.web_scraper.WebDriverWait") as mock_wait:
            mock_wait.return_value.until.return_value = mock_span
            await web_scraper.click_see_more_description(mock_browser)
            # Should attempt to click the span element
            self.assertTrue(mock_span.click.called or mock_browser.execute_script.called)

    def test_get_listings_full_description_found(self):
        """Test get_listings_full_description finds matching description in spans."""
        # Function looks for description text (minus last 3 chars) in span elements
        html = "<span>This is a long description tex</span><span>Other text</span>"
        soup = BeautifulSoup(html, "html.parser")
        result = web_scraper.get_listings_full_description(soup, "This is a long description text")
        self.assertIsNotNone(result)
        self.assertIn("description tex", result.text)

    def test_get_listings_full_description_not_found(self):
        """Test get_listings_full_description returns None if no match."""
        html = "<span>Other text</span><span>More text</span>"
        soup = BeautifulSoup(html, "html.parser")
        result = web_scraper.get_listings_full_description(soup, "Full description text")
        self.assertIsNone(result)

    def test_fill_listings_general_category(self):
        """Test fill_listings_general_category extracts category from marketplace link."""
        # Function looks for <a> tag with href pattern /marketplace/[0-9]+/[\w-]+/
        html = '<a href="/marketplace/123456/electronics/">Electronics</a>'
        soup = BeautifulSoup(html, "html.parser")
        listing = Listing()
        result = web_scraper.fill_listings_general_category(listing, soup)
        self.assertEqual(result.general_category, "Electronics")

    def test_fill_listings_specific_category(self):
        """Test fill_listings_specific_category extracts from title tag."""
        # Function parses title tag: looks for text between last two " - " separators
        # Format: "Title - Category - Location - Facebook"
        # It finds last index of " - " then second-to-last index, extracts between them
        html = "<html><head><title>Listing Title - CPUs/Processors - Location</title></head></html>"
        soup = BeautifulSoup(html, "html.parser")
        listing = Listing()
        result = web_scraper.fill_listings_specific_category(listing, soup)
        self.assertEqual(result.specific_category, "CPUs/Processors")

    async def test_fill_listings_description(self):
        """Test fill_listings_description extracts from meta description tag."""
        # Function looks for meta tag with name="description"
        html = '<html><head><meta name="description" content="Test description for listing"></head></html>'
        soup = BeautifulSoup(html, "html.parser")
        mock_browser = MagicMock()
        listing = Listing()
        result = await web_scraper.fill_listings_description(listing, soup, mock_browser)
        self.assertEqual(result.description, "Test description for listing")

    @patch("src.web_scraper.refresh_html_soup")
    async def test_fill_listings_informations(self, mock_refresh):
        """Test fill_listings_informations processes listings."""
        mock_soup = MagicMock()
        mock_refresh.return_value = mock_soup
        listings = [Listing()]
        mock_browser = MagicMock()
        result = await web_scraper.fill_listings_informations(listings, mock_browser)
        self.assertEqual(len(result), 1)
        mock_refresh.assert_called()

    def test_filter_previous_listings(self):
        """Test filter_previous_listings marks previous listings and checks unwanted titles."""
        # Function expects previous_listings to be a list of URLs (strings), not Listing objects
        previous = ["https://www.facebook.com/marketplace/item/old_url"]
        current = [
            Listing(url="https://www.facebook.com/marketplace/item/new_url", title="Free chair"),
            Listing(url="https://www.facebook.com/marketplace/item/old_url", title="Free table"),
        ]
        result = web_scraper.filter_previous_listings(previous, current)
        # Returns all listings but marks is_previous flag
        self.assertEqual(len(result), 2)
        self.assertTrue(result[1].is_previous)
        self.assertFalse(result[0].is_previous)

    @patch("src.web_scraper.refresh_html_soup")
    def test_extract_listings_informations_from_home_page(self, mock_refresh):
        """Test extract_listings_informations_from_home_page extracts listings from links."""
        html = """
        <a href="/marketplace/item/123456">
            <img src="http://example.com/img.jpg"/>
            <div>
                <span>Free</span>
                <span>Test Listing Title</span>
                <span>Montreal, QC</span>
            </div>
        </a>
        """
        mock_refresh.return_value = BeautifulSoup(html, "html.parser")
        mock_browser = MagicMock()

        listings = web_scraper.extract_listings_informations_from_home_page(mock_browser)

        self.assertIsInstance(listings, list)
        self.assertEqual(len(listings), 1)
        self.assertEqual(listings[0].title, "Test Listing Title")
        self.assertEqual(listings[0].location, "Montreal, QC")
        self.assertIn("/marketplace/item/123456", listings[0].url)


if __name__ == "__main__":
    unittest.main()
