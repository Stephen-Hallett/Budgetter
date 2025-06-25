import pytz

from database.db import BudgetterDB
from database.schemas.models import Model

from ..utils.logger import MyLogger, log

logger = MyLogger().get_logger()


class Controller:
    def __init__(self) -> None:
        self.logger = MyLogger().get_logger()
        self.tz = pytz.timezone("Pacific/Auckland")
        self.db = BudgetterDB()

    @log
    def list_models(self) -> list[Model]:
        return self.db.models.list_models()
