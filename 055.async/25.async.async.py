import asyncio

from scrapli import AsyncScrapli

device_scrapli = {
    "transport": "asyncssh",
    "platform": "cisco_iosxe",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "transport_options": {
        "open_cmd": [
            "-o",
            "KexAlgorithms=+diffie-hellman-group-exchange-sha1",
            "-o",
            "HostKeyAlgorithms=+ssh-rsa",
        ]
    },
}


async def get_output_scrapli(ip: str, cmd: str) -> str:
    print(f"{ip:>15}: connecting ...")
    device = device_scrapli | {"host": ip}
    async with AsyncScrapli(**device) as ssh:
        output = (await ssh.send_command(cmd)).result
    print(f"{ip:>15}: done")
    return output


async def get_output(ip_addresses: list[str], cmd: str) -> list[str]:
    result = []
    tasks = [asyncio.create_task(get_output_scrapli(ip, cmd)) for ip in ip_addresses]
    for coro in asyncio.as_completed(tasks):
        result.append(await coro)
    return result


ip_addresses = [
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


if __name__ == "__main__":
    # python 03.async.thread.py  3.03s user 37.24s system 380% cpu 10.588 total
    asyncio.run(get_output(ip_addresses, "show version"))
