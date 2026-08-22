import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

LOG_DIR = "logs"

current_time = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
LOG_FILE = f"{current_time}.log"

project_path = os.getcwd()
log_folder = os.path.join(project_path, LOG_DIR)
os.makedirs(log_folder, exist_ok=True)
log_file = os.path.join(log_folder, LOG_FILE)

log_format = logging.Formatter(
    "[%(asctime)s] %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(log_format)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(log_format)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)