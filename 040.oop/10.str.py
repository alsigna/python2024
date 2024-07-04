class ConfigTree:
    def __init__(self, line: str = "", parent=None) -> None:
        self.line: str = line
        self.parent: ConfigTree = parent
        self.children: list[ConfigTree] = []

        if parent is not None:
            parent.children.append(self)

    def __str__(self) -> str:
        return self.line or "root"


# no ip http server
# interface Vlan1

root = ConfigTree()
vlan = ConfigTree("interface Vlan1", root)
http = ConfigTree("no ip http server", root)

print(str(vlan))
print(str(http))
