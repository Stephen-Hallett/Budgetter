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
