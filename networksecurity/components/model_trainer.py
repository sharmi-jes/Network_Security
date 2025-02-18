import os
import sys
import pandas as pd

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logging

from networksecurity.constants import training_pipeline
from networksecurity.entity.artifact_entity import DataTransformationArtifact,ModelTrainerArtifact,ClassificationMetricArtifact
from networksecurity.entity.config_entity import ModelTrainerConfig
from networksecurity.utils.main_utils.utils import load_numpy_array_data,load_object,save_object,evaluate_models


from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from networksecurity.utils.ml_utils.metric.classification_metric import get_classification_score
from networksecurity.utils.ml_utils.model.estimator import NetworkModel
from sklearn.ensemble import (
    AdaBoostClassifier,
    
    GradientBoostingClassifier,
    RandomForestClassifier,
)

class ModelTrainer:
    def __init__(self,data_transformation_artifact:DataTransformationArtifact,
                model_trainer_config:ModelTrainerConfig):
        try:
            self.data_transformation_artifact=data_transformation_artifact
            self.model_trainer_config=model_trainer_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def read_data(self,file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def train_model(self,x_train,y_train,x_test,y_test):
        try:
            models={
                 "Random Forest": RandomForestClassifier(),
                "Decision Tree": DecisionTreeClassifier(),
                "Gradient Boosting": GradientBoostingClassifier(verbose=1),
                "Logistic Regression": LogisticRegression(verbose=1),
                "AdaBoost": AdaBoostClassifier(),




            } 
            params={
            "Decision Tree": {
                'criterion':['gini', 'entropy', 'log_loss'],
                # 'splitter':['best','random'],
                # 'max_features':['sqrt','log2'],
            },
            "Random Forest":{
                # 'criterion':['gini', 'entropy', 'log_loss'],
                
                # 'max_features':['sqrt','log2',None],
                'n_estimators': [8,16,32,128,256]
            },
            "Gradient Boosting":{
                # 'loss':['log_loss', 'exponential'],
                'learning_rate':[.1,.01,.05,.001],
                'subsample':[0.6,0.7,0.75,0.85,0.9],
                # 'criterion':['squared_error', 'friedman_mse'],
                # 'max_features':['auto','sqrt','log2'],
                'n_estimators': [8,16,32,64,128,256]
            },
            "Logistic Regression":{},
            "AdaBoost":{
                'learning_rate':[.1,.01,.001],
                'n_estimators': [8,16,32,64,128,256]
            }
            
        }
        

            model_report:dict=evaluate_models(x_train=x_train,x_test=x_test,y_train=y_train,y_test=y_test,models=models,params=params)

            best_score=max(sorted((model_report.values())))

            best_model_name=list(model_report.keys())[
                list(model_report.values()).index(best_score)
            ]

            best_model=models[best_model_name]


            y_train_pred=best_model.predict(x_train)

            # clasculate the alls cores

            classification_train_score=get_classification_score(y_true=y_train,y_pred=y_train_pred)

            y_test_pred=best_model.predict(x_test)

            classification_test_score=get_classification_score(y_true=y_test,y_pred=y_test_pred)

            # take the preprocessor objetc
            preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)
            dir_path=os.path.dirname(self.model_trainer_config.model_trainer_dir)
            os.makedirs(dir_path,exist_ok=True)

            # take the model from model folder

            network_model=NetworkModel(preprocessor=preprocessor,model=best_model)

            save_object(self.model_trainer_config.model_trainer_dir,obj=NetworkModel)
        #model pusher
            save_object("final_model/model.pkl",best_model)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def intitate_model_trainer(self)->ModelTrainerArtifact:
        try:
            train_data=self.data_transformation_artifact.transformed_train_file_path
            test_data=self.data_transformation_artifact.transformed_test_file_path


            train_arr = load_numpy_array_data(train_data)
            test_arr = load_numpy_array_data(test_data)

            x_train, y_train, x_test, y_test = (
                train_arr[:, :-1],
                train_arr[:, -1],
                test_arr[:, :-1],
                test_arr[:, -1],
            )

            model_trainer_artifact=self.train_model(x_train,y_train,x_test,y_test)
            return model_trainer_artifact

            
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
        # jio
