from types import TracebackType
from typing import Self, Type


class RedisPool:
    def __init__(self):
        self._session = None

    def connect(self):
        if self._session is None:
            print("first call, need to create connection...")
            self._session = "some redis session"
        else:
            print("session already exists, no need to connect")

    def disconnect(self):
        print("closing session...")
        self._session = None

    def get_data(self) -> int:
        if self._session is None:
            raise Exception("no active session")
        return 42

    def __enter__(self) -> Self:
        if self._session is None:
            self.connect()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool:
        print(f"{exc_type=}")
        print(f"{exc_val=}")
        print(f"{exc_tb=}")
        self.disconnect()
        return False


print("-" * 10, "test 1")
try:
    with RedisPool() as r:
        data = r.get_data()
except Exception as exc:
    print(f"error here: name: '{exc.__class__.__name__}', text: '{exc}'")
else:
    print("no errors")
    print(f"{data=}")

print("-" * 10, "test 2")
try:
    with RedisPool() as r:
        raise ValueError("test")
except Exception as exc:
    print(f"error here: name: '{exc.__class__.__name__}', text: '{exc}'")
else:
    print("no errors")
