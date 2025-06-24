import pytz

from ..schemas.segments import CreateSegment, Segment
from ..schemas.users import User
from ..utils.db import BudgetterDB
from ..utils.logger import MyLogger, log

logger = MyLogger().get_logger()


class Controller:
    def __init__(self) -> None:
        self.logger = MyLogger().get_logger()
        self.tz = pytz.timezone("Pacific/Auckland")
        self.db = BudgetterDB()

    @log
    def create_segment(self, new_segment: CreateSegment) -> None:
        self.db.create_segment(new_segment)

    @log
    def update_segment(self, segment: Segment) -> Segment:
        return self.db.update_segment(segment)

    @log
    def list_segments(self, user: User) -> list[Segment]:
        return self.db.list_segments(user)
