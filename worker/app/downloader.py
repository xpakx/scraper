import requests
from bs4 import BeautifulSoup
from data import ActivityData
from resolver import PropertyResolver

class CityStridesDownloader:
    def __init__(self, properties: PropertyResolver):
        self.url = properties.url
        self.activities_url = properties.activities_url
        self.streets_url = properties.streets_url

    def get_page(self, url) -> bytes:
        return requests.get(url).content
    
    def get_profile(self) -> bytes:
        return self.get_page(self.url)

    def extract(self, page: bytes) -> str:
        soup = BeautifulSoup(page, "html.parser")
        streets = soup.find("div", {"class": "text-gray-500"})
        return str(streets)

    def get_activities(self) -> list[ActivityData]:
        soup = BeautifulSoup(self.get_page(self.activities_url.format(page=1)), "html.parser")
        activities = soup.find("div", {"id": "activities"}).find_all("a")
        return map(self.to_activity, activities)

    def to_activity(self, html) -> ActivityData:
        id = html['id']
        date = html.find('h2').text
        distance = html.find('div', {'class' : 'text-gray-500'}).text
        completed = html.find('span').text
        return ActivityData(id, completed, date, distance)
