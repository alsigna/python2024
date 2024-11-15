import netmiko
from netmiko.exceptions import AuthenticationException, ConfigInvalidException, ReadTimeout

params = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}


def get_output(device: dict[str, str], cmd: str) -> str:
    with netmiko.ConnectHandler(**device) as ssh:
        ssh.enable()
        output = ssh.send_command(cmd)
        output = ssh.send_config_set(
            config_commands="crypto key generate rsa label SSH modulus 2048",
            error_pattern="%",
        )
    return output


cmd = "show platform"
try:
    output = get_output(params, cmd)
except AuthenticationException:
    print(f"невозможно подключиться, {params.get('host')}: {cmd}")
except ReadTimeout:
    print(f"таймаут во время сбора команды {params.get('host')}: {cmd}")
except ConfigInvalidException:
    print(f"ошибка при настройки устройства {params.get('host')}")
except Exception as exc:
    print(f"неизвестное исключение {params.get('host')}: {cmd}: {exc.__class__.__name__}: {str(exc)}")
else:
    print(output)
