from textwrap import dedent

from scrapli import Scrapli
from scrapli.response import Response

device_scrapli = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}


def send_config(device: dict[str, str], config: str) -> Response:
    try:
        with Scrapli(**device) as ssh:
            return ssh.send_config(
                config=config,
                # strip_prompt=False,
                # timeout_ops=10,
                # failed_when_contains="%",
                stop_on_failed=True,
            )
    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    config = dedent(
        """
        no int loo1001
        no int loo1002
        int loo1001
         ip address 100.64.72.201 255.255.255.255
        int loo1002
         ip address 100.64.73.101 255.255.255.255
        """
    )
    config = "no ip domain lookup"
    result = send_config(device_scrapli, config)
