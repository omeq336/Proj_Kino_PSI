"""A module containing DTO models for output showings."""

from asyncpg import Record
from pydantic import BaseModel, ConfigDict, UUID4  # type: ignore

from cinemaapi.core.domain.repertoire import Repertoire
from cinemaapi.infrastructure.dto.moviedto import MovieAltDTO


class ShowingDTO(BaseModel):
    """A model representing DTO for showing data."""
    id: int
    language_ver: str
    price: float
    date: str
    time: str
    repertoire: Repertoire
    movie: MovieAltDTO
    hall_id: int
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ShowingDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ShowingDTO: The final DTO instance.
        """

        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            language_ver=record_dict.get("language_ver"),
            price=record_dict.get("price"),
            date=record_dict.get("date"),
            time=record_dict.get("time"),
            repertoire=Repertoire(
                id=record_dict.get("id_1"),
                name=record_dict.get("name")
            ),
            movie=MovieAltDTO(
                id=record_dict.get("id_2"),
                title=record_dict.get("title"),
                genre=record_dict.get("genre"),
                age_restriction=record_dict.get("age_restriction"),
                duration=record_dict.get("duration"),
                rating=record_dict.get("rating")
            ),
            hall_id = record_dict.get("hall_id"),
            user_id = record_dict.get("user_id"),
        )

class ShowingAltDTO(BaseModel):
    """A model representing alternative DTO for showing data."""
    id: int
    language_ver: str
    price: float
    date: str
    time: str
    repertoire_id: int
    movie_id: int
    hall_id: int

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

