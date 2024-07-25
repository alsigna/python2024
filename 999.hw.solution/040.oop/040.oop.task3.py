# Продолжаем дорабатывать класс IPAddress, на этом этапе нужно сделать валидацию входных данных и приведение типов
# Валидация входных данных:
# - входной параметр ip должен быть строкой, формата `a.b.c.d/e`
#   - `a.b.c.d`  - 4 чисела с точками в качестве разделителя между ними, каждое число в диапазоне 0...255
#   - `/` - разделитель, может обрамляться пробелами до или после себя (в коде их нужно корректно обрабатывать и отрезать)
#   - `e` - число в диапазоне 0...32
# Если валидация входного параметра не пройдена, вызывать исключение ValueError
# Приведение типов: длинна префикса это число в диапазоне 0...32, поэтому сохранять терь его нужно не как строку (как в предудущих заданиях),
# а как челочисленную переменную (int)


class IPAddress:
    def __init__(self, ip: str) -> None:
        _address, _prefix_len = self._check_ip(ip)
        self.address = _address
        self.prefix_len = _prefix_len
        self.ip = f"{_address}/{_prefix_len}"

    def __str__(self) -> str:
        return self.ip

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ip='{self.ip}')"

    def __eq__(self, other: object) -> bool:
        return self.address == other.address and self.prefix_len == other.prefix_len

    @classmethod
    def _check_ip(cls, ip: str) -> tuple[str, int]:
        _ip = ip.split("/")
        if len(_ip) != 2:
            raise ValueError(f"некорректная запись ip: {ip}")
        _address = cls._check_address(_ip[0])
        _prefix_len = cls._check_prefix_len(_ip[1])
        return _address, _prefix_len

    @classmethod
    def _check_address(cls, address: str) -> str:
        _octets = address.strip().split(".")
        octets = [o for o in _octets if o.isdigit() and 0 <= int(o) <= 255]
        if len(_octets) != 4 or len(octets) != 4:
            raise ValueError(f"некорректная запись address {address}")
        return address.strip()

    @classmethod
    def _check_prefix_len(cls, prefix_len: str) -> int:
        prefix_len = prefix_len.strip()
        if prefix_len.isdigit() and 0 <= int(prefix_len) <= 32:
            return int(prefix_len)
        raise ValueError(f"некорректная запись prefix length {prefix_len}")


if __name__ == "__main__":
    ips = [
        "192.168.1.1/24",
        "192.168.1.1 /24",
        "192.168.1.1 / 24",
    ]
    for raw_ip in ips:
        ip = IPAddress(raw_ip)
        ip_stripped = raw_ip.split("/")[0].strip()
        prefix_len_stripper = raw_ip.split("/")[1].strip()
        assert ip.address == raw_ip.split("/")[0].strip(), f"неверный адрес для {raw_ip=}"
        assert ip.prefix_len == int(prefix_len_stripper), f"неверная длина маски для {raw_ip=}"
        assert ip.ip == ip_stripped + "/" + prefix_len_stripper, f"неверный ip адрес для {raw_ip=}"
        assert str(ip) == ip_stripped + "/" + prefix_len_stripper, f"неверная работа метода __str__ для {raw_ip=}"
        ip_repr: IPAddress = eval(repr(ip))
        assert ip_repr.address == ip.address, f"неправильная работа метода __repr__ для {raw_ip=}"
        assert ip_repr.prefix_len == ip.prefix_len, f"неправильная работа метода __repr__ для {raw_ip=}"
        assert ip_repr == ip, f"неправильная работа метода __eq__ для {raw_ip=}"
        ip_ne = IPAddress("0.0.0.0/0")
        assert ip_ne != ip, f"неправильная работа метода __eq__ для {raw_ip=}"
    bad_ips = [
        "192.168.1.1/42",
        "192.300.1.1/24",
        "192.300.123.123|24",
    ]
    for raw_ip in bad_ips:
        try:
            _ = IPAddress(raw_ip)
        except ValueError:
            continue
        else:
            assert False, f"ошибка валидации данных для {raw_ip}"
