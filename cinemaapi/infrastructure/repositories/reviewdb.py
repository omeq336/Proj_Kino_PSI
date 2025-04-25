"""Module containing review repository implementation."""

from typing import Any, Iterable

from asyncpg import Record
from pydantic import UUID4
from sqlalchemy import select, join, func
from datetime import date

from cinemaapi.core.domain.review import Review, ReviewBroker
from cinemaapi.core.repositories.ireview import IReviewRepository
from cinemaapi.db import (
    review_table,
    movie_table,
    database
)
from cinemaapi.infrastructure.dto.reviewdto import ReviewDTO


class ReviewRepository(IReviewRepository):
    """A class representing review DB repository."""

    async def get_all_reviews(self) -> Iterable[Any]:
        """The method getting all reviews from the data storage.

        Returns:
            Iterable[Any]: Reviews in the data storage.
        """

        query = (
            select(review_table, movie_table)
            .select_from(
                join(
                    review_table,
                    movie_table,
                    review_table.c.movie_id == movie_table.c.id
                )
            )
            .order_by(review_table.c.id.asc())
        )
        reviews = await database.fetch_all(query)

        return [ReviewDTO.from_record(review) for review in reviews]

    async def get_by_movie_id(self, movie_id: int) -> Iterable[Any]:
        """The method getting reviews assigned to particular movie.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            Iterable[Any]: Reviews assigned to a movie.
        """

        query = review_table.select().where(review_table.c.movie_id == movie_id).order_by(review_table.c.id.asc())
        reviews = await database.fetch_all(query)

        return [Review(**dict(review)) for review in reviews]

    async def get_by_movie_title(self, title: str) -> Iterable[Any]:
        """The method getting reviews assigned to movie with particular title.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[Any]: Reviews assigned to a movie.
        """

        query = (
            select(review_table, movie_table)
            .select_from(
                join(
                    review_table,
                    movie_table,
                    review_table.c.movie_id == movie_table.c.id
                )
            )
            .where(movie_table.c.title == title)
            .order_by(review_table.c.id.asc())
        )
        reviews = await database.fetch_all(query)

        return [Review(**dict(review)) for review in reviews]


    async def get_by_id(self, review_id: int) -> Any | None:
        """The method getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            Any | None: The review details.
        """

        query = (
            select(review_table, movie_table)
            .select_from(
                join(
                    review_table,
                    movie_table,
                    review_table.c.movie_id == movie_table.c.id
                )
            )
            .where(review_table.c.id == review_id)
            .order_by(review_table.c.id.asc())
        )

        review = await database.fetch_one(query)

        return ReviewDTO.from_record(review) if review else None

    async def get_by_date(self, title: str, date: str) -> Iterable[Any]:
        """The method getting reviews by provided date and title.

        Args:
            title (str): The title of the movie
            date (str): The date of the comment.

        Returns:
            Iterable[Any]: Reviews assigned to a movie.
        """

        query = (
            select(review_table, movie_table)
            .select_from(
                join(
                    review_table,
                    movie_table,
                    review_table.c.movie_id == movie_table.c.id
                )
            )
            .where(
                    movie_table.c.title == title,
                    review_table.c.date == date
            )
            .order_by(review_table.c.id.asc())
        )
        reviews = await database.fetch_all(query)

        return [Review(**dict(review)) for review in reviews]

    async def get_by_rating(self, title: str, rating: int) -> Iterable[Any]:
        """The method getting all reviews with the specified rating and movie title.

        Args:
            title (str): The title of the movie
            rating (int): Rating of the review.

        Returns:
            Iterable[Any]: The review details.
        """

        query = (
            select(review_table, movie_table)
            .select_from(
                join(
                    review_table,
                    movie_table,
                    review_table.c.movie_id == movie_table.c.id
                )
            )
            .where(
        movie_table.c.title == title,
                    review_table.c.rating == rating
            )
            .order_by(review_table.c.id.asc())
        )
        reviews = await database.fetch_all(query)

        return [Review(**dict(review)) for review in reviews]

    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The method getting all reviews from the user.

        Args:
            user_id (UUID4): The id of the user

        Returns:
            Iterable[Any]: Reviews assigned to user.
        """

        query = (
            select(review_table, movie_table)
            .select_from(
                join(
                    review_table,
                    movie_table,
                    review_table.c.movie_id == movie_table.c.id
                )
            )
            .where(
                    review_table.c.user_id == user_id
            )
            .order_by(review_table.c.id.asc())
        )
        reviews = await database.fetch_all(query)

        return [ReviewDTO.from_record(review) for review in reviews]

    async def add_review(self, data: ReviewBroker) -> Any | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Review: Full details of the newly added review.

        Returns:
            Any | None: The newly added review.
        """

        query = review_table.insert().values(**data.model_dump())
        new_review_id = await database.execute(query)
        new_review = await self._get_by_id(new_review_id)

        await self._update_movie_rating(data.movie_id)  #  movie rating update after new review is added

        return Review(**dict(new_review)) if new_review else None

    async def update_review(
            self,
            review_id: int,
            data: ReviewBroker,
    ) -> Any | None:
        """The method updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewBroker): The details of the updated review.

        Returns:
            Any | None: The updated review details.
        """

        if self._get_by_id(review_id):
            query = (
                review_table.update()
                .where(review_table.c.id == review_id)
                .values(
                    rating=data.rating,
                    comment=data.comment,
                    date=str(date.today())
                )
            )
            await database.execute(query)

            review = await self._get_by_id(review_id)

            fetched_movie_id = await self._fetch_movie_id(review_id)
            await self._update_movie_rating(fetched_movie_id) #  movie rating update after review is updated

            return Review(**dict(review)) if review else None

        return None

    async def delete_review(self, review_id: int) -> bool:
        """The method removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """

        if self._get_by_id(review_id):

            fetched_movie_id = await self._fetch_movie_id(review_id)
            query = review_table \
                .delete() \
                .where(review_table.c.id == review_id)
            await database.execute(query)

            await self._update_movie_rating(fetched_movie_id) #  movie rating update after review is updated

            return True

        return False

    async def _get_by_id(self, review_id: int) -> Record | None:
        """A private method getting review from the DB based on its ID.

        Args:
            review_id (int): The ID of the review.

        Returns:
            Record | None: Review record if exists.
        """

        query = (
            review_table.select()
            .where(review_table.c.id == review_id)
            .order_by(review_table.c.id.asc())
        )

        return await database.fetch_one(query)

    async def _fetch_avg_review_rating(self, movie_id: int) -> float | None:
        """A private method getting average review rating for a movie from the DB based on movie id.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            float | None: Average movie rating if exists.
        """

        query = (
            select(func.avg(review_table.c.rating))
            .select_from(
                join(
                    review_table,
                    movie_table,
                    review_table.c.movie_id == movie_table.c.id
                )
            )
            .where(movie_table.c.id == movie_id)
        )

        avg_rating = await database.fetch_one(query)

        if avg_rating[0] is None:
            return 0
        return float(avg_rating[0])

    async def _update_movie_rating(self, movie_id: int) -> None:
        """A private method updating movie rating.

        Args:
            movie_id (int): The ID of the movie.

        Returns:
            None.
        """

        query = (
            movie_table.update()
            .where(movie_table.c.id == movie_id)
            .values(rating = await self._fetch_avg_review_rating(movie_id))
        )
        await database.execute(query)

    async def _fetch_movie_id(self, review_id: int) -> int | None:
        """A private method getting movie id from the DB based on its id of the review.

        Args:
            review_id (int): The ID of the review.

        Returns:
            int | None: Movie id if exists.
        """

        query = (
            select(review_table.c.movie_id)
            .where(review_table.c.id == review_id)
        )

        fetched_movie_id = await database.fetch_one(query)
        return int(fetched_movie_id[0])
