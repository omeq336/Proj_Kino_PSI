"""Module containing hall service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from cinemaapi.core.domain.reservation import Reservation, ReservationBroker
from cinemaapi.infrastructure.dto.reservationdto import ReservationDTO


class IReservationService(ABC):
    """A class representing reservation repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[ReservationDTO]:
        """The abstract getting all reservations from the repository.

        Returns:
            Iterable[ReservationDTO]: All reservations.
        """

    @abstractmethod
    async def get_by_id(self, reservation_id: int) -> ReservationDTO | None:
        """The abstract getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO | None: The reservation details.
        """

    @abstractmethod
    async def add_reservation(self, data: ReservationBroker) -> Reservation | None:
        """The abstract adding new reservation to the data storage.

        Args:
            data (ReservationBroker): The details of the new reservation.

        Returns:
            Reservation | None: Full details of the newly added reservation.
        """

    @abstractmethod
    async def get_by_title(self, title: str) -> Iterable[Reservation]:
        """The abstract getting all reservations from the showing with given movie title.

        Args:
            title (str): title of the movie.

        Returns:
            Iterable[Reservation]: The reservation details.
        """

    @abstractmethod
    async def get_by_showing(self, showing_id: int) -> Iterable[Reservation]:
        """The abstract getting all reservations from the showing.

        Args:
            showing_id (int): ID of the showing.

        Returns:
            Iterable[Reservation]: The reservation details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID4) -> Iterable[ReservationDTO]:
        """The abstract getting all reservations from user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            Iterable[ReservationDTO]: The reservation details.
        """


    @abstractmethod
    async def update_reservation(
        self,
        reservation_id: int,
        data: ReservationBroker,
    ) -> Reservation | None:
        """The abstract updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationBroker): The details of the updated reservation.

        Returns:
            Reservation | None: The updated reservation details.
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
    async def validate_reservation(self, data: ReservationBroker) -> str | None:
        """The abstract responsible for validating data.

        Args:
            data (ReservationBroker): The data of the reservation.

        Returns:
            str | None: Validation status.
        """