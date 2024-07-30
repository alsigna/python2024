from scrapli import Scrapli

device = {
    "platform": "cisco_iosxe",
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}

ssh = Scrapli(**device)
ssh.open()
ssh.close()
