from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.constants.trainingPipeline import SCHEMA_FILE_PATH

## Configuration of the data Validation Config

from networkSecurity.entity import DataValidationConfig
from networkSecurity.entity import DataIngestionArtifact ,DataValidationArtificat

from scipy.stats import ks_2samp
import pandas as pd
import os,sys
from  networkSecurity.utils import read_yaml_file,write_yaml_file

class DataValidation:

    def __init__(self,data_ingestion_artificat:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        
        try:
            self.data_ingestion_artificat=data_ingestion_artificat
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    @staticmethod
    def read_data(file_Path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_Path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
     

    def validate_number_of_columns(self,dataframe:pd.DataFrame)-> bool:

        try:
            number_of_cols = len(self._schema_config["Columns"])
            logging.info(f"Required number of columns:{number_of_cols}")
            logging.info(f"Data frame has columns:{len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_cols:
                return True
            
            return False

        except Exception as e:
            return NetworkSecurityException(e,sys)

    
    def validate_all_columns_present(self,dataframe:pd.DataFrame) -> bool:

        try:       
            expected_columns = {}
            for col in self._schema_config['columns']:
                expected_columns.update(col)
            missing_cols = [col for col in expected_columns.keys() if col not in dataframe.columns]
            if not missing_cols:
                return True
            return False
        
        except Exception as e:
            return NetworkSecurityException(e,sys)

    def validate_all_data_types(self,dataframe:pd.DataFrame) -> bool:

        try:
            expected_columns = {}
            for col in self._schema_config['columns']:
                expected_columns.update(col)

            for col,expected_dtype in expected_columns.items():

                actual_dtype = str(dataframe[col].dtype)
                if actual_dtype != expected_dtype:

                    return False
            return True
        
        except Exception as e:
            return NetworkSecurityException(e,sys)

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:

        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                if threshold <= is_sample_dist.pvalue:
                    is_found=False
                else:
                    is_found =True
                    status = False
                report.update({column:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            #create directoy

            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report )


        except Exception as e:
            return NetworkSecurityException(e,sys)


    def initiate_data_validation(self) ->DataValidationArtificat:

        try:
            train_file_path = self.data_ingestion_artificat.trained_file_path
            test_file_path = self.data_ingestion_artificat.test_file_path

            ##   read the data from train and test

            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            ## validate number of colmns

            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all the columns.\n"
                logging.info(error_message)
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all the columns.\n" 
                logging.info(error_message)

            ## validate all the columns are present 

            status = self.validate_all_columns_present(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain same number of columns.\n"
                logging.info(error_message)

            status = self.validate_all_columns_present(dataframe=test_dataframe)

            if not status:
                error_message = f"Test dataframe does not contain same number of columns .\n" 
                logging.info(error_message)

            ## validate data types for all the columns
            status = self.validate_all_data_types(dataframe=train_dataframe)
            if not status:
                error_message = f"Train dataframe does not contain all the columns with same data type.\n"
                logging.info(error_message)

            status = self.validate_all_data_types(dataframe=test_dataframe)
            if not status:
                error_message = f"Test dataframe does not contain all the columns with same data type.\n" 
                logging.info(error_message)

            # lets check the data drift 
            status = self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok =True)

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path, index =False,header = True
            )
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path, index=False,header=True
            )

            data_validation_artificat = DataValidationArtificat(
                val_status = status,
                valid_train_file_path = self.data_ingestion_artificat.trained_file_path,
                valid_test_file_path= self.data_ingestion_artificat.test_file_path,
                invalid_train_file_path = None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artificat

        except Exception as e:
            return NetworkSecurityException(e,sys)