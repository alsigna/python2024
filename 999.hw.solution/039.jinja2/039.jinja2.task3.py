from pathlib import Path

from j2ipaddr.filters import ip_address, ip_netmask, ip_network, ip_wildcard
from jinja2 import Environment, FileSystemLoader

template_dir = str(Path(Path(__file__).parent, "templates"))
loader = FileSystemLoader(template_dir)

env = Environment(
    loader=loader,
    lstrip_blocks=True,
    trim_blocks=True,
    extensions=["jinja2.ext.loopcontrols"],
)

env.filters["ip_netmask"] = ip_netmask
env.filters["ip_network"] = ip_network
env.filters["ip_wildcard"] = ip_wildcard
env.filters["ip_address"] = ip_address

template_file = str(Path(Path(__file__).name).with_suffix(".j2"))
template = env.get_template(template_file)

interfaces = {
    "GigabitEthernet0/0/0": {
        "mtu": 1600,
        "ip": "192.168.0.1",
        "mask": "255.255.255.252",
        "type": "internal",
        "bfd": True,
        "area": 0,
    },
    "GigabitEthernet0/0/1": {
        "shutdown": True,
    },
    "GigabitEthernet0/0/2": {
        "mtu": 1600,
        "ip": "192.168.1.1",
        "mask": "255.255.255.252",
        "type": "external",
        "bfd": True,
    },
}
config = template.render(interfaces=interfaces)

print(config.replace("\n\n", "\n"))
