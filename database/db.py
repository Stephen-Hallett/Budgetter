from psycopg2.extras import RealDictCursor

from .modules.accounts import Accounts
from .modules.base import BaseDB
from .modules.models import Models
from .modules.predictions import Predictions
from .modules.segments import Segments
from .modules.transactions import Transactions
from .modules.users import Users


class BudgetterDB(BaseDB):
    def __init__(self) -> None:
        super().__init__()
        self.users = Users(self)
        self.accounts = Accounts(self)
        self.models = Models(self)
        self.predictions = Predictions(self)
        self.segments = Segments(self)
        self.transactions = Transactions(self)


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
