from typing import Annotated

from fastapi import APIRouter, Header

from ..API.accounts import Controller
from ..API.users import Controller as UserController
from ..schemas.accounts import Account
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()
user_con = UserController()


@router.get("/list")
async def accounts(username: Annotated[str, Header()]) -> list[Account]:
    user = user_con.get_user(username)
    return con.list_accounts(user)
