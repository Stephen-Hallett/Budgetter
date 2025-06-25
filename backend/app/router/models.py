from fastapi import APIRouter

from database.schemas.models import Model

from ..API.models import Controller
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()


@router.get("/list")
async def models() -> list[Model]:
    return con.list_models()
