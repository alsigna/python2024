from pprint import pprint

devices = {
    "rt3": {
        "nb_id": 32,
        "ip": "3.3.3.3",
    },
    "rt1": {
        "nb_id": 908,
        "ip": "1.1.1.1",
    },
    "sw2": {
        "nb_id": 5233,
        "ip": "2.2.2.2",
    },
}

pprint(
    dict(
        sorted(
            devices.items(),
            key=lambda x: x[1]["nb_id"],
        )
    ),
    sort_dicts=False,
)
