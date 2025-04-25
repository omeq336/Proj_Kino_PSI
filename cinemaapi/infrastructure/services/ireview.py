"""Module containing review service abstractions."""

from abc import ABC, abstractmethod
from typing import Iterable

from pydantic import UUID4

from cinemaapi.core.domain.review import Review, ReviewBroker
from cinemaapi.infrastructure.dto.reviewdto import ReviewDTO


class IReviewService(ABC):
    """A class representing review repository."""

    @abstractmethod
    async def get_all(self) -> Iterable[ReviewDTO]:
        """The abstract getting all reviews from the repository.

        Returns:
            Iterable[ReviewDTO]: All reviews.
        """

    @abstractmethod
    async def get_by_movie_id(self, movie_id: int) -> Iterable[Review]:
        """The abstract getting reviews by provided movie id from repository.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            Iterable[Review]: Reviews details.
        """

    @abstractmethod
    async def get_by_movie_title(self, title: str) -> Iterable[Review]:
        """The abstract getting reviews by provided movie title from repository.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[Review]: Reviews details.
        """

    @abstractmethod
    async def get_by_id(self, review_id: int) -> ReviewDTO | None:
        """The abstract getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            ReviewDTO | None: The review details.
        """

    @abstractmethod
    async def get_by_date(self, title: str, date: str) -> Iterable[Review]:
        """The abstract getting reviews by provided movie title and review date.

        Args:
            title (str): The title of the movie
            date (str): The date of the comment.

        Returns:
            Iterable[Review]: Reviews details.
        """

    @abstractmethod
    async def get_by_rating(self, title: str, rating: int) -> Iterable[Review]:
        """The abstract getting reviews by provided movie title and review rating.

        Args:
            title (str): The title of the movie
            rating (int): Rating of the review.

        Returns:
            Iterable[Review]: Reviews details.
        """

    @abstractmethod
    async def get_by_user(self, user_id: UUID4) -> Iterable[ReviewDTO]:
        """The abstract getting all reviews from user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            Iterable[ReviewDTO]: Reviews details.
        """

    @abstractmethod
    async def add_review(self, data: ReviewBroker) -> Review | None:
        """The abstract adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Review | None: Full details of the newly added review.
        """

    @abstractmethod
    async def update_review(
        self,
        review_id: int,
        data: ReviewBroker,
    ) -> Review | None:
        """The abstract updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewBroker): The details of the updated review.

        Returns:
            Review | None: The updated review details.
        """

    @abstractmethod
    async def delete_review(self, review_id: int) -> bool:
        """The abstract removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """

    @abstractmethod
    async def validate_review(self, data: ReviewBroker) -> str | None:
        """The abstract responsible for validating data.

        Args:
            data (ReviewBroker): The data of the review.

        Returns:
            str | None: Validation status.
        """