from __future__ import annotations

from typing import Type, cast

from .abstract import ConfigTree
from .models import Vendor
from .vendors import CiscoConfigTree, HuaweiConfigTree

__all__ = ("ConfigTreeFactory",)


class ConfigTreeFactory:
    VENDOR_MAP = {
        Vendor.CISCO: CiscoConfigTree,
        Vendor.HUAWEI: HuaweiConfigTree,
    }

    def __new__(cls, vendor: Vendor, line: str = "", parent: ConfigTree | None = None) -> ConfigTree:
        _class: ConfigTree = cls.get_class(vendor)
        node = _class(line=line, parent=parent)
        node = cast(ConfigTree, node)
        return node

    @classmethod
    def get_class(cls, vendor: str) -> Type[ConfigTree]:
        _class = cls.VENDOR_MAP.get(vendor)
        if _class is None:
            raise NotImplementedError("unknown vendor")
        r: CiscoConfigTree
        return _class
