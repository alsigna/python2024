from typing import Generator


def gen() -> Generator[int, None, None]:
    start = 0
    while True:
        start += 1
        yield pow(start, 2)


async def afoo() -> None:
    print(42)


if __name__ == "__main__":
    g = gen()
    print(g)

    a = afoo()
    print(a)
