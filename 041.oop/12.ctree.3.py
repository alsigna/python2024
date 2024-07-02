from __future__ import annotations

from collections import deque


class ConfigTree:
    SPACES = "  "
    QUIT = "exit"

    def __init__(self, line: str = "", parent: ConfigTree | None = None) -> None:
        self.line: str = line
        self.parent: ConfigTree = parent
        self.children: list[ConfigTree] = []

        if parent is not None:
            parent.children.append(self)

    def __str__(self) -> str:
        return self.line or "root"

    def __repr__(self) -> str:
        line = self.line or "root"
        return f"({id(self)}) {line}"

    def _config(self, symbol: str, level: int) -> str:
        result = [symbol * level + self.line]
        for child in self.children:
            result.extend(child._config(symbol=symbol, level=level + 1))
        return result

    @property
    def config(self) -> str:
        if self.line == "":
            result = []
            level = 0
        else:
            result = [self.line]
            level = 1
        for child in self.children:
            result.extend(child._config(symbol=self.SPACES, level=level))
        return "\n".join(result)

    @property
    def patch(self) -> str:
        nodes = deque(self.children)
        result = []
        while len(nodes) > 0:
            node = nodes.popleft()
            result.append(node.line)
            if len(node.children) != 0:
                nodes.appendleft(ConfigTree(line=self.QUIT))
                nodes.extendleft(node.children[::-1])
        return "\n".join(result)


# no ip http server
# interface Vlan1
#   ip address 192.168.1.1 255.255.255.0
#   no shutdown

root = ConfigTree()
vlan1 = ConfigTree("interface Vlan1", root)
ip = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan1)
shut = ConfigTree("no shutdown", vlan1)
http = ConfigTree("no ip http server", root)

print(root.config)
print("-" * 10)
print(vlan1.config)
print("-" * 10)
print(root.patch)
