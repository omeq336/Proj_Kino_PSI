"""Module containing hall repository implementation."""
from string import ascii_uppercase
from typing import Any, Iterable

from asyncpg import Record

from cinemaapi.core.domain.hall import Hall, HallBroker
from cinemaapi.core.repositories.ihall import IHallRepository
from cinemaapi.db import (
    hall_table,
    database
)


class HallRepository(IHallRepository):
    """A class representing hall DB repository."""

    async def get_all_halls(self) -> Iterable[Any]:
        """The method getting all halls from the data storage.

        Returns:
            Iterable[Any]: Halls in the data storage.
        """

        query = hall_table.select().order_by(hall_table.c.id.asc())
        halls = await database.fetch_all(query)

        return [Hall(**dict(hall)) for hall in halls]

    async def get_hall_by_id(self, hall_id: int) -> Any | None:
        """The method getting hall by provided id.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            Any | None: The hall details.
        """

        query = (
            hall_table.select().where(hall_table.c.id == hall_id).order_by(hall_table.c.id.asc())
        )

        hall = await database.fetch_one(query)

        return Hall(**dict(hall)) if hall else None


    async def get_hall_by_alias(self, alias: str) -> Any | None:
        """The method getting hall by provided alias.

        Args:
            alias (str): The alias code of the hall.

        Returns:
            Any | None: The hall details.
        """

        query = (
            hall_table.select().where(hall_table.c.alias == alias).order_by(hall_table.c.alias.asc())
        )

        hall = await database.fetch_one(query)

        return Hall(**dict(hall)) if hall else None

    async def add_hall(self, data: HallBroker) -> Any | None:
        """The method adding new hall to the data storage.

        Args:
            data (HallBroker): The details of the new hall.

        Returns:
            Hall: Full details of the newly added hall.

        Returns:
            Any | None: The newly added hall.
        """

        custom_seats = await self._hall_creator(data)

        query = hall_table.insert().values(
            alias=data.alias,
            seat_amount=data.seat_amount,
            row_amount=data.row_amount,
            seats=custom_seats,
            user_id=data.user_id,
        )
        new_hall_id = await database.execute(query)
        new_hall = await self._get_by_id(new_hall_id)

        return Hall(**dict(new_hall)) if new_hall else None

    async def update_hall(
            self,
            hall_id: int,
            data: HallBroker,
    ) -> Any | None:
        """The method updating hall data in the data storage.

        Args:
            hall_id (int): The id of the hall.
            data (HallBroker): The details of the updated hall.

        Returns:
            Any | None: The updated hall details.
        """

        if self._get_by_id(hall_id):
            query = (
                hall_table.update()
                .where(hall_table.c.id == hall_id)
                .values(
                    alias=data.alias,
                    user_id=data.user_id,
                )
            )
            await database.execute(query)

            hall = await self._get_by_id(hall_id)

            return Hall(**dict(hall)) if hall else None

        return None

    async def delete_hall(self, hall_id: int) -> bool:
        """The method removing hall from the data storage.

        Args:
            hall_id (int): The id of the hall.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(hall_id):
            query = hall_table \
                .delete() \
                .where(hall_table.c.id == hall_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, hall_id: int) -> Record | None:
        """A private method getting hall from the DB based on its ID.

        Args:
            hall_id (int): The ID of the hall.

        Returns:
            Record | None: Hall record if exists.
        """

        query = (
            hall_table.select()
            .where(hall_table.c.id == hall_id)
            .order_by(hall_table.c.id.asc())
        )

        return await database.fetch_one(query)

    async def _hall_creator(self, data: HallBroker) -> dict:
        """A private method creating hall layout based on given data.

        Args:
            data (HallBroker): The data of hall.

        Returns:
            dict: Hall layout.
        """

        row_len = data.row_amount
        seat_len = data.seat_amount
        new_layout = {}

        for row in ascii_uppercase[0:row_len]:
            new_layout[row] = []
            for seat in range(1, seat_len + 1):
                new_layout[row].append(str(seat))

        return new_layout