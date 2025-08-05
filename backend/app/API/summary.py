from datetime import datetime

import pytz

from database.db import BudgetterDB
from database.schemas.summary import Transaction
from database.schemas.users import User

from ..utils.logger import MyLogger, log

logger = MyLogger().get_logger()


class Controller:
    def __init__(self) -> None:
        self.logger = MyLogger().get_logger()
        self.tz = pytz.timezone("Pacific/Auckland")
        self.db = BudgetterDB()

    @log
    def list_transactions(
        self,
        user: User,
        start_date: datetime | None = None,
        end_date: datetime | None = None,
        limit: int | None = None,
        offset: int = 0,
    ) -> list[Transaction]:
        return self.db.summary.list_transactions(
            user=user,
            start_date=start_date,
            end_date=end_date,
            limit=limit,
            offset=offset,
        )
