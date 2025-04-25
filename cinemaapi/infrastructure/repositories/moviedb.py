"""Module containing movie repository implementation."""

from typing import Any, Iterable

from asyncpg import Record
from sqlalchemy import select

from cinemaapi.core.repositories.imovie import IMovieRepository
from cinemaapi.core.domain.movie import Movie, MovieBroker
from cinemaapi.db import (
    movie_table,
    database,
)
from cinemaapi.infrastructure.dto.moviedto import MovieDTO

class MovieRepository(IMovieRepository):
    """A class representing movie DB repository."""

    async def get_all_movies(self) -> Iterable[Any]:
        """The method getting all movies from the data storage.

        Returns:
            Iterable[Any]: Movies in the data storage.
        """

        query = (
            select(movie_table).order_by(movie_table.c.title.asc())
        )
        movies = await database.fetch_all(query)

        return [Movie(**dict(movie)) for movie in movies]

    async def get_by_id(self, movie_id: int) -> Any | None:
        """The method getting movie by provided id.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            Any | None: The movie details.
        """

        query = (
            select(movie_table).where(movie_table.c.id == movie_id).order_by(movie_table.c.id.asc())
        )
        movie = await database.fetch_one(query)

        return MovieDTO.from_record(movie) if movie else None

    async def get_by_title(self, title: str) -> Any | None:
        """The method getting movie by title.

        Args:
            title (str): The title of the movie.

        Returns:
            Any | None: The hall details.
        """

        query = (
            select(movie_table).where(movie_table.c.title == title).order_by(movie_table.c.title.asc())
        )
        movie = await database.fetch_one(query)

        return Movie(**dict(movie)) if movie else None

    async def get_by_genre(self, genre: str) -> Iterable[Any]:
        """The method getting movies by genre.

        Args:
            genre (str): The genre of the movie.

        Returns:
            Iterable[Any]: The movie collection.
        """

        query = (
            select(movie_table).where(movie_table.c.genre == genre).order_by(movie_table.c.id.asc())
        )
        movies = await database.fetch_all(query)

        return [MovieDTO.from_record(movie) for movie in movies]

    async def get_by_age_restriction(self, age: int) -> Iterable[Any]:
        """The method getting movies with below or equal age restriction.

        Args:
            age (int): The age restriction of the movie.

        Returns:
            Iterable[Any]: The movie collection.
        """

        query = (
            select(movie_table).where(movie_table.c.age_restriction <= age).order_by(movie_table.c.age_restriction.desc())
        )
        movies = await database.fetch_all(query)

        return [MovieDTO.from_record(movie) for movie in movies]

    async def get_by_rating(self, rating: int) -> Iterable[Any]:
        """The method getting movies with higher or equal rating.

        Args:
            rating (int): The rating of the movie.

        Returns:
            Iterable[Any]: The movie collection.
        """

        query = (
            select(movie_table).where(movie_table.c.rating >= rating).order_by(movie_table.c.rating.asc())
        )
        movies = await database.fetch_all(query)

        return [MovieDTO.from_record(movie) for movie in movies]

    async def add_movie(self, data: MovieBroker) -> Any | None:
        """The method adding new movie to the data storage.

        Args:
            data (MovieBroker): The details of the new movie.

        Returns:
            Movie: Full details of the newly added movie.

        Returns:
            Any | None: The newly added movie.
        """

        query = movie_table.insert().values(
            title=data.title,
            genre=data.genre,
            age_restriction=data.age_restriction,
            duration=data.duration,
            rating=0,
            user_id=data.user_id
        )
        new_movie_id = await database.execute(query)
        new_movie = await self._get_by_id(new_movie_id)

        return Movie(**dict(new_movie)) if new_movie else None

    async def update_movie(
        self,
        movie_id: int,
        data: MovieBroker,
    ) -> Any | None:
        """The method updating movie data in the data storage.

        Args:
            movie_id (int): The id of the movie.
            data (MovieBroker): The details of the updated movie.

        Returns:
            Any | None: The updated movie details.
        """

        if self._get_by_id(movie_id):
            query = (
                movie_table.update()
                .where(movie_table.c.id == movie_id)
                .values(
                    genre=data.genre,
                    age_restriction=data.age_restriction,
                    duration=data.duration,
                    user_id=data.user_id
                )
            )
            await database.execute(query)

            movie = await self._get_by_id(movie_id)

            return Movie(**dict(movie)) if movie else None

        return None

    async def delete_movie(self, movie_id: int) -> bool:
        """The method removing movie from the data storage.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(movie_id):
            query = movie_table \
                .delete() \
                .where(movie_table.c.id == movie_id)
            await database.execute(query)

            return True

        return False

    async def _get_by_id(self, movie_id: int) -> Record | None:
        """A private method getting movie from the DB based on its ID.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            Record | None: Movie record if exists.
        """

        query = (
            movie_table.select()
            .where(movie_table.c.id == movie_id)
            .order_by(movie_table.c.title.asc())
        )

        return await database.fetch_one(query)