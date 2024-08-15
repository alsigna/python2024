# Создать два класса-перечисления (на базе LowercaseStrEnum из strenum):
# - класс ScrapliPlatform для перечисления возможных платформ, для примера обозначим доступные варианты CISCO_IOSXE и как HUAWEI_VRP
# - класс ScrapliTransport для перечисления возможных transport's scrapli, для примера возьмем варианты SYSTEM, TELNET, SSH2

# Создать класс CiscoIOS c сигнатурой init метода
# `__init__(self, host: str, username: str, password: str, transport: ScrapliTransport = ScrapliTransport.SYSTEM) -> None`
# На входе принимается имя пользователя и пароль для подключения, переданные значения должны записываться в соответствующие атрибуты
# класса (self.username и self.password). А так же опционально параметр transport, который записывается в атрибут self._transport.

# У класса должен быть атрибут platform. Доступ к нему должен быть предоставлен через setter/getter. При этом во время установки атрибута,
# устанавливаемое значение должно проверяться на вхождение в класс ScrapliPlatform (т.е. сделать так, что бы нельзя было выставить значение,
# которое не описано в класса ScrapliPlatform). При попытке выставить некорректное значение нужно бросать исключение ValueError (текст ошибки
# по желанию).

# Аналогичным platform образом нужно создать атрибут transport: доступ через setter/getter, при установки должно проверяться значение и оно
# должно быть из списка, описанного классом ScrapliTransport, при неверном значении бросается исключение ValueError.

# У класса нужно описать атрибут scrapli, представляющий собой словарь необходимых параметров для подключения к оборудованию с использованием
# библиотеки Scrapli.

# У класса нужно описать два метода: `open(self) -> None:` и `close(self) -> None:`, которые открывают и закрывают подключение к оборудованию

# У класса нужно реализовать возможность работы в режиме контекстного менеджера.

# У класса нужно реализовать метод `get_version(self) -> str`, который забирает вывод "show version", парсит его (можно вручную, можно textfsm)
# и возвращает версию ПО в виде строки.


from __future__ import annotations

from enum import auto
from types import TracebackType
from typing import Any, Type

from scrapli import Scrapli
from strenum import LowercaseStrEnum


class ScrapliPlatform(LowercaseStrEnum):
    CISCO_IOSXE = auto()
    HUAWEI_VRP = auto()


class ScrapliTransport(LowercaseStrEnum):
    SYSTEM = auto()
    TELNET = auto()
    SSH2 = auto()


class CiscoIOS:
    def __init__(
        self,
        host: str,
        username: str,
        password: str,
        transport: ScrapliTransport = ScrapliTransport.SYSTEM,
    ) -> None:
        self.host = host
        self.username = username
        self.password = password
        self._platform = ScrapliPlatform.CISCO_IOSXE
        self._transport = ScrapliTransport.SYSTEM
        self.conn = None
        setattr(self, "transport", transport)

    @property
    def platform(self) -> ScrapliPlatform:
        return self._platform

    @platform.setter
    def platform(self, platform: ScrapliPlatform) -> None:
        if platform not in ScrapliPlatform:
            platform_list = ", ".join(ScrapliPlatform._value2member_map_.keys())
            raise ValueError(f"platform должна быть из списка: {platform_list}")
        if isinstance(platform, ScrapliPlatform):
            self._platform = platform
        else:
            self._platform = ScrapliPlatform._value2member_map_.get(platform)

    @property
    def transport(self) -> ScrapliTransport:
        return self._transport

    @transport.setter
    def transport(self, transport: ScrapliTransport) -> None:
        if transport not in ScrapliTransport:
            transport_list = ", ".join(ScrapliTransport._value2member_map_.keys())
            raise ValueError(f"transport должен быть из списка: {transport_list}")
        if isinstance(transport, ScrapliTransport):
            self._transport = transport
        else:
            self._transport = ScrapliTransport._value2member_map_.get(transport)

    @property
    def scrapli(self) -> dict[str, Any]:
        return {
            "host": self.host,
            "platform": self.platform,
            "transport": self.transport,
            "auth_username": self.username,
            "auth_password": self.password,
            "auth_strict_key": False,
            "transport_options": {
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ]
            },
        }

    def open(self) -> None:
        if self.conn is None:
            self.conn = Scrapli(**self.scrapli)
        self.conn.open()

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass
        finally:
            self.conn = None

    def __enter__(self) -> CiscoIOS:
        self.open()
        return self

    def __exit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        self.close()

    def get_version(self) -> str:
        if self.conn is None:
            self.open()
        output = self.conn.send_command("show version")
        if output.failed:
            return ""
        else:
            return output.textfsm_parse_output()[0].get("version")


if __name__ == "__main__":
    with CiscoIOS("192.168.122.101", "admin", "P@ssw0rd") as device:
        print(device.get_version())

# device = CiscoIOS("192.168.122.101", "admin", "P@ssw0rd")
# print(f"{device.transport=}")

# device.transport = "ssh2"
# print(f"{device.transport=}")

# device.transport = ScrapliTransport.TELNET
# print(f"{device.transport=}")

# device.transport = "dummy"
# print(f"{device.transport=}")


device = CiscoIOS("192.168.122.101", "admin", "P@ssw0rd")
device.open()
print(device.get_version())
print(device.conn.send_command("show clock").result)
device.close
