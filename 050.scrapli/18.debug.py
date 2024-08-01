from scrapli import Scrapli
from scrapli.exceptions import ScrapliConnectionNotOpened, ScrapliException
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}


def send_command(device: dict[str, str], command: str) -> Response:
    try:
        with Scrapli(
            **device,
            # channel_log=True,
            # channel_log_mode="append",
            channel_log="./19.debug.log",
        ) as ssh:
            return ssh.send_command(command=command)
    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    result = send_command(device, "show ver")
    print(result.result)
