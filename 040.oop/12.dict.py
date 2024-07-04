class Device:
    def __init__(self, ip: str, hostname: str) -> None:
        self.ip = ip
        self.hostname = hostname

    def __str__(self) -> str:
        return f"{self.ip}, {self.hostname}"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.ip}', '{self.hostname}')"


d = Device("192.168.1.1", "rt1")


print(Device.__dict__)
print(d.__dict__)


##
class DataCenter:
    devices = []


dc1 = DataCenter()
dc2 = DataCenter()

print("before adding")
print(dc1.devices)
print(dc2.devices)

dc1.devices.append("r1")
dc1.devices.append("r2")

print("after adding")
print(dc1.devices)
print(dc2.devices)

## borg pattern


class RedisPool:
    _state = {}

    def __init__(self):
        self.__dict__ = self._state
        self._session = None

    def connect(self):
        if self._session is None:
            print("first call, need to create connection...")
            self._session = "some redis session"
        else:
            print("session already exists, no need to connect")

    def disconnect(self):
        self._session = None


r1 = RedisPool()
r2 = RedisPool()

print("before connection")
print(r1._session)
print(r2._session)

r1.connect()
print("after connection")
print(r1._session)
print(r2._session)
