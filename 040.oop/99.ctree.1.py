from __future__ import annotations


class ConfigTree:
    def __init__(self, line: str = "", parent: ConfigTree | None = None) -> None:
        self.line: str = line
        self.parent: ConfigTree = parent
        self.children: list[ConfigTree] = []

        if parent is not None:
            parent.children.append(self)


# no ip http server
# interface Vlan1
#   ip address 192.168.1.1 255.255.255.0
#   no shutdown

root = ConfigTree()
vlan1 = ConfigTree("interface Vlan1", root)
ip = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan1)
shut = ConfigTree("no shutdown", vlan1)
http = ConfigTree("no ip http server", root)
