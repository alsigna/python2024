import paramiko

with open("/Users/alexigna/.ssh/gcp_eve_rsa", "r") as _file:
    privkey = paramiko.RSAKey.from_private_key(_file)

with paramiko.Transport(("34.140.213.179", 22)) as transport:
    transport.connect(username="alexigna", pkey=privkey)

    remotepath = "/home/alexigna/python.exaple"
    localpath = "/Users/alexigna/key.json"
    with paramiko.SFTPClient.from_transport(transport) as sftp:
        # sftp.get(remotepath, localpath)
        sftp.put(localpath, remotepath)
