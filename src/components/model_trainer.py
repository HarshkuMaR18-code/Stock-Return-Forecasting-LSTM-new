import os
import sys

import numpy as np
import tensorflow as tf
from sklearn.metrics import mean_absolute_error, r2_score
from tensorflow.keras import layers, models

from src.constants import (
    FEATURE_COLUMNS,
    MODEL_TRAINER_BATCH_SIZE,
    MODEL_TRAINER_CONV_FILTERS,
    MODEL_TRAINER_DROPOUT,
    MODEL_TRAINER_EARLY_STOPPING_PATIENCE,
    MODEL_TRAINER_EMBEDDING_DIM,
    MODEL_TRAINER_EPOCHS,
    MODEL_TRAINER_EXPECTED_MAE,
    MODEL_TRAINER_LEARNING_RATE,
    MODEL_TRAINER_LSTM_UNITS,
    NIFTY50_STOCKS,
    SEQUENCE_WINDOW_SIZE,
)
from src.exception import MyException
from src.logger import logging
from src.utils.main_utils import load_numpy_array_data

ARTIFACT_DIR = "artifact"
MODEL_PATH = os.path.join(ARTIFACT_DIR, "model_trainer", "model.keras")


class ModelTrainer:
    def __init__(self, train_npz_path: str, test_npz_path: str):
        self.train_npz_path = train_npz_path
        self.test_npz_path = test_npz_path

    @staticmethod
    def build_model(num_tickers: int, window: int, n_features: int) -> tf.keras.Model:
        seq_input = layers.Input(shape=(window, n_features), name="seq_input")

        x = layers.Conv1D(
            MODEL_TRAINER_CONV_FILTERS,
            kernel_size=3,
            activation="relu",
            padding="causal",
        )(seq_input)
        x = layers.Conv1D(
            MODEL_TRAINER_CONV_FILTERS,
            kernel_size=3,
            activation="relu",
            padding="causal",
        )(x)
        x = layers.LSTM(MODEL_TRAINER_LSTM_UNITS)(x)
        x = layers.Dropout(MODEL_TRAINER_DROPOUT)(x)

        ticker_input = layers.Input(shape=(1,), name="ticker_input")
        ticker_embed = layers.Embedding(
            input_dim=num_tickers,
            output_dim=MODEL_TRAINER_EMBEDDING_DIM,
        )(ticker_input)
        ticker_embed = layers.Flatten()(ticker_embed)

        merged = layers.Concatenate()([x, ticker_embed])
        merged = layers.Dense(32, activation="relu")(merged)
        merged = layers.Dropout(MODEL_TRAINER_DROPOUT)(merged)
        output = layers.Dense(1, activation="linear", name="output")(merged)

        return models.Model(
            inputs=[seq_input, ticker_input],
            outputs=output,
        )

    def run(self) -> tuple[str, float]:
        try:
            logging.info("Loading data")

            train = load_numpy_array_data(self.train_npz_path)
            test = load_numpy_array_data(self.test_npz_path)

            X_seq_train = train["X_seq"]
            X_ticker_train = train["X_ticker"]
            y_train = train["y"]

            X_seq_test = test["X_seq"]
            X_ticker_test = test["X_ticker"]
            y_test = test["y"]

            model = self.build_model(
                len(NIFTY50_STOCKS),
                SEQUENCE_WINDOW_SIZE,
                len(FEATURE_COLUMNS),
            )

            model.compile(
                optimizer=tf.keras.optimizers.Adam(
                    learning_rate=MODEL_TRAINER_LEARNING_RATE
                ),
                loss="mae",
                metrics=["mae"],
            )

            early_stop = tf.keras.callbacks.EarlyStopping(
                monitor="val_loss",
                patience=MODEL_TRAINER_EARLY_STOPPING_PATIENCE,
                restore_best_weights=True,
            )

            logging.info("Training model")

            model.fit(
                [X_seq_train, X_ticker_train],
                y_train,
                validation_data=([X_seq_test, X_ticker_test], y_test),
                epochs=MODEL_TRAINER_EPOCHS,
                batch_size=MODEL_TRAINER_BATCH_SIZE,
                callbacks=[early_stop],
                verbose=2,
            )

            y_pred = model.predict([X_seq_test, X_ticker_test]).flatten()

            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            direction_accuracy = np.mean(np.sign(y_test) == np.sign(y_pred))

            logging.info(
                f"MAE: {mae}, R2: {r2}, Direction Accuracy: {direction_accuracy}"
            )

            if mae > MODEL_TRAINER_EXPECTED_MAE:
                logging.info(
                    f"MAE {mae} is greater than expected {MODEL_TRAINER_EXPECTED_MAE}"
                )

            os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
            model.save(MODEL_PATH)

            return MODEL_PATH, mae

        except Exception as e:
            raise MyException(e, sys)