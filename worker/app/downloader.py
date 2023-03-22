import requests
from bs4 import BeautifulSoup
from app.data import ActivityData
from app.data import Street
from app.resolver import PropertyResolver
from typing import List, Optional


class CityStridesDownloader:
    def __init__(self, properties: PropertyResolver):
        self.url = properties.url
        self.activities_url = properties.activities_url
        self.streets_url = properties.streets_url

    def get_page(self, url) -> bytes:
        return requests.get(url).content
    
    def get_profile(self) -> bytes:
        return self.get_page(self.url)

    def extract(self, page: bytes) -> Optional[str]:
        soup = BeautifulSoup(page, "html.parser")
        streets = soup.find("div", {"class": "text-gray-500"})
        if streets == None:
            return None
        return str(streets)

    def get_activities(self) -> List[ActivityData]:
        soup = BeautifulSoup(self.get_page(self.activities_url.format(page=1)), "html.parser")
        activities = soup.find("div", {"id": "activities"}).find_all("a")
        return map(self.to_activity, activities)

    def to_activity(self, html) -> ActivityData:
        id = html['id'].strip().replace('activity_', '')
        date = html.find('h2').text.strip()
        distance = html.find('div', {'class' : 'text-gray-500'}).text.strip()
        completed = html.find('span').text.strip()
        streets = list(self.get_streets(id))
        return ActivityData(id, completed, date, distance, streets)

    def get_streets(self, activity_id: str) -> List[Street]:
        soup = BeautifulSoup(self.get_page(self.streets_url.format(page=1, id=activity_id)), "html.parser")
        streets = soup.select("[id^=street_]")
        return map(self.to_street, streets)
    
    def to_street(self, html) -> Street:
        street_name = html.find('div', {'class' : 'font-medium'}).text
        city_name = html.find('div', {'class' : 'font-light'}).text
        return Street(street_name, city_name)
