import pexpect

result = pexpect.run("ping 192.168.122.101 -c 3")
print(result.decode())
