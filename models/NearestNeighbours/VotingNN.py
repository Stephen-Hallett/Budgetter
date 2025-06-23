from collections import Counter

import litserve as ls

from backend.app.schemas.transactions import Transaction
from backend.app.schemas.predictions
from database.db import BudgetterDB


# define the api to include any number of models, dbs, etc...
class VotingNN(ls.LitAPI):
    def setup(self, device: ls.api.LitAPI.device, neighbours: int = 1):
        self.db = BudgetterDB()
        self.neighbours = neighbours
        self.name = "1nn"

    def decode_request(self, request: dict[str, dict]) -> Transaction:
        return Transaction.model_validate(request["input"])

    def predict(self, transaction: Transaction) -> dict[str, str | float]:
        results = self.db.find_nearest_neibours(
            query_embedding=transaction["embedding"], neighbours=self.neighbours
        )
        segment_counts = Counter(result["segment_id"] for result in results)
        segment = segment_counts.most_common(1)[0]
        prediction = Prediction(
            user_id=transaction["user_id"],
            model=self.name,
            hash=transaction["hash"],
            prediction=segment[0],
            confidence=segment[1] / self.neighbours,
        )

        return prediction

    def encode_response(self, output: Prediction):
        return output.model_dump_json()
