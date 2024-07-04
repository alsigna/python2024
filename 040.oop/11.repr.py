class ConfigTree:
    def __init__(self, line: str = "", parent=None) -> None:
        self.line: str = line
        self.parent: ConfigTree = parent
        self.children: list[ConfigTree] = []

        if parent is not None:
            parent.children.append(self)

    def __str__(self) -> str:
        return self.line or "root"

    def __repr__(self) -> str:
        # return f"{self.__class__.__name__}('{self.line}', {self.parent!r})"
        return f"({id(self)}) {str(self)}"


# no ip http server
# interface Vlan1
#   ip address 192.168.1.1 255.255.255.0

root = ConfigTree()
vlan = ConfigTree("interface Vlan1", root)
http = ConfigTree("no ip http server", root)
ip = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)

print("__str__")
print(str(vlan))
print(str(http))
print(str(ip))

print("__repr__")
print(repr(vlan))
print(repr(http))
print(repr(ip))
