import threading
import time
from concurrent.futures import ThreadPoolExecutor


def foo(count: int, flag: bool) -> None:
    thr_name = threading.current_thread().name
    for i in range(count):
        print(f"[{thr_name}]: {i}, flag: {flag}")
        time.sleep(1)


# with ThreadPoolExecutor() as pool:
#     pool.map(foo, (7, 5, 2), (False, True, False))

params = (
    (7, True),
    (5, False),
    (2, True),
)

with ThreadPoolExecutor() as pool:
    pool_map = pool.map(foo, *list(zip(*params)))
