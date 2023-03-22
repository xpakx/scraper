from app.downloader import CityStridesDownloader
from test.resolver import EmptyPropertyResolver

def test_extract():
    downloader = CityStridesDownloader(EmptyPropertyResolver())
    output = downloader.extract("<html><body><div class='text-gray-500'>Test</div></body></html>")
    assert 'Test' in output