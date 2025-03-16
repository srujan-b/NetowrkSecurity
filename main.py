from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.components.data_transformation import DatTransformation
from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.entity import DataIngestionConfig,DataValidationConfig,DataTransformationConfig
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
        data_transformation = DatTransformation(data_Validation_artificat,data_transformation_config)
        data_transformation_artifict = data_transformation.initiate_data_transformation()
        print(data_transformation_artifict)
        logging.info("Model Transformation completed")

    except Exception as e:

        raise NetworkSecurityException(e,sys)


