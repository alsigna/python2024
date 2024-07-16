from pydantic import BaseModel


class Device(BaseModel):
    name: str
    serial: str
    location: str
    interface_count: int
    interfaces: list[str]


device = Device(
    name="r1",
    serial="12345",
    location="msk",
    interface_count=3,
    interfaces=["gi0/0", "gi0/1", "gi0/2"],
)
