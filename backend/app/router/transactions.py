from typing import Annotated

from fastapi import APIRouter, Header

from ..API.transactions import Controller
from ..API.users import Controller as UserController
from ..schemas.transactions import Transaction
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()
user_con = UserController()


@router.get("/list")
async def transactions(username: Annotated[str, Header()]) -> list[Transaction]:
    user = user_con.get_user(username)
    return con.list_transactions(user)
