import os
import sys
import pandas as pd
import numpy as np


"""
defining common constant variable for training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFACT_DIR: str = "Artifacts"
FILE_NAME: str = "phisingData.csv"

TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH = os.path.join("schema_path", "schema.yaml")

SAVED_MODEL_DIR =os.path.join("saved_models")
MODEL_FILE_NAME = "model.pkl"




"""
Data Ingestion related constant start with DATA_INGESTION VAR NAME
"""
DATA_INGESTION_COLLECTION_NAME: str = "network_data"
DATA_INGESTION_DATABASE_NAME: str = "sharmianyum"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATION: float = 0.2


'''DAta validation related constant variables'''

DATA_VALIDATION_DIR_NAME="data_validation"
DATA_VALIDATION_VALID_DIR="validation"
DATA_VALIDATION_INVALIED_DIR="invalied"

DATA_VALIDATION_DIRFT_REPORT_DIR="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_PATH="report.yaml"

PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"