import logging

import pytz
import requests

from ..schemas.accounts import Account
from ..schemas.users import User
from ..utils.db import BudgetterDB
from ..utils.logger import MyLogger, log

logger = MyLogger().get_logger()


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.tz = pytz.timezone("Pacific/Auckland")
        self.db = BudgetterDB()

    @log
    def load_accounts(self, user: User) -> list[Account]:
        headers = {
            "X-Akahu-ID": user.akahu_id,
            "Authorization": f"Bearer {user.auth_token}",
        }
        akahu_accounts = requests.get(
            "https://api.akahu.io/v1/accounts", headers=headers, timeout=5
        ).json()
        for account in akahu_accounts["items"]:
            self.db.upsert_account(
                Account.model_validate(
                    {
                        "id": account["_id"],
                        "user_id": user.id,
                        "name": account["name"],
                        "company": account["connection"]["name"],
                        "amount": account["balance"]["current"],
                    }
                ),
                user,
            )

    @log
    def list_accounts(self, user: User) -> list[Account]:
        return self.db.list_accounts(user)
