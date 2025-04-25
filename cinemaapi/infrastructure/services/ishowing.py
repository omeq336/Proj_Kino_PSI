"""Module containing showing service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from cinemaapi.core.domain.showing import Showing, ShowingBroker
from cinemaapi.infrastructure.dto.showingdto import ShowingDTO


class IShowingService(ABC):
    """A class representing showing repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[ShowingDTO]:
        """The abstract getting all showings from the repository.

        Returns:
            Iterable[ShowingDTO]: All showings.
        """

    @abstractmethod
    async def get_by_id(self, showing_id: int) -> ShowingDTO | None:
        """The abstract getting showing by provided id.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            ShowingDTO | None: The showing details.
        """

    @abstractmethod
    async def get_by_repertoire(self, repertoire_id: int) -> Iterable[ShowingDTO]:
        """The abstract getting showings assigned to particular repertoire.

        Args:
            repertoire_id (int): The id of the repertoire.

        Returns:
            Iterable[ShowingDTO]: Showings assigned to a repertoire.
        """

    @abstractmethod
    async def get_showings_by_date(self, showing_date: str) -> Iterable[ShowingDTO]:
        """The abstract getting showings assigned to date.

        Args:
            showing_date (int): The date of the showing.

        Returns:
            Iterable[ShowingDTO]: Showings assigned to a date.
        """

    @abstractmethod
    async def get_showings_by_time(self, showing_time: str) -> Iterable[ShowingDTO]:
        """The abstract getting showings with time equal to showing_time or above.

        Args:
            showing_time (int): The time of the showing.

        Returns:
            Iterable[ShowingDTO]: Showings within given time or above.
        """

    @abstractmethod
    async def get_showings_by_language_ver(self, language_ver: str) -> Iterable[ShowingDTO]:
        """The abstract getting showings assigned to language version.

        Args:
            language_ver (str): The language version of the showing.

        Returns:
            Iterable[ShowingDTO]: Showings with given language version.
        """

    @abstractmethod
    async def get_showings_by_movie_genre(self, genre: str) -> Iterable[ShowingDTO]:
        """The abstract getting showings assigned to particular movie genre.

        Args:
            genre (str): The genre of the movie.

        Returns:
            Iterable[ShowingDTO]: Showings assigned to genre.
        """

    @abstractmethod
    async def get_showing_by_movie_title(self, title: str) -> Iterable[ShowingDTO] | None:
        """The abstract getting showings assigned to particular title.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[ShowingDTO]: Showings with given title.
        """

    @abstractmethod
    async def get_showings_by_age_restriction(self, age: int) -> Iterable[ShowingDTO]:
        """The abstract getting showings with age restriction lower or equal to given age.

        Args:
            age (int): The age restriction of the movie.

        Returns:
            Iterable[ShowingDTO]: Showings with lower or equal age restriction.
        """

    @abstractmethod
    async def add_showing(self, data: ShowingBroker) -> Showing | None:
        """The abstract adding new showing to the data storage.

        Args:
            data (ShowingBroker): The details of the new showing.

        Returns:
            Showing | None: Full details of the newly added showing.
        """


    @abstractmethod
    async def update_showing(
        self,
        showing_id: int,
        data: ShowingBroker,
    ) -> Showing | None:
        """The abstract updating showing data in the data storage.

        Args:
            showing_id (int): The id of the showing.
            data (ShowingBroker): The details of the updated showing.

        Returns:
            Showing | None: The updated showing details.
        """

    @abstractmethod
    async def delete_showing(self, showing_id: int) -> bool:
        """The abstract removing showing from the data storage.

        Args:
            showing_id (int): The id of the showing.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def validate_showing(self, data: ShowingBroker) -> str | None:
        """The abstract responsible for validating data.

        Args:
            data (ShowingBroker): The data of the showing.

        Returns:
            str | None: Validation status.
        """