import time

from scrapli import Driver

device = {
    "host": "192.168.122.101",
    "auth_username": "admin",
    "auth_password": "P@ssw0rd",
    "auth_strict_key": False,
}

with Driver(**device) as ssh:
    _, output_ch = ssh.channel.send_input("show clock")
    prompt = ssh.channel.get_prompt()

    ssh.transport.write(b"show clock\n")
    time.sleep(1)
    output_tr = ssh.transport.read()

print(prompt)
print("-" * 10)
print(output_ch.decode())
print("-" * 10)
print(output_tr.decode())
