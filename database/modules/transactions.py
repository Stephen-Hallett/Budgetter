import os

import requests
from psycopg2.extras import RealDictCursor

from ..schemas.transactions import Transaction
from ..schemas.users import User


class Transactions:
    def __init__(self, db) -> None:
        self.db = db

    def create_transaction(self, transaction: Transaction) -> str:
        """Insert transaction and generate embedding for description."""

        # Generate hash and embedding for description
        info_string = self.db.get_info_string(transaction)
        text_hash = self.db.create_text_hash(info_string)
        embedding = self.db.generate_embedding(info_string)

        with self.db.get_connection() as conn, conn.cursor() as cur:
            # Insert transaction
            cur.execute(
                """
                    INSERT INTO transactions (id, account, user_id, hash, date, type, amount, 
                                            description, category, group_name, merchant)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """,
                (
                    transaction.id,
                    transaction.account,
                    transaction.user_id,
                    text_hash,
                    transaction.date,
                    transaction.type,
                    transaction.amount,
                    transaction.description,
                    transaction.category,
                    transaction.group_name,
                    transaction.merchant,
                ),
            )

            # Insert embedding
            cur.execute(
                """
                    INSERT INTO embeddings (hash, embedding)
                    VALUES (%s, %s)
                    ON CONFLICT (hash) DO NOTHING
                """,
                (text_hash, embedding.tolist()),
            )
            conn.commit()

        model_names = self.db.models.list_models()
        predictive_info = self.db.predictions.get_prediction_input(transaction.id)
        for model in model_names:
            _ = requests.post(
                f"http://models:{os.environ['MODELS_PORT']}/{model.name}",
                json={"input": predictive_info.model_dump(mode="json")},
                timeout=10,
            )

        return text_hash

    def list_transactions(self, user: User) -> list[Transaction]:
        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    SELECT * FROM transactions WHERE user_id = %s
                """,
                (user.id,),
            )
            try:
                return [Transaction(**dict(row)) for row in cur.fetchall()]
            except Exception as e:
                raise e
