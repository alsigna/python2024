# Модифицировать функцию `get_output(device: dict[str, str], command: str) -> str`, добавив в нее
# обработку следующих исключений:
# - некорректная пара логин/пароль -> печатаем в stdout "Неправильные логин/пароль для устройства <fqdn/ip устройства>"
#   и возвращаем из функции пустую строку
# - таймаут подключения к устройству -> печатаем в stdout "Таймаут подключения к устройству <fqdn/ip устройства>"
#   и возвращаем из функции пустую строку
# - все неизвестные исключения -> печатаем в stdout "Неизвестное исключение при работе с устройством
#   <fqdn/ip устройства><класс исключения>:<текст исключения>" и возвращаем из функции пустую строку


from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

device = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}


def get_output(device: dict[str, str], command: str) -> str:
    try:
        with ConnectHandler(**device) as ssh:
            ssh.enable()
            result = ssh.send_command(command)
    except NetmikoAuthenticationException:
        print(f"Неправильные логин/пароль для устройства {device.get('host')}")
        return ""
    except NetmikoTimeoutException:
        print(f"Таймаут подключения к устройству {device.get('host')}")
        return ""
    except Exception as exc:
        print(f"Неизвестная ошибка при работе с устройством {device.get('host')}: {exc.__class__.__name__}: {exc}")
        return ""
    else:
        return result


if __name__ == "__main__":
    command = "show clock"
    print(get_output(device, command))
