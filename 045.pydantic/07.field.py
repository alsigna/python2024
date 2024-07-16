from ipaddress import IPv4Address

from pydantic import BaseModel, Field


class IP(BaseModel):
    address: IPv4Address
    mask: int = Field(ge=0, le=32, default=24)


raw = {
    "address": "1.1.1.1",
    "mask": 42,
}

ip = IP.model_validate(raw)
