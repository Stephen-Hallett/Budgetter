import requests

from ..schemas.users import CreateUser, User
from ..utils.db import BudgetterDB
from ..utils.logger import MyLogger, log


class Controller:
    def __init__(self) -> None:
        self.logger = MyLogger().get_logger()
        self.db = BudgetterDB()

    @log
    def create_user(self, new_user: CreateUser) -> User:
        headers = {
            "X-Akahu-ID": new_user.akahu_id,
            "Authorization": f"Bearer {new_user.auth_token}",
        }
        user_info = requests.get(
            "https://api.akahu.io/v1/me", headers=headers, timeout=5
        ).json()
        if "success" in user_info:
            user = User(
                id=user_info["item"]["_id"],
                name=new_user.name,
                email=user_info["item"]["email"],
                akahu_id=new_user.akahu_id,
                auth_token=new_user.auth_token,
            )
            _ = self.db.create_user(user)  # TODO Add check if user already exists
            return user
        raise ValueError("Those access tokens dont belong to a valid user!")
