import os
import sys
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging import logging
from networksecurity.entity.artifact_entity import ModelTrainerArtifact,ClassificationMetricArtifact
from sklearn.metrics import recall_score,f1_score,precision_score

def get_classification_score(y_true,y_pred)->ClassificationMetricArtifact:
    try:
        model_recall_score=recall_score(y_true,y_pred)
        model_f1_score=f1_score(y_true,y_pred)
        model_precision_score=precision_score(y_true,y_pred)

        classification_metric=ClassificationMetricArtifact(f1_score=model_f1_score,recall_score=model_recall_score,precision_score=model_precision_score)
        return classification_metric
    
    except Exception as e:
        raise NetworkSecurityException(e,sys)


