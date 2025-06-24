import numpy as np
from pydantic import BaseModel

from .transactions import Transaction


class PredictionInput(Transaction):
    embedding: np.ndarray

    class Config:
        arbitrary_types_allowed = True


class Prediction(BaseModel):
    user_id: str
    model: str
    hash: str
    prediction: int
    confidence: float
