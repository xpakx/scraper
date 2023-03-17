from rocketry import Rocketry
from rocketry.conds import every, after_success
from rocketry.args import Return
import downloader
import repository
import logging
from publisher import Publisher
from data import PageData
from resolver import PropertyResolver

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = Rocketry()

properties = PropertyResolver()

rabbit = Publisher()
rabbit.connect(properties.rabbit)
rabbit.setup()

@scheduler.task(every("5 minutes"))
def do_check() -> bytes:
    logger.info("Downloading…")
    page: bytes = downloader.get_page(properties.url)
    return page

@scheduler.task(after_success(do_check))
def do_process(page: bytes = Return('do_check')) -> None:
    logger.info("Processing…")
    title = downloader.extract(page)
    changeDetected: bool = repository.test_changes(properties.url, title)
    print(title, '(change detected)' if changeDetected else '')
    if(changeDetected):
        data: PageData = PageData(properties.url, title, 'a')
        rabbit.publish(data)

if __name__ == "__main__":
    logger.info("App started")
    scheduler.run()