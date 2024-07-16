from ipaddress import IPv4Address

from pydantic import BaseModel, Field


class IP(BaseModel):
    address: IPv4Address
    mask: int = Field(ge=0, le=32, default=24, alias="pfx_len", serialization_alias="pfx_len")


raw = {
    "address": "1.1.1.1",
    "pfx_len": 32,
}
ip = IP.model_validate(raw)

ip.model_dump()
ip.model_dump(by_alias=True)
