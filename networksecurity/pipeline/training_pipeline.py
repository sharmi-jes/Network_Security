import os
import sys

from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logging

logging.info("take the all components")
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer


logging.info("take the all config files")
from networksecurity.entity.config_entity import(
    TrainingPipelineConfig,
    DataIngestionConfig,
    DataValidationConfig,
    DataTrasformationConfig,
    ModelTrainerConfig
)


logging.info("take tha all artifacts ")
from networksecurity.entity.artifact_entity import (
    DataIngestionArtifact,
    DataValidationArtifact,DataTransformationArtifact,ModelTrainerArtifact
)


class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config=TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()
            return data_ingestion_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config=DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact,data_validation_config=data_validation_config)
            data_validation_artifacts=data_validation.initiate_data_validation()
            return data_validation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_data_transformation(self,data_validation_artifacts:DataValidationArtifact):
        try:
            data_transformation_config=DataTrasformationConfig(training_pipeline_config=self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifacts,data_transformation_config=data_transformation_config)
            data_transformation_artifacts=data_transformation.initiate_data_transformation()
            return data_transformation_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifacts:DataTransformationArtifact):
        try:
            model_trainer_config=ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer=ModelTrainer(data_transformation_artifacts,model_trainer_config=model_trainer_config)
            model_trainer_artifacts=model_trainer.intitate_model_trainer()
            return model_trainer_artifacts
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def start_run(self):
        try:
           data_ingestion_artifacts=self.start_data_ingestion()
           data_validation_artifact=self.start_data_validation(data_ingestion_artifacts)
           data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
           model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
           return model_trainer_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
