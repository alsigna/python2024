from pydantic import BaseModel


class Device(BaseModel):
    class Config:
        extra = "forbid"
        str_to_upper = True

    name: str
    serial: str
    location: str
    interface_count: int


device = Device(
    name="r1",
    serial="12345",
    location="msk",
    interface_count=3,
    interfaces=["gi0/0", "gi0/1", "gi0/2"],
)

print(device)
