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
    output = ssh.send_command_timing("copy running-config bootflash:", strip_command=False) + "\n"
    output += ssh.send_command_timing("") + "\n"
    output += ssh.send_command_timing("")


print(output)
