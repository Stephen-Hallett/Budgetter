from pydantic import BaseModel


class Segment(BaseModel):
    id: str
    user_id: str
    name: str
    colour: str
