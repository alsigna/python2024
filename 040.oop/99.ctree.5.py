from __future__ import annotations

from collections import deque
from textwrap import dedent

__all__ = (
    "ConfigTree",
    "ConfigTreeParser",
)


class ConfigTree:
    SPACES = "  "
    END_OF_SECTION = "exit"

    def __init__(self, line: str = "", parent: ConfigTree | None = None) -> None:
        self.line: str = line
        self.parent: ConfigTree | None = parent
        self.children: dict[str, ConfigTree] = {}

        if parent is not None:
            parent.children[line.strip()] = self

    def __str__(self) -> str:
        return self.line or "root"

    def __repr__(self) -> str:
        line = self.line or "root"
        return f"({id(self)}) {line}"

    def __eq__(self, other: ConfigTree) -> bool:
        if self.line != other.line:
            return False
        if len(self.children) != len(other.children):
            return False

        self_parent_patch = []
        parent = self.parent
        while parent is not None:
            self_parent_patch.append(parent.line)
            parent = parent.parent

        other_parent_path = []
        parent = other.parent
        while parent is not None:
            other_parent_path.append(parent.line)
            parent = parent.parent

        if self_parent_patch != other_parent_path:
            return False

        children_eq = []
        for line, node in self.children.items():
            other_node = other.children.get(line)
            if other_node is None:
                return False
            children_eq.append(node == other_node)
        return all(children_eq)

    def _config(self, symbol: str, level: int) -> str:
        result = [symbol * level + self.line]
        for child in self.children.values():
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
        for child in self.children.values():
            result.extend(child._config(symbol=self.SPACES, level=level))
        return "\n".join(result)

    @property
    def patch(self) -> str:
        nodes = deque(self.children.values())
        result = []
        while len(nodes) > 0:
            node = nodes.popleft()
            result.append(node.line)
            if len(node.children) != 0:
                nodes.appendleft(ConfigTree(line=self.END_OF_SECTION))
                nodes.extendleft(list(node.children.values())[::-1])
        return "\n".join(result)


class ConfigTreeParser:
    SKIP_LINES = ["!"]

    @classmethod
    def parse(cls, config: str) -> ConfigTree:
        # создаем корень, куда будем цеплять весь конфиг
        root = ConfigTree()
        # создаем переменную-стек, в которую будем складывать текущую секцию
        # с самого начала это корень, а дальше будем дописывать конфигурационые секции
        # interface xxx, router bgp xxx, и т.д. в которые заходим
        # можно и обычный list использовать, но попробуем deque
        sections = deque([root])
        # секции определяются сдвигами через пробелы, на старте сдвига нет
        spaces = 0
        # итерируемся по линиям конфигурации
        for line in config.splitlines():
            # если вдруг строка пустая
            if len(line.strip()) == 0:
                continue
            # если наша строка или первый её символ это строка из списка для пропуска
            if line.strip() in cls.SKIP_LINES or line.strip()[0] in cls.SKIP_LINES:
                continue
            # считаем текущее количество пробелов в начале строки
            current_spaces = len(line) - len(line.lstrip())
            # если число пробелов в начале строки стало больше, значит мы провалились в секцию
            # и нужно в sections справа накинуть предудующую строку, точнее элемет, который представляет строку
            # (доступ к нему получаем через последний дочерний элемент последнего элемента в sections)
            # она будет parent'ом для текущей и следующих строк, пока не выйдем из секции
            # (число пробелов станет меньше, чем было)
            if current_spaces > spaces:
                sections.append(list(sections[-1].children.values())[-1])
            # а если число пробелов стало меньше, это значит мы вышли из текущей секции и нам нужно из
            # sections удалить верхний элемент
            elif current_spaces < spaces:
                sections.pop()
            # пробелы мы отработали, поэтому устанавливаем запоминаем текущее количество пробелов как опорное значение
            spaces = current_spaces
            # создаем узел дерева, сам экземпляр нам не нужен, так как доступ все равно через корень дерева будет
            # родителя берем как узел из sections, это та секция, в которой мы в текущий момент находимся
            _ = ConfigTree(line=line.strip(), parent=sections[-1])

        return root


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

    vlan_config = dedent(
        """
        interface Vlan1
          ip address 192.168.1.1 255.255.255.0
          no shutdown
        """
    ).strip()

    http_config = "no ip http server"

    root = ConfigTree()
    http = ConfigTree("no ip http server", root)
    vlan = ConfigTree("interface Vlan1", root)
    _ = ConfigTree("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ConfigTree("no shutdown", vlan)

    # print("-" * 10)
    # print(root.config)
    # print("-" * 10)
    # print(vlan.config)
    # print("-" * 10)
    # print(root.patch)
    # print("-" * 10)

    assert root.config == root_config, "full config is wrong"
    assert root.patch == root_patch, "root patch is wrong"
    assert vlan.config == vlan_config, "vlan config is wrong"
    assert http.config == http_config, "http config is wrong"

    root = ConfigTreeParser.parse(root_config)
    # print("-" * 10)
    # print(root.config)
    # print("-" * 10)
    # print(root.patch)

    vlan_config2 = dedent(
        """
        interface Vlan1
          ip address 192.168.1.1 255.255.255.0
          no shutdown
        """
    ).strip()

    vlan_configs = [
        dedent(
            """
            interface Vlan1
              ip address 192.168.1.1 255.255.255.0
              no shutdown
            """
        ).strip(),
        dedent(
            """
            interface Vlan1
              ip address 192.168.1.1 255.255.255.0
              no shutdown
            """
        ).strip(),
        dedent(
            """
            interface Vlan2
              ip address 192.168.1.1 255.255.255.0
              no shutdown
            """
        ).strip(),
        dedent(
            """
            interface Vlan1
              ip address 192.168.1.2 255.255.255.0
              no shutdown
            """
        ).strip(),
        dedent(
            """
            interface Vlan1
              ip address 192.168.1.1 255.255.255.0
            """
        ).strip(),
    ]
    vlans = []
    for vlan_config in vlan_configs:
        vlans.append(ConfigTreeParser.parse(vlan_config))

    # for vlan in vlans:
    #     print("-" * 10)
    #     print(vlan.config)

    assert vlans[0] == vlans[1], "should be True"
    assert vlans[0] != vlans[2], "should be False"
    assert vlans[0] != vlans[3], "should be False"
    assert vlans[0] != vlans[4], "should be False"

    ip1 = vlans[0].children.get("interface Vlan1").children.get("ip address 192.168.1.1 255.255.255.0")
    ip2 = vlans[2].children.get("interface Vlan2").children.get("ip address 192.168.1.1 255.255.255.0")
    assert ip1 != ip2, "wrong parent check"
