"""Module containing reservation repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

from cinemaapi.core.domain.reservation import ReservationBroker


class IReservationRepository(ABC):
    """An abstract class representing protocol of ireservation repository."""

    @abstractmethod
    async def get_all_reservations(self) -> Iterable[Any]:
        """The abstract getting all reservations from the data storage.

        Returns:
            Iterable[Any]: Reservations in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> Any | None:
        """The abstract getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation details.
        """

    @abstractmethod
    async def get_by_title(self, title: str) -> Iterable[Any]:
        """The abstract getting all reservations from the showing with given movie title.

        Args:
            title (str): title of the movie.

        Returns:
            Any | None: The reservation details.
        """


    @abstractmethod
    async def get_by_showing(self, showing_id: int) -> Iterable[Any]:
        """The abstract getting all reservations from the showing.

        Args:
            showing_id (int): ID of the showing.

        Returns:
            Any | None: The reservation details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The abstract getting all reservations from user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            Any | None: The reservation details.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationBroker) -> Any | None:
        """The abstract adding new reservation to the data storage.

        Args:
            data (ReservationBroker): The details of the new reservation.

        Returns:
            Any | None: The newly added reservation.
        """

    @abstractmethod
    async def update_reservation(
        self,
        reservation_id: int,
        data: ReservationBroker,
    ) -> Any | None:
        """The abstract updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationBroker): The details of the updated reservation.

        Returns:
            Any | None: The updated reservation details.
        """

    @abstractmethod
    async def delete_reservation(self, reservation_id: int) -> bool:
        """The abstract removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """
    @abstractmethod
    async def fetch_seats_from_hall(self, showing_id: int) -> dict | None:
        """An abstract getting seats from hall based on showing's id.

        Args:
            showing_id (int): The ID of the showing.

        Returns:
            dict | None: Dictionary containing hall's seats.
        """
