import netmiko

params = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}

with netmiko.ConnectHandler(**params) as ssh:
    ssh.enable()
    prompt = ssh.find_prompt()
    output = ssh.send_command(
        command_string="copy running-config bootflash:",
        expect_string=r"\[running-config\]\?",
    )
    output += ssh.send_command(
        command_string="running-config",
        expect_string=rf"(?:\[confirm\]|{prompt})",
    )
    output += ssh.send_command(
        command_string="",
    )

print(output)
