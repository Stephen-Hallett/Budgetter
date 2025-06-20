from datetime import datetime

from pydantic import AliasPath, BaseModel, Field, field_validator


class Transaction(BaseModel):
    id: str
    account: str
    date: datetime
    type: str
    amount: float
    description: str
    category: str | None = None
    group: str | None = Field(
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
