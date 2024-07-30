from pydantic import BaseModel
from scrapli import Scrapli
from scrapli.response import Response


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
}

devices = {
    Device(host="192.168.122.107", platform="huawei_vrp"): "display arp",
    Device(host="192.168.122.101", platform="cisco_iosxe", transport="telnet"): "show ip arp",
    Device(host="192.168.122.106", platform="eltex_esr"): "show ip interface",
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
