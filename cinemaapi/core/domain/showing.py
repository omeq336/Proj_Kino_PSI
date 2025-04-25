"""Module containing showing-related domain models"""

from datetime import date
from pydantic import BaseModel, ConfigDict, UUID4


class ShowingIn(BaseModel):
    """Model representing showing's DTO attributes."""
    language_ver: str = "Dubbing, Subtitles, Lector"
    price: float
    date: str = str(date.today())
    time: str = "10:00"
    repertoire_id: int
    movie_id: int
    hall_id: int


class ShowingBroker(ShowingIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Showing(ShowingIn):
    """Model representing showing's attributes in the database."""
    id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
