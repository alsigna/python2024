# Scrapli Replay

- [Scrapli Replay](#scrapli-replay)
  - [Описание](#описание)
  - [Использование](#использование)
    - [Mock SSH](#mock-ssh)
    - [PyTest](#pytest)

## Описание

[Scrapli Replay](https://github.com/scrapli/scrapli_replay) это библиотека для тестирования, позволяет создать mock SSH сервер и выступить в роли сетевого устройства.

Устанавливается `pip install scrapli_replay`

У библиотеки две области применения:

- создать mock ssh сервер который будет вести как сетевое устройство (в рамках собранных команд)
- предоставить декоратор для маркировки тестов, изменяя их таким образом, что данные для тестирования будут браться из слепков устройств

Для mock сервера библиотека определяет три основных компонента:

- collector - ходит на реальное устройство и делает слепок его ответов для заранее определенных команд.
- server - ssh сервер, запускаемый на основе собранных collector'ом информацией и представляющийся сетевым устройством
- client - ssh клиент, разрабатываемый скрипт, который во время разработки/тестирования будет ходить не реальное оборудование, а на server

Для pytest используется collector для сбора дампа с устройства, и декоратор `@pytest.mark.scrapli_replay` для маркировки тестов. При первом выполнении тестов collector собирает нужную информация (пользователь не нужен), а при втором и третьем тестах уже происходит чтение из дампа устройства, а не сбор с реального оборудования.

## Использование

### Mock SSH

Для получения слепка устройства необходимо использовать класс `ScrapliCollector`, помимо стандартных параметров для подключения, для его настройки необходимо передать какие команды снимать, параметры пагинации и еще ряд атрибутов, см пример ниже.

```python
from scrapli_replay.server.collector import ScrapliCollector

host = "192.168.122.101"
device = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
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

collector = ScrapliCollector(
    channel_inputs=[
        "show version",
        "show ip int br",
        "sh lacp ne",
        "sh ip ospf ne",
    ],
    interact_events=[
        [
            ("clear logging", "[confirm]", False),
            ("", "#", False),
        ],
    ],
    paging_indicator="--More--",
    paging_escape_string="\x1b",
    collector_session_filename=f"collector_session_dump_{host}.yaml",
    host=host,
    **device,
)

collector.open()
collector.collect()
collector.close()
collector.dump()
```

После завершения работы скрипта, в каталоге будет создан файл `collector_session_dump_192.168.122.101.yaml`, в котором будет информация по устройству. Это статичная информация и она будет обновляться только при повторном запуске коллектора.

Для запуска сервера на базе собранной информации можно использовать следующий пример. Сервер будет запущен на 2022 порту и на него можно попасть стандартным способом (ssh -p 2022 ...)

```python
import asyncio

from scrapli_replay.server.server import start


async def main() -> None:
    await start(
        port=2022,
        collect_data="collector_session_dump_192.168.122.101.yaml",
    )


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    try:
        loop.run_until_complete(main())
        loop.run_forever()
    finally:
        loop.close()
```

В качестве клиента может выступать любое приложение или скрипт (не обязательно на scrapli). Ограничение только в том, что нельзя поменять имя пользователя, оно всегда должно быть scrapli/scrapli (user/password).

```python
from scrapli import Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "127.0.0.1",
    "port": 2022,
    "auth_username": "scrapli",
    "auth_password": "scrapli",
    "auth_strict_key": False,
}


def send_command(device: dict[str, str], command: str) -> Response:
    try:
        with Scrapli(**device) as ssh:
            return ssh.send_command(command)
    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    commands = [
        "sh lacp ne",
        "sh ip ospf ne",
        "show version",
    ]
    for command in commands:
        result = send_command(device, command)
        print("=" * 10)
        print(result.channel_input)
        print(result.result)
```

### PyTest

Нами написан класс `CiscoDevice` в котором есть метод `get_version` возвращающий версию ПО оборудования.

```python
import re

from scrapli import Scrapli


class CiscoDevice:
    def __init__(self, host: str):
        self.ssh = Scrapli(
            host=host,
            platform="cisco_iosxe",
            auth_strict_key=False,
            auth_username="admin",
            auth_password="P@ssw0rd",
            transport_options={
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ],
            },
        )

    def _open(self):
        if not self.ssh.isalive():
            try:
                self.ssh.open()
            except Exception:
                raise

    def get_version(self):
        self._open()
        output = self.ssh.send_command("show version | i Software")
        self.ssh.close()
        if output.failed:
            return "__FAILURE__"

        version = re.findall(r"version ([a-z0-9_\.\(\)]*)", output.result, flags=re.I)
        if not version:
            return "__FAILURE__"

        return version[0]
```

Для тестирования этого метода нами написан тест

```python
import pytest
from devices import CiscoDevice


@pytest.mark.parametrize(
    "host, expected_version",
    [
        ("192.168.122.101", "17.03.03"),
        ("192.168.122.201", "15.2(CML_NIGHTLY_20190423)FLO_DSGS7"),
    ],
)
@pytest.mark.scrapli_replay
def test_cisco_get_version(host, expected_version):
    device = CiscoDevice(host)
    assert device.get_version() == expected_version
```

Вызывая который `python -m pytest .` будет проверятся работа метода `get_version`. Но без scrapli-replay каждый вызов теста будет приводить к сбору данных с устройства, это занимает время и очень ресурсоемкая операция. При добавлении декоратора `@pytest.mark.scrapli_replay` первый запуск теста пройдет как обычно, но в после него будет созданы дампы устройств, и следующие запуски будут брать информацию не с реального оборудования, я из собранных ранее дампов. Для обновления информации (повторного сбора) можно запустить тесты с флагом `python -m pytest . --scrapli-replay-mode overwrite`. Более подробные примере есть в [документации](https://scrapli.github.io/scrapli_replay/user_guide/basic_usage/).
