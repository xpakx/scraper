from app.downloader import CityStridesDownloader
from test.resolver import EmptyPropertyResolver

def test_extract_should_return_result():
    downloader = CityStridesDownloader(EmptyPropertyResolver())
    output = downloader.extract("<html><body><div class='text-gray-500'>Test</div></body></html>")
    assert 'Test' in output

def test_extract_should_return_none():
    downloader = CityStridesDownloader(EmptyPropertyResolver())
    output = downloader.extract("<html><body><div>Test</div></body></html>")
    assert output == None

def test_extract_should_return_first_result():
    downloader = CityStridesDownloader(EmptyPropertyResolver())
    output = downloader.extract("<html><body><div class='text-gray-500'>First</div><div class='text-gray-500'>Second</div></body></html>")
    assert 'First' in output
    assert not 'Second' in output

def test_extract_returns_string():
    downloader = CityStridesDownloader(EmptyPropertyResolver())
    output = downloader.extract("<html><body><div class='text-gray-500'>Test</div></body></html>")
    assert isinstance(output, str)
