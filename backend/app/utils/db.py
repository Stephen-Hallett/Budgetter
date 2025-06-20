import os

import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer


class BudgetterDB:
    def __init__(
        self,
        host: str = os.environ["POSTGRES_HOST"],
        port: int = int(os.environ["POSTGRES_PORT"]),
        database: str = os.environ["POSTGRES_DB"],
        user: str = os.environ["POSTGRES_USER"],
        password: str = os.environ["POSTGRES_PW"],
    ) -> None:
        self.connection_params = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }

        # Initialize sentence transformer model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def get_connection(self):
        """Get database connection."""
        return psycopg2.connect(**self.connection_params)

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text using sentence transformers."""
        return self.model.encode(text)


if __name__ == "__main__":
    # Testing that the db connection works
    db = BudgetterDB()
    with db.get_connection() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """
                SELECT tablename FROM pg_tables WHERE schemaname = 'public';
            """
        )
        print([dict(row) for row in cur.fetchall()])
