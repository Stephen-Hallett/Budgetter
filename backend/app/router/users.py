from fastapi import APIRouter

from ..API.users import Controller
from ..schemas.users import CreateUser, User
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()


@router.post("/create")
async def users(user: CreateUser) -> User:
    return con.create_user(user)
