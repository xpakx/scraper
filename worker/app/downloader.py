import requests
from bs4 import BeautifulSoup
from data import ActivityData

def get_page(url: str) -> bytes:
    return requests.get(url).content

def extract(page: bytes) -> str:
    soup = BeautifulSoup(page, "html.parser")
    streets = soup.find("div", {"class": "text-gray-500"})
    return str(streets)

def get_activities(url: str) -> list[ActivityData]:
    soup = BeautifulSoup(get_page(url.format(page=1)), "html.parser")
    activities = soup.find("div", {"id": "activities"}).find_all("a")
    return map(to_activity, activities)

def to_activity(html) -> ActivityData:
    id = html['id']
    date = html.find('h2').text
    distance = html.find('div', {'class' : 'text-gray-500'}).text
    completed = html.find('span').text
    return ActivityData(id, completed, date, distance)
