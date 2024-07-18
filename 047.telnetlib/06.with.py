import telnetlib

with telnetlib.Telnet(host="192.168.122.101", timeout=10) as telnet:
    telnet.expect([b"[Uu]sername:"], timeout=5)

    telnet.write(b"admin\n")
    telnet.expect([b"[Pp]assword:"], timeout=5)

    telnet.write(b"P@ssw0rd\n")
    _, m, _ = telnet.expect([rb"(?P<hostname>\S+)(?P<mode>[#>])"], timeout=5)

    hostname = m.group("hostname")
    mode = m.group("mode")
    prompt = hostname + mode

    telnet.write(b"term len 0\n")
    telnet.expect([prompt], timeout=5)

    telnet.write(b"show ip arp\n")
    _, _, output = telnet.expect([prompt], timeout=5)

    telnet.write(b"exit\n")
    telnet.read_until(b"foreign host.")

print(output.decode())
