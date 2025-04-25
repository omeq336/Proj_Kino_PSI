"""Module containing hall service abstractions."""

from abc import ABC, abstractmethod

from typing import Iterable

from cinemaapi.core.domain.hall import Hall, HallBroker


class IHallService(ABC):
    """A class representing hall repository."""

    @abstractmethod
    async def get_all_halls(self) -> Iterable[Hall]:
        """The abstract getting all halls from the repository.

        Returns:
            Iterable[Hall]: All halls.
        """

    @abstractmethod
    async def get_hall_by_id(self, hall_id: int) -> Hall | None:
        """The abstract getting hall by provided id.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            Hall | None: The hall details.
        """

    @abstractmethod
    async def get_hall_by_alias(self, alias: str) -> Hall | None:
        """The abstract getting hall by provided alias.

        Args:
            alias (int): The alias of the hall.

        Returns:
            Hall | None: The hall details.
        """

    @abstractmethod
    async def add_hall(self, data: HallBroker) -> Hall | None:
        """The abstract adding new hall to the data storage.

        Args:
            data (HallBroker): The details of the new hall.

        Returns:
            Hall | None: Full details of the newly added hall.
        """

    @abstractmethod
    async def update_hall(
        self,
        hall_id: int,
        data: HallBroker,
    ) -> Hall | None:
        """The abstract updating hall data in the data storage.

        Args:
            hall_id (int): The id of the hall.
            data (HallBroker): The details of the updated hall.

        Returns:
            Hall | None: The updated hall details.
        """

    @abstractmethod
    async def delete_hall(self, hall_id: int) -> bool:
        """The abstract removing hall from the data storage.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def validate_hall(self, data: HallBroker) -> str | None:
        """The abstract responsible for validating data.

        Args:
            data (HallBroker): The data of the hall.

        Returns:
            str | None: Validation status.
        """