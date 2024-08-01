import time

from scrapli import Scrapli
from scrapli.exceptions import ScrapliConnectionError

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "default_desired_privilege_level": "exec",
}


def check_alive(device: dict[str, str]) -> None:
    try:
        with Scrapli(**device) as ssh:
            print(ssh.get_prompt())
            isalive = ssh.isalive()
            print(f"after connect: {isalive=}")

            time.sleep(20)
            try:
                _ = ssh.get_prompt()
            except ScrapliConnectionError:
                ssh.open()

            isalive = ssh.isalive()
            print(f"after clear: {isalive=}")

            if not isalive:
                ssh.open()

                isalive = ssh.isalive()
                print(f"after reconnect: {isalive=}")

            print(ssh.get_prompt())

    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    check_alive(device)
