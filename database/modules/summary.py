from datetime import datetime

import pytz
from psycopg2.extras import RealDictCursor

from ..schemas.summary import Transaction
from ..schemas.users import User

tz = pytz.timezone("Pacific/Auckland")


class Summary:
    def __init__(self, db) -> None:
        self.db = db
        self.tz = tz

    def list_transactions(
        self,
        user: User,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Transaction]:
        if start_date is None:
            start_date = datetime.now(self.tz).replace(year=1).date()
        if end_date is None:
            end_date = datetime.now(self.tz).date()
        if limit is None:
            limit = 1e7  # This is just a small scale app so this hacky fix will do

        with (
            self.db.get_connection() as conn,
            conn.cursor(cursor_factory=RealDictCursor) as cur,
        ):
            cur.execute(
                """
                    WITH big_table AS (
                        SELECT
                            t.id,
                            t.account,
                            t.user_id,
                            COALESCE(a.segment_id, p.prediction) AS segment_id,
                            t.hash,
                            t.date,
                            t.type,
                            t.amount,
                            t.description,
                            t.category,
                            t.group_name,
                            t.merchant,
                            s.colour,
                            CASE WHEN a.segment_id IS NULL
                                THEN false
                                ELSE true
                            END AS confirmed
                        FROM transactions t
                        LEFT JOIN assignments a
                            ON t.user_id = a.user_id AND t.hash = a.hash
                        LEFT JOIN predictions p
                            ON t.user_id = p.user_id AND t.hash = p.hash
                        LEFT JOIN segments s
                            ON t.user_id = s.user_id
                            AND COALESCE(a.segment_id, p.prediction) = s.id
                        WHERE t.user_id = %s AND t.date >= %s AND t.date <= %s
                        ORDER BY t.date DESC
                        LIMIT %s
                        OFFSET %s
                    )

                    SELECT
                        b.*,
                        s.name AS segment
                    FROM big_table b
                    LEFT JOIN segments s
                        ON b.user_id = s.user_id AND b.segment_id = s.id
                """,  # TODO: This will make duplicates when there is > 1 model
                (user.id, start_date, end_date, limit, offset),
            )
            try:
                return [Transaction(**dict(row)) for row in cur.fetchall()]
            except Exception as e:
                raise e
