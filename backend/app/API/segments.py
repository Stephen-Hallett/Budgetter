import pytz

from database.db import BudgetterDB
from database.schemas.segments import CreateSegment, Segment
from database.schemas.users import User

from ..utils.logger import MyLogger, log

logger = MyLogger().get_logger()


class Controller:
    def __init__(self) -> None:
        self.logger = MyLogger().get_logger()
        self.tz = pytz.timezone("Pacific/Auckland")
        self.db = BudgetterDB()

    @log
    def create_segment(self, new_segment: CreateSegment) -> None:
        self.db.segments.create_segment(new_segment)

    @log
    def update_segment(self, segment: Segment) -> Segment:
        return self.db.segments.update_segment(segment)

    @log
    def list_segments(self, user: User) -> list[Segment]:
        return self.db.segments.list_segments(user)
