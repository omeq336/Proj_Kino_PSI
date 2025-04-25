"""Module containing hall service implementation."""

from typing import Iterable

from cinemaapi.core.domain.repertoire import Repertoire, RepertoireBroker
from cinemaapi.core.repositories.irepertoire import IRepertoireRepository
from cinemaapi.infrastructure.services.irepertoire import IRepertoireService


class RepertoireService(IRepertoireService):
    """A class implementing the hall service."""

    _repository: IRepertoireRepository

    def __init__(self, repository: IRepertoireRepository) -> None:
        """The initializer of the `repertoire service`.

        Args:
            repository (IRepertoireRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_repertoire_by_id(self, repertoire_id: int) -> Repertoire | None:
        """The method getting repertoire by provided id.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            Repertoire | None: The repertoire details.
        """

        return await self._repository.get_by_id(repertoire_id)


    async def get_all_repertoires(self) -> Iterable[Repertoire]:
        """The method getting all repertoires from the repository.

        Returns:
            Iterable[Repertoire]: All repertoires.
        """

        return await self._repository.get_all_repertoires()

    async def add_repertoire(self, data: RepertoireBroker) -> Repertoire | None:
        """The method adding new repertoire to the data storage.

        Args:
            data (RepertoireBroker): The details of the new repertoire.

        Returns:
            Repertoire | None: Full details of the newly added repertoire.
        """

        return await self._repository.add_repertoire(data)

    async def update_repertoire(
        self,
        repertoire_id: int,
        data: RepertoireBroker,
    ) -> Repertoire | None:
        """The method updating repertoire data in the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.
            data (RepertoireBroker): The details of the updated repertoire.

        Returns:
            Repertoire | None: The updated repertoire details.
        """

        return await self._repository.update_repertoire(
            repertoire_id=repertoire_id,
            data=data,
        )

    async def delete_repertoire(self, repertoire_id: int) -> bool:
        """The method removing repertoire from the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_repertoire(repertoire_id)