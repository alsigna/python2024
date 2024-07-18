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

    output = ssh.send_multiline(
        [
            ["ping", r"\[ip\]:"],
            ["ip", r"Target IP address:"],
            ["10.255.255.101", r"Repeat count \[5\]:"],
            ["10", r"Datagram size \[100\]:"],
            ["1500", r"Timeout in seconds \[2\]:"],
            ["1", r"Extended commands \[n\]:"],
            ["", r"Sweep range of sizes \[n\]:"],
            ["", prompt],
        ],
    )

print(output)
