import re

from .abstract import ConfigTree

__all__ = ("ConfigTreeSearcher",)


class ConfigTreeSearcher:
    @classmethod
    def _search(cls, ct: ConfigTree, string: str, children) -> list[ConfigTree]:
        result = []

        if re.search(rf"{string.strip()}", ct.line.strip()) is not None:
            result.append(ct.copy(children=children))
        for child in ct.children.values():
            result.extend(cls._search(child, string, children))

        return result

    @classmethod
    def search(cls, ct: ConfigTree, string: str, *, children: bool = False) -> ConfigTree:
        root = ct.__class__()
        if len(string) == 0:
            return root
        filter_result = cls._search(ct, string, children)
        for node in filter_result:
            root.merge(node)
        return root
