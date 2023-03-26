from app.repository import StreetRepository
import json
import os
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataInit():
    def test(self, datafile: str, repo: StreetRepository) -> bool:
        return os.path.exists(datafile) and not repo.has_areas_data()

    def populate(self, datafile: str, repo: StreetRepository) -> None:
        data = {}
        logger.info("Reading file from area data…")
        with open(datafile, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info("Saving areas…")
        repo.add_area_data(data['areas'])
        logger.info("Saving streets")
        repo.add_street_data(data['streets'])