from networkSecurity.entity import ClassificationMetricArtificat
from networkSecurity.exception import NetworkSecurityException
from sklearn.metrics import f1_score,precision_score,recall_score
import sys

def get_classification_score(y_true,y_pred) -> ClassificationMetricArtificat:

    try:
        model_f1_score = f1_score(y_true,y_pred)
        model_recall_score = recall_score(y_true,y_pred)
        model_prescision_score = precision_score(y_true,y_pred)

        classification_metric = ClassificationMetricArtificat(f1_score=model_f1_score,
                                                              precision_score = model_prescision_score,
                                                              recall_score = model_recall_score)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e,sys) 
    