from scrapli import Scrapli
from scrapli.response import MultiResponse

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}


def send_commands(device: dict[str, str], commands: list[str]) -> MultiResponse:
    try:
        with Scrapli(**device) as ssh:
            return ssh.send_commands(
                commands=commands,
                stop_on_failed=True,
            )
    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    result = send_commands(
        device,
        [
            "show ip arp",
            "shw ip int br",
            "show version",
        ],
    )
    print(result.result)
