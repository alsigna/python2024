# Написать функцию c сигнатурой `clear_logging(device: dict[str, str]) -> bool`, которая очищает
# буфер syslog-сообщений на cisco оборудовании командой `clear logging`. В качестве аргумента
# функция принимает словарь с параметрами оборудования для подключения.
#
# Ключевые особенности, которым должна соответствовать функция:
# - выполнении команды на оборудовании требует подтверждения операции:
#   router#clear logging
#   Clear logging buffer [confirm]
#   router#
#   функция должна обеспечить обработку интерактивного события (способ остается за разработчиком)
# - должны обрабатываться исключения из задания 2:
#   - не подходят логин/пароль -> пишем в stdout "Неправильные логин/пароль для устройства" и
#     и возвращаем False из функции
#   - таймаут подключения к устройству -> пишем в stdout "Таймаут подключения к устройству" и
#     и возвращаем False из функции
#   - все неизвестные исключения -> пишем в stdout "Неизвестная ошибка при работе с устройством" и
#     и возвращаем False из функции
# - функция должна проверять результат ввода команды, если команда была принята оборудованием,
#   тогда функция возвращает True, если выполнить команду не удалось -> возвращает False
#
# Пример успешного выполнения
#
#   router# clear logging
#   Clear logging buffer [confirm]
#   router#
#
# Пример неуспешного выполнения
#
#   router> clear logging
#                  ^
#   % Invalid input detected at '^' marker.
#   router>


from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

device = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}


def clear_logging(device: dict[str, str]) -> bool:
    try:
        with ConnectHandler(**device) as ssh:
            result = ssh.send_command_timing(
                command_string="clear logging",
                strip_prompt=False,
                strip_command=False,
            )
            result += ssh.send_command_timing(
                command_string="",
                strip_prompt=False,
                strip_command=False,
            )
    except NetmikoAuthenticationException:
        print(f"Неправильные логин/пароль для устройства {device.get('host')}")
        return False
    except NetmikoTimeoutException:
        print(f"Таймаут подключения к устройству {device.get('host')}")
        return False
    except Exception as exc:
        print(f"Неизвестная ошибка при работе с устройством {device.get('host')}: {exc.__class__.__name__}: {exc}")
        return False
    if "Invalid input detected" in result:
        return False
    else:
        return True


if __name__ == "__main__":
    print(clear_logging(device))
