import hashlib
import os
from typing import Any

import numpy as np
import psycopg2
from sentence_transformers import SentenceTransformer

from ..schemas.transactions import Transaction


class BaseDB:
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
