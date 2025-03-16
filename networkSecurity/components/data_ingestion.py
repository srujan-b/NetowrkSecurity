from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging


## Configuration of the data Ingestion Config

from networkSecurity.entity import DataIngestionConfig
from networkSecurity.entity import DataIngestionArtifact

import os 
import sys 
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import pymongo 

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")


class DataIngestion:

    def __init__(self,data_ingestion_config : DataIngestionConfig):

        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e :
            raise NetworkSecurityException(e,sys)
    
    def export_collection_as_dataframe(self):

        logging.info("Starting export_collection_as_dataframe ")

        # Read data from mongo DB
        try:
            database_name = self.data_ingestion_config.database_name  # get the data base name from config file
            collection_name = self.data_ingestion_config.collection_name # get the collection name from config file
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL) # connect to mongo DB get the url from .env file
            collection = self.mongo_client[database_name][collection_name] # get data from mongo db 

            df = pd.DataFrame(list(collection.find())) # convert thte json format to list format 
            if "_id" in df.columns.to_list(): # check if the column header has "_id" column thrn drop it
                df = df.drop(columns=["_id"],axis = 1) 
            
            df.replace({"na":np.nan},inplace=True) # replace all the nan values into np.nan

            
            return df
        except Exception as e:   # Raise any exception if found
            raise NetworkSecurityException(e,sys)
        
    def  export_data_into_feature_store(self,dataframe:pd.DataFrame):

        logging.info("starting export_data_into_feature_store")
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            #creating folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        
        except Exception as e:
            return NetworkSecurityException(e,sys)
    
    def split_data_as_train_test(self,dataframe: pd.DataFrame):


        try:
  
            train_set, test_set = train_test_split(
                dataframe,test_size = self.data_ingestion_config.train_test_split_ratio
            )

            logging.info("Performed train test split on the data frame")
            logging.info("Exicted split_data_as_train_test method of data_ingestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)

            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Exporting train and test file path")
            train_set.to_csv(
                self.data_ingestion_config.training_file_path, index=False,header = True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path, index=False, header=True
            )
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            return NetworkSecurityException(e,sys)
                
    def initiate_data_ingestion(self):

        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataIngestionArtificat = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                                                           test_file_path=self.data_ingestion_config.testing_file_path)
            return dataIngestionArtificat

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        




