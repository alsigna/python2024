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
    output = ssh.save_config()

print(output)
