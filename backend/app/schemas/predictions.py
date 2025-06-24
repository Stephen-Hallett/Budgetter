import numpy as np
from pydantic import BaseModel

from .transactions import Transaction


class PredictionInput(Transaction):
    embedding: np.ndarray


class Prediction(BaseModel):
    user_id: str
    model: str
    hash: str
    prediction: int
    confidence: float
