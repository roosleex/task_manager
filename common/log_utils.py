# Utilities for logging
import os
import logging
from datetime import datetime


class DailyLogFileHandler(logging.Handler):
    def __init__(self, base_dir):
        super().__init__()
        self.base_dir = base_dir
        self.current_date = None
        self.file_handler = None

    def _get_log_path(self):
        now = datetime.now()
        year = str(now.year)
        month = str(now.month)
        filename = now.strftime("%Y%m%d") + ".log"

        folder = os.path.join(self.base_dir, year, month)
        os.makedirs(folder, exist_ok=True)

        return os.path.join(folder, filename), now.date()

    def emit(self, record):
        try:
            log_path, today = self._get_log_path()

            # recreate handler if date changed
            if self.current_date != today:
                if self.file_handler:
                    self.file_handler.close()

                self.file_handler = logging.FileHandler(log_path)
                self.file_handler.setFormatter(self.formatter)
                self.current_date = today

            self.file_handler.emit(record)

        except Exception:
            self.handleError(record)