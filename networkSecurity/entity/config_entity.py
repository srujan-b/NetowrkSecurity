from datetime import datetime
import os
from networkSecurity.constants import trainingPipeline


print(trainingPipeline.PIPELINE_NAME)

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
