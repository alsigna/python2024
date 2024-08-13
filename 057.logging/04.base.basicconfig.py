import logging

logging.basicConfig(
    # filename="app.log",
    # filemode="w",
    level=logging.DEBUG,
    encoding="utf-8",
)
log = logging.getLogger()
print(log)


def main() -> None:
    print(log)
    print(log.handlers)
    log.info("INFO MESSAGE")
    log.warning("WARNING MESSAGE")


if __name__ == "__main__":
    main()
