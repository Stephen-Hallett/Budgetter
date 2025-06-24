from datetime import datetime

from pydantic import AliasChoices, AliasPath, BaseModel, Field, field_validator


class Transaction(BaseModel):
    id: str = Field(validation_alias=AliasChoices("id", "_id"))
    account: str = Field(validation_alias=AliasChoices("account", "_account"))
    user_id: str = Field(validation_alias=AliasChoices("user_id", "_user"))
    hash: str
    date: datetime
    type: str
    amount: float
    description: str
    category: str | None = None
    group_name: str | None = Field(
        validation_alias=AliasPath("category", "groups", "personal_finance", "name"),
        default=None,
    )
    merchant: str | None = None

    @field_validator("category", mode="plain")
    @classmethod
    def val_category(cls, value: dict | str | None = None) -> str | None:
        if isinstance(value, dict):
            return value["name"]
        return value

    @field_validator("merchant", mode="plain")
    @classmethod
    def val_merchant(cls, value: dict | str | None = None) -> str | None:
        if isinstance(value, dict):
            return value["name"]
        return value

    def model_dump(self, **kwargs: object) -> dict[str, str]:
        return super().model_dump(by_alias=True, **kwargs)
