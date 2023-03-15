from rocketry import Rocketry
from rocketry.conds import every, after_success
from rocketry.args import Return
import downloader

scheduler = Rocketry()

@scheduler.task(every("5 minutes"))
def do_check() -> str:
    print("Downloading…")
    return downloader.get_page('https://aeon.co/essays/on-nonconformism-or-why-we-need-to-be-seen-and-not-herded')

@scheduler.task(after_success(do_check))
def do_process(page: bytes = Return('do_check')) -> None:
    print("Processing")
    title = downloader.extract(page)
    print(title)
