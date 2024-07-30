from scrapli import Scrapli
from scrapli.response import Response

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "user",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    # "auth_secondary": "P@ssw0rd",
    "default_desired_privilege_level": "exec",
    # "default_desired_privilege_level": "privilege_exec",
    # "default_desired_privilege_level": "configuration",
}


def send_command(device: dict[str, str], command: str) -> Response:
    try:
        with Scrapli(**device) as ssh:
            # ssh.acquire_priv("privilege_exec")
            output = ssh.send_command(command)
            return output

    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    result = send_command(device, "show ip arp")
    print(result.result)
