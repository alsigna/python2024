import telnetlib

telnet = telnetlib.Telnet(host="192.168.122.101", timeout=10)
telnet.read_until(b"Username:")

telnet.write(b"admin\n")
telnet.read_until(b"Password:")

telnet.write(b"P@ssw0rd\n")
telnet.read_until(b">")

telnet.write(b"term len 0\n")
result = telnet.read_until(b">")

telnet.write(b"show version\n")
result += telnet.read_until(b">")

telnet.write(b"exit\n")
telnet.read_until(b"foreign host.")

telnet.close()

result = result.decode()
print(result)
