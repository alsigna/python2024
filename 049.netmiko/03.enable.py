import netmiko

params = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}

with netmiko.ConnectHandler(**params) as ssh:
    output = ssh.send_command("show platform")
    ssh.enable()
    output += ssh.send_command("show platform")
    ssh.exit_enable_mode()

print(output)
