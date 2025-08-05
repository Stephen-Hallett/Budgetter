from datetime import date
from typing import Annotated

from fastapi import APIRouter, Header

from database.schemas.summary import Transaction

from ..API.summary import Controller
from ..API.users import Controller as UserController
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()
user_con = UserController()


@router.get("/transactions")
async def transactions(
    username: Annotated[str, Header()],
    start_date: date | None = None,
    end_date: date | None = None,
) -> list[Transaction]:
    user = user_con.get_user(username)
    return con.list_transactions(user=user, start_date=start_date, end_date=end_date)
