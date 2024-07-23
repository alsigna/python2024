# Во время лекция писали класс ConfigTree для парсинга конфигурации в дерево. Сам класс представляет собой только структуру для хранения данных
# в виде листа (node / leaf) дерева, и служебные методы, типа __str__, __eq__, ... Сам же парсинг текста конфигурации в дерево выполняется
# классом ConfigTreeParser. В логике метода `parse` есть баг, и в некоторых случаях он неправильно парсит вложенные структуры. Нужно понять
# в чем проблема и сделать фикс бага. После этого проверка `assert_parse_nested` должна проходить без ошибок.

from __future__ import annotations

from textwrap import dedent


class ConfigTree:
    __slots__ = ["line", "parent", "children"]
    SPACES = " "

    def __init__(self, line: str = "", parent: ConfigTree | None = None) -> None:
        self.line = line
        self.parent = parent
        self.children = {}
        if parent is not None:
            parent.children[line] = self

    def __str__(self) -> str:
        return self.line or "root"

    def __repr__(self) -> str:
        return f"({id(self)}) '{str(self)}'"

    def _config(self, symbol: str, level: int) -> str:
        result = [symbol * level + self.line]
        for child in self.children.values():
            result.extend(child._config(symbol=symbol, level=level + 1))
        return result

    def __eq__(self, other: ConfigTree) -> bool:
        if self.line != other.line:
            return False
        if len(self.children) != len(other.children):
            return False

        self_parents = []

        p = self.parent
        while p is not None:
            self_parents.append(p.line)
            p = p.parent

        other_parents = []
        p = other.parent
        while p is not None:
            other_parents.append(p.line)
            p = p.parent

        if self_parents != other_parents:
            return False

        children_eq = []
        for line, node in self.children.items():
            other_node = other.children.get(line)
            if other_node is None:
                return False
            children_eq.append(node == other_node)
        return all(children_eq)

    @property
    def config(self) -> str:
        if self.parent is None:
            result = []
            level = 0
        else:
            result = [self.line]
            level = 1
        for child in self.children.values():
            result.extend(child._config(symbol=self.SPACES, level=level))
            result.append("!")
        return "\n".join(result)

    def _copy(self, parent: ConfigTree) -> ConfigTree:
        new_obj = ConfigTree(self.line, parent)
        for child in self.children.values():
            _ = child._copy(new_obj)
        return new_obj

    def copy(self) -> ConfigTree:
        root = self._copy(None)
        return root


class ConfigTreeParser:
    SKIP_LINES = ["!"]

    @classmethod
    def parse(cls, config: str) -> ConfigTree:
        root = ConfigTree()

        section: list = [root]
        # количество пробелов в предыдущей итерации
        last_spaces = 0
        for line in config.splitlines():
            if len(line.strip()) == 0:
                continue
            if line.strip() in cls.SKIP_LINES:
                continue

            # число пробелов у текущей строки
            current_space = len(line) - len(line.lstrip())

            # мы вошли в секцию
            if current_space > last_spaces:
                node = list(section[-1].children.values())[-1]
                section.append(node)
            # мы вышли из секции
            elif current_space < last_spaces:
                _ = section.pop()

            _ = ConfigTree(line.lstrip(), section[-1])
            last_spaces = current_space
        return root


def assert_basic_creation() -> None:
    root = ConfigTree()
    _ = ConfigTree("no ip http server", root)
    vlan = ConfigTree("interface Vlan1", root)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ConfigTree("no shutdown", vlan)

    assert str(root) == "root", "root is failed"
    assert str(root.children.get("interface Vlan1")) == "interface Vlan1", "vlan is failed"

    node: ConfigTree = root.children.get("interface Vlan1")
    ip: ConfigTree = node.children.get("ip address 192.168.1.1 255.255.255.0")
    assert str(ip) == "ip address 192.168.1.1 255.255.255.0", "ip is failed"


def assert_config() -> None:
    root = ConfigTree()
    _ = ConfigTree("no ip http server", root)
    vlan = ConfigTree("interface Vlan1", root)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ConfigTree("no shutdown", vlan)

    target_config = dedent(
        """
        no ip http server
        !
        interface Vlan1
         ip address 192.168.1.1 255.255.255.0
         no shutdown
        !
        """
    ).strip()
    assert root.config == target_config, "config is failed"


def assert_eq() -> None:
    root1 = ConfigTree()
    _ = ConfigTree("no ip http server", root1)
    vlan = ConfigTree("interface Vlan1", root1)
    _ = ConfigTree("no shutdown", vlan)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)

    root2 = ConfigTree()
    _ = ConfigTree("no ip http server", root2)
    vlan = ConfigTree("interface Vlan1", root2)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ConfigTree("no shutdown", vlan)

    root3 = ConfigTree()
    _ = ConfigTree("no ip http server", root3)
    vlan = ConfigTree("interface Vlan2", root3)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ConfigTree("no shutdown", vlan)

    root4 = ConfigTree()
    _ = ConfigTree("no ip http server", root3)
    vlan = ConfigTree("interface Vlan1", root3)
    _ = ConfigTree("ip address 192.168.1.2 255.255.255.0", vlan)
    _ = ConfigTree("no shutdown", vlan)

    root5 = ConfigTree()
    _ = ConfigTree("no ip http server", root5)
    vlan = ConfigTree("interface Vlan1", root5)
    _ = ConfigTree("description test", vlan)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ConfigTree("no shutdown", vlan)

    assert root1 == root2, "should be eq"
    assert root1 != root3, "should not be eq (vlan id)"
    assert root1 != root4, "should not be eq (ip address)"
    assert root1 != root5, "should not be eq (extra command)"


def assert_parse() -> None:
    config = dedent(
        """
        lldp run
        !
        ntp source-interface Loopback0
        !
        interface FastEthernet0/1
         switchport access vlan 10
         switchport mode access
         spanning-tree portfast edge
         spanning-tree bpduguard enable
        !
        line vty 0 4
         password cisco
        !
        """
    ).strip()
    ct = ConfigTreeParser.parse(config)
    assert ct.config == config, "wrong parsing"


def assert_copy() -> None:
    config = dedent(
        """
        lldp run
        !
        ntp source-interface Loopback0
        !
        interface FastEthernet0/1
         switchport access vlan 10
         switchport mode access
         spanning-tree portfast edge
         spanning-tree bpduguard enable
        !
        line vty 0 4
         password cisco
        !
        """
    ).strip()
    ct1 = ConfigTreeParser.parse(config)
    ct2 = ct1.copy()
    assert ct1.config == ct2.config, "wrong copy"


def assert_parse_nested() -> None:
    config = dedent(
        """
        license udi pid CSR1000V sn 9BZNE1T61US
        !
        diagnostic bootup level minimal
        !
        archive
         log config
          logging enable
           level 1
            level 2
        !
        memory free low-watermark processor 71497
        !
        spanning-tree extend system-id
        !
        """
    ).strip()
    ct = ConfigTreeParser.parse(config)
    assert ct.config == config, "wrong parsing nested config"


if __name__ == "__main__":
    assert_basic_creation()
    assert_config()
    assert_eq()
    assert_parse()
    assert_copy()
    assert_parse_nested()
