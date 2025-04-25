"""Module containing repertoire service abstractions."""

from abc import ABC, abstractmethod

from typing import Iterable

from cinemaapi.core.domain.repertoire import Repertoire, RepertoireBroker


class IRepertoireService(ABC):
    """A class representing repertoire repository."""

    @abstractmethod
    async def get_repertoire_by_id(self, repertoire_id: int) -> Repertoire | None:
        """The abstract getting repertoire by provided id.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            Repertoire | None: The repertoire details.
        """

    @abstractmethod
    async def get_all_repertoires(self) -> Iterable[Repertoire]:
        """The abstract getting all repertoires from the repository.

        Returns:
            Iterable[Repertoire]: All repertoires.
        """

    @abstractmethod
    async def add_repertoire(self, data: RepertoireBroker) -> Repertoire | None:
        """The abstract adding new repertoire to the data storage.

        Args:
            data (RepertoireBroker): The details of the new repertoire.

        Returns:
            Repertoire | None: Full details of the newly added repertoire.
        """

    @abstractmethod
    async def update_repertoire(
        self,
        repertoire_id: int,
        data: RepertoireBroker,
    ) -> Repertoire | None:
        """The abstract updating repertoire data in the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.
            data (RepertoireBroker): The details of the updated repertoire.

        Returns:
            Repertoire | None: The updated hall details.
        """

    @abstractmethod
    async def delete_repertoire(self, repertoire_id: int) -> bool:
        """The abstract removing repertoire from the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            bool: Success of the operation.
        """