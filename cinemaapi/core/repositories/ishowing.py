"""Module containing showing repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from cinemaapi.core.domain.showing import ShowingBroker


class IShowingRepository(ABC):
    """An abstract class representing protocol of ishowing repository."""

    @abstractmethod
    async def get_showing_by_id(self, showing_id: int) -> Any | None:
        """The abstract getting showing by provided id.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            Any | None: The showing details.
        """

    @abstractmethod
    async def get_all_showings(self) -> Iterable[Any]:
        """The abstract getting all showings from the data storage.

        Returns:
            Iterable[Any]: Showings in the data storage.
        """

    @abstractmethod
    async def get_by_repertoire(self, repertoire_id: int) -> Iterable[Any]:
        """The abstract getting showings assigned to repertoire.

        Args:
            repertoire_id(int): The id of the repertoire.

        Returns:
            Iterable[Any]: Showings assigned to repertoire.
        """

    @abstractmethod
    async def get_showings_by_date(self, showing_date: str) -> Iterable[Any]:
        """The abstract getting showings by date.

        Args:
            showing_date(str): The date of the showing.

        Returns:
            Iterable[Any]: Showings assigned to provided date.
        """

    @abstractmethod
    async def get_showings_by_time(self, showing_time: str) -> Iterable[Any]:
        """The abstract getting showings assigned time of the day.

        Args:
            showing_time(int): The time of the showing.

        Returns:
            Iterable[Any]: Showings assigned to a particular time.
        """

    @abstractmethod
    async def get_showings_by_language_ver(self, language_ver: str) -> Iterable[Any]:
        """The abstract getting showings assigned to language version.

        Args:
            language_ver(str): The language version of the showing.

        Returns:
            Iterable[Any]: Showings assigned to language version.
        """

    @abstractmethod
    async def get_showings_by_movie_genre(self, genre: str) -> Iterable[Any]:
        """The abstract getting showings assigned to movie genre.

        Args:
            genre(str): The genre of the showing.

        Returns:
            Iterable[Any]: Showings assigned to genre.
        """

    @abstractmethod
    async def get_showing_by_movie_title(self, title: str) -> Any | None:
        """The abstract getting showings with provided movie title.

        Args:
            title(str): The title of the movie.

        Returns:
            Iterable[Any]: Showings assigned to movie with given title.
        """

    @abstractmethod
    async def get_showings_by_age_restriction(self, age: int) -> Iterable[Any]:
        """The abstract getting showings that are equal or below given age.

        Args:
            age(int): The age restriction of the showing.

        Returns:
            Iterable[Any]: Showings that are below or equal to age restriction.
        """

    @abstractmethod
    async def fetch_showing_duration(self, movie_id: int) -> str | None:
        """The abstract getting showing duration movie id.

        Args:
            movie_id(int): The id of the movie.

        Returns:
            str | None: Showings duration.
        """

    @abstractmethod
    async def add_showing(self, data: ShowingBroker) -> Any | None:
        """The abstract adding new showing to the data storage.

        Args:
            data (ShowingBroker): The details of the new showing.

        Returns:
            Any | None: The newly added showing.
        """

    @abstractmethod
    async def update_showing(
        self,
        showing_id: int,
        data: ShowingBroker,
    ) -> Any | None:
        """The abstract updating showing data in the data storage.

        Args:
            showing_id (int): The id of the showing.
            data (ShowingBroker): The details of the updated showing.

        Returns:
            Any | None: The updated showing details.
        """

    @abstractmethod
    async def delete_showing(self, showing_id: int) -> bool:
        """The abstract removing showing from the data storage.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            bool: Success of the operation.
        """