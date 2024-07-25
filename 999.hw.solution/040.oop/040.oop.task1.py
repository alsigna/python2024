# Создать класс IPAddress, для создания объекта этого класса необходимо передать ip адрес и маску в формате
# "address/prefix_len". У класса должно быть три атрибута:
# - address
# - prefix_len
# - ip
# в address и prefix_len записываются соответсвующие части входных данных. в ip записывается ip в формате address/prefix_len.
# Для написанного класса должен без ошибок выполняться код в секции `if __name__ == "__main__"`.


class IPAddress:
    def __init__(self, ip: str) -> None:
        _address, _prefix_len = ip.split("/")
        self.address = _address
        self.prefix_len = _prefix_len
        self.ip = ip


if __name__ == "__main__":
    ip_for_test = [
        "192.168.1.1/24",
    ]
    for raw_ip in ip_for_test:
        ip = IPAddress(raw_ip)
        assert ip.address == raw_ip.split("/")[0], f"неверный адрес для {raw_ip=}"
        assert ip.prefix_len == raw_ip.split("/")[1], f"неверная длина маски для {raw_ip=}"
        assert ip.ip == raw_ip, f"неверный ip адрес для {raw_ip=}"
