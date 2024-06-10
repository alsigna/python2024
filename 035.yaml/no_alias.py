import yaml

_core_faced_features = ["ospf", "lldp", "pim"]


interfaces = {
    "Eth0/1": {
        "description": "to core-1",
        "mtu": 9000,
        "features": _core_faced_features,
        "speed": 10000,
        "duplex": "full",
    },
    "Eth0/2": {
        "description": "to core-2",
        "mtu": 9000,
        "features": _core_faced_features,
        "speed": 10000,
        "duplex": "full",
    },
}


print(
    yaml.safe_dump(
        data=interfaces,
    )
)

# Eth0/1:
#   description: to core-1
#   duplex: full
#   features: &id001
#   - ospf
#   - lldp
#   - pim
#   mtu: 9000
#   speed: 10000
# Eth0/2:
#   description: to core-2
#   duplex: full
#   features: *id001
#   mtu: 9000
#   speed: 10000


class NoAliasDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


print(
    yaml.dump(
        data=interfaces,
        Dumper=NoAliasDumper,
    )
)
