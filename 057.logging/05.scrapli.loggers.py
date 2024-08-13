import logging

from scrapli import Scrapli
from scrapli.response import Response

logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger()

for logger in logging.root.manager.loggerDict.values():
    print(logger)

# logging.getLogger("scrapli").setLevel(logging.WARNING)
# logging.getLogger("asyncio").setLevel(logging.WARNING)

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def main() -> None:
    with Scrapli(**device) as ssh:
        output: Response = ssh.send_command("show clock")

    print(output.result)


if __name__ == "__main__":
    main()
