from rocketry import Rocketry
from rocketry.conds import every, after_success
from rocketry.args import Return

scheduler: Rocketry = Rocketry()

@scheduler.task(every("5 minutes"))
def do_check() -> any:
    print("Check")

@scheduler.task(after_success(do_check))
def do_process(arg = Return('do_check')) -> any:
    print("Process")

