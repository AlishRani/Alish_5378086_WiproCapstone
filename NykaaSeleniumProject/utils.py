import logging
from datetime import datetime
from pathlib import Path

import allure


def take_screenshot(driver, name):
    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


def save_screenshot(driver, name, subdir="end to end"):
    screenshot_dir = Path(__file__).parent / subdir
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    filepath = screenshot_dir / f"{name}.png"
    driver.save_screenshot(str(filepath))

    allure.attach(
        driver.get_screenshot_as_png(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )

    return filepath


class TestLogger:
    __test__ = False
    def __init__(self, name="test_run"):
        self.log_dir = Path(__file__).parent / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = self.log_dir / f"{name}_{timestamp}.log"

        self.logger = logging.getLogger(f"{name}_{timestamp}")
        self.logger.setLevel(logging.DEBUG)
        self.logger.handlers.clear()

        fh = logging.FileHandler(self.log_file)
        fh.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s"))
        self.logger.addHandler(fh)

        ch = logging.StreamHandler()
        ch.setFormatter(logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s"))
        self.logger.addHandler(ch)

    def info(self, message):
        self.logger.info(message)

    def step(self, message):
        self.logger.info(f">>> {message}")

    def assert_msg(self, message):
        self.logger.info(f"  ASSERT: {message}")

    def action(self, message):
        self.logger.info(f"  ACTION: {message}")

    def attach_to_allure(self, name="test_log"):
        with open(self.log_file) as f:
            allure.attach(f.read(), name=name, attachment_type=allure.attachment_type.TEXT)

    @property
    def path(self):
        return str(self.log_file)
