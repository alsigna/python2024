from enum import Enum


class Vendor(str, Enum):
    HUAWEI = "huawei"
    ARISTA = "arista"
    CISCO = "cisco"


def parse_output(vendor: Vendor):
    if vendor == Vendor.HUAWEI:
        print("parsing huawei config...")
    elif vendor == Vendor.ARISTA:
        print("parsing arista config...")
    elif vendor == Vendor.CISCO:
        print(f"parsing {vendor} config...")
    else:
        raise ValueError(f"неизвестный производитель {vendor}")


parse_output("huawei")
parse_output("arista")
parse_output("CiScO")
