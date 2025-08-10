from datetime import datetime

from pydantic import BaseModel


class Transaction(BaseModel):
    id: str
    account: str
    user_id: str
    segment_id: int
    segment: str
    hash: str
    date: datetime
    type: str
    amount: float
    description: str
    category: str | None
    group_name: str | None
    merchant: str | None
    colour: str
    confirmed: bool


class Metrics(BaseModel):
    spent: float
    income: float
    percentage: float
