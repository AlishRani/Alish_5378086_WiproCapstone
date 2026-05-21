import logging
import os

LOG_PATH = "reports/logs/nykaa.log"

os.makedirs("reports/logs", exist_ok=True)

logging.basicConfig(
    filename=LOG_PATH,
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()