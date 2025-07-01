from psycopg2.extras import RealDictCursor

from ..schemas.predictions import Prediction, PredictionInput


class Predictions:
    def __init__(self, db) -> None:
        self.db = db

    def get_prediction_input(self, trans_id: str) -> PredictionInput:
        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """SELECT
                    *
                FROM transactions t
                LEFT JOIN embeddings e
                    ON t.hash = e.hash
                WHERE t.id = %s""",
                (trans_id,),
            )
            return next(PredictionInput(**dict(row)) for row in cur.fetchall())

    def find_nearest_neibours(
        self, query_embedding: list[float], neighbours: int = 1
    ) -> list[dict[str, str | float]]:
        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """SELECT
                    a.segment_id,
                    1 - (e.embedding <=> %s::vector) AS cosine_similarity
                FROM assignments a
                LEFT JOIN embeddings e
                    ON a.hash = e.hash
                WHERE a.segment_id IS NOT NULL
                ORDER BY (1 - (e.embedding <=> %s::vector)) DESC
                LIMIT %s""",
                (query_embedding, query_embedding, neighbours),
            )
            return [dict(row) for row in cur.fetchall()]

    def upsert_prediction(self, prediction: Prediction) -> None:
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO predictions (user_id, model, hash, prediction, confidence)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (user_id, model, hash) DO UPDATE SET
                        prediction = EXCLUDED.prediction,
                        confidence = EXCLUDED.confidence
                """,
                (
                    prediction.user_id,
                    prediction.model,
                    prediction.hash,
                    prediction.prediction,
                    prediction.confidence,
                ),
            )
            conn.commit()
