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
    with open(f'{name}.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def save_obj(data, name: str) -> None:
    with open(f'{name}.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)


areas = getAreas('https://pl.wikipedia.org/wiki/Podzia%C5%82_administracyjny_Wroc%C5%82awia')
save_obj(areas, 'areas')


