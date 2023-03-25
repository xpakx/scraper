import requests
from bs4 import BeautifulSoup, Tag
from data import ActivityData
from data import Street
from resolver import PropertyResolver
from typing import List, Optional, Any
from datetime import datetime


class CityStridesDownloader():
    def __init__(self, properties: PropertyResolver):
        self.url = properties.url
        self.activities_url = properties.activities_url
        self.streets_url = properties.streets_url

    def get_page(self, url: str) -> bytes:
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
        activity_list = soup.find("div", {"id": "activities"})
        assert isinstance(activity_list, Tag)
        activities = activity_list.find_all("a")
        return list(map(self.to_activity, activities))

    def to_activity(self, html: Any) -> ActivityData:
        id = html['id'].strip().replace('activity_', '')
        date = self.transform_date(html.find('h2').text.strip())
        distance = self.distance_to_km(html.find('div', {'class' : 'text-gray-500'}).text.strip())
        completed = html.find('span').text.strip()
        streets = self.get_streets(id)
        return ActivityData(id, completed, date, distance, streets)
    
    def distance_to_km(self, distance: str) -> str:
        miles = distance.replace('miles', '').strip()
        dist_in_km = float(miles) * 1.60934
        return '{km:.2f}'.format(km = dist_in_km)
    
    def transform_date(self, date: str) -> str:
        return datetime.strptime(date, "%B %d, %Y").strftime("%d-%m-%Y")

    def get_streets(self, activity_id: str) -> List[Street]:
        soup = BeautifulSoup(self.get_page(self.streets_url.format(page=1, id=activity_id)), "html.parser")
        streets = soup.select("[id^=street_]")
        return list(map(self.to_street, streets))
    
    def to_street(self, html: Any) -> Street:
        street_name = html.find('div', {'class' : 'font-medium'}).text
        city_name = html.find('div', {'class' : 'font-light'}).text
        return Street(street_name, city_name)
