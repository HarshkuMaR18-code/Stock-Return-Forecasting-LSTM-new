import sys

from src.exception import MyException
from src.logger import logging


class DataValidation:
    def __init__(self, train_path: str, test_path: str):
        self.train_path = train_path
        self.test_path = test_path

    def run(self) -> bool:
        try:
            logging.info("Data validation skipped.")
            return True
        except Exception as e:
            raise MyException(e, sys)