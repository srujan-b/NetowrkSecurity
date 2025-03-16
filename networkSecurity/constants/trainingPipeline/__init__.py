import os
import sys
import numpy as np
import pandas as pd



"""
Defining common constants variable for training pipeline
"""
TARGET_COLUMN = "Result"
PIPELINE_NAME: str = "NetworkSecurity"
ARTIFICAT_DIR: str = "Artificats"
FILE_NAME: str = "phishingData.csv"
 
TRAIN_FILE_NAME: str = "train.csv"
TEST_FILE_NAME: str = "test.csv"

SCHEMA_FILE_PATH: str = os.path.join("data_schema","schema.yaml")


"""
data ingestion realted constants start with DATA_INGESTION VAR NAME
"""

DATA_INGESTION_COLLECTION_NAME: str = "NetworkData"
DATA_INGESTION_DATABASE_NAME : str = "NetworkDB"
DATA_INGESTION_DIR_NAME: str = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR : str = "feature_store"
DATA_INGESTION_INGESTED_DIR: str = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO: str = 0.2

"""
Data Validation related constants start with DATA_VAL VAR Name
"""

DATA_VAL_DIR_NAME: str = "data_validation"
DATA_VAL_VALID_DIR: str = "validated"
DATA_VAL_INVALID_DIR: str = "invalid"
DATA_VAL_DRIFT_REPORT_DIR: str = "drift_report"
DATA_VAL_DRIFT_REPORT_FILE_NAME: str = "report.yaml"
 

