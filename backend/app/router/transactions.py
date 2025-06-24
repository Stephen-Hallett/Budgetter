from typing import Annotated

from fastapi import APIRouter, Header

from database.schemas.transactions import Transaction

from ..API.transactions import Controller
from ..API.users import Controller as UserController
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()
user_con = UserController()


@router.get("/list")
async def transactions(username: Annotated[str, Header()]) -> list[Transaction]:
    user = user_con.get_user(username)
    return con.list_transactions(user)
