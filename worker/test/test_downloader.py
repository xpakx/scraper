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
    
