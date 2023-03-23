from rocketry import Rocketry 
from rocketry.conds import every, after_success
from rocketry.args import Return
from downloader import CityStridesDownloader
import repository
import logging
from publisher import Publisher
from data import ActivityData
from resolver import PropertyResolver
from exceptions import ExtractionException
from typing import List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = Rocketry()

properties = PropertyResolver()
downloader = CityStridesDownloader(properties)
repo = repository.PageRepository(properties.db_url)

rabbit = Publisher()
rabbit.connect(properties.rabbit, properties.rabbit_port)
rabbit.setup()

@scheduler.task(every("5 minutes"))
def do_check() -> bytes:
    logger.info("Downloading…")
    page: bytes = downloader.get_profile()
    return page

@scheduler.task(after_success(do_check))
def do_process(page: bytes = Return('do_check')) -> None:
    logger.info("Processing…")
    text = downloader.extract(page)
    if(text is None):
        raise ExtractionException()
    changeDetected: bool = repo.test_changes(properties.url, text)
    if(changeDetected):
        logger.info("Change detected")
        activities: List[ActivityData] = downloader.get_activities()
        rabbit.publish_all(activities)

if __name__ == "__main__":
    logger.info("App started")
    scheduler.run()