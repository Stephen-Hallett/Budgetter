from psycopg2.extras import RealDictCursor

from ..schemas.segments import CreateSegment, Segment
from ..schemas.users import User


class Segments:
    def __init__(self, db) -> None:
        self.db = db

    def create_segment(self, new_segment: CreateSegment, user: User) -> Segment:
        """Insert a segment."""
        text_hash = self.db.create_text_hash(new_segment.name)
        embedding = self.db.generate_embedding(new_segment.name)
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO segments (user_id, name, colour, hash)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (user_id, name) DO NOTHING
                    RETURNING id
                """,
                (user.id, new_segment.name, new_segment.colour, text_hash),
            )
            row = cur.fetchone()
            if row is not None:
                segment_id = row[0]
            else:
                # If conflict, fetch the existing segment's id
                cur.execute(
                    "SELECT id FROM segments WHERE user_id = %s AND name = %s",
                    (user.id, new_segment.name),
                )
                segment_id = cur.fetchone()[0]

            cur.execute(
                """
                    INSERT INTO embeddings (hash, embedding)
                    VALUES (%s, %s)
                    ON CONFLICT (hash) DO NOTHING
                """,
                (text_hash, embedding.tolist()),
            )
            conn.commit()
        return Segment(
            id=segment_id, user_id=user.id, hash=text_hash, **new_segment.model_dump()
        )

    def update_segment(self, segment: Segment) -> Segment:
        """Update a segment."""
        text_hash = self.db.create_text_hash(segment.name)
        segment.hash = text_hash
        embedding = self.db.generate_embedding(segment.name)
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    UPDATE segments
                    SET name = %s, colour = %s, hash = %s
                    WHERE id = %s
                """,
                (segment.name, segment.colour, text_hash, segment.id),
            )
            cur.execute(
                """
                    INSERT INTO embeddings (hash, embedding)
                    VALUES (%s, %s)
                    ON CONFLICT (hash) DO NOTHING
                """,
                (text_hash, embedding.tolist()),
            )
            conn.commit()
        return segment

    def list_segments(self, user: User) -> list[Segment]:
        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    SELECT * FROM segments WHERE user_id = %s
                """,
                (user.id,),
            )
            try:
                return [Segment(**dict(row)) for row in cur.fetchall()]
            except Exception as e:
                raise e
