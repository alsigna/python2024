import time

import paramiko

with paramiko.SSHClient() as client:
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname="192.168.122.101",
        port=22,
        username="admin",
        password="P@ssw0rd",
        look_for_keys=False,
        allow_agent=False,
        timeout=5,
    )
    with client.invoke_shell() as ssh:
        ssh.send("show ip interface brief\n")
        time.sleep(2)
        result = ssh.recv(10000)


print(result.decode())
