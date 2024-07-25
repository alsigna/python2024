from typing import Any

from pydantic import BaseModel, field_validator


class Device(BaseModel):
    class Config:
        extra = "allow"
        # str_to_upper = True
        frozen = True

    name: str
    serial: str
    location: str
    interface_count: int

    @field_validator("*")
    @classmethod
    def str_to_upper(cls, value: Any) -> Any:
        if isinstance(value, str):
            return value.upper()
        else:
            return value


raw_device = dict(
    name="r1",
    serial="abcd",
    location="msk",
    interface_count=3,
    interfaces=["gi0/0", "gi0/1", "gi0/2"],
)

device = Device.model_validate(raw_device)
print(device)
