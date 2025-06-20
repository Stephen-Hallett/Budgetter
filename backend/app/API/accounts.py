import logging

import pytz
import requests

from ..schemas.accounts import Account
from ..utils.logger import MyLogger, log

logger = MyLogger().get_logger()


class Controller:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.tz = pytz.timezone("Pacific/Auckland")

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
