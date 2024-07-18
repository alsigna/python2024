import netmiko

params = {
    "device_type": "cisco_xe",
    "host": "192.168.122.101",
    "username": "admin",
    "password": "P@ssw0rd",
    "secret": "P@ssw0rd",
}
# with netmiko.ConnectHandler(**params) as ssh:
#     with netmiko.FileTransfer(
#         ssh_conn=ssh,
#         source_file="/Users/alexigna/key.json",
#         dest_file="my_master_password",
#         file_system="bootflash:",
#     ) as scp:
#         scp.transfer_file()

with netmiko.ConnectHandler(**params) as ssh:
    with netmiko.FileTransfer(
        ssh_conn=ssh,
        source_file="/Users/alexigna/key.json",
        dest_file="my_master_password",
        file_system="bootflash:",
    ) as scp:
        space = scp.remote_space_available()
        print(f"===> {space} bytes available")
        if scp.check_file_exists() and scp.compare_md5():
            print("===> file exists")
        elif scp.verify_space_available():
            print("===> copying file...")
            scp.transfer_file()
