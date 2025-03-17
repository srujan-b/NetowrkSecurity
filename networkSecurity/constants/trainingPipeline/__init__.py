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
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"

"""
Data Transformation related constant start with Data_transformation var nmae
"""

DATA_TRANS_DIR_NAME: str = "data_transformation"
DATA_TRANS_TRANSFORMED_DATA_DIR: str = "transformed"
DATA_TRANS_TRANSFORMED_OBJECT_DIR:str = "transformed_object"

## KNN imputer to replace nan values

DATA_TRANS_IMPUTER_PARAMS: dict = {
    "missing_values": np.nan,
    "n_neighbors": 3,
    "weights": "uniform",
}

DATA_TRANS_TRAIN_FILE_PATH: str = "train.npy" 
DATA_TRANS_TEST_FILE_PATH: str = "test.npy"

"""
## Model Training related constants starts with Model_Trainer
"""
MODEL_TRAINER_DIR_NAME : str =  "model_trainer"
MODEL_TRAINER_TRAINED_MODEL_DIR:str = "trained_model"
MODEL_TRAINER_TRAINED_MODEL_NAME:str = "model.pkl"
MODEL_TRAINER_EXPECTED_SCORE:float = 0.6
MODEL_TRAINER_OVER_FITTING_UNDER_FITTING_THRESHOLD:float = 0.05 

SAVED_MODE_DIR: str = os.path.join("saved_models")
MODEL_FILE_NAME: str = "model.pkl"