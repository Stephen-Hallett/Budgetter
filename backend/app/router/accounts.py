from typing import Annotated

from fastapi import APIRouter, Header

from ..API.accounts import Controller
from ..schemas.accounts import Account
from ..schemas.users import Authorization
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()


@router.get("/list")
async def accounts(headers: Annotated[Authorization, Header()]) -> list[Account]:
    logger.info(headers.model_dump())
    return con.get_accounts(headers.model_dump())
