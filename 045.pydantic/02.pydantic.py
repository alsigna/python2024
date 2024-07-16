import os
from pprint import pprint

import requests
from pydantic import BaseModel


class Device(BaseModel):
    name: str
    serial: str
    id: int


def get_nb_device(hostname: str) -> dict[str, str]:
    # export NB_URL=http://10.211.55.7:8000
    # export NB_TOKEN=d6f4e314a5b5fefd164995169f28ae32d987704f

    url = os.environ.get("NB_URL", "")
    token = os.environ.get("NB_TOKEN", "")

    headers = {
        "Authorization": f"Token {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.get(
        url=f"{url}/api/dcim/devices/?name={hostname}",
        headers=headers,
    )
    response.raise_for_status()
    result_json = response.json()
    if result_json["count"] != 1:
        return {}
    else:
        return result_json["results"][0]


raw_device = get_nb_device("rt01")

pprint(raw_device)

device = Device.model_validate(raw_device)

device.model_dump()
device.model_dump_json()
