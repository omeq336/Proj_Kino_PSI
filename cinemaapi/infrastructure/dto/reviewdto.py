"""A module containing DTO models for output reviews."""

from pydantic import UUID4, BaseModel, ConfigDict
from asyncpg import Record

from cinemaapi.infrastructure.dto.moviedto import MovieAltDTO


class ReviewDTO(BaseModel):
    """A model representing DTO for review data."""
    id: int
    rating: int
    comment: str
    date: str
    movie: MovieAltDTO
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReviewDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReviewDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            rating=record_dict.get("rating"),
            comment=record_dict.get("comment"),
            date=record_dict.get("date"),
            movie=MovieAltDTO(
                id=record_dict.get("id_1"),
                title=record_dict.get("title"),
                genre=record_dict.get("genre"),
                age_restriction=record_dict.get("age_restriction"),
                duration=record_dict.get("duration"),
                rating=record_dict.get("rating_1")
            ),
            user_id=record_dict.get("user_id"),
        )
