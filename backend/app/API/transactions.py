import logging
from datetime import datetime

import pytz
import requests

from database.db import BudgetterDB
from database.schemas.transactions import Transaction
from database.schemas.users import User

from ..utils.logger import MyLogger, log
from .accounts import Controller as AccountsController

logger: logging.Logger = MyLogger().get_logger()
acc_con: AccountsController = AccountsController()


class Controller:
    def __init__(self) -> None:
        self.logger: logging.Logger = MyLogger().get_logger()
        self.tz: pytz.BaseTzInfo = pytz.timezone("Pacific/Auckland")
        self.db: BudgetterDB = BudgetterDB()

    @log
    def load_transactions(self, user: User) -> None:
        headers = {
            "X-Akahu-ID": user.akahu_id,
            "Authorization": f"Bearer {user.auth_token}",
        }
        accounts = acc_con.list_accounts(user)
        for account in accounts:
            account_transactions = requests.get(
                f"https://api.akahu.io/v1/accounts/{account.id}/transactions",
                headers=headers,
                timeout=5,
            ).json()["items"]
            for transaction in account_transactions:
                transaction["date"] = datetime.strptime(
                    transaction["date"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=self.tz)
                self.db.create_transaction(Transaction.model_validate(transaction))

    def list_transactions(
        self, user: User
    ) -> list[Transaction]:  # TODO: Add time limit
        return self.db.list_transactions(user)
