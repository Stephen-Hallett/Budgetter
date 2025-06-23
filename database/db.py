import hashlib
import os
from typing import Any

import numpy as np
import psycopg2
from psycopg2.extras import RealDictCursor
from sentence_transformers import SentenceTransformer

from backend.app.schemas.accounts import Account
from backend.app.schemas.segments import Segment
from backend.app.schemas.transactions import Transaction
from backend.app.schemas.users import User


class BudgetterDB:
    def __init__(
        self,
        host: str = os.environ["POSTGRES_HOST"],
        port: int = os.environ["POSTGRES_PORT"],
        database: str = os.environ["POSTGRES_DB"],
        user: str = os.environ["POSTGRES_USER"],
        password: str = os.environ["POSTGRES_PW"],
    ) -> None:
        self.connection_params: dict[str, str] = {
            "host": host,
            "port": port,
            "database": database,
            "user": user,
            "password": password,
        }

        # Initialize sentence transformer model
        self.embedding_model: SentenceTransformer = SentenceTransformer(
            "all-mpnet-base-v2"
        )

    def get_connection(self) -> Any:  # NOQA
        """Get database connection."""
        return psycopg2.connect(**self.connection_params)  # pyright: ignore

    def get_info_string(self, transaction: Transaction) -> str:
        return " ".join(
            [
                str(transaction.type),
                str(transaction.description),
                str(transaction.category),
                str(transaction.group_name),
                str(transaction.merchant),
            ]
        )

    def create_text_hash(self, text: str) -> str:
        return hashlib.sha256(text.encode()).hexdigest()

    def generate_embedding(self, text: str) -> np.ndarray:
        """Generate embedding for text using sentence transformers."""
        return self.embedding_model.encode(text)

    def create_user(self, user: User) -> None:
        with self.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO users (id, name, email, akahu_id, auth_token)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                """,
                (user.id, user.name, user.email, user.akahu_id, user.auth_token),
            )
            conn.commit()

    def get_user(self, name: str) -> User:
        with (
            self.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    SELECT * FROM users WHERE name = %s
                """,
                (name,),
            )
            try:
                return User.model_validate(next(dict(row) for row in cur.fetchall()))
            except Exception as e:
                raise ValueError("A user with that name doesnt exist") from e

    def upsert_account(self, account: Account, user: User) -> None:
        """Insert or update an account (upsert)."""
        with self.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO accounts (id, user_id, name, company, amount)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        name = EXCLUDED.name,
                        company = EXCLUDED.company,
                        amount = EXCLUDED.amount
                """,
                (account.id, user.id, account.name, account.company, account.amount),
            )
            conn.commit()

    def list_accounts(self, user: User) -> list[Account]:
        with (
            self.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    SELECT * FROM accounts WHERE user_id = %s
                """,
                (user.id,),
            )
            try:
                return [Account.model_validate(dict(row)) for row in cur.fetchall()]
            except Exception as e:
                raise e

    def create_transaction(self, transaction: Transaction) -> str:
        """Insert transaction and generate embedding for description."""

        # Generate hash and embedding for description
        info_string = self.get_info_string(transaction)
        text_hash = self.create_text_hash(info_string)
        embedding = self.generate_embedding(info_string)

        with self.get_connection() as conn, conn.cursor() as cur:
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

        return text_hash

    def list_transactions(self, user: User) -> list[Transaction]:
        with (
            self.get_connection() as conn,
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

    def list_segments(self) -> list[Segment]:
        with (
            self.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    SELECT * FROM segments
                """
            )
            try:
                return [Segment(**dict(row)) for row in cur.fetchall()]
            except Exception as e:
                raise e

    def find_nearest_neibours(
        self, query_embedding: np.ndarray, neighbours: int = 1
    ) -> list[dict[str, str | float]]:
        with (
            self.get_connection() as conn,
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
