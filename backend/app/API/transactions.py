import logging
from datetime import datetime

import pytz
import requests

from ..schemas.transactions import Transaction
from ..utils.logger import MyLogger, log
from .accounts import Controller as AccountsController

logger = MyLogger().get_logger()
acc_con = AccountsController()


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.tz = pytz.timezone("Pacific/Auckland")

    @log
    def get_transactions(self, headers: dict[str, str]) -> list[Transaction]:
        accounts = acc_con.get_accounts(headers)
        all_transactions = []
        for account in accounts:
            account_transactions = requests.get(
                f"https://api.akahu.io/v1/accounts/{account['_id']}/transactions",
                headers=headers,
            ).json()["items"]
            for transaction in account_transactions:
                transaction["date"] = datetime.strptime(
                    transaction["date"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=self.tz)
                all_transactions.append(Transaction.model_validate(transaction))
        return all_transactions
