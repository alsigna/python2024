import telnetlib
import time

telnet = telnetlib.Telnet(host="192.168.122.101", timeout=10)
telnet.expect([b"[Uu]sername:"], timeout=5)

telnet.write(b"admin\n")
telnet.expect([b"[Pp]assword:"], timeout=5)

telnet.write(b"P@ssw0rd\n")
telnet.expect([b"[#>]"], timeout=5)

telnet.write(b"term len 0\n")
telnet.expect([b"[#>]"], timeout=5)

telnet.write(b"show version\n")
telnet.write(b"show ip interface brief\n")
telnet.write(b"exit\n")

result = telnet.read_all().decode()
telnet.close()

print(result)
