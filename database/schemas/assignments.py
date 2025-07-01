from pydantic import BaseModel


class Assignment(BaseModel):
    user_id: str
    hash: str
    segment_id: str
