from datetime import datetime
from time import sleep

# def my_log(msg, *, dt=datetime.now()):
#     print(f"[{dt:%Y-%m-%d %H:%M:%S}]: {msg}")


def my_log(msg, *, dt=None):
    if dt is None:
        dt = datetime.now()
    print(f"[{dt:%Y-%m-%d %H:%M:%S}]: {msg}")


my_log("test")
sleep(2)

# ждем пару секунд ...
my_log("test")
sleep(3)
# еще ждем ...
my_log("test")
