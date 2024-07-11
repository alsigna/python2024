from enum import auto

from strenum import LowercaseStrEnum, PascalSnakeCaseStrEnum


class Vendor(LowercaseStrEnum):
    HUAWEI = auto()
    ARISTA = auto()
    CISCO = auto()


class Role(PascalSnakeCaseStrEnum):
    BorderRouter = auto()
    ACCESS_SWITCH = auto()
    WIRELESSController = auto()


def parse_output(vendor: Vendor):
    if vendor == Vendor.HUAWEI:
        print("parsing huawei config...")
    elif vendor == Vendor.ARISTA:
        print("parsing arista config...")
    elif vendor == Vendor.CISCO:
        print(f"parsing {vendor} config...")
    else:
        raise ValueError(f"неизвестный производитель {vendor}")


print(Role.BorderRouter.value)
print(Role.ACCESS_SWITCH.value)
print(Role.WIRELESSController.value)
