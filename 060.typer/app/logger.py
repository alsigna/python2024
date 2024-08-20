import logging

from rich.logging import RichHandler

log = logging.getLogger("collector")
log.setLevel(logging.DEBUG)

# sh = logging.StreamHandler()
# sh.setLevel(logging.NOTSET)
# sh.setFormatter(
#     logging.Formatter(
#         fmt="%(asctime)s - [%(levelname)s] - %(message)s",
#         datefmt="%Y-%m-%d %H:%M:%S",
#     )
# )


rh = RichHandler(show_time=False)
# rh.setLevel(logging.NOTSET)
rh.setFormatter(
    logging.Formatter(
        fmt="%(asctime)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
)


log.addHandler(rh)
