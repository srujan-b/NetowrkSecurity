from networkSecurity.constants.trainingPipeline import MODEL_FILE_NAME,SAVED_MODE_DIR
import os
import sys
from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging

class NetworkModel:

    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def predict(self,x):
        try:
            x_transform = self.preprocessor.transform(x)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        