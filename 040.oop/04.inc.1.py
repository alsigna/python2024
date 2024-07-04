class Device:
    def __init__(self) -> None:
        self._uptime = 0
        self.__hostname = "r1"

    def get_hostname(self) -> str:
        return self.__hostname


d = Device()

print(d._uptime)
d._uptime = 1
print(d._uptime)

print(d.get_hostname())
print(d.__hostname)
