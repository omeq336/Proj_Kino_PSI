"""A module containing DTO models for output movies."""

from typing import Optional
from asyncpg import Record
from pydantic import BaseModel, ConfigDict, UUID4


class MovieDTO(BaseModel):
    """A model representing DTO for movie data."""
    id: int
    title: str
    genre: str
    age_restriction: int
    duration: Optional[float]
    rating: Optional[float]
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "MovieDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            MovieDTO: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            title=record_dict.get("title"),
            genre=record_dict.get("genre"),
            age_restriction=record_dict.get("age_restriction"),
            duration=record_dict.get("duration"),
            rating=record_dict.get("rating"),
            user_id = record_dict.get("user_id")
        )

class MovieAltDTO(BaseModel):
    id: int
    title: str
    genre: str
    age_restriction: int
    duration: Optional[float]
    rating: Optional[float]

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )