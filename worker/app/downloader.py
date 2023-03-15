import requests
from bs4 import BeautifulSoup

def get_page(url: str) -> bytes:
    return requests.get(url).content

def extract(page: bytes) -> str:
    soup = BeautifulSoup(page, "html.parser")
    return str(soup.title.text)

