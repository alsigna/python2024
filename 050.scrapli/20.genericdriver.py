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
    ssh.send_command("terminal width 512")
    output = ssh.send_command("show ip arp")
    ssh.send_command("conf t")
    ssh.send_command("int loo123")
    ssh.send_command("ip add 1.2.3.4 255.255.255.0")
    prompt = ssh.get_prompt()

print(prompt)
print(output.result)
