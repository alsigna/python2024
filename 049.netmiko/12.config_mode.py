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
    output = ssh.config_mode()
    prompt = ssh.find_prompt()
    # print(f"{prompt=}")
    output += ssh.send_command("crypto key generate rsa label TEST modulus 2048")
    ssh.exit_config_mode()

print(output)
