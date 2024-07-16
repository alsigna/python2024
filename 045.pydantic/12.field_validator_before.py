from ipaddress import IPv4Address

from pydantic import AliasPath, BaseModel, Field, field_validator

response = {
    "id": 24,
    "url": "http://10.211.55.7:8000/api/dcim/devices/24/",
    "display": "rt01",
    "name": "rt01",
    "device_type": {
        "id": 3,
        "url": "http://10.211.55.7:8000/api/dcim/device-types/3/",
        "display": "ASR1001-HX",
        "manufacturer": {
            "id": 1,
            "url": "http://10.211.55.7:8000/api/dcim/manufacturers/1/",
            "display": "Cisco",
            "name": "Cisco",
            "slug": "cisco",
            "description": "",
        },
        "model": "ASR1001-HX",
        "slug": "asr1001-hx",
        "description": "",
    },
    "role": {
        "id": 1,
        "url": "http://10.211.55.7:8000/api/dcim/device-roles/1/",
        "display": "router",
        "name": "router",
        "slug": "router",
        "description": "",
    },
    "tenant": None,
    "platform": None,
    "serial": "123456qwerty",
    "asset_tag": None,
    "site": {
        "id": 1,
        "url": "http://10.211.55.7:8000/api/dcim/sites/1/",
        "display": "hq",
        "name": "hq",
        "slug": "hq",
        "description": "",
    },
    "location": None,
    "rack": None,
    "position": None,
    "face": None,
    "latitude": None,
    "longitude": None,
    "parent_device": None,
    "status": {"value": "active", "label": "Active"},
    "airflow": None,
    "primary_ip": {
        "id": 1,
        "url": "http://10.211.55.7:8000/api/ipam/ip-addresses/1/",
        "display": "192.168.123.123/24",
        "family": {"value": 4, "label": "IPv4"},
        "address": "192.168.123.123/24",
        "description": "",
    },
    "primary_ip4": {
        "id": 1,
        "url": "http://10.211.55.7:8000/api/ipam/ip-addresses/1/",
        "display": "192.168.123.123/24",
        "family": {"value": 4, "label": "IPv4"},
        "address": "192.168.123.123/24",
        "description": "",
    },
    "primary_ip6": None,
    "oob_ip": None,
    "cluster": None,
    "virtual_chassis": None,
    "vc_position": None,
    "vc_priority": None,
    "description": "some new description",
    "comments": "",
    "config_template": None,
    "config_context": {},
    "local_context_data": None,
    "tags": [],
    "custom_fields": {},
    "created": "2024-05-28T08:57:28.426846Z",
    "last_updated": "2024-07-16T11:07:02.326251Z",
    "console_port_count": 0,
    "console_server_port_count": 0,
    "power_port_count": 0,
    "power_outlet_count": 0,
    "interface_count": 5,
    "front_port_count": 0,
    "rear_port_count": 0,
    "device_bay_count": 0,
    "module_bay_count": 0,
    "inventory_item_count": 0,
}


class IP(BaseModel):
    address: IPv4Address
    mask: int = Field(ge=0, le=32)


class Site(BaseModel):
    name: str
    description: str


class Device(BaseModel):
    name: str
    model: str = Field(validation_alias=AliasPath("device_type", "model"))
    vendor: str = Field(validation_alias=AliasPath("device_type", "manufacturer", "name"))
    role: str = Field(validation_alias=AliasPath("role", "name"))
    serial: str
    site: Site
    mgmt_ip: IP = Field(validation_alias=AliasPath("primary_ip4", "address"))

    @field_validator("vendor")
    @classmethod
    def validate_vendor(cls, value: str) -> str:
        if value.lower() not in ["huawei", "cisco", "arista"]:
            raise ValueError(f"неизвестный проиводитель {value}")
        return value.upper()

    @field_validator("mgmt_ip", mode="before")
    @classmethod
    def validate_ip(cls, value: str) -> dict[str, str]:
        address, mask = value.split("/")
        return dict(address=address, mask=mask)


device = Device.model_validate(response)
print(device)
