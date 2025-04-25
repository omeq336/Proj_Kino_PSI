"""A module containing DTO models for output reservations."""

from pydantic import UUID4, BaseModel, ConfigDict
from asyncpg import Record

from cinemaapi.infrastructure.dto.showingdto import ShowingAltDTO


class ReservationDTO(BaseModel):
    """A model representing DTO for reservation data."""
    id: int
    seat_row: str
    seat_num: str
    showing: ShowingAltDTO
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "ReservationDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            ReservationDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            seat_row=record_dict.get("seat_row"),
            seat_num=record_dict.get("seat_num"),
            showing=ShowingAltDTO(
                id=record_dict.get("id_1"),  # type: ignore
                language_ver=record_dict.get("language_ver"),
                price=record_dict.get("price"),
                date=record_dict.get("date"),
                time=record_dict.get("time"),
                repertoire_id=record_dict.get("repertoire_id"),
                movie_id = record_dict.get("movie_id"),
                hall_id = record_dict.get("hall_id"),
        ),
            user_id=record_dict.get("user_id"),
        )
