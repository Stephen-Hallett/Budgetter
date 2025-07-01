from psycopg2.extras import RealDictCursor

from ..schemas.assignments import Assignment


class Assignments:
    def __init__(self, db) -> None:
        self.db = db

    def get_assignment(self, user_id: str, hash: str) -> Assignment:  # NOQA: A002
        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    SELECT * FROM assignments WHERE user_id = %s AND hash = %s
                """,
                (user_id, hash),
            )
            try:
                return Assignment.model_validate(
                    next(dict(row) for row in cur.fetchall())
                )
            except Exception as e:
                raise ValueError("An assignment for that hash doesnt exist") from e

    def upsert_assignment(self, assignment: Assignment) -> None:
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO assignments (user_id, hash, segment_id)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, hash) DO UPDATE SET
                        segment_id = EXCLUDED.segment_id
                """,
                (assignment.user_id, assignment.hash, assignment.segment_id),
            )
            conn.commit()
