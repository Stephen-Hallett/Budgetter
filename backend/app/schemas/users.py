from pydantic import BaseModel, Field


class User(BaseModel):
    id: str
    name: str
    email: str
    akahu_id: str
    auth_token: str


class CreateUser(BaseModel):
    name: str
    akahu_id: str
    auth_token: str


class Authorization(BaseModel):
    X_Akahu_ID: str = Field(alias="X-Akahu-ID")
    Authorization: str

    class Config:
        populate_by_name = True

    def model_dump(self, **kwargs: object) -> dict[str, str]:
        return super().model_dump(by_alias=True, **kwargs)
