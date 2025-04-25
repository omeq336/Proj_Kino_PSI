"""Module containing hall-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional


class HallIn(BaseModel):
    """Model representing hall's DTO attributes."""
    alias: str
    seat_amount: int
    row_amount: int
    seats: Optional[dict]


class HallBroker(HallIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Hall(HallIn):
    """Model representing hall's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

