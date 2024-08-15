# Написать функцию с сигнатурой `get_output(device: dict[str, str], command: str) -> str`,
# аргументами которой являются словарь с параметрами для подключения и команда,
# которую необходимо выполнить на устройстве. Для подключения используется библиотека scrapli,
# платформа - любая, доступная для тестирования, команда, так же произвольная, существующая на оборудовании
# Задание полностью аналогично Task1 по теме netmiko, но для подключения должна использоваться библиотека Scrapli.
# Возвращать функция должна результат выполнения команды, а не объект Response


from scrapli import Scrapli

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}


def get_output(device: dict[str, str], command: str) -> str:
    with Scrapli(**device) as ssh:
        result = ssh.send_command(command)
    return result.result


if __name__ == "__main__":
    command = "show clock"
    print(get_output(device, command))
