from __future__ import annotations

import re
from abc import ABC, abstractmethod
from collections import deque
from textwrap import dedent

__all__ = (
    "AbstractConfigTree",
    "ConfigTree",
    "ConfigTreeCisco",
    "ConfigTreeHuawei",
)


class AbstractConfigTree(ABC):
    __slots__ = ["line", "parent", "children"]

    # число пробелов для сдвига блока
    @property
    @abstractmethod
    def SPACES(self) -> str:
        pass

    # команда выхода из блока
    @property
    @abstractmethod
    def END_OF_SECTION(self) -> str:
        pass

    # разделитель секций
    @property
    @abstractmethod
    def SECTION_SEPARATOR(self) -> str:
        pass

    def __init__(self, line: str = "", parent: ConfigTree | None = None) -> None:
        # конфигурационная команда
        self.line: str = line
        # каждый узел имеет родителя, для самого первого уровня это None
        self.parent: ConfigTree | None = parent
        # каждый узел имеет подчиненные узлы (команды)
        self.children: dict[str, ConfigTree] = {}

        # если для создаваемого узла указан родитель, то помимо создания ссылки на него
        # так же прописываем создаваемый узел в сабкоманды у родителя
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

    def _copy(self, children: bool, parent: ConfigTree) -> ConfigTree:
        # объект невозможно скопировать без родителя, поэтому восстанавливаем путь до объекта
        # рекурсивно копируя родителей вверх до самого верхнего (self.parent == None)
        # при этом потомки этих родителей нам не нужны, только сами родители
        if self.parent is not None and parent is None:
            parent = self.parent._copy(children=False, parent=None)

        new_obj = ConfigTree(line=self.line, parent=parent)

        if children:
            for child in self.children.values():
                _ = child._copy(children=True, parent=new_obj)

        return new_obj

    def copy(self, children: bool = True) -> ConfigTree:
        root = self._copy(children=children, parent=None)
        # поднимаемся вверх по дереву и возвращаем корень
        while root.parent is not None:
            root = root.parent
        return root

    def merge(self, other: ConfigTree) -> None:
        for line, node in other.children.items():
            if line not in self.children:
                _ = node._copy(children=True, parent=self)
            else:
                self.children[line].merge(node)

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
            if level == 0:
                result.append(self.SECTION_SEPARATOR)
        if level != 0:
            result.append(self.SECTION_SEPARATOR)
        return "\n".join(result)

    @property
    def patch(self) -> str:
        nodes = deque(self.children.values())
        result = []
        while len(nodes) > 0:
            node = nodes.popleft()
            result.append(node.line)
            if len(node.children) != 0:
                nodes.appendleft(self.__class__(line=self.END_OF_SECTION))
                nodes.extendleft(list(node.children.values())[::-1])
        return "\n".join(result)


class ConfigTreeCisco(AbstractConfigTree):
    SPACES = "  "
    END_OF_SECTION = "exit"
    SECTION_SEPARATOR = "!"


class ConfigTreeHuawei(AbstractConfigTree):
    SPACES = " "
    END_OF_SECTION = "quit"
    SECTION_SEPARATOR = "#"


class ConfigTree:
    MAPPING = {
        "cisco": ConfigTreeCisco,
        "huawei": ConfigTreeHuawei,
    }

    def __new__(cls, platform: str, *args, **kwargs) -> AbstractConfigTree:
        _class = cls.get_tree_class(platform)
        return _class(*args, **kwargs)

    @classmethod
    def get_tree_class(cls, platform: str) -> AbstractConfigTree:
        _class = cls.MAPPING.get(platform)
        if _class is None:
            raise NotImplementedError("unknown vendor")
        return _class


def assert_tree_cisco() -> None:
    vendor = "cisco"
    root_config = dedent(
        """
        no ip http server
        !
        interface Vlan1
          ip address 192.168.1.1 255.255.255.0
          no shutdown
        !
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
        !
        """
    ).strip()

    http_config = dedent(
        """
        no ip http server
        !
        """
    ).strip()

    ct = ConfigTree.get_tree_class(vendor)
    root = ct()
    http = ct("no ip http server", root)
    vlan = ct("interface Vlan1", root)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ct("no shutdown", vlan)

    print("-" * 10, "root confi")
    print(root.config)
    print("-" * 10, "vlan config")
    print(vlan.config)
    print("-" * 10, "root patch")
    print(root.patch)
    print("-" * 10)

    assert root.config == root_config, "cisco full config is wrong"
    assert root.patch == root_patch, "cisco root patch is wrong"
    assert vlan.config == vlan_config, "cisco vlan config is wrong"
    assert http.config == http_config, "cisco http config is wrong"


def assert_tree_huawei() -> None:
    vendor = "huawei"
    root_config = dedent(
        """
        no ip http server
        #
        interface Vlan1
         ip address 192.168.1.1 255.255.255.0
         undo shutdown
        #
        """
    ).strip()

    root_patch = dedent(
        """
        no ip http server
        interface Vlan1
        ip address 192.168.1.1 255.255.255.0
        undo shutdown
        quit
        """
    ).strip()

    vlan_config = dedent(
        """
        interface Vlan1
         ip address 192.168.1.1 255.255.255.0
         undo shutdown
        #
        """
    ).strip()

    http_config = dedent(
        """
        no ip http server
        #
        """
    ).strip()

    ct = ConfigTree.get_tree_class(vendor)
    root = ct()
    http = ct("no ip http server", root)
    vlan = ct("interface Vlan1", root)
    _ = ct("ip address 192.168.1.1 255.255.255.0", vlan)
    _ = ct("undo shutdown", vlan)

    print("-" * 10, "root config")
    print(root.config)
    print("-" * 10, "vlan config")
    print(vlan.config)
    print("-" * 10, "root patch")
    print(root.patch)
    print("-" * 10)

    assert root.config == root_config, "huawei full config is wrong"
    assert root.patch == root_patch, "huawei root patch is wrong"
    assert vlan.config == vlan_config, "huawei vlan config is wrong"
    assert http.config == http_config, "huawei http config is wrong"


if __name__ == "__main__":
    assert_tree_cisco()
    assert_tree_huawei()
