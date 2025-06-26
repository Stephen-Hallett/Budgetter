from fastapi import APIRouter, BackgroundTasks

from database.schemas.users import CreateUser, User

from ..API.accounts import Controller as AccountsController
from ..API.transactions import Controller as TransactionsController
from ..API.segments import Controller as SegmentsController
from ..API.users import Controller
from ..utils.logger import MyLogger

router = APIRouter()
logger = MyLogger().get_logger()

con = Controller()
acc_con = AccountsController()
trans_con = TransactionsController()
segment_con = SegmentsController()


@router.post("/create")
async def users(user: CreateUser, background_tasks: BackgroundTasks) -> User:
    new_user = con.create_user(user)

    def load_accounts_and_transactions(user: User) -> None:
        segment_con.create_default_segments(user)
        acc_con.load_accounts(user)
        trans_con.load_transactions(user)

    background_tasks.add_task(load_accounts_and_transactions, new_user)
    return new_user
