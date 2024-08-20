# Написать функцию с сигнатурой `get_output(device: dict[str, str], command: str) -> str`,
# аргументами которой являются словарь с параметрами для подключения и команда,
# которую необходимо выполнить на устройстве. Для подключения используется библиотека netmiko,
# платформа - любая, доступная для тестирования, команда, так же произвольная, существующая на оборудовании

from netmiko import ConnectHandler

device = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}


def get_output(device: dict[str, str], command: str) -> str:
    with ConnectHandler(**device) as ssh:
        ssh.enable()
        result = ssh.send_command(command)
    return result


if __name__ == "__main__":
    command = "show clock"
    print(get_output(device, command))
