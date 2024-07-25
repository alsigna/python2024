# К классе из первого таска добавить методы __str__, дающий строку в виде ip (пример ниже) и __repr__, дающий строку,
# вставив которую в терминал, можно получить тот же python объект (пример ниже) и метод __eq__, позволяющий сравнить два объекта
# класса (считаем объекты равными, если равны атрибуты address и prefix_len)
# Для написанного класса должен без ошибок выполняться код в секции `if __name__ == "__main__"`.


class IPAddress:
    def __init__(self, ip: str) -> None:
        _address, _prefix_len = ip.split("/")
        self.address = _address
        self.prefix_len = _prefix_len
        self.ip = ip

    def __str__(self) -> str:
        return self.ip

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ip='{self.ip}')"

    def __eq__(self, other: object) -> bool:
        return self.address == other.address and self.prefix_len == other.prefix_len


if __name__ == "__main__":
    ip_for_test = [
        "192.168.1.1/24",
    ]
    for raw_ip in ip_for_test:
        ip = IPAddress(raw_ip)
        assert ip.address == raw_ip.split("/")[0], f"неверный адрес для {raw_ip=}"
        assert ip.prefix_len == raw_ip.split("/")[1], f"неверная длина маски для {raw_ip=}"
        assert ip.ip == raw_ip, f"неверный ip адрес для {raw_ip=}"
        assert str(ip) == raw_ip, f"неверная работа метода __str__ для {raw_ip=}"
        ip_repr: IPAddress = eval(repr(ip))
        assert ip_repr.address == ip.address, f"неправильная работа метода __repr__ для {raw_ip=}"
        assert ip_repr.prefix_len == ip.prefix_len, f"неправильная работа метода __repr__ для {raw_ip=}"
        assert ip_repr == ip, f"неправильная работа метода __eq__ для {raw_ip=}"
        ip_ne = IPAddress("0.0.0.0/0")
        assert ip_ne != ip, f"неправильная работа метода __eq__ для {raw_ip=}"
