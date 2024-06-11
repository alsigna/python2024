from pprint import pprint
from typing import Any


def case_example(value: Any) -> Any:
    match value:
        case {"transport": "system", **other}:
            return value | {
                "port": other.get("port") or 22,
                "auth_strict_key": False,
                "transport_options": {
                    "open_cmd": [
                        "-o",
                        "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                        "-o",
                        "HostKeyAlgorithms=+ssh-rsa",
                    ]
                },
            }

        case {"transport": "ssh", **other}:
            return value | {
                "port": other.get("port") or 22,
                "auth_strict_key": False,
                "transport_options": {
                    "open_cmd": [
                        "-o",
                        "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                        "-o",
                        "HostKeyAlgorithms=+ssh-rsa",
                    ]
                },
            }

        case {
            "name": name,
            "device_type": {"manufacturer": {"name": vendor}, "model": model},
            "primary_ip": {"address": ip},
        }:
            return {"hostname": name, "vendor": vendor, "model": model, "ip": ip}

        case list(l), _ if len(l) == 1:
            return l[1]
        case _:
            raise ValueError(f"неизвестный формат {value}")


if __name__ == "__main__":
    scrapli1 = {"transport": "system", "host": "192.168.1.1"}
    scrapli2 = {"transport": "ssh", "host": "192.168.1.1"}
    pprint(case_example(scrapli2))

    response = {
        "id": 110,
        "url": "https://demo.netbox.dev/api/dcim/devices/110/",
        "display": "G-Switch",
        "name": "G-Switch",
        "device_type": {
            "id": 7,
            "url": "https://demo.netbox.dev/api/dcim/device-types/7/",
            "display": "C9200-48P",
            "manufacturer": {
                "id": 3,
                "url": "https://demo.netbox.dev/api/dcim/manufacturers/3/",
                "display": "Cisco",
                "name": "Cisco",
                "slug": "cisco",
                "description": "",
            },
            "model": "C9200-48P",
            "slug": "c9200-48p",
            "description": "",
        },
        "role": {
            "id": 2,
            "url": "https://demo.netbox.dev/api/dcim/device-roles/2/",
            "display": "Core Switch",
            "name": "Core Switch",
            "slug": "core-switch",
            "description": "",
        },
        "tenant": None,
        "platform": {
            "id": 1,
            "url": "https://demo.netbox.dev/api/dcim/platforms/1/",
            "display": "Cisco IOS",
            "name": "Cisco IOS",
            "slug": "cisco-ios",
            "description": "",
        },
        "serial": "",
        "asset_tag": None,
        "site": {
            "id": 24,
            "url": "https://demo.netbox.dev/api/dcim/sites/24/",
            "display": "Butler Communications",
            "name": "Butler Communications",
            "slug": "ncsu-128",
            "description": "",
        },
        "location": None,
        "rack": {
            "id": 39,
            "url": "https://demo.netbox.dev/api/dcim/racks/39/",
            "display": "IDF128",
            "name": "IDF128",
            "description": "",
        },
        "position": 8.0,
        "face": {"value": "front", "label": "Front"},
        "latitude": None,
        "longitude": None,
        "parent_device": None,
        "status": {"value": "active", "label": "Active"},
        "airflow": None,
        "primary_ip": {
            "id": 31,
            "url": "https://demo.netbox.dev/api/ipam/ip-addresses/31/",
            "display": "172.16.0.1/24",
            "family": {"value": 4, "label": "IPv4"},
            "address": "172.16.0.1/24",
            "description": "",
        },
        "primary_ip4": {
            "id": 31,
            "url": "https://demo.netbox.dev/api/ipam/ip-addresses/31/",
            "display": "172.16.0.1/24",
            "family": {"value": 4, "label": "IPv4"},
            "address": "172.16.0.1/24",
            "description": "",
        },
    }

    pprint(case_example(response))

    seq = [[100, 132], 42]
    seq = ["1", 42]
    pprint(case_example(seq))
