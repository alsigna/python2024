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
