import logging
from typing import Annotated

from fastapi import FastAPI, Header
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .controller import Controller
from .schemas import Account, Authorization, SpendingSummary, Test, Transaction

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger("app")
con = Controller()


@app.get("/test")
async def test(
    headers: Annotated[Authorization, Header(convert_underscores=True)],
) -> Test:
    logger.error(headers.model_dump())
    return con.test()


@app.get("/accounts")
async def accounts(headers: Annotated[Authorization, Header()]) -> list[Account]:
    logger.info(headers.model_dump())
    return con.get_accounts(headers.model_dump())


@app.get("/transactions")
async def transactions(
    headers: Annotated[Authorization, Header()],
) -> list[Transaction]:
    return con.get_transactions(headers.model_dump())


@app.get("/spending_summary")
async def spending_summary(
    headers: Annotated[Authorization, Header()],
) -> SpendingSummary:
    return con.spending_summary(headers.model_dump())
