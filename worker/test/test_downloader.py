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

    @patch('requests.get')
    def test_get_activities(self, mock_get):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        mock_response = """
        <div id="activities">
            <a id="activity_1">
                <h2>date 1</h2>
                <div class="text-gray-500">10 miles</div>
                <span>5</span>
            </a>
            <a id="activity_2">
                <h2>date 2</h2>
                <div class="text-gray-500">5 miles</div>
                <span>2</span>
            </a>
        </div>
        """
        mock_get.return_value.content = mock_response

        activities = list(downloader.get_activities())
        assert len(activities) == 2
        assert activities[0].id == '1'
        assert activities[0].completed_streets == '5'
        assert activities[0].date == 'date 1'
        assert activities[0].distance == '10 miles'
        assert activities[1].id == '2'
        assert activities[1].completed_streets == '2'
        assert activities[1].date == 'date 2'
        assert activities[1].distance == '5 miles'

    @patch('requests.get')
    def test_get_activities_when_activity_list_empty(self, mock_get):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        mock_response = """
        <div id="activities">
        </div>
        """
        mock_get.return_value.content = mock_response

        activities = list(downloader.get_activities())
        assert len(activities) == 0

    
    @patch('requests.get')
    def test_get_streets(self, mock_get):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        mock_response = """
        <div id="street_1">
            <div class="font-medium">Street 1</div>
            <div class="font-light">City 1</div>
        </div>
        <div id="street_2">
            <div class="font-medium">Street 2</div>
            <div class="font-light">City 1</div>
        </div>
        """
        mock_get.return_value.content = mock_response

        activities = list(downloader.get_streets("1"))
        assert len(activities) == 2
        assert activities[0].name == 'Street 1'
        assert activities[0].city_name == 'City 1'
        assert activities[1].name == 'Street 2'
        assert activities[1].city_name == 'City 1'

    @patch('requests.get')
    def test_get_streets_when_activity_list_empty(self, mock_get):
        downloader = CityStridesDownloader(EmptyPropertyResolver())
        mock_response = ""
        mock_get.return_value.content = mock_response

        activities = list(downloader.get_streets("1"))
        assert len(activities) == 0  