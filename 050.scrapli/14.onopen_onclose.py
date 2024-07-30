from scrapli import Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}


def write_memory(ssh: Scrapli) -> None:
    ssh.send_command("write memory")


def enable_timestamp(ssh: Scrapli) -> None:
    ssh.send_command("term exec prompt timestamp")
    ssh.send_command("term len 0")


def send_command(device: dict[str, str]) -> Response:
    try:
        with Scrapli(
            **device,
            on_open=enable_timestamp,
            on_close=write_memory,
        ) as ssh:
            output = ssh.send_command("show ip arp")
            return output

    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    result = send_command(device)
    print(result.result)
