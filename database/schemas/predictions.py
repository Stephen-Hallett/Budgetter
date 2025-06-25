import numpy as np
from pydantic import BaseModel, field_validator

from .transactions import Transaction


class PredictionInput(Transaction):
    embedding: list[float]

    @field_validator("embedding", mode="before")
    @classmethod
    def parse_embedding(cls, v: str | list | np.ndarray) -> list[float]:
        if isinstance(v, str):
            v = v.strip("[]")
            return [float(num) for num in v.split(",")]
        if isinstance(v, np.ndarray):
            return v.tolist()
        return v

    class Config:
        arbitrary_types_allowed = True


class Prediction(BaseModel):
    user_id: str
    model: str
    hash: str
    prediction: int
    confidence: float
