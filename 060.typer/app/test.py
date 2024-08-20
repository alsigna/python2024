import sys

from loguru import logger

logger.remove()
logger.add(
    sink=sys.stderr,
    level="INFO",
    serialize=False,
)

logger.add(
    sink="log.log",
    level="DEBUG",
    rotation="10 KB",
    compression="zip",
    encoding="utf-8",
)

for _ in range(100):
    logger.debug("That's it, beautiful and simple logging!")
    logger.info("INFO тест сообщение")
    logger.warning("Warning")
