from threading import BoundedSemaphore, Thread
from typing import Any

from scrapli import Scrapli


class ThreadWithReturn(Thread):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None

    def run(self) -> None:
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args) -> Any:
        Thread.join(self, *args)
        return self._return


max_connections = 2
pool = BoundedSemaphore(max_connections)


scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def print_version(host: str) -> str:
    print(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}
    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")
    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    result = f"{host:>15}: {hostname:>3}, {version}"
    print(f"{host:>15}: завершено")
    return result


def print_version_sem(host: str) -> str:
    with pool:
        return print_version(host)


ids = [1, 2]
ids.extend(range(9, 19))
ip_addresses = [f"192.168.122.1{i:02}" for i in ids]

### последовательный сбор
# for ip in ip_addresses:
#     try:
#         print_version(ip)
#     except:
#         pass

### сбор в потоках
threads: list[Thread] = []
for ip in ip_addresses:
    threads.append(
        ThreadWithReturn(
            target=print_version_sem,
            args=(ip,),
        )
    )

for t in threads:
    t.start()

results = []
for t in threads:
    results.append(t.join())


for r in results:
    print(r)
