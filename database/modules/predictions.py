import numpy as np
from psycopg2.extras import RealDictCursor


class Predictions:
    def __init__(self, db) -> None:
        self.db = db

    def find_nearest_neibours(
        self, query_embedding: np.ndarray, neighbours: int = 1
    ) -> list[dict[str, str | float]]:
        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """SELECT
                    t.id,
                    t.segment_id,
                    1 - (e.embedding <=> '%s') AS cosine_similarity
                FROM transactions t
                LEFT JOIN embeddings e
                    ON t.hash = e.hash
                WHERE t.segment_id IS NOT NULL
                ORDER BY 3 DESC
                LIMIT %s""",
                (str(query_embedding), neighbours),
            )
        return [dict(row) for row in cur.fetchall()]
