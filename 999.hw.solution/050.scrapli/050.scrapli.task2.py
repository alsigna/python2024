# Дорабатывает функцию `get_output(device: dict[str, str], command: str) -> str` из первого задания. Как и
# в заданиях по netmiko нужно добавить обработку исключений:
# - неправильного логин/пароля (выводим в терминал "неправильные логин/пароль для подключения к устройству")
# - недоступности устройства (выводим в терминал "устройство недоступно"). Тут следует учесть, что при использовании разных
#   методов подключения (параметр transport) к устройству, scrapli будет выводить разные ошибки при недоступности. Нужно отлавливать,
#   по возможности, их все. Что бы при смене транспорта недоступность устройства не попала в неизвестные ошибки
# - все остальные ошибки (выводим в терминал "неизвестное исключение при работе с устройством")
# В случаи исключения функция должна возвращать пустую строку.
#
# Кроме этого, у пользователя может не быть прав для доступа в привилегированный режим на устройству, и нужно сделать так, что бы функция,
# при подключении к оборудованию, выполняла сбор команды в том режиме, в котором пользователь подключается на устройство. Т.е. если
# подключается пользователь admin с priv 15 и сразу попадает в # (privilege exec) режим, то мы никуда не переходим и вывод собираем в нем,
# а если подключается пользователь user с priv level 1, и попадает в > (exec) режим, то никуда не переходим (не даем enable), а собираем
# выводы из > режима
#
# Так же нужно проверять успешность сбора команды. Если команду собрать не удалось, тогда печатать на экран "Ошибка в сборе команды"
# и выводить саму ошибку. Функция при этом должна возвращать пустую строку.

from scrapli import Scrapli
from scrapli.driver import NetworkDriver
from scrapli.exceptions import ScrapliAuthenticationFailed, ScrapliConnectionError, ScrapliTimeout

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "user",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "system",
}


def get_output(device: dict[str, str], command: str) -> str:
    def on_open(conn: NetworkDriver) -> None:
        prompt = conn.get_prompt()
        if prompt.endswith(">"):
            conn.default_desired_privilege_level = "exec"
        conn.send_command(command="terminal length 0")
        conn.send_command(command="terminal width 512")

    try:
        with Scrapli(**device, on_open=on_open) as ssh:
            result = ssh.send_command(command)
    except ScrapliAuthenticationFailed:
        print(f"Неправильные логин/пароль для устройства {device.get('host')}")
        return ""
    except (ScrapliTimeout, OSError, ScrapliConnectionError):
        print(f"Таймаут подключения к устройству {device.get('host')}")
        return ""
    except Exception as exc:
        print(f"Неизвестная ошибка при работе с устройством {device.get('host')}: {exc.__class__.__name__}: {exc}")
        return ""
    if result.failed:
        print(f"Ошибка в сборе команды:\n{result.channel_input}\n{result.result}")
        return ""
    else:
        return result.result


if __name__ == "__main__":
    command = "show platform"
    print(get_output(device, command))
