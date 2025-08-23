from typing import Annotated

from fastapi import APIRouter, Header

from database.schemas.segments import CreateSegment, Segment

from ..API.segments import Controller
from ..API.users import Controller as UserController
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()
user_con = UserController()


@router.get("/list")
async def segments(username: Annotated[str, Header()]) -> list[Segment]:
    user = user_con.get_user(username)
    return con.list_segments(user)


@router.post("/create")
async def create_segment(
    segment: CreateSegment, username: Annotated[str, Header()]
) -> Segment:
    user = user_con.get_user(username)
    return con.create_segment(segment, user)


@router.put("/update")
async def update_segment(segment: Segment) -> Segment:
    return con.update_segment(segment)
