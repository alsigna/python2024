from scrapli import Scrapli
from scrapli.logging import enable_basic_logging
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}

enable_basic_logging("./18.debug.log", "DEBUG")


def ping_interactive(device: dict[str, str], target: str) -> Response:
    try:
        with Scrapli(**device) as ssh:
            return ssh.send_interactive(
                interact_events=[
                    ("ping", "[ip]:", False),
                    ("ip", "Target IP address:", False),
                    (target, "Repeat count [5]:", False),
                    ("10", "Datagram size [100]:", False),
                    ("1500", "Timeout in seconds [2]:", False),
                    ("1", "Extended commands [n]:", False),
                    ("", "Sweep range of sizes [n]:", False),
                    ("", "#", False),
                ],
            )
    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


def send_command(device: dict[str, str], command: str) -> Response:
    try:
        with Scrapli(**device) as ssh:
            return ssh.send_command(command=command)
    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    result = ping_interactive(device, "10.255.255.102")
    print(result.result)
    result = send_command(device, "show ver")
    print(result.result)
