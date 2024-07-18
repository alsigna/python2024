import netmiko
from netmiko.utilities import structured_data_converter

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
    output = ssh.send_command(command)
    s_output = structured_data_converter(
        raw_data=output,
        command=command,
        platform=ssh.device_type,
        use_textfsm=True,
    )


print(output)
print(s_output)
