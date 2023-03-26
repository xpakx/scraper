from bs4 import BeautifulSoup
import requests
from typing import List
import json
import logging



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def getAreas(url: str) -> List[str]:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', class_='wikitable')
    column_data = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 0:
            column_data.append(cells[0].get_text().strip())
    return column_data

def getListFromFile(name: str) -> List[str]:
    with open(f'data/{name}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_obj(data, name: str) -> None:
    with open(f'data/{name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def get_streets_for_area(name: str) -> List[str]:
    overpass_query = f'''
        [out:json];
        area[name="Osiedle {name}"];
        way(area)["highway"~"^(primary|secondary|tertiary|residential)$"][name];
        out body;
    '''
    response = requests.post("https://overpass-api.de/api/interpreter", data=overpass_query.encode('utf-8'))
    streets = []
    for street in response.json()["elements"]:
        if street['tags'] and street['tags']['name']:
            streets.append(street['tags']['name'])
    return list(set(streets))

logger.info("Getting areas from Wikipedia…")
areas = getAreas('https://pl.wikipedia.org/wiki/Podzia%C5%82_administracyjny_Wroc%C5%82awia')

areas_result = []
streets_result = []


logger.info("Collecting street data with overpass API…")
for area in areas:
    logger.info(f"Collecting data for {area}…")
    streets = get_streets_for_area(area)
    areas_result.append({'area': area, 'streets': streets})
    streets_result.extend(streets)


logger.info("Saving data set…")
streets_result = list(set(streets_result))
result = {'areas': areas_result, 'streets': streets_result, 'street_count': len(streets_result)}
save_obj(result, 'dataset')