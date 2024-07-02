from typing import Generator


class ConfigParser:
    JUNK_LINES = ["!", "exit-address-family"]

    @classmethod
    def get_config(cls, config: str) -> Generator[str, None, None]:
        for line in config.strip().splitlines():
            if line.strip() in cls.JUNK_LINES:
                continue
            else:
                yield line

    @classmethod
    def get_patch(cls, config: str) -> Generator[str, None, None]:
        last_space = 0
        for line in config.strip().splitlines():
            current_space = len(line) - len(line.lstrip())
            if current_space < last_space:
                last_space = current_space
                yield "exit"
            last_space = current_space
            if line.strip() in cls.JUNK_LINES:
                continue
            else:
                yield line.strip()
