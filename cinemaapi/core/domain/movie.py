"""Module containing movie-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4
from typing import Optional


class MovieIn(BaseModel):
    """Model representing movie's DTO attributes."""
    title: str
    genre: str
    age_restriction: int
    duration: Optional[str] = "1.30"
    rating: Optional[float] = None


class MovieBroker(MovieIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Movie(MovieIn):
    """Model representing movie's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

