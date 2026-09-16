from typing import Optional, Dict, Any, List
from pydantic import BaseModel

class FeatureImportanceItem(BaseModel):
    feature: str
    importance: float

class ModelMetadataSchema(BaseModel):
    id: int
    model_name: str
    version: str
    dataset_name: str
    trained_at: Optional[str] = None
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    status: str
    confusion_matrix: Optional[List[List[int]]] = None
    feature_importances: Optional[List[FeatureImportanceItem]] = None

    class Config:
        from_attributes = True
