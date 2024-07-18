import paramiko
from scp import SCPClient

with paramiko.Transport(("192.168.122.101", 22)) as transport:
    transport.connect(username="admin", password="P@ssw0rd")
    localpath = "/Users/alexigna/key.json"
    with SCPClient(transport) as scp:
        scp.put(localpath, "test.json")
