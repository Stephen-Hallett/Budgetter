from psycopg2.extras import RealDictCursor

from ..schemas.accounts import Account
from ..schemas.users import User


class Accounts:
    def __init__(self, db) -> None:
        self.db = db

    def upsert_account(self, account: Account, user: User) -> None:
        """Insert or update an account (upsert)."""
        with self.db.get_connection() as conn, conn.cursor() as cur:
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
            self.db.get_connection() as conn,
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
