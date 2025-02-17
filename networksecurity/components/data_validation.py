import os
import sys
from scipy.stats import ks_2samp
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logging
import pandas as pd
from networksecurity.constants import training_pipeline
from networksecurity.entity import config_entity,artifact_entity
from networksecurity.entity.config_entity import DatavalidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact


from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH

class DataValidation:
    def __init__(self,data_ingestion_artifact:str=DataIngestionArtifact,
                 data_validation_config=DatavalidationConfig):
        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_path=read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def read_data(self,file_path):

        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_no_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            schema_cols=len(SCHEMA_FILE_PATH)
            df_cols=len(dataframe.columns)
            if schema_cols==df_cols:
                return True
            else:
                return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    
    def detect_drift_path(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}

            for col in base_df.columns:
                d1=base_df[col]
                d2=current_df[col]
                is_same_dist=ks_2samp(d1,d2)

                if threshold<=is_same_dist:
                   is_found=False
                else:
                    is_found=True
                    status=False
                report.update({col:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift_status":is_found
                    
                    }})
                
                drift_file_path=self.data_validation_config.drift_report_file_path
                dir_path=os.path.dirname(drift_file_path)

                write_yaml_file(file_path=drift_file_path,content=report)

                os.makedirs(dir_path,exist_ok=True)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

                




    



    def intiate_data_validation(self)->DataValidationArtifact:
        try:
            train_data=self.data_ingestion_artifact.train_file_path
            test_data=self.data_ingestion_artifact.test_file_path

            train_df=self.read_data(train_data)
            test_df=self.read_data(test_data)

            stuats=self.validate_no_of_columns(dataframe=train_data)
            if not stuats:
                return "Train dataframe has not all col"
            
            stuats=self.validate_no_of_columns(dataframe=test_data)
            if not stuats:
                return "test dataframe has not all col"
            

            # drify check
            stauts=self.detect_drift_path(base_df=train_data,current_df=test_data)
            dir_path=os.path.dirname(self.data_validation_config.train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            train_data.to_csv(self.data_validation_config.train_file_path, index=False, header=True)
            test_data.to_csv(self.data_validation_config.test_file_path, index=False, header=True)

            data_validation_artifact=DataValidationArtifact(
                validation_status=stuats,
                valid_train_file_path=self.data_validation_config.train_file_path,
                valid_test_file_path=self.data_validation_config.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)



            




