import os

import pynetbox


def create_device(name: str, site: str, role: str, model: str) -> int:
    nb = pynetbox.api(
        url=os.environ.get("NB_URL"),
        token=os.environ.get("NB_TOKEN"),
    )
    if nb.dcim.devices.get(name=name) is not None:
        print(f"устройство с именем {name=} уже существует")
        return 0

    nb_model = nb.dcim.device_types.get(model=model)
    nb_role = nb.dcim.device_roles.get(name=role)
    nb_site = nb.dcim.sites.get(name=site)

    for t, v in zip((nb_model, nb_role, nb_site), ("модель", "роль", "сайт")):
        if t is None:
            print(f"{v} не существует")
            return 0

    device = nb.dcim.devices.create(
        name=name,
        device_type=nb_model.id,
        role=nb_role.id,
        site=nb_site.id,
        status="inventory",
    )
    return device.id


def delete_device(name: str) -> bool:
    nb = pynetbox.api(
        url=os.environ.get("NB_URL"),
        token=os.environ.get("NB_TOKEN"),
    )
    device = nb.dcim.devices.get(name=name)
    if device is None:
        print(f"устройства с именем {name=} не существует")
        return False
    return device.delete()


if __name__ == "__main__":
    print(
        create_device(
            name="dmi01-buffalo-rtr01",
            site="DM-Camden",
            role="Router",
            model="ISR 1111-8P",
        )
    )
    print(create_device("dmi01-buffalo-rtr99", "DM-", "Router", "ISR 1111-8P"))
    print(create_device("dmi01-buffalo-rtr99", "DM-Camden", "Roiter", "ISR 1111-8P"))
    print(create_device("dmi01-buffalo-rtr99", "DM-Camden", "Router", "ISR 1111-8Pdd"))
    print(create_device("dmi01-buffalo-rtr99", "DM-Camden", "Router", "ISR 1111-8P"))

    _ = delete_device("dmi01-buffalo-rtr99")
