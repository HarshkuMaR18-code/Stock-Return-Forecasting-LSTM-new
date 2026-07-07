import os
import sys

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

from src.constants import FEATURE_COLUMNS, FORECAST_HORIZON_DAYS, SEQUENCE_WINDOW_SIZE
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import save_numpy_array_data, save_object

ARTIFACT_DIR = "artifact"
TRAIN_NPZ_PATH = os.path.join(ARTIFACT_DIR, "data_transformation", "train.npz")
TEST_NPZ_PATH = os.path.join(ARTIFACT_DIR, "data_transformation", "test.npz")
SCALER_PATH = os.path.join(ARTIFACT_DIR, "data_transformation", "scaler.pkl")

TARGET_COLUMN = f"target_{FORECAST_HORIZON_DAYS}d_return"


class DataTransformation:
    def __init__(self, train_path: str, test_path: str):
        self.train_path = train_path
        self.test_path = test_path

    @staticmethod
    def read_data(file_path:  str):
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])
        return df

    @staticmethod
    def add_technical_features(group: pd.DataFrame):
        group = group.copy()
        group["return_1d"] = group["Close"].pct_change()
        group["ma_7"] = group["Close"].rolling(7).mean()
        group["ma_21"] = group["Close"].rolling(21).mean()
        group["volatility_7"] = group["return_1d"].rolling(7).std()
        group[TARGET_COLUMN] = (
            group["Close"].shift(-FORECAST_HORIZON_DAYS) / group["Close"] - 1
        )  
        return group

    def engineer_features(self, df: pd.DataFrame):
        df = df.sort_values(["ticker", "date"])
        df = df.groupby("ticker", group_keys=False).apply(self.add_technical_features)
        df.dropna(inplace=True)
        return df

    @staticmethod
    def create_sequences(df: pd.DataFrame, window: int = SEQUENCE_WINDOW_SIZE):
        X_seq, X_ticker, y = [], [], []

        for ticker_id, group in df.groupby("ticker_id"):
            values = group[FEATURE_COLUMNS].values
            targets = group[TARGET_COLUMN].values

            for i in range(window, len(group)):
                X_seq.append(values[i - window:i])
                X_ticker.append(ticker_id)
                y.append(targets[i])

        return np.array(X_seq), np.array(X_ticker), np.array(y)

    def run(self) -> tuple[str, str, str]:
        try:
            logging.info("Starting data transformation")

            train_df = self.engineer_features(self.read_data(self.train_path))
            test_df = self.engineer_features(self.read_data(self.test_path))

            scaler = MinMaxScaler()

            train_df[FEATURE_COLUMNS] = scaler.fit_transform(train_df[FEATURE_COLUMNS])
            test_df[FEATURE_COLUMNS] = scaler.transform(test_df[FEATURE_COLUMNS])

            X_seq_train, X_ticker_train, y_train = self.create_sequences(train_df)
            X_seq_test, X_ticker_test, y_test = self.create_sequences(test_df)

            save_numpy_array_data(
                TRAIN_NPZ_PATH,
                X_seq=X_seq_train,
                X_ticker=X_ticker_train,
                y=y_train,
            )

            save_numpy_array_data(
                TEST_NPZ_PATH,
                X_seq=X_seq_test,
                X_ticker=X_ticker_test,
                y=y_test,
            )

            save_object(SCALER_PATH, scaler)

            logging.info("Data transformation completed")

            return TRAIN_NPZ_PATH, TEST_NPZ_PATH, SCALER_PATH

        except Exception as e:
            raise MyException(e, sys)