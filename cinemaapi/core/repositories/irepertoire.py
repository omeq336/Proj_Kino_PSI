"""Module containing repertoire repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from cinemaapi.core.domain.repertoire import RepertoireBroker


class IRepertoireRepository(ABC):
    """An abstract class representing protocol of irepertoire repository."""

    @abstractmethod
    async def get_by_id(self, repertoire_id: int) -> Any | None:
        """The abstract getting repertoire by provided id.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            Any | None: The repertoire details.
        """

    @abstractmethod
    async def get_all_repertoires(self) -> Iterable[Any]:
        """The abstract getting all repertoires from the data storage.

        Returns:
            Iterable[Any]: Repertoires in the data storage.
        """

    @abstractmethod
    async def add_repertoire(self, data: RepertoireBroker) -> Any | None:
        """The abstract adding new repertoire to the data storage.

        Args:
            data (RepertoireBroker): The details of the new repertoire.

        Returns:
            Any | None: The newly added repertoire.
        """

    @abstractmethod
    async def update_repertoire(
        self,
        repertoire_id: int,
        data: RepertoireBroker,
    ) -> Any | None:
        """The abstract updating repertoire data in the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.
            data (RepertoireBroker): The details of the updated repertoire.

        Returns:
            Any | None: The updated repertoire details.
        """

    @abstractmethod
    async def delete_repertoire(self, repertoire_id: int) -> bool:
        """The abstract removing repertoire from the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            bool: Success of the operation.
        """