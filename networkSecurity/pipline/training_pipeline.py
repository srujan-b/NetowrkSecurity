import os
import sys
from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.components import DataIngestion,DataTransformation,DataValidation,ModelTrainer

from networkSecurity.entity import (TrainingPiplineConfig,DataIngestionConfig,
                                    DataTransformationConfig,DataValidationConfig,ModelTrainerConfig,
                                    DataIngestionArtifact,DataValidationArtificat,DataTransformationArtifact,ModelTrainerArtificat)

from networkSecurity.constants.trainingPipeline import TRAINING_BUCKET_NAME
from networkSecurity.cloud import S3sync
class TrainingPipeline:

    def __init__(self):
        self.training_pipline_config = TrainingPiplineConfig()
        self.s3_sync = S3sync()
    
    def start_data_ingestion(self):

        try: 
            self.data_ingestion_config = DataIngestionConfig(training_pipline_config= self.training_pipline_config)
            logging.info("start data Ingestion")
            data_ingestion = DataIngestion(data_ingestion_config= self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and artifact: {data_ingestion_artifact}")
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_validation(self,data_ingestion_artificat:DataIngestionArtifact):

                
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipline_config)
            data_validation = DataValidation(data_ingestion_artificat=data_ingestion_artificat,data_validation_config=data_validation_config)
            logging.info("Initiate the data Validation")
            data_validation_artificat = data_validation.initiate_data_validation()
            return data_validation_artificat

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_data_transformation(self,data_validation_artifact = DataValidationArtificat):
        try:
            data_transformation_config = DataTransformationConfig(training_pipline_config=self.training_pipline_config)
            logging.info("started the transformations")
            data_transformation = DataTransformation(data_validation_artificat= data_validation_artifact,
                                                     data_transforamtion_config= data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            return data_transformation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def start_model_trainer(self,data_transformation_artificat:DataTransformationArtifact):

        try:
            self.model_trainer_config : ModelTrainerConfig = ModelTrainerConfig(
                training_pipeline_config=self.training_pipline_config
            )
            model_trainer = ModelTrainer(
                data_transformation_artificat= data_transformation_artificat,
                model_trainer_config = self.model_trainer_config,
            )

            model_trainer_artificat = model_trainer.initiate_model_trainer()

            return model_trainer_artificat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def sync_artificat_dir_to_s3(self):

        try:
            print("uploading artificats")
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/artifact/{self.training_pipline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipline_config.artificat_dir,aws_bucket_url = aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    print(" ")
    def sync_model_dir_to_s3(self):

        try:
            aws_bucket_url = f"s3://{TRAINING_BUCKET_NAME}/final_model/{self.training_pipline_config.timestamp}"
            self.s3_sync.sync_folder_to_s3(folder = self.training_pipline_config.artificat_dir,aws_bucket_url = aws_bucket_url)

        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact)

            self.sync_artificat_dir_to_s3()
            self.sync_model_dir_to_s3()


            return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)

