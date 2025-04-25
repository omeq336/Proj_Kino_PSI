"""Module containing review repository abstractions."""

from abc import ABC, abstractmethod
from typing import Any, Iterable

from pydantic import UUID4

from cinemaapi.core.domain.review import ReviewIn, ReviewBroker


class IReviewRepository(ABC):
    """An abstract class representing protocol of ireview repository."""

    @abstractmethod
    async def get_all_reviews(self) -> Iterable[Any]:
        """The abstract getting all reviews from the data storage.

        Returns:
            Iterable[Any]: Reviews in the data storage.
        """

    @abstractmethod
    async def get_by_movie_id(self, movie_id: int) -> Iterable[Any]:
        """The abstract getting reviews assigned to movie.

        Args:
            movie_id(int): The id of the movie.

        Returns:
            Iterable[Any]: Reviews related to a movie.
        """

    @abstractmethod
    async def get_by_movie_title(self, title: str) -> Iterable[Any]:
        """The method getting reviews assigned to movie with provided title.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[Any]: Reviews assigned to a movie.
        """

    @abstractmethod
    async def get_by_id(self, review_id: int) -> Any | None:
        """The abstract getting review by id.

        Args:
            review_id (int): The id of the review.

        Returns:
            Any | None: The review details.
        """

    @abstractmethod
    async def get_by_date(self, title: str, date: str) -> Iterable[Any]:
        """The abstract getting reviews by provided date and title.

        Args:
            title (str): The title of the movie
            date (str): The date of the comment.

        Returns:
            Any | None: The movie details.
        """

    @abstractmethod
    async def get_by_rating(self, title: str, rating: int) -> Iterable[Any]:
        """The abstract getting reviews by provided rating and title.

        Args:
            title (str): Title of the movie.
            rating (int): Rating of the review.

        Returns:
            Any | None: The review details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID4) -> Iterable[Any]:
        """The abstract getting all reviews from user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            Any | None: The review details.
        """

    @abstractmethod
    async def add_review(self, data: ReviewBroker) -> Any | None:
        """The abstract adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Any | None: The newly added review.
        """

    @abstractmethod
    async def update_review(
        self,
        review_id: int,
        data: ReviewBroker,
    ) -> Any | None:
        """The abstract updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewIn): The details of the updated review.

        Returns:
            Any | None: The updated review details.
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The abstract removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """