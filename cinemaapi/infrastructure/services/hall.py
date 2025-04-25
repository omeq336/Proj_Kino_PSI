"""Module containing hall service implementation."""

from typing import Iterable

from cinemaapi.core.domain.hall import Hall, HallBroker
from cinemaapi.core.repositories.ihall import IHallRepository
from cinemaapi.infrastructure.services.ihall import IHallService


class HallService(IHallService):
    """A class implementing the hall service."""

    _repository: IHallRepository

    def __init__(self, repository: IHallRepository) -> None:
        """The initializer of the `hall service`.

        Args:
            repository (IHallRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all_halls(self) -> Iterable[Hall]:
        """The method getting all halls from the repository.

        Returns:
            Iterable[Hall]: All halls.
        """

        return await self._repository.get_all_halls()

    async def get_hall_by_id(self, hall_id: int) -> Hall | None:
        """The method getting hall by provided id.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            Hall | None: The hall details.
        """

        return await self._repository.get_hall_by_id(hall_id)

    async def get_hall_by_alias(self, alias: str) -> Hall | None:
        """The method getting hall by provided alias.

        Args:
            alias (int): The alias of the hall.

        Returns:
            Hall | None: The hall details.
        """

        return await self._repository.get_hall_by_alias(alias)

    async def add_hall(self, data: HallBroker) -> Hall | None:
        """The method adding new hall to the data storage.

        Args:
            data (HallBroker): The details of the new hall.

        Returns:
            Hall | None: Full details of the newly added hall.
        """

        return await self._repository.add_hall(data)

    async def update_hall(self, hall_id: int, data: HallBroker) -> Hall | None:
        """The method updating hall data in the data storage.

        Args:
            hall_id (int): The id of the hall.
            data (HallBroker): The details of the updated hall.

        Returns:
            Hall | None: The updated hall details.
        """

        return await self._repository.update_hall(
            hall_id=hall_id,
            data=data,
        )

    async def delete_hall(self, hall_id: int) -> bool:
        """The method removing hall from the data storage.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_hall(hall_id)

    async def validate_hall(self, data: HallBroker) -> str | None:
        """The method responsible for validating data.

        Args:
            data (HallBroker): The data of the hall.

        Returns:
            str | None: Validation status.
        """

        if data.seat_amount <= 0 or data.row_amount <= 0:
            return "hall-seat-row-invalid"

        if await self.get_hall_by_alias(data.alias):
            return "hall-alias-occupied"

        return None