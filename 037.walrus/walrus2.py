import time


def get_site_type(site: str) -> str:
    time.sleep(1)
    if site in ["MSK", "NSK", "SPB"]:
        return "DC"
    else:
        return "LAN"


site_codes = ["MSK", "NSK", "SPB", "OMS", "KLG"]


sites = [
    {
        "name": site_code,
        "type": get_site_type(site_code),
    }
    for site_code in site_codes
    if get_site_type(site_code) == "DC"
]


sites = []
for site_code in site_codes:
    site_type = get_site_type(site_code)
    if site_type == "DC":
        sites.append({"name": site_code, "type": site_type})


sites = [
    {"name": site_code, "type": site_type}
    for site_code in site_codes
    if (site_type := get_site_type(site_code)) == "DC"
]
