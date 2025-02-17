from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logging
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig,DataTrasformationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact,DataTransformationArtifact

import sys

if __name__ == '__main__':
    try:
        # Initialize training pipeline config
        training_pipeline_config = TrainingPipelineConfig()
        
        # Initialize data ingestion config and ingestion component
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        
        logging.info("Initiating the data ingestion process")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(data_ingestion_artifact)
        
        # Initialize data validation config and validation component
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        
        logging.info("Initiating the data validation process")
        data_validation_artifact = data_validation.initiate_data_validation()  # Corrected method name here
        logging.info("Data validation completed")
        print(data_validation_artifact)


        data_transformation_config=DataTrasformationConfig(training_pipeline_config)
        data_transformation=DataTransformation(data_validation_artifact,data_transformation_config)
        logging.info("intitaing the data transformation")
        data_transformation_artifact=data_transformation.initiate_data_transformation()
        logging.info("data transformation is completed")
        print(data_transformation_artifact)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys)




