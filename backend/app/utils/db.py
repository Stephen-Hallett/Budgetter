import os

import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer

from ..schemas.accoutns import Account
from ..schemas.users import User


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

    def create_user(self, user: User) -> None:
        with self.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO users (id, name, email, akahu_id, auth_token)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO NOTHING
                """,
                (user.id, user.name, user.email, user.akahu_id, user.auth_token),
            )
            conn.commit()

    def create_account(self, account: Account, user: User) -> None:
        """Create a new account."""
        with self.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO accounts (id, user_id, name, company, amount)
                    VALUES (%s, %s, %s, %s, %d)
                    ON CONFLICT (id) DO NOTHING
                """,
                (account.id, user.id, account.name, account.company, account.amount),
            )
            conn.commit()


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
