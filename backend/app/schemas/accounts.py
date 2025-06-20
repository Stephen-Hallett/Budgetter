from pydantic import BaseModel


class Account(BaseModel):
    id: str
    name: str
    company: str
    amount: float
