from psycopg2.extras import RealDictCursor

from ..schemas.predictions import PredictionInput


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
            cur.execute(  # TODO Should be on assignments not on transactions
                """SELECT
                    t.id,
                    t.segment_id,
                    1 - (e.embedding <=> %s::vector) AS cosine_similarity
                FROM transactions t
                LEFT JOIN embeddings e
                    ON t.hash = e.hash
                WHERE t.segment_id IS NOT NULL
                ORDER BY 3 DESC
                LIMIT %s""",
                (query_embedding, neighbours),
            )
            return [dict(row) for row in cur.fetchall()]
