from netaddr import EUI

mac1 = EUI("0007.ECE1.5D18")
mac2 = EUI("0007ECE15D18")
mac3 = EUI("00-07-EC-E1-5D-18")
mac4 = EUI("00:07:ec:e1:5d:18")

print(mac1 == mac2)
print(mac1 == mac3)
print(mac1 == mac4)

print(mac1)
