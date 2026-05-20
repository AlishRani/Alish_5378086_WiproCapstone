'''import logging
import os

LOG_PATH = "reports/logs/nykaa.log"

os.makedirs("reports/logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()'''

import logging
import os
from datetime import datetime

LOG_DIR = "reports/logs"
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(
    LOG_DIR,
    f"nykaa_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)

def get_logger(name="nykaa_logger"):
    logger = logging.getLogger(name)

    if logger.hasHandlers():  # avoid duplicate logs
        logger.handlers.clear()

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )

    # File handler
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger