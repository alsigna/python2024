import threading
import time


def foo(count: int) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}")
        time.sleep(1)


thr1 = threading.Timer(
    interval=10,
    function=foo,
    args=(5,),
)


thr1.start()
