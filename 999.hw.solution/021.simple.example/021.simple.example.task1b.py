def range_vlans(vlans):
    vlans_int = list(map(int, vlans.split(",")))
    vlans_int.sort()

    result = []
    start = vlans_int[0]
    end = vlans_int[0]

    for vlan in vlans_int[1:]:
        if vlan == end + 1:
            end = vlan
        else:
            if start == end:
                result.append(f"{start}")
            else:
                result.append(f"{start}-{end}")
            start = vlan
        end = vlan

    result.append(str(start) if start == end else f"{start}-{end}")

    return ",".join(result)


def unrange_vlans(vlans):
    result = []
    for vlan in vlans.split(","):
        if vlan.isdigit():
            result.append(int(vlan))
        elif "-" in vlan:
            vlan_start, vlan_end = vlan.split("-")
            vlan_list = range(int(vlan_start), int(vlan_end) + 1)
            result.extend(vlan_list)
    result_str = map(str, result)
    return ",".join(result_str)


if __name__ == "__main__":
    vlans = {
        "10": "10",
        "10,21": "10,21",
        "10,11": "10-11",
        "10,11,12": "10-12",
        "10,11,12,15": "10-12,15",
        "10,11,12,15,16,17": "10-12,15-17",
        "10,11,12,15,16,17,20": "10-12,15-17,20",
    }
    for long_form, short_form in vlans.items():
        assert range_vlans(long_form) == short_form, f"Ошибка свертывания {long_form}"
        assert unrange_vlans(short_form) == long_form, f"Ошибка развертывания {short_form}"
