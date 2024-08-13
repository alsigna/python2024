import logging

log = logging.getLogger("myapp")
log.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)

fmt = logging.Formatter(
    fmt="%(asctime)s - [%(levelname)s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
sh.setFormatter(fmt)

fh = logging.FileHandler(filename="./app.log", mode="a")
fh.setLevel(logging.INFO)
fh.setFormatter(fmt)

log.addHandler(sh)
log.addHandler(fh)


def main() -> None:
    log.info("INFO MESSAGE")
    log.warning("WARNING MESSAGE")


if __name__ == "__main__":
    main()
