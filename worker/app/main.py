from rocketry import Rocketry
from rocketry.conds import every, after_success
from rocketry.args import Return
import downloader
import repository
import logging
from publisher import Publisher

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = Rocketry()
url = 'https://aeon.co/essays/on-nonconformism-or-why-we-need-to-be-seen-and-not-herded'

rabbit = Publisher()
rabbit.connect()
rabbit.setup()


@scheduler.task(every("5 minutes"))
def do_check() -> bytes:
    logger.info("Downloading…")
    page: bytes = downloader.get_page(url)
    return page

@scheduler.task(after_success(do_check))
def do_process(page: bytes = Return('do_check')) -> None:
    logger.info("Processing…")
    title = downloader.extract(page)
    changeDetected: bool = repository.test_changes(url, title)
    print(title, '(change detected)' if changeDetected else '')

if __name__ == "__main__":
    logger.info("App started")
    scheduler.run()