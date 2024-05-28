from time import perf_counter, sleep


def timer():
    start = perf_counter()

    def inner():
        nonlocal start
        print(f"{perf_counter() - start:.2f}сек.")
        start = perf_counter()

    return inner


t = timer()

t()
sleep(2)
t()
sleep(3)
t()
