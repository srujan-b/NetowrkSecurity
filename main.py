from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.components.data_validation import DataValidation
from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.entity import DataIngestionConfig,DataValidationConfig
from networkSecurity.entity import TrainingPiplineConfig

import sys
if __name__ =='__main__':

    try:
        
        data_ingestion = DataIngestion(DataIngestionConfig(TrainingPiplineConfig()))
        logging.info("Initiate the data Ingestion")
        data_ingestion_artificat = data_ingestion.initiate_data_ingestion()  
        print(data_ingestion_artificat)
        logging.info("Data Initiation Completed")
        data_validation_config = DataValidationConfig(TrainingPiplineConfig())
        data_validation = DataValidation(data_ingestion_artificat,data_validation_config)
        
        logging.info("Initiate the data Validation")
        data_Validation_artificat = data_validation.initiate_data_validation()
        print(data_Validation_artificat)

    except Exception as e:

        raise NetworkSecurityException(e,sys)


