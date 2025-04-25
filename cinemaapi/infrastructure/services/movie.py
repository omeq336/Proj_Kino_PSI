"""Module containing movie service implementation."""

from typing import Iterable

from cinemaapi.core.domain.movie import Movie, MovieBroker
from cinemaapi.core.repositories.imovie import IMovieRepository
from cinemaapi.infrastructure.dto.moviedto import MovieDTO
from cinemaapi.infrastructure.services.imovie import IMovieService


class MovieService(IMovieService):
    """A class implementing the movie service."""

    _repository: IMovieRepository

    def __init__(self, repository: IMovieRepository) -> None:
        """The initializer of the `movie service`.

        Args:
            repository (IMovieRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[Movie]:
        """The method getting all movies from the repository.

        Returns:
            Iterable[MovieDTO]: All movies.
        """

        return await self._repository.get_all_movies()

    async def get_by_id(self, movie_id: int) -> MovieDTO | None:
        """The method getting movie by provided id.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            MovieDTO | None: The movie details.
        """

        return await self._repository.get_by_id(movie_id)

    async def get_by_title(self, title: str) -> Movie | None:
        """The abstract getting movie by provided title.

        Args:
            title (str): The title of the movie.

        Returns:
            MovieDTO | None: The movie details.
        """

        return await self._repository.get_by_title(title)

    async def get_by_genre(self, genre: str) -> Iterable[MovieDTO]:
        """The abstract getting movie by provided genre.

        Args:
            genre (str): The genre of the movie.

        Returns:
            Iterable[MovieDTO]: The movie details.
        """

        return await self._repository.get_by_genre(genre)

    async def get_by_age_restriction(self, age: int) -> Iterable[MovieDTO]:
        """The method getting all movies below or equal to the provided age.

        Args:
            age (int): highest age allowed for the movie.

        Returns:
            Any | None: The movie details.
        """
        return await self._repository.get_by_age_restriction(age)

    async def get_by_rating(self, rating: int) -> Iterable[MovieDTO]:
        """The abstract getting all movies above the provided rating.

        Args:
            rating (int): Lowest rating allowed for the movie.

        Returns:
            Iterable[MovieDTO]: The movie details.
        """

        return await self._repository.get_by_rating(rating)

    async def add_movie(self, data: MovieBroker) -> Movie | None:
        """The method adding new movie to the data storage.

        Args:
            data (MovieBroker): The details of the new movie.

        Returns:
            Movie | None: Full details of the newly added movie.
        """

        return await self._repository.add_movie(data)

    async def update_movie(
        self,
        movie_id: int,
        data: MovieBroker
    ) -> Movie | None:
        """The method updating movie data in the data storage.

        Args:
            movie_id (int): The id of the movie.
            data (MovieBroker): The details of the updated Movie.

        Returns:
            Movie | None: The updated movie details.
        """

        return await self._repository.update_movie(
            movie_id=movie_id,
            data=data,
        )

    async def delete_movie(self, movie_id: int) -> bool:
        """The method updating removing movie from the data storage.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            bool: Success of the operation.
        """

        return await self._repository.delete_movie(movie_id)

    async def validate_movie(self, data: MovieBroker) -> str | None:
        """The method responsible for validating data.

        Args:
            data (MovieBroker): The data of the movie.

        Returns:
            str | None: Validation status.
        """

        if await self.get_by_title(data.title):
            return "movie-title-occupied"

        if data.age_restriction < 0:
            return "movie-age_restriction-invalid"

        time_split = data.duration.split(".")

        if len(time_split) != 2:
            return "movie-duration-invalid"

        try:
            hours = int(time_split[0])
            minutes = int(time_split[1])
        except:
            return "movie-duration-invalid"

        if minutes > 59 or minutes < 0 or hours < 0:
            return "movie-duration-invalid"

        return None