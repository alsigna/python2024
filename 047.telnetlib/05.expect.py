import telnetlib

telnet = telnetlib.Telnet(host="192.168.122.101", timeout=10)
telnet.expect([b"[Uu]sername:"], timeout=5)

telnet.write(b"admin\n")
telnet.expect([b"[Pp]assword:"], timeout=5)

telnet.write(b"P@ssw0rd\n")
_, m, _ = telnet.expect([rb"(?P<hostname>\S+)(?P<mode>[#>])"], timeout=5)

telnet.write(b"exit\n")
telnet.read_until(b"foreign host.")
telnet.close()

hostname = m.group("hostname").decode()
mode = m.group("mode").decode()
prompt = hostname + mode

print(f"{hostname=}")
print(f"{mode=}")
print(f"{prompt=}")
