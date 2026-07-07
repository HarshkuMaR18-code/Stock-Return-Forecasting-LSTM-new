import sys

from src.constants import MODEL_TRAINER_EXPECTED_MAE
from src.exception import MyException
from src.logger import logging


class ModelEvaluation:
    def __init__(self, model_mae: float):
        self.model_mae = model_mae

    def run(self) -> bool:
        try:
            is_accepted = self.model_mae <= MODEL_TRAINER_EXPECTED_MAE

            if is_accepted:
                logging.info("Model accepted")
            else:
                logging.info(
                    f"Model rejected. MAE: {self.model_mae}, "
                    f"Expected MAE: {MODEL_TRAINER_EXPECTED_MAE}"
                )

            return is_accepted

        except Exception as e:
            raise MyException(e, sys)