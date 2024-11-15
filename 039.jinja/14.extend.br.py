from pathlib import Path

from j2ipaddr.filters import ip_address, ip_netmask, ip_network, ip_wildcard
from jinja2 import Environment, FileSystemLoader
from netaddr import IPNetwork


def shift_ip_address(addr, offset):
    return IPNetwork(addr).ip + offset


template_dir = str(Path(Path(__file__).parent, "templates"))
loader = FileSystemLoader(template_dir)


env = Environment(
    loader=FileSystemLoader(template_dir),
    lstrip_blocks=True,
    trim_blocks=True,
)
env.filters["ip_netmask"] = ip_netmask
env.filters["ip_network"] = ip_network
env.filters["ip_wildcard"] = ip_wildcard
env.filters["ip_address"] = ip_address

template_file = str(Path(Path(__file__).name).with_suffix(".j2"))
template = env.get_template(template_file)

data = {
    "service_dhcp": True,
    "ospf_bw": 800000,
    "interfaces": {
        "gi0/0/0": {
            "type": "user",
            "ospf": {
                "status": True,
                "area": 0,
            },
            "ipv4": [
                "10.0.0.1/24",
                "192.168.1.254/23",
            ],
        },
        "gi0/0/1": {
            "type": "server",
            "ipv4": [
                "10.1.0.1/24",
            ],
        },
    },
}

config = template.render(data)

print(config)
