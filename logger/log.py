#
#           Контакты разработчика:
#               VK: vk.com/dimawinchester
#               Telegram: t.me/teanus
#               Github: github.com/teanus
#
#
#
# ████████╗███████╗ █████╗ ███╗   ██╗██╗   ██╗███████╗
# ╚══██╔══╝██╔════╝██╔══██╗████╗  ██║██║   ██║██╔════╝
#    ██║   █████╗  ███████║██╔██╗ ██║██║   ██║███████╗
#    ██║   ██╔══╝  ██╔══██║██║╚██╗██║██║   ██║╚════██║
#    ██║   ███████╗██║  ██║██║ ╚████║╚██████╔╝███████║
#    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

import logging
from logging.handlers import RotatingFileHandler
from resources import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_filename = f"{config.logging_config()['file_name']}.log"

file_handler = RotatingFileHandler(
    log_filename,
    maxBytes=config.logging_config()["max_bytes"],
    backupCount=config.logging_config()["backup_count"],
)

formatter = logging.Formatter(
    "%(asctime)s - TeaLogger - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
