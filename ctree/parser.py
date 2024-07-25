import re
from typing import Type

from .abstract import ConfigTree
from .factory import ConfigTreeFactory

__all__ = ("ConfigTreeParser",)


class ConfigTreeParser:
    def __init__(self, vendor: str) -> None:
        self._parser = ConfigTreeFactory.get_class(vendor)

    @classmethod
    def _parse(cls, ct: Type[ConfigTree], config: str) -> ConfigTree:
        root = ct()
        section = [root]
        spaces = [0]
        for line in config.splitlines():
            if len(line.strip()) == 0:
                continue
            skip = [re.fullmatch(p, line) for p in ct.JUNK_LINES]
            if any(skip):
                continue

            # число пробелов у текущей строки
            current_space = len(line) - len(line.lstrip())

            # мы вошли в секцию
            if current_space > spaces[-1]:
                node = list(section[-1].children.values())[-1]
                section.append(node)
                spaces.append(current_space)
            # мы вышли из секции
            elif current_space < spaces[-1]:
                while current_space != spaces[-1]:
                    _ = section.pop()
                    _ = spaces.pop()
            _ = ct(line.lstrip(), section[-1])
        return root

    @classmethod
    def vendor_parse(cls, vendor: str, config: str) -> ConfigTree:
        _parser = ConfigTreeFactory.get_class(vendor)
        root = cls._parse(_parser, config)
        return root

    def parse(self, config: str) -> ConfigTree:
        root = self._parse(self._parser, config)
        return root
