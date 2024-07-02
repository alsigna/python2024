from random import randint


class Switch:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    @property
    def free_interface_count(self) -> int:
        # подключаемся к устройству/обращаемся в базе и вычисляем
        # количество свободных портов
        print("...делаем вычисления...")
        return randint(10, 20)


sw = Switch("192.168.1.1", "sw1")

print(sw.free_interface_count)
