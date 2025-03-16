from networkSecurity.components.data_ingestion import DataIngestion
from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.entity import DataIngestionConfig
from networkSecurity.entity import TrainingPiplineConfig

import sys
if __name__ =='__main__':

    try:
    
        data_ingestion = DataIngestion(DataIngestionConfig(TrainingPiplineConfig()))
        logging.info("Initiate the data Ingestion")
        data_ingestion_artificat = data_ingestion.initiate_data_ingestion()  
        print(data_ingestion_artificat)
    
    except Exception as e:

        raise NetworkSecurityException(e,sys)


