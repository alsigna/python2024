import logging
import logging.config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "default": {
            "format": "%(asctime)s - [%(levelname)s] - %(message)s",
            "style": "%",
        },
    },
    "handlers": {
        "console": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "mylog": {
            "handlers": ["console"],
            "level": "INFO",
        },
    },
}
logging.config.dictConfig(config=LOGGING_CONFIG)

log = logging.getLogger("mylog")


def main() -> None:
    log.info("INFO MESSAGE")
    log.warning("WARNING MESSAGE")


if __name__ == "__main__":
    main()
