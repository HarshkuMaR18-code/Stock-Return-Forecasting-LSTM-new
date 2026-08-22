import os
import sys

import pandas as pd

from src.exception import MyException
from src.logger import logging


class DataValidation:
    def __init__(self, train_path: str, test_path: str):
        self.train_path = train_path
        self.test_path = test_path

    def run(self) -> bool:
        try:
            logging.info("Validating dataset files")
            for path in [self.train_path, self.test_path]:
                if not os.path.exists(path):
                    logging.error(f"File not found: {path}")
                    return False
                df = pd.read_csv(path, nrows=10)
                if df.empty:
                    logging.error(f"File is empty: {path}")
                    return False
                required_cols = {"date", "ticker", "ticker_id", "Close", "High", "Low", "Open", "Volume"}
                if not required_cols.issubset(set(df.columns)):
                    logging.error(f"Missing required columns in {path}")
                    return False
            logging.info("Data validation successful")
            return True
        except Exception as e:
            raise MyException(e, sys) from e