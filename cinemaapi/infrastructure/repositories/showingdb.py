"""Module containing hall repository implementation."""

from typing import Any, Iterable

from asyncpg import Record
from sqlalchemy import select, join

from cinemaapi.core.domain.showing import Showing, ShowingBroker
from cinemaapi.core.repositories.ishowing import IShowingRepository
from cinemaapi.db import (
    showing_table,
    database, movie_table, repertoire_table
)
from cinemaapi.infrastructure.dto.showingdto import ShowingDTO


class ShowingRepository(IShowingRepository):
    """A class representing showing DB repository."""

    async def get_all_showings(self) -> Iterable[Any]:
        """The method getting all the showings within the data storage.

        Returns:
            Iterable[Any]: Showings in the data storage.
        """

        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .order_by(showing_table.c.id.asc())
        )

        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]


    async def get_showing_by_id(self, showing_id: int) -> Any | None:
        """The method getting showing by provided id.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            Any | None: The showing details.
        """

        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(showing_table.c.id == showing_id)
            .order_by(showing_table.c.id.asc())
        )

        showing = await database.fetch_one(query)

        return ShowingDTO.from_record(showing) if showing else None

    async def get_by_repertoire(self, repertoire_id: int) -> Iterable[Any]:
        """The method getting showings assigned to particular repertoire.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            Iterable[Any]: Showings assigned to a repertoire.
        """
        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(showing_table.c.repertoire_id == repertoire_id)
            .order_by(movie_table.c.title.asc())
        )

        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]


    async def get_showings_by_date(self, showing_date: str) -> Iterable[Any]:
        """The method getting showings assigned to particular date.

        Args:
            showing_date(int): The date of the showing.

        Returns:
            Iterable[Any]: Showings assigned to a particular date.
        """
        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(showing_table.c.date == showing_date)
            .order_by(showing_table.c.date.asc())
        )

        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]

    async def get_showings_by_time(self, showing_time: str) -> Iterable[Any]:
        """The method getting showings with time equal to showing_time or above.

        Args:
            showing_time(int): The time of the showing.

        Returns:
            Iterable[Any]: Showings assigned to a particular time.
        """

        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(showing_table.c.time >= showing_time)
            .order_by(showing_table.c.time.asc())
        )

        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]


    async def get_showings_by_language_ver(self, language_ver: str) -> Iterable[Any]:
        """The method getting showings assigned to language version.

        Args:
            language_ver(int): The language version of the showing.

        Returns:
            Iterable[Any]: Showings assigned to language version.
        """

        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(showing_table.c.language_ver == language_ver)
            .order_by(showing_table.c.id.asc())
        )

        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]

    async def get_showings_by_movie_genre(self, genre: str) -> Iterable[Any]:
        """The method getting showings assigned to movie genre.

        Args:
            genre(str): The genre of the showing.

        Returns:
            Iterable[Any]: Showings with given genre.
        """

        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(movie_table.c.genre == genre)
            .order_by(movie_table.c.genre.asc())
        )
        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]


    async def get_showing_by_movie_title(self, title: str) -> Iterable[Any] | None:
        """The method getting showing by movie title.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[Any]: Showings with given title.
        """

        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(movie_table.c.title == title)
            .order_by(movie_table.c.title.asc())
        )

        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]

    async def get_showings_by_age_restriction(self, age: int) -> Iterable[Any]:
        """The method getting showings that are equal or below given age.

        Args:
            age(int): The age restriction of the showing.

        Returns:
            Iterable[Any]: Showings with higher or equal age restriction.
        """

        query = (
            select(showing_table, repertoire_table, movie_table)
            .select_from(
                join(
                    join(
                        showing_table,
                        repertoire_table,
                        showing_table.c.repertoire_id == repertoire_table.c.id
                    ),
                    movie_table,
                    showing_table.c.movie_id == movie_table.c.id,
                )
            )
            .where(movie_table.c.age_restriction <= age)
            .order_by(movie_table.c.age_restriction.desc())
        )

        showings = await database.fetch_all(query)

        return [ShowingDTO.from_record(showing) for showing in showings]

    async def fetch_showing_duration(self, movie_id: int) -> str | None:
        """The method getting showing duration by movie id.

        Args:
            movie_id(int): The id of the movie.

        Returns:
            str | None: Showings duration.
        """

        query = (
            select(movie_table.c.duration).where(movie_table.c.id == movie_id)
        )

        if showing_duration := await database.fetch_one(query):
            return str(showing_duration[0])
        return None

    async def add_showing(self, data: ShowingBroker) -> Any | None:
        """The method adding new showing to the data storage.

        Args:
            data (ShowingBroker): The details of a new showing.

        Returns:
            Any | None: the newly added showing
        """

        query = showing_table.insert().values(**data.model_dump())
        new_showing_id = await database.execute(query)
        new_showing = await self._get_by_id(new_showing_id)


        return Showing(**dict(new_showing)) if new_showing else None

    async def update_showing(self, showing_id: int, data: ShowingBroker) -> Any | None:
        """The method updating showing data in the data storage.

        Args:
            showing_id (int): The id of the showing.
            data (ShowingBroker): The details of the updated showing.

        Returns:
            Any | None: The updated showing details.
        """

        if self._get_by_id(showing_id):
            query = (
                showing_table.update()
                .where(showing_table.c.id == showing_id)
                .values(**data.model_dump())
            )
            await database.execute(query)

            showing = await self._get_by_id(showing_id)

            return Showing(**dict(showing)) if showing else None

        return None

    async def delete_showing(self, showing_id: int) -> bool:
        """The method removing showing from the data storage.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(showing_id):
            query = showing_table \
                .delete() \
                .where(showing_table.c.id == showing_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, showing_id: int) -> Record | None:
        """A private method getting showing from the DB based on its ID.

        Args:
            showing_id (int): The ID of the showing.

        Returns:
            Record | None: Showing record if exists.
        """

        query = (
            showing_table.select()
            .where(showing_table.c.id == showing_id)
            .order_by(showing_table.c.id.asc())
        )

        return await database.fetch_one(query)
