class CiscoNXOS:
    def get_version(self) -> str:
        print("getting version from NX-OS via NETCONF")
        return "1.2.3"


class CiscoIOS:
    def get_version(self) -> str:
        print("getting version from IOS via SSH")
        return "3.2.1"


devices = [
    CiscoNXOS(),
    CiscoIOS(),
]
for device in devices:
    print("-" * 10)
    print(device.get_version())
