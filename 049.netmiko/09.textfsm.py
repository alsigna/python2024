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
    command = "show ip interface brief"
    output = ssh.send_command(
        command_string=command,
        use_textfsm=True,
    )

print(output)
