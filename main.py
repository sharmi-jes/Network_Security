from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DatavalidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact

 

import sys

if __name__=='__main__':
    try:
        trainingpipelineconfig=TrainingPipelineConfig()
        dataingestionconfig=DataIngestionConfig(trainingpipelineconfig)
        data_ingestion=DataIngestion(dataingestionconfig)
        logging.info("Initiate the data ingestion")
        dataingestionartifact=data_ingestion.initiate_data_ingestion()
        logging.info("Data Initiation Completed")
        print(dataingestionartifact)


        
        data_validation_config=DatavalidationConfig(trainingpipelineconfig)
        data_validation=DataValidation(dataingestionartifact,data_validation_config)
        logging.info("Initiate the data Validation")
        data_validation_artifact=data_validation.intiate_data_validation()
        logging.info("data Validation Completed")
        print(data_validation_artifact)





    except Exception as e:
        raise NetworkSecurityException(e,sys)





