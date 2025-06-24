from pydantic import BaseModel


class Account(BaseModel):
    id: str
    user_id: str
    name: str
    company: str
    amount: float
