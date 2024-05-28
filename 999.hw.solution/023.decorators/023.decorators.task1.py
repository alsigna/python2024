from time import perf_counter

import requests


def benchmark(repeat_count):
    def _benchmark(func):

        def wrapper(*args, **kwargs):
            total = 0
            for _ in range(repeat_count):
                t0 = perf_counter()
                result = func(*args, **kwargs)
                total += perf_counter() - t0
            print(f"Среднее время выполнения: {total / repeat_count:.5f}сек.")
            return result

        return wrapper

    return _benchmark


@benchmark(10)
def get_url(url):
    result = requests.get(url)


get_url("https://google.com/")
