def parse_device(value: str | list | tuple | dict) -> dict[str, str]:
    match value:
        case hostname, ip, platform:
            return {"hostname": hostname, "ip": ip, "platform": platform}
        case {"hostname": hostname, "ip": ip, "platform": platform}:
            return {"hostname": hostname, "ip": ip, "platform": platform}
        case str() if len(value.split()) == 3:
            hostname, ip, platform = value.split()
            return {"hostname": hostname, "ip": ip, "platform": platform}
        case _:
            return {"error": "неизвестный формат данных"}


if __name__ == "__main__":
    hostname = "rt1.hq.lab.ru"
    ip = "192.168.1.2"
    platform = "cisco_ios"
    target = {"hostname": hostname, "ip": ip, "platform": platform}
    assert parse_device([hostname, ip, platform]) == target
    assert parse_device((hostname, ip, platform)) == target
    assert parse_device(target) == target
    assert parse_device(target | {"transport": "system"}) == target
    assert parse_device(f"{hostname} {ip} {platform}") == target
    assert parse_device([hostname, ip, platform, "border"]) == {"error": "неизвестный формат данных"}
