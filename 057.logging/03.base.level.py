import logging

log = logging.getLogger()
print(log)
log.setLevel(logging.DEBUG)
print(log)


def main() -> None:
    print(log)
    print(log.handlers)
    log.info("INFO MESSAGE")
    log.warning("WARNING MESSAGE")


if __name__ == "__main__":
    main()
