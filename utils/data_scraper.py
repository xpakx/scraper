from bs4 import BeautifulSoup
import requests
from typing import List
import json

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

def getAreasFromFile(name: str) -> List[str]:
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


'''
areas = getAreas('https://pl.wikipedia.org/wiki/Podzia%C5%82_administracyjny_Wroc%C5%82awia')
save_obj(areas, 'areas')
'''

areas = getAreasFromFile('areas')

for area in areas:
    streets = get_streets_for_area(area)
    save_obj(streets, area.replace(' ', '_').lower())
