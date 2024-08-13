import logging

log = logging.getLogger()


def main() -> None:
    print(log)
    print(log.handlers)
    log.info("INFO MESSAGE")
    log.warning("WARNING MESSAGE")


if __name__ == "__main__":
    main()
