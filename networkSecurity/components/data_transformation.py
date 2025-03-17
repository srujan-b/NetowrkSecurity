import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networkSecurity.constants.trainingPipeline import TARGET_COLUMN
from networkSecurity.constants.trainingPipeline import DATA_TRANS_IMPUTER_PARAMS

from networkSecurity.entity import DataValidationArtificat,DataTransformationArtifact,DataTransformationConfig

from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.utils import save_numpy_array,save_object

class DataTransformation:
    def __init__(self,data_validation_artificat: DataValidationArtificat,
                 data_transforamtion_config: DataTransformationConfig):
        try:
            self.data_validation_artificat: DataValidationArtificat = data_validation_artificat
            self.data_transformation_config:DataTransformationConfig = data_transforamtion_config
        except Exception as e:
            return NetworkSecurityException(e,sys)


    @staticmethod
    def read_data(file_path)-> pd.DataFrame:

        print(file_path)

        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def get_data_transformer_object(cls) -> Pipeline:

        """
        It initilises a KNNImputer object with the parameters specified in the training_pipline.py file
        and returns a Pipline object with KNNImputer object as the first step.


        Args:
            cls: DataTransformation
        
        Returns:
            A pipeline Object
        """

        logging.info("Enterd get_data_transformer_object method of Transformation class")

        try:
            imputer:KNNImputer = KNNImputer(**DATA_TRANS_IMPUTER_PARAMS)   
            logging.info(f"Initilize KNNImputer with {DATA_TRANS_IMPUTER_PARAMS}")

            processor:Pipeline = Pipeline([("imputer",imputer)])
            return processor
        
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def initiate_data_transformation(self) -> DataTransformationArtifact:

        logging.info("Entered initiate_data_transformation method of DataTransformation class")
        try:
            logging.info("Starting the data transformation")

            train_df = DataTransformation.read_data(self.data_validation_artificat.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artificat.valid_test_file_path)

            ## Training dataframe
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)

            ## Testing dataframe
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN],axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)

            preprocessor = self.get_data_transformer_object()
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

            train_arr = np.c_[transformed_input_train_feature,np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature,np.array(target_feature_test_df)]

            # save numpy array data 

            save_numpy_array(self.data_transformation_config.transformed_train_file_path,array = train_arr, )
            save_numpy_array(self.data_transformation_config.transformed_test_file_path,array = test_arr, )
            save_object(self.data_transformation_config.transformed_object_file_path,preprocessor_object)  

            # preparing artificats

            data_transformation_artificat = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path = self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path = self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artificat




                                                                            





            
        except Exception as e:
            return NetworkSecurityException(e,sys)

