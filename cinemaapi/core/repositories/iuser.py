"""A repository for user entity."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID5, UUID4

from cinemaapi.core.domain.user import UserIn


class IUserRepository(ABC):
    """An abstract repository class for user."""

    @abstractmethod
    async def register_user(self, user: UserIn, authorization_code: str) -> Any | None:
        """A method registering new user.

        Args:
            user (UserIn): The user input data.
            authorization_code (str): The user's authorization_code

        Returns:
            Any | None: The new user object.
        """

    @abstractmethod
    async def register_admin(self, user: UserIn) -> Any | None:
        """A method registering new admin.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID5) -> Any | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID5): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

    @abstractmethod
    async def view_recommended_movies(self, uuid: UUID4) -> Iterable[Any]:
        """The abstract getting movie recommendations to user.

        Args:
            uuid(UUID4): The id of the user.

        Returns:
            Iterable[Any]: Recommended movies.
        """

    @abstractmethod
    async def view_recommended_genre(self, uuid: UUID4) -> Any | None:
        """The abstract getting genre recommendation to user.

        Args:
            uuid(UUID4): The id of the user.

        Returns:
            Any | None: Recommended genre.
        """