# Написать функцию c сигнатурой `patch_interfaces(device: dict[str, str]) -> bool`, которая
# делает следующее (на примере cisco устройства):
# - подключается к оборудованию
# - собирает вывод команды `show ip interface brief`
# - для каждого интерфейса с IP адресом формирует конфигурацию на основе jinja2 шаблона
# - применяет полученную конфигурацию на устройстве (можно применять для каждого интерфейса
#   в отдельности, т.е. по мере разбора вывода `show ip interface brief`, а можно собрать
#   конфигурацию для всех интерфейсов в один большой патч и разово его применить - выбор
#   логики остается за разработчиком)
#
# Ключевые особенности, которым должна соответствовать функция:
# - должны обрабатываться исключения из задания 2:
#   - не подходят логин/пароль -> пишем в stdout "Неправильные логин/пароль для устройства" и
#     и возвращаем False из функции
#   - таймаут подключения к устройству -> пишем в stdout "Таймаут подключения к устройству" и
#     и возвращаем False из функции
#   - все неизвестные исключения -> пишем в stdout "Неизвестная ошибка при работе с устройством" и
#     и возвращаем False из функции
# - кроме этого, нужно обеспечить проверку корректности вводимых конфигурационных команд средствами
#   самой netmiko, и обработку исключения, возникающего в случае ошибки при конфигурации. В этом
#   случае нужно писать в stdout "Ошибка при настройки устройства" и возвращать False из функции
# - если конфигурация прошла успешно, то возвращать True из функции
#


import re
from textwrap import dedent

from jinja2 import Template
from netmiko import ConnectHandler
from netmiko.exceptions import ConfigInvalidException, NetmikoAuthenticationException, NetmikoTimeoutException

template = Template(
    dedent(
        """
        interface {{ ifname }}
         no ip redirects
         no ip unreachables
         no ip proxy-arp
        exit
        """
    ).strip()
)

device = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}


def patch_interfaces(device: dict[str, str]) -> bool:
    try:
        ssh = ConnectHandler(**device)
    except NetmikoAuthenticationException:
        print(f"Неправильные логин/пароль для устройства {device.get('host')}")
        return False
    except NetmikoTimeoutException:
        print(f"Таймаут подключения к устройству {device.get('host')}")
        return False
    except Exception as exc:
        print(f"Неизвестная ошибка при работе с устройством {device.get('host')}: {exc.__class__.__name__}: {exc}")
        return False

    result = ssh.send_command("show ip interface brief")
    config_commands = []
    for m in re.finditer(r"(?P<ifname>\S+)\s+\d\S+\s+", result):
        config_commands.extend(template.render(ifname=m.group("ifname")).splitlines())
    if len(config_commands) == 0:
        ssh.disconnect()
        return True
    try:
        result = ssh.send_config_set(
            config_commands=config_commands,
            error_pattern="%",
        )
    except ConfigInvalidException:
        print(f"Ошибка при настройки устройства {device.get('host')}")
        return False
    else:
        return True
    finally:
        ssh.disconnect()


if __name__ == "__main__":
    print(patch_interfaces(device))
