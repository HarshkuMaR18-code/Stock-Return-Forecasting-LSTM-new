import sys

import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

from src.components.data_transformation import SCALER_PATH
from src.components.model_trainer import MODEL_PATH
from src.constants import (
    FEATURE_COLUMNS,
    SEQUENCE_WINDOW_SIZE,
    TICKER_TO_ID,
)
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_object


class StockData:
    def __init__(self, ticker: str, recent_ohlcv: pd.DataFrame):
        self.ticker = ticker
        self.recent_ohlcv = recent_ohlcv

    def get_stock_input_data_frame(self) -> pd.DataFrame:
        df = self.recent_ohlcv.copy()
        df["ticker"] = self.ticker
        df["ticker_id"] = TICKER_TO_ID[self.ticker]
        return df


class StockDataClassifier:
    @staticmethod
    def add_technical_features(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()
        df["return_1d"] = df["Close"].pct_change()
        df["ma_7"] = df["Close"].rolling(7).mean()
        df["ma_21"] = df["Close"].rolling(21).mean()
        df["volatility_7"] = df["return_1d"].rolling(7).std()
        df.dropna(inplace=True)
        return df

    def predict(self, stock_data: StockData) -> float:
        try:
            logging.info("Loading model")
            model = load_model(MODEL_PATH)

            scaler: MinMaxScaler = load_object(SCALER_PATH)

            df = stock_data.get_stock_input_data_frame()
            df = self.add_technical_features(df)

            if len(df) < SEQUENCE_WINDOW_SIZE:
                raise Exception(
                    f"Need at least {SEQUENCE_WINDOW_SIZE} rows, got {len(df)}."
                )

            df[FEATURE_COLUMNS] = scaler.transform(df[FEATURE_COLUMNS])

            X_seq = np.expand_dims(
                df[FEATURE_COLUMNS].values[-SEQUENCE_WINDOW_SIZE:],
                axis=0,
            )

            X_ticker = np.array([df["ticker_id"].iloc[-1]])

            prediction = model.predict([X_seq, X_ticker], verbose=0)

            predicted_return = float(prediction[0][0])

            logging.info(
                f"Predicted return for {stock_data.ticker}: {predicted_return}"
            )

            return predicted_return

        except Exception as e:
            raise MyException(e, sys)
        
