"""A module containing user service."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID5, UUID4

from cinemaapi.core.domain.user import UserIn
from cinemaapi.infrastructure.dto.userdto import UserDTO
from cinemaapi.infrastructure.dto.tokendto import TokenDTO


class IUserService(ABC):
    """An abstract class for user service."""

    @abstractmethod
    async def register_user(self, user: UserIn, authorization_code: str) -> UserDTO | None:
        """The abstract registering a new user.

        Args:
            user (UserIn): The user input data.
            authorization_code (str): The user's authorization code.

        Returns:
            UserDTO | None: The user DTO model.
        """

    @abstractmethod
    async def register_admin(self, user: UserIn) -> UserDTO | None:
        """The abstract registering a new user with admin privileges.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

    @abstractmethod
    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The abstract authenticating the user.

        Args:
            user (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

    @abstractmethod
    async def get_by_uuid(self, uuid: UUID5) -> UserDTO | None:
        """The abstract getting user by UUID.

        Args:
            uuid (UUID5): The UUID of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def get_by_email(self, email: str) -> UserDTO | None:
        """The abstract getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

    @abstractmethod
    async def view_recommended_movies(self, uuid: UUID4) -> Iterable[dict]:
        """The abstract getting movie recommendations for user.

        Args:
            uuid(UUID4): The id of the user.

        Returns:
            Iterable[Any]: Movie recommendation details.
        """

    @abstractmethod
    async def view_recommended_genre(self, uuid: UUID4) -> dict | None:
        """The abstract getting genre recommendation for user by uuid.

        Args:
            uuid (UUID4): The id of the user.

        Returns:
            dict | None: The genre details.
        """

    async def validate_user(self, uuid: UUID4) -> str | None:
        """The abstract responsible for validating data.

        Args:
            uuid (UUID4): The id of the user.

        Returns:
            str | None: Validation status.
        """