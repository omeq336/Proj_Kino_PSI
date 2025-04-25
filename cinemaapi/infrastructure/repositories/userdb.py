"""A repository for user entity."""

from typing import Any, Iterable

from sqlalchemy import select, join, func

from pydantic import UUID5, UUID4

from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES
from cinemaapi.infrastructure.utils.password import hash_password
from cinemaapi.core.domain.user import UserIn
from cinemaapi.core.repositories.iuser import IUserRepository
from cinemaapi.db import database, user_table, review_table, movie_table
from cinemaapi.infrastructure.utils.privilege import check_privilege_code


class UserRepository(IUserRepository):
    """An implementation of repository class for user."""

    async def register_user(self, user: UserIn, authorization_code: str) -> Any | None:
        """A method registering new user.

        Args:
            user (UserIn): The user input data.
            authorization_code (Optional[str]): The user's authorization code.

        Returns:
            Any | None: The new user object.
        """

        if await self.get_by_email(user.email):
            return None

        user.password = hash_password(user.password)

        role = check_privilege_code(authorization_code)

        if role and not await self._check_for_super_admin():
            print("Authorized.")
            query = user_table.insert().values(
            email=user.email,
            password=user.password,
            privilege=role
            )
        else:
            print("Provided code is invalid")
            query = user_table.insert().values(
            email=user.email,
            password=user.password,
            privilege=AVAILABLE_ROLES[0]
            )

        new_user_uuid = await database.execute(query)

        return await self.get_by_uuid(new_user_uuid)

    async def register_admin(self, user: UserIn) -> Any | None:
        """A method registering new user with admin privileges.

        Args:
            user (UserIn): The user input data.

        Returns:
            Any | None: The new user object.
        """

        if await self.get_by_email(user.email):
            return None

        user.password = hash_password(user.password)

        query = user_table.insert().values(
        email=user.email,
        password=user.password,
        privilege=AVAILABLE_ROLES[1]
        )

        new_user_uuid = await database.execute(query)

        return await self.get_by_uuid(new_user_uuid)

    async def get_by_uuid(self, uuid: UUID5) -> Any | None:
        """A method getting user by UUID.

        Args:
            uuid (UUID5): UUID of the user.

        Returns:
            Any | None: The user object if exists.
        """

        query = user_table \
            .select() \
            .where(user_table.c.id == uuid)
        user = await database.fetch_one(query)

        return user

    async def get_by_email(self, email: str) -> Any | None:
        """A method getting user by email.

        Args:
            email (str): The email of the user.

        Returns:
            Any | None: The user object if exists.
        """

        query = user_table \
            .select() \
            .where(user_table.c.email == email)
        user = await database.fetch_one(query)

        return user

    async def view_recommended_movies(self, uuid: UUID4) -> Iterable[Any]:
        """The method getting movie recommendations for user.

        Args:
            uuid(UUID4): The id of the user.

        Returns:
            Iterable[Any]: Movie recommendation details.
        """

        subquery = select(review_table.c.movie_id).where(review_table.c.user_id == uuid)
        recommended_genre = await self.view_recommended_genre(uuid)

        query = (
            select(movie_table.c.id, movie_table.c.title, movie_table.c.genre)
            .where(
                movie_table.c.genre == recommended_genre['genre'],
                movie_table.c.id.notin_(subquery)
                   )
            .order_by(movie_table.c.id.asc())
        )

        movies = await database.fetch_all(query)

        return [dict(movie) for movie in movies]

    async def view_recommended_genre(self, uuid: UUID4) -> dict | None:
        """The method getting genre recommendation for user by uuid.

        Args:
            uuid (UUID4): The id of the user.

        Returns:
            dict | None: The genre details.
        """

        query = (
            select(func.avg(review_table.c.rating), movie_table.c.genre)
            .select_from(
                join(
                    movie_table,
                    review_table,
                    movie_table.c.id == review_table.c.movie_id
                ),
            )
            .where(
                review_table.c.user_id == uuid
            )
            .group_by(movie_table.c.genre)
            .order_by(func.avg(review_table.c.rating).desc()).limit(1)
        )

        genre = await database.fetch_one(query)

        if genre is not None:
            return {'genre': genre['genre']}
        else:
            return None

    async def _check_for_super_admin(self) -> bool:
        """The private method searching for super_admin.

        Returns:
            bool: super_admin status.
        """

        query = user_table.select().where(user_table.c.privilege == "super_admin")

        result = await database.fetch_one(query)

        return True if result else False
