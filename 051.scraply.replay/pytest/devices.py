import re

from scrapli import Scrapli


class CiscoDevice:
    def __init__(self, host: str):
        self.ssh = Scrapli(
            host=host,
            platform="cisco_iosxe",
            auth_strict_key=False,
            auth_username="admin",
            auth_password="P@ssw0rd",
            transport_options={
                "open_cmd": [
                    "-o",
                    "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
                    "-o",
                    "HostKeyAlgorithms=+ssh-rsa",
                ],
            },
        )

    def _open(self):
        if not self.ssh.isalive():
            try:
                self.ssh.open()
            except Exception:
                raise

    def get_version(self):
        self._open()
        output = self.ssh.send_command("show version | i Software")
        self.ssh.close()
        if output.failed:
            return "__FAILURE__"

        version = re.findall(r"version ([a-z0-9_\.\(\)]*)", output.result, flags=re.I)
        if not version:
            return "__FAILURE__"

        return version[0]


if __name__ == "__main__":
    device = CiscoDevice("192.168.122.113")
    version = device.get_version()
    print(version)
