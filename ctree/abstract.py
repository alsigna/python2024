from __future__ import annotations

from abc import ABC, abstractmethod
from collections import deque

__all__ = ("ConfigTree",)


class ConfigTree(ABC):
    __slots__ = ["line", "parent", "children"]

    @property
    @abstractmethod
    def SPACES(self) -> str:
        """количество пробелов для нового уровня"""

    @property
    @abstractmethod
    def END_OF_SECTION(self) -> str:
        """как выходим из секции: exit/quit/..."""

    @property
    @abstractmethod
    def SECTION_SEPARATOR(self) -> str:
        """чем разделяем блоки конфига между собой: !/#/..."""

    @property
    @abstractmethod
    def JUNK_LINES(self) -> list[str]:
        """список линий, которые нужно игнорировать при парсинге конфигурации,
        типа Building configuration, exit-address-famil и прочее"""

    @property
    @abstractmethod
    def UNDO(self) -> str:
        """как убираем конфигурацию, в общем случае: no/undo/..."""

    def __init__(self, line: str = "", parent: ConfigTree | None = None) -> None:
        self.line = line
        self.parent = parent
        self.children: dict[str, ConfigTree] = {}
        if parent is not None:
            parent.children[line] = self

    def __str__(self) -> str:
        return self.line or "root"

    def __repr__(self) -> str:
        return f"({id(self)}) '{str(self)}'"

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

    def _config(self, symbol: str, level: int) -> str:
        result = [symbol * level + self.line]
        for child in self.children.values():
            result.extend(child._config(symbol=symbol, level=level + 1))
        return result

    @property
    def config(self) -> str:
        result = []
        level = 0
        node = self
        while node.parent is not None:
            result.append(node.line)
            level += 1
            node = node.parent
        result.reverse()
        result = [self.SPACES * l + line for l, line in enumerate(result)]
        for child in self.children.values():
            result.extend(child._config(symbol=self.SPACES, level=level))
            result.append(self.SECTION_SEPARATOR)
        return "\n".join(result)

    @property
    def patch(self) -> str:
        nodes = deque(self.children.values())
        result = []
        path_to_root = []

        node = self
        while node.parent is not None:
            path_to_root.append(node.line)
            node = node.parent
        path_to_root.reverse()

        while len(nodes) > 0:
            node = nodes.popleft()
            result.append(node.line)
            if len(node.children) != 0:
                nodes.appendleft(self.__class__(line=self.END_OF_SECTION))
                nodes.extendleft(list(node.children.values())[::-1])
        result = path_to_root + result + [self.END_OF_SECTION] * len(path_to_root)
        return "\n".join(result)

    def _copy(self, children: bool, parent: ConfigTree | None) -> ConfigTree:
        if self.parent is not None and parent is None:
            parent = self.parent._copy(children=False, parent=None)

        new_obj = self.__class__(line=self.line, parent=parent)
        if children:
            for child in self.children.values():
                _ = child._copy(children, new_obj)
        return new_obj

    def copy(self, children: bool = True) -> ConfigTree:
        root = self._copy(children=children, parent=None)
        while root.parent is not None:
            root = root.parent
        return root

    def merge(self, other: ConfigTree) -> None:
        for line, node in other.children.items():
            if line not in self.children:
                _ = node._copy(children=True, parent=self)
            else:
                self.children[line].merge(node)
