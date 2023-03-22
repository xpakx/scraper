from app.downloader import CityStridesDownloader
from test.resolver import EmptyPropertyResolver
import unittest
from unittest.mock import patch

class TestDownloader(unittest.TestCase):
    def test_extract_should_return_result(self):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        output = downloader.extract("<html><body><div class='text-gray-500'>Test</div></body></html>")
        assert 'Test' in output

    def test_extract_should_return_none(self):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        output = downloader.extract("<html><body><div>Test</div></body></html>")
        assert output == None

    def test_extract_should_return_first_result(self):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        output = downloader.extract("<html><body><div class='text-gray-500'>First</div><div class='text-gray-500'>Second</div></body></html>")
        assert 'First' in output
        assert not 'Second' in output

    def test_extract_returns_string(self):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        output = downloader.extract("<html><body><div class='text-gray-500'>Test</div></body></html>")
        assert isinstance(output, str)

    @patch('requests.get')
    def test_get_page(self, mock_get):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        mock_response = "<html><title>Test</title></html>"
        mock_get.return_value.content = mock_response
        expected_content = mock_response
        activities = downloader.get_page('http://example.com')
        assert activities == expected_content

    @patch('requests.get')
    def test_get_profile(self, mock_get):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        mock_response = "<html><title>Test</title></html>"
        mock_get.return_value.content = mock_response
        expected_content = mock_response
        activities = downloader.get_page('http://example.com')
        assert activities == expected_content