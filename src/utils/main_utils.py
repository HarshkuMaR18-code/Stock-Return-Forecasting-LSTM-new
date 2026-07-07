"""
src/utils/main_utils.py
 
Step 19 of the project flow.
Generic helper functions (read/write YAML, save/load objects with
dill, save/load numpy arrays) reused across multiple components.
"""
import os
import sys
 
import dill
import numpy as np
import yaml
 
from src.exception import MyException
from src.logger import logging
 
 
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise MyException(e, sys) from e
 
 
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)
    except Exception as e:
        raise MyException(e, sys) from e
 
 
def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of utils")
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
        logging.info("Exited the save_object method of utils")
    except Exception as e:
        raise MyException(e, sys) from e
 
 
def load_object(file_path: str) -> object:
    try:
        with open(file_path, "rb") as file_obj:
            return dill.load(file_obj)
    except Exception as e:
        raise MyException(e, sys) from e
 
 
def save_numpy_array_data(file_path: str, **arrays: np.ndarray) -> None:
    """
    Saves one or more named numpy arrays into a single compressed .npz file.
    Example: save_numpy_array_data(path, X_seq=X_seq, X_ticker=X_ticker, y=y)
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        np.savez_compressed(file_path, **arrays)
    except Exception as e:
        raise MyException(e, sys) from e
 
 
def load_numpy_array_data(file_path: str) -> dict:
    try:
        with np.load(file_path) as data:
            return {key: data[key] for key in data.files}
    except Exception as e:
        raise MyException(e, sys) from e