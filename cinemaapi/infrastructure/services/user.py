"""A module containing user service."""
from typing import Iterable

from pydantic import UUID4, UUID5

from cinemaapi.core.domain.user import UserIn
from cinemaapi.core.repositories.iuser import IUserRepository
from cinemaapi.infrastructure.dto.userdto import UserDTO
from cinemaapi.infrastructure.dto.tokendto import TokenDTO
from cinemaapi.infrastructure.services.iuser import IUserService
from cinemaapi.infrastructure.utils.password import verify_password
from cinemaapi.infrastructure.utils.token import generate_user_token


class UserService(IUserService):
    """An abstract class for user service."""

    _repository: IUserRepository

    def __init__(self, repository: IUserRepository) -> None:
        self._repository = repository

    async def register_user(self, user: UserIn, authorization_code: str) -> UserDTO | None:
        """A method registering a new user.

        Args:
            user (UserIn): The user input data.
            authorization_code (str): The user's authorization code.

        Returns:
            UserDTO | None: The user DTO model.
        """

        return await self._repository.register_user(user, authorization_code)

    async def register_admin(self, user: UserIn) -> UserDTO | None:
        """A method registering a new user with admin privileges.

        Args:
            user (UserIn): The user input data.

        Returns:
            UserDTO | None: The user DTO model.
        """

        return await self._repository.register_admin(user)

    async def authenticate_user(self, user: UserIn) -> TokenDTO | None:
        """The method authenticating the user.

        Args:
            user (UserIn): The user data.

        Returns:
            TokenDTO | None: The token details.
        """

        if user_data := await self._repository.get_by_email(user.email):
            if verify_password(user.password, user_data.password):
                token_details = generate_user_token(user_data.id, user_data.privilege)
                # trunk-ignore(bandit/B106)
                return TokenDTO(token_type="Bearer", **token_details)

            return None

        return None

    async def get_by_uuid(self, uuid: UUID4) -> UserDTO | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID5): The UUID of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self._repository.get_by_uuid(uuid)

    async def get_by_email(self, email: str) -> UserDTO | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            UserDTO | None: The user data, if found.
        """

        return await self.get_by_email(email)

    async def view_recommended_movies(self, uuid: UUID4) -> Iterable[dict]:
        """The method getting movie recommendations for user.

        Args:
            uuid(UUID4): The id of the user.

        Returns:
            Iterable[Any]: Movie recommendation details.
        """

        return await self._repository.view_recommended_movies(uuid)

    async def view_recommended_genre(self, uuid: UUID4) -> dict | None:
        """The method getting genre recommendation for user by uuid.

        Args:
            uuid (UUID4): The id of the user.

        Returns:
            dict | None: The genre details.
        """

        return await self._repository.view_recommended_genre(uuid)

    async def validate_user(self, uuid: UUID4) -> str | None:
        """The method responsible for validating data.

        Args:
            uuid (UUID4): The id of the user.

        Returns:
            str | None: Validation status.
        """

        if await self._repository.view_recommended_genre(uuid) is None:
            return "user-genre-not-found"

        return None
