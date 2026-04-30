import os
import logging
from datetime import datetime
from ..log_utils import DailyLogFileHandler
from django.test import SimpleTestCase
from environs import Env
env = Env()
env.read_env()
from pathlib import Path


class LogUtilsTests(SimpleTestCase):
    def get_dir_name(self):
        return os.path.join(env.str("APP_CONFIG_ROOT_DIR"), "log")


    def get_file_name(self):
        now = datetime.now()
        return os.path.join(self.get_dir_name(), f"{now.year}/{now.month}/{now.strftime('%Y%m%d')}.log")

    # def create_file(self):
    #     file_path = Path(self.get_file_name())
    #     if not file_path.exists():
    #         file_path.touch()


    def test_log_file_created(self):
        tmp_path = self.get_dir_name()
        handler = DailyLogFileHandler(base_dir=tmp_path)

        logger = logging.getLogger("test_logger_1")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        logger.info("hello world")

        
        log_file = Path(self.get_file_name())
        # print(f"log_file = {log_file}")

        self.assertTrue(log_file.exists())

        content = log_file.read_text()
        self.assertTrue("hello world" in content)


    def test_multiple_logs_same_file(self):
        tmp_path = self.get_dir_name()
        handler = DailyLogFileHandler(base_dir=tmp_path)

        logger = logging.getLogger("test_logger_2")
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

        logger.info("test first line of logfile")
        logger.info("test second line of logfile")

        log_file = Path(self.get_file_name())

        content = log_file.read_text()

        self.assertTrue("test first line of logfile" in content)
        self.assertTrue("test second line of logfile" in content)