from typing import Annotated

from fastapi import APIRouter, Header

from ..API.transactions import Controller
from ..schemas.transactions import Transaction
from ..schemas.users import Authorization
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()


@router.get("/list")
async def transactions(
    headers: Annotated[Authorization, Header()],
) -> list[Transaction]:
    return con.get_transactions(headers.model_dump())
