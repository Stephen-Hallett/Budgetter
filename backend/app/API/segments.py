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
    def create_segment(self, new_segment: CreateSegment, user: User) -> Segment:
        self.db.segments.create_segment(new_segment, user)

    @log
    def create_default_segments(self, user: User) -> None:
        names = ("Income", "Food & Drink", "Lifestyle", "Household", "Subscriptions")
        colours = ("#40a02b", "#d20f39", "#04a5e5", "#ea76cb", "#fe640b")
        for name, colour in zip(names, colours, strict=False):
            self.create_segment(CreateSegment(name=name, colour=colour), user)

    @log
    def update_segment(self, segment: Segment) -> Segment:
        return self.db.segments.update_segment(segment)

    @log
    def list_segments(self, user: User) -> list[Segment]:
        return self.db.segments.list_segments(user)

    @log
    def get_segment(self, segment_id: int, user: User) -> Segment:
        self.db.segments.get_segment(segment_id, user)
