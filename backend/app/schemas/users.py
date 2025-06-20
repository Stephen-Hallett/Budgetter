from pydantic import BaseModel, Field


class Authorization(BaseModel):
    X_Akahu_ID: str = Field(alias="X-Akahu-ID")
    Authorization: str

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True

    def model_dump(self, **kwargs: object) -> dict[str, str]:
        return super().model_dump(by_alias=True, **kwargs)
