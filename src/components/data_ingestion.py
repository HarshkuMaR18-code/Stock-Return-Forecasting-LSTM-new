import os
import sys
from datetime import date

import pandas as pd
import yfinance as yf
from sklearn.model_selection import train_test_split

from src.constants import DATA_START_DATE, NIFTY50_STOCKS, TICKER_TO_ID
from src.exception import MyException
from src.logger import logging

ARTIFACT_DIR = "artifact"
FEATURE_STORE_PATH = os.path.join(ARTIFACT_DIR, "data_ingestion", "stock_data.csv")
TRAIN_PATH = os.path.join(ARTIFACT_DIR, "data_ingestion", "train.csv")
TEST_PATH = os.path.join(ARTIFACT_DIR, "data_ingestion", "test.csv")
TRAIN_TEST_SPLIT_RATIO = 0.2


class DataIngestion:
    def download_stock_data(self) -> pd.DataFrame:
        try:
            logging.info("Downloading stock data")
            df = yf.download(
                NIFTY50_STOCKS,
                start=DATA_START_DATE,
                end=date.today(),
                progress=False,
                auto_adjust=True,
            )
            df = df.stack(level="Ticker", future_stack=True).reset_index()
            df.rename(columns={"Ticker": "ticker", "Date": "date"}, inplace=True)
            df["ticker_id"] = df["ticker"].map(TICKER_TO_ID)
            df.sort_values(["ticker", "date"], inplace=True)
            df.reset_index(drop=True, inplace=True)
            logging.info(f"Data Shape: {df.shape}")
            return df
        except Exception as e:
            raise MyException(e, sys)

    def run(self) -> tuple[str, str]:
        try:
            df = self.download_stock_data()
            os.makedirs(os.path.dirname(FEATURE_STORE_PATH), exist_ok=True)
            df.to_csv(FEATURE_STORE_PATH, index=False)
            df = df.sort_values("date")
            train, test = train_test_split(
                df, test_size=TRAIN_TEST_SPLIT_RATIO, shuffle=False
            )
            train.to_csv(TRAIN_PATH, index=False)
            test.to_csv(TEST_PATH, index=False)
            logging.info("Train and test data saved")
            return TRAIN_PATH, TEST_PATH
        except Exception as e:
            raise MyException(e, sys)