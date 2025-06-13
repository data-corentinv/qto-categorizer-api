""" Default settings.
"""
import os
import pathlib

DATA_LOADER_MODULE = ""

MODEL_LOCAL_REL_DIR = "data/models"

# LOCAL
LOCAL_DIR = pathlib.Path(os.getcwd())
LOCAL_TEMP_DIR = pathlib.Path(os.getcwd()) / "tmp"

MODEL_LOCAL_DIR = LOCAL_DIR / MODEL_LOCAL_REL_DIR
URL_OR_MODEL_PATH = MODEL_LOCAL_DIR

LOG_LEVEL = "DEBUG"

SVR_HOST = "0.0.0.0"
SVR_PORT = 80

ROOT_PATH = "/"

WORKERS = 1
