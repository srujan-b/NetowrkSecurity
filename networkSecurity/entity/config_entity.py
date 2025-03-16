from datetime import datetime
import os
from networkSecurity.constants import trainingPipeline


class TrainingPiplineConfig:
    def __init__(self,timstamp = datetime.now()):
        timestamp = timstamp.strftime("%m_%d_%Y_%H_%M_%S")
        self.pipeline_name = trainingPipeline.PIPELINE_NAME
        self.artificat_name = trainingPipeline.ARTIFICAT_DIR
        self.artificat_dir = os.path.join(self.artificat_name,timestamp)
        self.timestamp: str=timestamp
        
class DataIngestionConfig:

    def __init__(self,training_pipline_config:TrainingPiplineConfig):
        self.data_ingestion_dir:str = os.path.join(
            training_pipline_config.artificat_dir,trainingPipeline.DATA_INGESTION_COLLECTION_NAME
        )
        self.feature_store_file_path : str = os.path.join(
            self.data_ingestion_dir,trainingPipeline.DATA_INGESTION_FEATURE_STORE_DIR,trainingPipeline.FILE_NAME
        )
        self.training_file_path : str = os.path.join(
            self.data_ingestion_dir,trainingPipeline.DATA_INGESTION_INGESTED_DIR,trainingPipeline.TRAIN_FILE_NAME
        )
        self.testing_file_path : str = os.path.join(
            self.data_ingestion_dir,trainingPipeline.DATA_INGESTION_INGESTED_DIR,trainingPipeline.TEST_FILE_NAME
        )         
        self.train_test_split_ratio : float = trainingPipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name:str = trainingPipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name : str = trainingPipeline.DATA_INGESTION_DATABASE_NAME



class DataValidationConfig:

    def __init__(self, training_pipeline_config: TrainingPiplineConfig):

        # Creates the main directory for storing data validation artifacts
        self.data_val_dir: str = os.path.join(
            training_pipeline_config.artificat_dir, 
            trainingPipeline.DATA_VAL_DIR_NAME
        )
        
        # Creates directories for storing valid and invalid data separately
        self.valid_data_dir: str = os.path.join(self.data_val_dir, trainingPipeline.DATA_VAL_VALID_DIR)
        self.invalid_data_dir: str = os.path.join(self.data_val_dir, trainingPipeline.DATA_VAL_INVALID_DIR)

        # Defines file paths for valid training and test datasets
        self.valid_train_file_path: str = os.path.join(self.valid_data_dir, trainingPipeline.TRAIN_FILE_NAME)
        self.valid_test_file_path: str = os.path.join(self.valid_data_dir, trainingPipeline.TEST_FILE_NAME)
        
        # Defines file paths for invalid training and test datasets
        self.invalid_train_file_path: str = os.path.join(self.invalid_data_dir, trainingPipeline.TRAIN_FILE_NAME)
        self.invalid_test_file_path: str = os.path.join(self.invalid_data_dir, trainingPipeline.TEST_FILE_NAME)

        # Defines the path for the data drift report and creates a directory for it
        self.drift_report_file_path: str = os.path.join(
            self.data_val_dir,
            trainingPipeline.DATA_VAL_DRIFT_REPORT_DIR,
            trainingPipeline.DATA_VAL_DRIFT_REPORT_FILE_NAME,
        )


