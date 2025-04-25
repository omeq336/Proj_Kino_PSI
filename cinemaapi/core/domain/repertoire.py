"""Module containing repertoire-related domain models"""

from pydantic import BaseModel, ConfigDict, UUID4


class RepertoireIn(BaseModel):
    """Model representing repertoire's DTO attributes."""
    name: str


class RepertoireBroker(RepertoireIn):
    """A broker class including user in the model."""
    user_id: UUID4


class Repertoire(RepertoireIn):
    """Model representing repertoire's attributes in the database."""
    id: int

    model_config = ConfigDict(from_attributes=True, extra="ignore")

