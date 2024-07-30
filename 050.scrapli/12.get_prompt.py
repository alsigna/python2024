from scrapli import Scrapli

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_secondary": "P@ssw0rd",
    "auth_strict_key": False,
    "default_desired_privilege_level": "exec",
}


def change_prompt(device: dict[str, str]) -> None:
    try:
        with Scrapli(**device) as ssh:
            print(ssh.get_prompt())
            ssh.acquire_priv("privilege_exec")
            print(ssh.get_prompt())
            ssh.acquire_priv("configuration")
            print(ssh.get_prompt())
            ssh.acquire_priv("tclsh")
            print(ssh.get_prompt())
            ssh.acquire_priv("exec")
            print(ssh.get_prompt())

    except Exception as exc:
        print(f"exception class: {exc.__class__.__name__}")
        print(f"exception message: {str(exc)}")
        raise exc


if __name__ == "__main__":
    change_prompt(device)
