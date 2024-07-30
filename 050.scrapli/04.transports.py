from itertools import product

from scrapli import Scrapli
from scrapli.response import Response

hosts = [
    "192.168.122.101",
    "192.168.122.102",
]

transports = [
    "system",
    # "ssh2",
    "paramiko",
    "telnet",
]

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
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
    for transport, host in product(transports, hosts):
        print("\n<<<" + "=" * 100 + ">>>")
        print(f"{host=}, {transport=}")
        result = send_command(
            device=scrapli_template | {"host": host, "transport": transport},
            command="show ip arp",
        )
        print(result.result)
