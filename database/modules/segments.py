from psycopg2.extras import RealDictCursor

from ..schemas.segments import CreateSegment, Segment


class Segments:
    def __init__(self, db) -> None:
        self.db = db

    def create_segment(self, new_segment: CreateSegment) -> None:
        """Insert a segment."""
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO segments (user_id, name, colour)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (user_id, name) DO NOTHING,
                """,
                (new_segment.user_id, new_segment.name, new_segment.colour),
            )
            conn.commit()

    def update_segment(self, segment: Segment) -> None:
        """Update a segment."""
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE segments
                    SET user_id = %s, name = %s, colour = %s
                    WHERE id = %s
                """,
                (segment.user_id, segment.name, segment.colour, segment.id),
            )
            conn.commit()

    def list_segments(self) -> list[Segment]:
        with (
            self.db.get_connection() as conn,
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
