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
    output = ssh.send_config_set(
        config_commands=[
            "interface loop215",
            "ip address 100.64.215.1 255.255.255.255",
            "exit",
            "interface loop216",
            "ip address 100.64.216.1 255.255.255.355",
            "end",
        ],
        # error_pattern="%",
    )

print(output)
