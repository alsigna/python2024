from threading import BoundedSemaphore, Thread

from scrapli import Scrapli

max_connections = 2
pool = BoundedSemaphore(max_connections)


scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}


def print_version(host: str) -> None:
    print(f"{host:>15}: подключение...")
    device = scrapli_template | {"host": host}
    with Scrapli(**device) as ssh:
        output = ssh.send_command("show version")
    parsed_output = output.textfsm_parse_output()[0]
    version = parsed_output.get("version")
    hostname = parsed_output.get("hostname")
    print(f"{host:>15}: {hostname:>3}, {version}")


def print_version_sem(host: str) -> None:
    with pool:
        print_version(host)


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
        Thread(
            target=print_version_sem,
            args=(ip,),
        )
    )

for t in threads:
    t.start()

for t in threads:
    t.join()
