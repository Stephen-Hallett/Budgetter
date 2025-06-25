from collections import Counter

import litserve as ls

from database.db import BudgetterDB
from database.schemas.predictions import Prediction, PredictionInput


# define the api to include any number of models, dbs, etc...
class VotingNN(ls.LitAPI):
    def setup(self, device: ls.api.LitAPI.device, neighbours: int = 1):
        self.db = BudgetterDB()
        self.neighbours = neighbours
        self.name = "1nn"

    def decode_request(self, request: dict[str, dict]) -> PredictionInput:
        return PredictionInput.model_validate(request["input"])

    def predict(self, transaction: PredictionInput) -> Prediction:
        results = self.db.predictions.find_nearest_neibours(
            query_embedding=transaction["embedding"], neighbours=self.neighbours
        )
        segment_counts = Counter(result["segment_id"] for result in results)
        segment = segment_counts.most_common(1)[0]
        return Prediction(
            user_id=transaction["user_id"],
            model=self.name,
            hash=transaction["hash"],
            prediction=segment[0],
            confidence=segment[1] / self.neighbours,
        )

    def encode_response(self, output: Prediction) -> dict[str, str | float]:
        return output.model_dump()
