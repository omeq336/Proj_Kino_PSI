"""A module containing DTO models for output repertoire."""

from pydantic import BaseModel, ConfigDict
from asyncpg import Record


class RepertoireDTO(BaseModel):
    """A model representing DTO for repertoire data."""
    id: int
    name: str


    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_record(cls, record: Record) -> "RepertoireDTO":
        """A method for preparing DTO instance based on DB record.

        Args:
            record (Record): The DB record.

        Returns:
            RepertoireDTO: The final DTO instance.
        """
        record_dict = dict(record)

        return cls(
            id=record_dict.get("id"),
            name=record_dict.get("name"),
        )