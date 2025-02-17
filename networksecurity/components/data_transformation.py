import os
import sys
import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants import training_pipeline
from networksecurity.entity.config_entity import DataTrasformationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact,DataTransformationArtifact
from sklearn.pipeline import Pipeline
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logging
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.utils.main_utils.utils import save_numpy_array_data,save_object

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,
                 data_transformation_config:DataTrasformationConfig):
        try:
            self.data_validation_artifact=data_validation_artifact
            self.data_transformation_config=data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def read_data(self,file_path):
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def get_data_transformer_object(self):
        try:
            impute:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)

            logging.info("knnimputer is intialised")

            processor:Pipeline=Pipeline([("imputer",impute)])
            return processor
        except Exception as e:
            raise NetworkSecurityException(e,sys)

        

    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            train_data=self.data_validation_artifact.valid_train_file_path
            test_data=self.data_validation_artifact.valid_test_file_path

            train_df=self.read_data(train_data)
            test_df=self.read_data(test_data)



            input_feature_train_array=train_df.drop(columns=[TARGET_COLUMN])
            input_feature_target_train_array=train_df[TARGET_COLUMN]
            input_feature_target_train_array=input_feature_target_train_array.replace(-1,0)

            input_feature_test_array=test_df.drop(columns=[TARGET_COLUMN])
            input_feature_target_tets_array=test_df[TARGET_COLUMN]
            input_feature_target_tets_array=input_feature_target_tets_array.replace(-1,0)

            preprocessor=self.get_data_transformer_object()

            preprocessor_train=preprocessor.fit_transform(input_feature_train_array)
            preprocessor_test=preprocessor.transform(input_feature_test_array)

            train_arr=np.c_[
                preprocessor_train,input_feature_target_train_array

            ]

            test_arr=np.c_[
                preprocessor_test,input_feature_target_tets_array

            ]

            #save numpy array data
            save_numpy_array_data( self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data( self.data_transformation_config.transformed_test_file_path,array=test_arr,)
            save_object( self.data_transformation_config.transformed_object_file_path,preprocessor)

            save_object( "final_model/preprocessor.pkl", preprocessor,)


            #preparing artifacts

            data_transformation_artifact = DataTransformationArtifact(
            transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
            transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
            transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,)
            return data_transformation_artifact


            
        except Exception as e:
            raise NetworkSecurityException(e,sys)








