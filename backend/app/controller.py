import logging
from datetime import datetime

import pytz
import requests

from .schemas import Account, Test, Transaction
from .util import log

logger = logging.getLogger(__name__)


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.tz = pytz.timezone("Pacific/Auckland")

    @log
    def test(self) -> Test:
        return {"test": "Dw it's working king"}

    @log
    def get_accounts(self, headers: dict[str, str]) -> list[Account]:
        akahu_accounts = requests.get(
            "https://api.akahu.io/v1/accounts", headers=headers
        ).json()
        return [
            {
                "_id": account["_id"],
                "name": account["name"],
                "company": account["connection"]["name"],
                "amount": account["balance"]["available"],
            }
            for account in akahu_accounts["items"]
        ]

    @log
    def get_transactions(self, headers: dict[str, str]) -> list[Transaction]:
        accounts = self.get_accounts(headers)
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
