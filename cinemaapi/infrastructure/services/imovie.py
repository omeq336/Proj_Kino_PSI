"""Module containing movie service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from cinemaapi.core.domain.movie import Movie, MovieBroker
from cinemaapi.infrastructure.dto.moviedto import MovieDTO


class IMovieService(ABC):
    """A class representing movie repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[Movie]:
        """The abstract getting all movies from the repository.

        Returns:
            Iterable[Movie]: All movies.
        """

    @abstractmethod
    async def get_by_id(self, movie_id: int) -> MovieDTO | None:
        """The abstract getting movie by provided id.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            MovieDTO | None: The movie details.
        """

    @abstractmethod
    async def get_by_title(self, title: str) -> Movie | None:
        """The abstract getting movie by provided title.

        Args:
            title (str): The title of the movie.

        Returns:
            Movie | None: The movie details.
        """

    @abstractmethod
    async def get_by_genre(self, genre: str) -> Iterable[MovieDTO]:
        """The abstract getting movie by provided genre.

        Args:
            genre (str): The genre of the movie.

        Returns:
            Iterable[MovieDTO]: Movies assigned to a genre.
        """

    @abstractmethod
    async def get_by_age_restriction(self, age: int) -> Iterable[MovieDTO]:
        """The abstract getting all movies below or equal to the provided age.

        Args:
            age (int): highest age allowed for the movie.

        Returns:
            Iterable[MovieDTO]: Movies assigned to a genre.
        """

    @abstractmethod
    async def get_by_rating(self, rating: int) -> Iterable[MovieDTO]:
        """The abstract getting all movies above the provided rating.

        Args:
            rating (int): Lowest rating allowed for the movie.

        Returns:
            Iterable[MovieDTO]: The movie details.
        """

    @abstractmethod
    async def add_movie(self, data: MovieBroker) -> Movie | None:
        """The method adding new movie to the data storage.

        Args:
            data (MovieBroker): The details of the new movie.

        Returns:
            Movie | None: Full details of the newly added movie.
        """

    @abstractmethod
    async def update_movie(
        self,
        movie_id: int,
        data: MovieBroker,
    ) -> Movie | None:
        """The method updating movie data in the data storage.

        Args:
            movie_id (int): The id of the movie.
            data (MovieBroker): The details of the updated Movie.

        Returns:
            Movie | None: The updated movie details.
        """

    @abstractmethod
    async def delete_movie(self, movie_id: int) -> bool:
        """The method removing movie from the data storage.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def validate_movie(self, data: MovieBroker) -> str | None:
        """The abstract responsible for validating data.

        Args:
            data (MovieBroker): The data of the movie.

        Returns:
            str | None: Validation status.
        """