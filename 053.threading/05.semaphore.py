from threading import BoundedSemaphore, Thread

from scrapli import Scrapli

max_connections = 3
pool = BoundedSemaphore(max_connections)

scrapli_template = {
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "transport": "telnet",
}


def print_version(host: str) -> None:
    print(f"{host:>15}: начало работы функции")
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


ip_addresses = [
    "192.168.122.101",
    "192.168.122.102",
    "192.168.122.109",
    "192.168.122.110",
    "192.168.122.111",
    "192.168.122.112",
    "192.168.122.113",
    "192.168.122.114",
    "192.168.122.115",
    "192.168.122.116",
    "192.168.122.117",
    "192.168.122.118",
]

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
