import os
import sys
import mlflow
from networkSecurity.exception import NetworkSecurityException
from networkSecurity.logging import logging
from networkSecurity.entity import DataTransformationArtifact,ModelTrainerConfig,ModelTrainerArtificat


from networkSecurity.utils import save_object,load_npy_array_data,load_object,get_classification_score,NetworkModel,evalaute_models
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import AdaBoostClassifier,GradientBoostingClassifier,RandomForestClassifier

import dagshub
dagshub.init(repo_owner='srujanb28', repo_name='NetowrkSecurity', mlflow=True)



class ModelTrainer:

    def __init__(self,model_trainer_config:ModelTrainerConfig,
                 data_transformation_artificat:DataTransformationArtifact):
        
        try:
            self.model_trainer_config = model_trainer_config
            self.data_transformation_artificat = data_transformation_artificat

        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def track_mlflow(self,best_model,classificationMetric):

        with mlflow.start_run():
            f1_score = classificationMetric.f1_score
            precision_score = classificationMetric.precision_score
            recall_score = classificationMetric.recall_score

            mlflow.log_metric("f1_score",f1_score)
            mlflow.log_metric("precision_score",precision_score)
            mlflow.log_metric("recall_score",recall_score)
            mlflow.sklearn.log_model(best_model,"model")

    def train_model(self,x_train,y_train,x_test,y_test):

        models = {
            "Random Forest": RandomForestClassifier(verbose=1),
            "Descision Tree": DecisionTreeClassifier(),
            "Gradient Boosting": GradientBoostingClassifier(verbose=1),
            "Logistic Regression": LogisticRegression(verbose=1),
            "AdaBoost": AdaBoostClassifier()
        }

        params = {
            "Descision Tree":{
                'criterion' : ['gini'],
                # 'splitter': ['best','random']
                # 'max_features' : ['sqrt', 'log2']
            
            },
            "Random Forest":{
                
                # 'criterion' : ['gini','entropy','log_loss'],
                # 'max_features' : ['sqrt', 'log2',None]
                'n_estimators' : [8,16]
            },
            "Gradient Boosting":{

                'learning_rate':[.1,.01], # ,.05,.001
                'subsample':[0.6,0.7],#,0.75,0.8,0.85,0.9
                # 'criterion':['squared_error','friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators':[8,16]# ,32,64,128,256
            },
            "Logistic Regression":{

            },
            "AdaBoost":{
                'learning_rate': [.1,0.], #1,0.5,.001
                'n_estimators': [8,16] #,32,64,128,256
            }
        }

        model_reports:dict = evalaute_models(x_train,y_train,x_test,y_test,models= models,params = params)
        

        # To get the best model score 
        best_model_score = max(sorted(model_reports.values()))

        # to get the best model name from dict
        best_model_name = list(model_reports.keys())[list(model_reports.values()).index(best_model_score)]

        best_model = models[best_model_name]
        y_train_pred = best_model.predict(x_train)

        classification_train_metric = get_classification_score(y_train,y_train_pred)
        
        ## track in ML flow

        self.track_mlflow(best_model,classification_train_metric)

        y_test_pred = best_model.predict(x_test)
        classification_test_metric = get_classification_score(y_test,y_test_pred)
        self.track_mlflow(best_model,classification_test_metric)

        preprocessor = load_object(self.data_transformation_artificat.transformed_object_file_path)

        model_dir_path = os.path.dirname(self.model_trainer_config.trained_model_file_path)

        os.makedirs(model_dir_path,exist_ok=True)

        Network_Model = NetworkModel(preprocessor=preprocessor, model=best_model)

        save_object(self.model_trainer_config.trained_model_file_path,obj=Network_Model)

        # Model pusher
        save_object("final_model/model.pkl",best_model)

        # model Trainer Artificat
        model_trainer_artificat = ModelTrainerArtificat(trained_model_file_path = self.model_trainer_config.trained_model_file_path,
                                                        train_metric_artificat = classification_train_metric,
                                                        test_metric_artificat = classification_test_metric)
        logging.info(f"Model trainer Artificat:{ModelTrainerArtificat}")
        return model_trainer_artificat


    def initiate_model_trainer(self) -> ModelTrainerArtificat:

        try:
            
            train_file_path = self.data_transformation_artificat.transformed_train_file_path
            test_file_path = self.data_transformation_artificat.transformed_test_file_path

            # loading traing and testing array 
            train_arr = load_npy_array_data(train_file_path)
            test_arr = load_npy_array_data(test_file_path)

            x_train,y_train,x_test,y_test = (
                train_arr[:,:-1],
                train_arr[:,-1],
                test_arr[:,:-1],
                test_arr[:,-1]
            )

            model_trainer_artificat = self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artificat
        except Exception as e:
            raise NetworkSecurityException(e,sys)
