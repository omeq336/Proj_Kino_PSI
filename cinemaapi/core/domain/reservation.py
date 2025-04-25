"""Module containing reservation-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4


class ReservationIn(BaseModel):
    """Model representing reservation's DTO attributes."""
    seat_row: str = "A"
    seat_num: str = "1"
    showing_id: int


class ReservationBroker(ReservationIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Reservation(ReservationIn):
    """Model representing reservation's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

