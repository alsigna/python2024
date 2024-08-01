from pydantic import BaseModel
from scrapli import Scrapli
from scrapli.logging import enable_basic_logging
from scrapli.response import Response

enable_basic_logging("./test.log", "DEBUG")


class Device(BaseModel):
    host: str
    platform: str
    transport: str = "system"

    def __hash__(self) -> int:
        return hash(self.host + self.platform)


scrapli_template = {
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "ssh_config_file": "./ssh_scrapli",
    # "transport_options": {
    #     "open_cmd": [
    #         "-o",
    #         "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
    #         "-o",
    #         "HostKeyAlgorithms=+ssh-rsa",
    #     ]
    # },
}

devices = {
    # Device(host="192.168.122.107", platform="huawei_vrp"): "display arp",
    Device(host="192.168.122.201", platform="cisco_iosxe"): "show ip int br",
    # Device(host="192.168.122.106", platform="eltex_esr"): "show ip interface",
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
    for device, command in devices.items():
        print("\n<<<" + "=" * 100 + ">>>")
        print(f"{device.host=}, {command}")
        result = send_command(
            device=scrapli_template | device.model_dump(),
            command=command,
        )
        print(result.result)
