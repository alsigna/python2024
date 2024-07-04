from __future__ import annotations

from collections import deque
from textwrap import dedent

__all__ = ("ConfigTree",)


class ConfigTree:
    SPACES = "  "
    END_OF_SECTION = "exit"

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
        if self.parent is None:
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
                nodes.appendleft(ConfigTree(line=self.END_OF_SECTION))
                nodes.extendleft(node.children[::-1])
        return "\n".join(result)


if __name__ == "__main__":
    root_config = dedent(
        """
        no ip http server
        interface Vlan1
          ip address 192.168.1.1 255.255.255.0
          no shutdown
        """
    ).strip()

    root_patch = dedent(
        """
        no ip http server
        interface Vlan1
        ip address 192.168.1.1 255.255.255.0
        no shutdown
        exit
        """
    ).strip()

    vlan1_config = dedent(
        """
        interface Vlan1
          ip address 192.168.1.1 255.255.255.0
          no shutdown
        """
    ).strip()

    http_config = "no ip http server"

    root = ConfigTree()
    http = ConfigTree("no ip http server", root)
    vlan1 = ConfigTree("interface Vlan1", root)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan1)
    _ = ConfigTree("no shutdown", vlan1)

    print("-" * 10)
    print(root.config)
    print("-" * 10)
    print(root.patch)
    print("-" * 10)

    assert root.config == root_config, "full config is wrong"
    assert root.patch == root_patch, "root patch is wrong"
    assert vlan1.config == vlan1_config, "vlan1 config is wrong"
    assert http.config == http_config, "http config is wrong"
