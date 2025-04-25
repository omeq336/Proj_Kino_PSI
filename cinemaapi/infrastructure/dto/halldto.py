"""A module containing DTO models for output halls."""


from pydantic import UUID4, BaseModel, ConfigDict


class HallDTO(BaseModel):
    """A model representing DTO for hall data."""
    id: int
    alias: str
    seat_amount: int
    row_amount: int
    seats: dict
    user_id: UUID4

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )
