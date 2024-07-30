from scrapli.driver import GenericDriver

device = {
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
    "transport": "telnet",
}

with GenericDriver(**device) as ssh:
    ssh.send_command("terminal length 0")
    output = ssh.send_command("show version")
    prompt = ssh.get_prompt()

print(prompt)
print(output.result)
