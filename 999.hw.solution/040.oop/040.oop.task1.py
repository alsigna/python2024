# Создать класс IPAddress, для создания объекта этого класса необходимо передать ip адрес и маску в формате
# "address/prefix_len". У класса должно быть три атрибута:
# - address
# - prefix_len
# - ip
# в address и prefix_len записываются соответсвующие части входных данных. в ip записывается ip в формате address/prefix_len.
# При этом должна быть выполнена валидация введенных параметров
# ip должен быть строкой из 4 чисел с точками в качестве разделителя, каждое число в диапазоне 0...255
# prefix_len должен быть числом в диапазоне 0...32
# вокруг разделителя "/" могут быть пробелы, нужно их корректно обрабатывать
# Если валидация параметров не пройдена, вызывать исключение ValueError


class IPAddress:
    def __init__(self, ip: str) -> None:
        _address, _prefix_len = self._check_ip(ip)
        self.address = _address
        self.prefix_len = _prefix_len
        self.ip = f"{_address}/{_prefix_len}"

    @classmethod
    def _check_ip(cls, ip: str) -> tuple[str, int]:
        _ip = ip.split("/")
        if len(_ip) != 2:
            raise ValueError("некорректная запись ip")
        _address = cls._check_address(_ip[0])
        _prefix_len = cls._check_prefix_len(_ip[1])
        return _address, _prefix_len

    @classmethod
    def _check_address(cls, address: str) -> str:
        _octets = address.strip().split(".")
        octets = [o for o in _octets if o.isdigit() and 0 <= int(o) <= 255]
        if len(_octets) != 4 or len(octets) != 4:
            raise ValueError("некорректная запись address")
        return address.strip()

    @classmethod
    def _check_prefix_len(cls, prefix_len: str) -> int:
        prefix_len = prefix_len.strip()
        if prefix_len.isdigit() and 0 <= int(prefix_len) <= 32:
            return int(prefix_len)
        raise ValueError("некорректная запись prefix length")


def check(value: str):
    ip = IPAddress(value)
    print(ip.ip)
    print(ip.address)
    print(ip.prefix_len)


ips = [
    "192.168.1.1/24",
    "192.168.1.1 /24",
    "192.168.1.1 / 24",
    "192.168.1.1/42",
    "192.500.1.1/24",
    "192.500.123.123|24",
]
for i in ips:
    try:
        ip = IPAddress(i)
    except Exception as exc:
        print(f"{i:>19}: {exc}")
    else:
        print(f"{i:>19}: {ip.address=}, {ip.prefix_len=}, {ip.ip=}")
