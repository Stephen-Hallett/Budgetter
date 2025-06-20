from pydantic import BaseModel


class Account(BaseModel):
    _id: str
    name: str
    company: str
    amount: float
