from textwrap import dedent

from scrapli import Scrapli
from scrapli.response import MultiResponse

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}


def send_configs(device: dict[str, str], configs: list[str]) -> MultiResponse:
    try:
        with Scrapli(**device) as ssh:
            return ssh.send_configs(
                configs=configs,
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
        int loo1001
         ip address 100.64.72.101 255.255.255.255
        int loo1002
         ip address 100.64.73.101 255.255.255.255
        """
    ).strip()
    result = send_configs(device, config.splitlines())
    print(result.result)
