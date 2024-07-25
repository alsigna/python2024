from enum import auto

from strenum import LowercaseStrEnum

__all__ = ("Vendor",)


class Vendor(LowercaseStrEnum):
    HUAWEI = auto()
    CISCO = auto()
