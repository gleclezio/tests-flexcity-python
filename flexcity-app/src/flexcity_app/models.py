import datetime
from typing import Self

from pydantic import BaseModel, Field, model_validator


class ActivationBody(BaseModel):
    date: datetime.date = Field(
        description="Activation date. format like 'YYYY-MM-DD'",
        example="2026-02-01",
        default=datetime.date.today(),
    )
    volume: int = Field(
        description="Number of kW needed. format like '10'", example=10, gt=0
    )


class Asset(BaseModel):
    code: str = Field(description="Asset code")
    name: str = Field(description="Asset name", example="Asset A")
    activation_cost: float = Field(description="Activation cost in €", example=1.2)
    availability: list[datetime.date] = Field(
        description="List of dates when the asset is available",
        example=["2026-02-01", "2026-02-02"],
    )
    volume: int = Field(
        description="Number of kW that can be activated for this asset", example=2
    )


class AssetToActivate(BaseModel):
    code: str = Field(description="Asset code")
    name: str = Field(description="Asset name", example="Asset A")
    activation_cost: float = Field(description="Activation cost in €", example=1.2)
    power_requested: int = Field(
        description="Power requested for the activation", example=1, default=None
    )
    # TODO make it invisible in the response (kept for debugging purposes)
    volume: int = Field(
        description="Number of kW that can be activated for this asset", example=2
    )

    @model_validator(mode="after")
    def update_power(self) -> Self:
        if self.power_requested is None:
            self.power_requested = self.volume
        return self
