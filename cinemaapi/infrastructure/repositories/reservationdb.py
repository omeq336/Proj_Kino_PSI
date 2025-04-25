"""Module containing reservation repository implementation."""

from typing import Any, Iterable

from asyncpg import Record
from pydantic import UUID4
from sqlalchemy import select, join

from cinemaapi.core.domain.reservation import Reservation, ReservationBroker
from cinemaapi.core.repositories.ireservation import IReservationRepository
from cinemaapi.db import (
    reservation_table,
    hall_table,
    showing_table,
    movie_table,
    database,
)
from cinemaapi.infrastructure.dto.reservationdto import ReservationDTO


class ReservationRepository(IReservationRepository):
    """A class representing reservation DB repository."""

    async def get_all_reservations(self) -> Iterable[Any]:
        """The method getting all reservations from the data storage.

        Returns:
            Iterable[Any]: Reservations in the data storage.
        """

        query = (
            select(reservation_table, showing_table)
            .select_from(
                join(
                    reservation_table,
                    showing_table,
                    reservation_table.c.showing_id == showing_table.c.id
                )
            )
            .order_by(reservation_table.c.id.asc())
        )
        reservations = await database.fetch_all(query)

        return [ReservationDTO.from_record(reservation) for reservation in reservations]

    async def get_by_id(self, reservation_id: int) -> Any | None:
        """The method getting reservation by provided id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation details.
        """

        query = (
            select(reservation_table, showing_table)
            .select_from(
                    join(
                    reservation_table,
                    showing_table,
                    reservation_table.c.showing_id == showing_table.c.id
                )
            )
            .where(reservation_table.c.id == reservation_id)
            .order_by(reservation_table.c.id.asc())
        )

        reservation = await database.fetch_one(query)

        return ReservationDTO.from_record(reservation) if reservation else None

    async def get_by_title(self, title: str) -> Iterable[Any]:
        """The method getting reservations by movie title.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[Any]: The reservation collection.
        """

        query = (
            select(reservation_table, showing_table, movie_table)
            .select_from(
                join(
                    join(
                        reservation_table,
                        showing_table,
                        reservation_table.c.showing_id == showing_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(movie_table.c.title == title)
            .order_by(reservation_table.c.id.asc())
        )

        reservations = await database.fetch_all(query)

        return [Reservation(**dict(reservation)) for reservation in reservations]


    async def get_by_showing(self, showing_id: int) -> Iterable[Any]:
        """The method getting reservations by showing_id.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            Iterable[Any]: The reservation collection.
        """

        query = (
            reservation_table.select().where(reservation_table.c.showing_id == showing_id).order_by(reservation_table.c.id.asc())
        )

        reservations = await database.fetch_all(query)

        return [Reservation(**dict(reservation)) for reservation in reservations]


    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The method getting reservations by user.

        Args:
            user_id (str): The id of the user.

        Returns:
            Iterable[Any]: The reservation collection.
        """

        query = (
            select(reservation_table, showing_table)
            .select_from(
                join(
                    reservation_table,
                    showing_table,
                    reservation_table.c.showing_id == showing_table.c.id
                )
            )
            .where(reservation_table.c.user_id == user_id)
            .order_by(reservation_table.c.user_id.asc())
        )

        reservations = await database.fetch_all(query)

        return [ReservationDTO.from_record(reservation) for reservation in reservations]

    async def add_reservation(self, data: ReservationBroker) -> Any | None:
        """The method adding new reservation to the data storage.

        Args:
            data (ReservationBroker): The details of the new reservation.

        Returns:
            Reservation: Full details of the newly added reservation.

        Returns:
            Any | None: The newly added reservation.
        """

        if await self._check_seat_availability(data):
            query = reservation_table.insert().values(**data.model_dump())
            new_reservation_id = await database.execute(query)
            new_reservation = await self._get_by_id(new_reservation_id)

            await self._mark_reserved_seats(data)

            return Reservation(**dict(new_reservation)) if new_reservation else None

    async def update_reservation(
            self,
            reservation_id: int,
            data: ReservationBroker,
    ) -> Any | None:
        """The method updating reservation data in the data storage.

        Args:
            reservation_id (int): The id of the reservation.
            data (ReservationBroker): The details of the updated reservation.

        Returns:
            Any | None: The updated reservation details.
        """

        if self._get_by_id(reservation_id) and await self._check_seat_availability(data):

            await self._unmark_reserved_seats(reservation_id)  #  unmarks previously marked seats

            query = (
                reservation_table.update()
                .where(reservation_table.c.id == reservation_id)
                .values(
                    seat_row = data.seat_row,
                    seat_num = data.seat_num
                )
            )

            await database.execute(query)

            reservation = await self._get_by_id(reservation_id)

            await self._mark_reserved_seats(data)

            return Reservation(**dict(reservation)) if reservation else None

        return None

    async def delete_reservation(self, reservation_id: int) -> bool:
        """The method removing reservation from the data storage.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(reservation_id):
            query = reservation_table \
                .delete() \
                .where(reservation_table.c.id == reservation_id)
            await self._unmark_reserved_seats(reservation_id)  #  unmarks previously marked seats
            await database.execute(query)

            return True

        return False

    async def fetch_seats_from_hall(self, showing_id: int) -> dict | None:
        """A method getting seats from hall based on showing's id.

        Args:
            showing_id (int): The ID of the showing.

        Returns:
            dict | None: Dictionary containing hall's seats.
        """

        query = (
            select(hall_table.c.seats)
            .select_from(
                join(
                showing_table,
                hall_table,
                showing_table.c.hall_id == hall_table.c.id
                )
            )
            .where(showing_table.c.id == showing_id)
        )

        fetched_seats = await database.fetch_one(query)

        if fetched_seats is not None:
            return dict(fetched_seats[0])
        else:
            return None


    async def _get_by_id(self, reservation_id: int) -> Record | None:
        """A private method getting reservation from the DB based on its ID.

        Args:
            reservation_id (int): The ID of the reservation.

        Returns:
            Record | None: Reservation record if exists.
        """

        query = (
            reservation_table.select()
            .where(reservation_table.c.id == reservation_id)
            .order_by(reservation_table.c.id.asc())
        )

        return await database.fetch_one(query)

    async def _fetch_reservation_data(self, reservation_id: int) -> Any | None:
        """The private method getting reservation data by reservation_id.

        Args:
            reservation_id (int): The id of the reservation.

        Returns:
            Any | None: The reservation details.
        """

        query = (
            reservation_table.select()
            .where(reservation_table.c.id == reservation_id)
            .order_by(reservation_table.c.id.asc())
        )
        reservation = await database.fetch_one(query)

        return Reservation(**dict(reservation)) if reservation else None

    async def _check_seat_availability(self, data: ReservationBroker) -> bool:
        """A private method checking if the given seat is available.

        Args:
            data (ReservationBroker): Data with given information.

        Returns:
            bool: Seat availability status.
        """

        updated_seats = await self.fetch_seats_from_hall(data.showing_id)

        seat_row = data.seat_row
        seat_num = int(data.seat_num)

        for row, seat_list in updated_seats.items():
            index = 0
            if row == seat_row:
                for seat in seat_list:
                    if seat == "X" and seat_num == index+1:
                        return False
                    index += 1

        return True

    async def _mark_reserved_seats(self, data: ReservationBroker) -> None:
        """A private method marking the desired seats.

        Args:
            data (ReservationBroker): Data with given information.

        Returns:
            None.
        """

        updated_seats = await self.fetch_seats_from_hall(data.showing_id)

        seat_row = data.seat_row
        seat_num = int(data.seat_num)

        updated_seats[seat_row][seat_num - 1] = "X"
        await self._update_hall_seats(updated_seats, data.showing_id)

    async def _update_hall_seats(self, updated_seats: dict, showing_id: int) -> None:
        """A private method updating seats.

        Args:
            updated_seats (dict): Updated version of seats
            showing_id (int): Id of the showing.

        Returns:
            None.
        """

        query = (
            hall_table.update()
            .where(
                showing_table.c.id == showing_id,
                showing_table.c.hall_id == hall_table.c.id
            )
            .values(seats=updated_seats)
        )
        await database.execute(query)

    async def _unmark_reserved_seats(self, reservation_id: int) -> None:
        """A private method unmarking previously marked seats.

        Args:
            reservation_id (int): Id of the reservation.

        Returns:
            None.
        """

        reservation_data = await self._fetch_reservation_data(reservation_id)
        updated_seats = await self.fetch_seats_from_hall(reservation_data.showing_id)

        seat_row = reservation_data.seat_row
        seat_num = int(reservation_data.seat_num)

        for row, seat_list in updated_seats.items():
            index = 0
            if row == seat_row:
                for seat in seat_list:
                    if seat == "X" and seat_num == index+1:
                        updated_seats[row][index] = str(index+1)
                    index += 1

        await self._update_hall_seats(updated_seats, reservation_data.showing_id)
