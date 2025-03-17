from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.components.data_transformation import DataTransformation
from networkSecurity.components.model_trainer import ModelTrainer
from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig,ModelTrainerConfig
from networkSecurity.entity import TrainingPiplineConfig

import sys
if __name__ =='__main__':

    try:
        trainingPiplineConfig = TrainingPiplineConfig()
        dataIngestionConfig = DataIngestionConfig(trainingPiplineConfig)
        data_ingestion = DataIngestion(dataIngestionConfig)
        logging.info("Initiate the data Ingestion")
        dataingestionartificat = data_ingestion.initiate_data_ingestion()  
        print(dataingestionartificat)
        logging.info("Data Initiation Completed")
        data_validation_config = DataValidationConfig(trainingPiplineConfig)
        data_validation = DataValidation(dataingestionartificat,data_validation_config)
        logging.info("Initiate the data Validation")
        data_Validation_artificat = data_validation.initiate_data_validation() 
        logging.info("data Validation completed")

        print(data_Validation_artificat)

        data_transformation_config= DataTransformationConfig(trainingPiplineConfig)

        logging.info("data Transformation started")
        data_transformation = DataTransformation(data_Validation_artificat,data_transformation_config)

        data_transformation_artifict = data_transformation.initiate_data_transformation()
        print(data_transformation_artifict)
        logging.info("Model Transformation completed")

        logging.info(" model training started")
        model_trainer_config = ModelTrainerConfig(trainingPiplineConfig)
        model_trainer = ModelTrainer(model_trainer_config,data_transformation_artifict)
        model_trainer_artifact=model_trainer.initiate_model_trainer()

        logging.info("Model Traing artificat created")



    except Exception as e:

        raise NetworkSecurityException(e,sys)


