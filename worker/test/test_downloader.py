from app.downloader import extract

def test_extract():
    output = extract("<html><title>Title</title></html>")
    assert output == 'Title'