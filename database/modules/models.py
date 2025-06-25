from psycopg2.extras import RealDictCursor

from ..schemas.models import Model


class Models:
    def __init__(self, db) -> None:
        self.db = db

    def list_models(self) -> list[Model]:
        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    SELECT * FROM models
                """
            )
            try:
                return [Model(**dict(row)) for row in cur.fetchall()]
            except Exception as e:
                raise e

    def register_model(self, model: Model) -> str:
        """Insert or update a model (upsert)."""
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO models (name, active)
                    VALUES (%s, %s)
                    ON CONFLICT (name) DO UPDATE SET
                        active = EXCLUDED.active
                """,
                (model.name, model.active),
            )
            conn.commit()
        return f"Registered {model.name} model."
