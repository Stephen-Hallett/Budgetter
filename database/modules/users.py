from psycopg2.extras import RealDictCursor

from ..schemas.users import User


class Users:
    def __init__(self, db) -> None:
        self.db = db

    def get_user(self, name: str) -> User:
        with (
            self.db.et_connection() as conn,
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

    def create_user(self, user: User) -> None:
        with self.db.get_connection() as conn, conn.cursor() as cur:
            cur.execute(
                """
                    INSERT INTO users (id, name, email, akahu_id, auth_token)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (name) DO NOTHING
                """,
                (user.id, user.name, user.email, user.akahu_id, user.auth_token),
            )
            conn.commit()
