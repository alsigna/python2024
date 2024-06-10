from typing import Generator

import yaml


def get_branch_devices(branch_num: int) -> Generator[dict[str, dict], None, None]:
    for branch in range(1, branch_num + 1):
        yield {
            f"branch{branch}": {
                "routers": [f"rt{branch}{i}.hq" for i in range(2)],
                "switches": [f"sw{branch}{i}.hq" for i in range(2)],
            },
        }


print(
    yaml.safe_dump_all(
        documents=get_branch_devices(2),
    )
)
