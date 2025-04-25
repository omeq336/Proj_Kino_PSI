"""Module containing repertoire repository implementation."""

from typing import Any, Iterable

from asyncpg import Record
from sqlalchemy import select

from cinemaapi.core.domain.repertoire import Repertoire, RepertoireBroker
from cinemaapi.core.repositories.irepertoire import IRepertoireRepository
from cinemaapi.db import (
    repertoire_table,
    database
)


class RepertoireRepository(IRepertoireRepository):
    """A class representing repertoire DB repository."""

    async def get_all_repertoires(self) -> Iterable[Any]:
        """The method getting all repertoires from the data storage.

        Returns:
            Iterable[Any]: Repertoires in the data storage.
        """

        query = (
            select(repertoire_table).order_by(repertoire_table.c.id.asc())
        )
        repertoires = await database.fetch_all(query)

        return [Repertoire(**dict(repertoire)) for repertoire in repertoires]

    async def get_by_id(self, repertoire_id: int) -> Any | None:
        """The method getting repertoire by provided id.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            Any | None: The repertoire details.
        """

        query = (
            select(repertoire_table).where(repertoire_table.c.id == repertoire_id).order_by(repertoire_table.c.id.asc())
        )

        repertoire = await database.fetch_one(query)

        return Repertoire(**dict(repertoire)) if repertoire else None

    async def add_repertoire(self, data: RepertoireBroker) -> Any | None:
        """The method adding new repertoire to the data storage.

        Args:
            data (RepertoireBroker): The details of the new repertoire.

        Returns:
            Repertoire: Full details of the newly added repertoire.

        Returns:
            Any | None: The newly added repertoire.
        """

        query = repertoire_table.insert().values(**data.model_dump())
        new_repertoire_id = await database.execute(query)
        new_repertoire = await self._get_by_id(new_repertoire_id)

        return Repertoire(**dict(new_repertoire)) if new_repertoire else None

    async def update_repertoire(
            self,
            repertoire_id: int,
            data: RepertoireBroker,
    ) -> Any | None:
        """The method updating repertoire data in the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.
            data (RepertoireBroker): The details of the updated repertoire.

        Returns:
            Any | None: The updated repertoire details.
        """

        if self._get_by_id(repertoire_id):
            query = (
                repertoire_table.update()
                .where(repertoire_table.c.id == repertoire_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            repertoire = await self._get_by_id(repertoire_id)

            return Repertoire(**dict(repertoire)) if repertoire else None

        return None

    async def delete_repertoire(self, repertoire_id: int) -> bool:
        """The method removing repertoire from the data storage.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(repertoire_id):
            query = repertoire_table \
                .delete() \
                .where(repertoire_table.c.id == repertoire_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, repertoire_id: int) -> Record | None:
        """A private method getting repertoire from the DB based on its ID.

        Args:
            repertoire_id (int): The ID of the repertoire.

        Returns:
            Record | None: Repertoire record if exists.
        """

        query = (
            repertoire_table.select()
            .where(repertoire_table.c.id == repertoire_id)
            .order_by(repertoire_table.c.name.asc())
        )

        return await database.fetch_one(query)