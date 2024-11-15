print("\n" * 2 + "=" * 10, "example 1", "=" * 10)
VENDOR_CISCO = "cisco"
VENDOR_HUAWEI = "huawei"

data = ["r1", "huawei"]

match data:
    case hostname, VENDOR_CISCO:
        print("this is cisco device")
    case hostname, VENDOR_HUAWEI:
        print("this is huawei device")
    case _:
        print("неизвестный производитель")


# ======
print("\n" * 2 + "=" * 10, "example 2", "=" * 10)

VENDOR_CISCO = "cisco"
VENDOR_HUAWEI = "huawei"

data = ["r1", "huawei"]


match data:
    case hostname, vendor if vendor == VENDOR_CISCO:
        print("this is cisco device")
    case hostname, vendor if vendor == VENDOR_HUAWEI:
        print("this is huawei device")
    case _:
        print("неизвестный производитель")


# ======
print("\n" * 2 + "=" * 10, "example 3", "=" * 10)

from collections import namedtuple

# только для примера, пока не знаем Enum для подобных вещей
Vendor = namedtuple("Vendor", "CISCO HUAWEI ARISTA JUNIPER")
VENDOR = Vendor("cisco", "huawei", "arista", "juniper")

data = ["r1", "huawei"]


match data:
    case hostname, VENDOR.CISCO:
        print("this is cisco device")
    case hostname, VENDOR.HUAWEI:
        print("this is huawei device")
    case _:
        print("неизвестный производитель")
