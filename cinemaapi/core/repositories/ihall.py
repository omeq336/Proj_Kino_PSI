"""Module containing hall repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from cinemaapi.core.domain.hall import HallBroker


class IHallRepository(ABC):
    """An abstract class representing protocol of ihall repository."""

    @abstractmethod
    async def get_hall_by_id(self, hall_id: int) -> Any | None:
        """The abstract getting hall by provided id.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            Any | None: The hall details.
        """

    @abstractmethod
    async def get_hall_by_alias(self, alias: str) -> Any | None:
        """The abstract getting hall by its alias.

        Args:
            alias (str): The alias of the hall.

        Returns:
            Any | None: The hall details.
        """

    @abstractmethod
    async def get_all_halls(self) -> Iterable[Any]:
        """The abstract getting all halls from the data storage.

        Returns:
            Iterable[Any]: Halls in the data storage.
        """

    @abstractmethod
    async def add_hall(self, data: HallBroker) -> Any | None:
        """The abstract adding new hall to the data storage.

        Args:
            data (HallBroker): The details of the new hall.

        Returns:
            Any | None: The newly added hall.
        """

    @abstractmethod
    async def update_hall(
        self,
        hall_id: int,
        data: HallBroker,
    ) -> Any | None:
        """The abstract updating hall data in the data storage.

        Args:
            hall_id (int): The id of the hall.
            data (HallBroker): The details of the updated hall.

        Returns:
            Any | None: The updated hall details.
        """

    @abstractmethod
    async def delete_hall(self, hall_id: int) -> bool:
        """The abstract removing hall from the data storage.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            bool: Success of the operation.
        """