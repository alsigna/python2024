from pathlib import Path

from j2ipaddr.filters import ip_broadcast, ip_netmask, ip_network_first, ip_network_last
from jinja2 import Environment, FileSystemLoader
from netaddr import IPNetwork


def shift_ip_address(addr, offest):
    return IPNetwork(addr).ip + offest


template_dir = str(Path(Path(__file__).parent, "templates"))
loader = FileSystemLoader(template_dir)

env = Environment(loader=loader)
env.filters["ip_netmask"] = ip_netmask
env.filters["ip_broadcast"] = ip_broadcast
env.filters["ip_network_first"] = ip_network_first
env.filters["ip_network_last"] = ip_network_last
env.filters["shift_ip_address"] = shift_ip_address


template_file = str(Path(Path(__file__).name).with_suffix(".j2"))
template = env.get_template(template_file)


data = {
    "name0": "rt01-msk",
    "owner": "Tim",
    "prefix": "",
    "loud": "CAPSLOCK",
    "trunks": {
        "gi0/0/1": {
            "vlans": [100],
        },
        "gi0/0/0": {
            "vlans": [101, 102],
        },
        "gi0/0/2": {
            "vlans": [103],
        },
    },
    "vlans": [101, 102, 103],
    "string_with_spaces": "   some string with spaces   ",
    "host": {
        "interfaces": {
            "gi0/0/0": {
                "ospf": {
                    "status": True,
                    "area": 0,
                },
                "ipv4": ["10.1.2.3/24"],
            }
        }
    },
}


config = template.render(data)

print(config)
