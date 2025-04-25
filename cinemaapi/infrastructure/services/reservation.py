"""Module containing reservation service implementation."""
from typing import Iterable

from pydantic import UUID4

from cinemaapi.core.domain.reservation import Reservation, ReservationBroker
from cinemaapi.core.repositories.ireservation import IReservationRepository
from cinemaapi.infrastructure.dto.reservationdto import ReservationDTO
from cinemaapi.infrastructure.services.ireservation import IReservationService


class ReservationService(IReservationService):
    """A class implementing the reservation service."""

    _repository: IReservationRepository

    def __init__(self, repository: IReservationRepository) -> None:
        """The initializer of the `reservation service`.

        Args:
            repository (IReservationRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[ReservationDTO]:
        """The method getting all reservations from the repository.

        Returns:
            Iterable[ReservationDTO]: All halls.
        """

        return await self._repository.get_all_reservations()

    async def get_by_id(self, reservation_id: int) -> ReservationDTO | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            ReservationDTO | None: The reservation details.
        """

        return await self._repository.get_by_id(reservation_id)

    async def get_by_title(self, title: str) -> Iterable[Reservation]:
        """The abstract getting all reservations from the showing with given movie title.

        Args:
            title (str): title of the movie.

        Returns:
            Iterable[Reservation]: The reservations details.
        """

        return await self._repository.get_by_title(title)

    async def get_by_showing(self, showing_id: int) -> Iterable[Reservation]:
        """The method getting all reservations from the showing.

        Args:
            showing_id (int): ID of the showing.

        Returns:
            Iterable[Reservation]: The reservations details.
        """

        return await self._repository.get_by_showing(showing_id)

    async def get_by_user(self, user_id: UUID4) -> Iterable[ReservationDTO]:
        """The method getting all reservations from user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
           Iterable[ReservationDTO]: The reservations details.
        """

        return await self._repository.get_by_user(user_id)

    async def add_reservation(self, data: ReservationBroker) -> Reservation | None:
        """The method adding new reservation to the data storage.

        Args:
            data (ReservationBroker): The details of the new reservation.

        Returns:
            Reservation | None: Full details of the newly added reservation.
        """

        return await self._repository.add_reservation(data)

    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationBroker,
    ) -> Reservation | None:
        """The method updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationBroker): The details of the updated reservation.

        Returns:
            Reservation | None: The updated reservation details.
        """

        return await self._repository.update_reservation(
            reservation_id=reservation_id,
            data=data,
        )

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_reservation(reservation_id)

    async def validate_reservation(self, data: ReservationBroker) -> str | None:
        """The method responsible for validating data.

        Args:
            data (ReservationBroker): The data of the reservation.

        Returns:
            str | None: Validation status.
        """

        fetch_seats = await self._repository.fetch_seats_from_hall(data.showing_id)

        if fetch_seats is None:
            return "showing-availability-error"

        if reservation_data :=  await self.get_by_showing(data.showing_id):
            for res in reservation_data:
                if res.seat_num == data.seat_num and res.seat_row == data.seat_row:
                    return "seat-status-error"

        if data.seat_row not in fetch_seats.keys():
            return "seat-row-error"

        for row, seat_list in fetch_seats.items():
            if data.seat_num not in seat_list:
                return "seat-num-error"

        return None
