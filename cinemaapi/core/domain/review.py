"""Module containing review-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4
from datetime import date


class ReviewIn(BaseModel):
    """Model representing review's DTO attributes."""
    rating: int = 1
    comment: str
    date: str = str(date.today())
    movie_id: int


class ReviewBroker(ReviewIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Review(ReviewIn):
    """Model representing review's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

