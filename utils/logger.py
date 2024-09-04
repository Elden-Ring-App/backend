import logging


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("Backend")
        self.logger.setLevel(logging.INFO)

        if not self.logger.hasHandlers():
            console_handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def get_logger(self):
        return self.logger


# Instantiate the Logger class and get the logger
logger_instance = Logger()
logger = logger_instance.get_logger()
