import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.data_validation import DataValidation
from src.components.model_evaluation import ModelEvaluation
from src.components.model_trainer import ModelTrainer
from src.exception import MyException
from src.logger import logging


class TrainPipeline:
    def run_pipeline(self) -> None:
        try:
            logging.info("Starting data ingestion")
            train_path, test_path = DataIngestion().run()

            logging.info("Starting data validation")
            if not DataValidation(train_path, test_path).run():
                logging.info("Data validation failed")
                return

            logging.info("Starting data transformation")
            train_npz, test_npz, _ = DataTransformation(
                train_path,
                test_path,
            ).run()

            logging.info("Starting model training")
            _, test_mae = ModelTrainer(train_npz, test_npz).run()

            logging.info("Starting model evaluation")
            if not ModelEvaluation(test_mae).run():
                logging.info("Model evaluation failed")
                return

            logging.info("Training pipeline completed successfully")

        except Exception as e:
            raise MyException(e, sys)
        
        
if __name__ == "__main__":
    print("Pipeline Started...")

    obj = TrainPipeline()
    obj.run_pipeline()

    print("Pipeline Finished...")