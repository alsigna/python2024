from enum import Enum


class Status(Enum):
    BAD = 0
    OK = 1


def print_result(status: Status) -> None:
    if status == Status.OK:
        print("все хорошо")
    elif status == Status.BAD:
        print("что-то пошло не так")


print_result(Status.OK)
print_result(Status.BAD)
