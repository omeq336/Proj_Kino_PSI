"""Module containing movie repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from cinemaapi.core.domain.movie import MovieBroker


class IMovieRepository(ABC):
    """An abstract class representing protocol of imovie repository."""

    @abstractmethod
    async def get_all_movies(self) -> Iterable[Any]:
        """The abstract getting all movies from the data storage.

        Returns:
            Iterable[Any]: Movies in the data storage.
        """

    @abstractmethod
    async def get_by_id(self, movie_id: int) -> Any | None:
        """The abstract getting movie by provided id.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            Any | None: The movie details.
        """

    @abstractmethod
    async def get_by_title(self, title: str) -> Any | None:
        """The abstract getting movie by provided title.

        Args:
            title (str): The title of the movie.

        Returns:
            Any | None: The movie details.
        """

    @abstractmethod
    async def get_by_genre(self, genre: str) -> Iterable[Any]:
        """The abstract getting movie by provided genre.

        Args:
            genre (str): The genre of the movie.

        Returns:
            Any | None: The movie details.
        """

    @abstractmethod
    async def get_by_age_restriction(self, age: int) -> Iterable[Any]:
        """The abstract getting all movies below or equal to the provided age.

        Args:
            age (int): highest age allowed for the movie.

        Returns:
            Any | None: The movie details.
        """

    @abstractmethod
    async def get_by_rating(self, rating: int) -> Iterable[Any]:
        """The abstract getting all movies above or equal to the provided rating.

        Args:
            rating (int): Lowest rating allowed for the movie.

        Returns:
            Any | None: The movie details.
        """

    @abstractmethod
    async def add_movie(self, data: MovieBroker) -> Any | None:
        """The abstract adding new movie to the data storage.

        Args:
            data (MovieBroker): The details of the new movie.

        Returns:
            Any | None: The newly added movie.
        """

    @abstractmethod
    async def update_movie(
        self,
        movie_id: int,
        data: MovieBroker,
    ) -> Any | None:
        """The abstract updating movie data in the data storage.

        Args:
            movie_id (int): The id of the movie.
            data (MovieBroker): The details of the updated movie.

        Returns:
            Any | None: The updated movie details.
        """

    @abstractmethod
    async def delete_movie(self, movie_id: int) -> bool:
        """The abstract removing movie from the data storage.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            bool: Success of the operation.
        """