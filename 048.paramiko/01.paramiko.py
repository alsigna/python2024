import time

import paramiko

client = paramiko.SSHClient()
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
ssh = client.invoke_shell()
ssh.send("term len 0\n")
# time.sleep(1)
ssh.send("show ip int br\n")
# time.sleep(1)
ssh.send("show ver\n")
# time.sleep(1)
ssh.send("exit\n")

time.sleep(0.15)

result = ssh.recv(10000)

ssh.close()

print(result.decode())
