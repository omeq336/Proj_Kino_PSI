"""Module containing review service implementation."""
from datetime import datetime
from typing import Iterable

from pydantic import UUID4

from cinemaapi.core.domain.review import Review, ReviewBroker
from cinemaapi.core.repositories.ireview import IReviewRepository
from cinemaapi.infrastructure.dto.reviewdto import ReviewDTO
from cinemaapi.infrastructure.services.ireview import IReviewService


class ReviewService(IReviewService):
    """A class implementing the review service."""

    _repository: IReviewRepository

    def __init__(self, repository: IReviewRepository) -> None:
        """The initializer of the `review service`.

        Args:
            repository (IReviewRepository): The reference to the repository.
        """

        self._repository = repository

    async def get_all(self) -> Iterable[ReviewDTO]:
        """The method getting all reviews from the repository.

        Returns:
            Iterable[ReviewDTO]: All reviews.
        """

        return await self._repository.get_all_reviews()

    async def get_by_movie_id(self, movie_id: int) -> Iterable[Review]:
        """The method getting reviews by provided movie id from repository.

        Args:
            movie_id (int): The id of the movie.

        Returns:
            Iterable[Review]: Reviews details.
        """

        return await self._repository.get_by_movie_id(movie_id)


    async def get_by_movie_title(self, title: str) -> Iterable[Review]:
        """The method getting reviews by provided movie title from repository.

        Args:
            title (str): The title of the movie.

        Returns:
            Iterable[Review]: Reviews details.
        """

        return await self._repository.get_by_movie_title(title)


    async def get_by_id(self, review_id: int) -> ReviewDTO | None:
        """The method getting review by provided id.

        Args:
            review_id (int): The id of the review.

        Returns:
            ReviewDTO | None: The review details.
        """

        return await self._repository.get_by_id(review_id)

    async def get_by_date(self, title: str, date: str) -> Iterable[Review]:
        """The method getting reviews by provided movie title and review date.

          Args:
              title (str): The title of the movie
              date (str): The date of the comment.

          Returns:
              Iterable[Review]: Reviews details.
          """

        return await self._repository.get_by_date(title, date)

    async def get_by_rating(self, title: str, rating: int) -> Iterable[Review]:
        """The method getting reviews by provided movie title and review rating.

        Args:
            title (str): The title of the movie
            rating (int): Rating of the review.

        Returns:
            Iterable[Review]: Reviews details.
        """

        return await self._repository.get_by_rating(title, rating)

    async def get_by_user(self, user_id: UUID4) -> Iterable[ReviewDTO]:
        """The method getting all reviews from user.

        Args:
            user_id (UUID4): ID of the user.

        Returns:
            Iterable[ReviewDTO]: Reviews details.
        """

        return await self._repository.get_by_user(user_id)

    async def add_review(self, data: ReviewBroker) -> Review | None:
        """The method adding new review to the data storage.

        Args:
            data (ReviewBroker): The details of the new review.

        Returns:
            Review | None: Full details of the newly added review.
        """

        return await self._repository.add_review(data)

    async def update_review(
            self,
            review_id: int,
            data: ReviewBroker,
    ) -> Review | None:
        """The method updating review data in the data storage.

        Args:
            review_id (int): The id of the review.
            data (ReviewBroker): The details of the updated review.

        Returns:
            Review | None: The updated review details.
        """

        return await self._repository.update_review(
            review_id=review_id,
            data=data,
        )

    async def delete_review(self, review_id: int) -> bool:
        """The method removing review from the data storage.

        Args:
            review_id (int): The id of the review.

        Returns:
            bool: Success of the operation.
        """
        return await self._repository.delete_review(review_id)

    async def validate_review(self, data: ReviewBroker) -> str | None:
        """The method responsible for validating data.

        Args:
            data (ReviewBroker): The data of the review.

        Returns:
            str | None: Validation status.
        """

        if review_data := await self.get_by_user(data.user_id):
            for rev in review_data:
                if rev.movie.id == data.movie_id:
                    return "review-exists"

        if data.rating < 1 or data.rating > 5:
            return "review-rating-invalid"

        try:
            converted_date = datetime.strptime(data.date, "%Y-%m-%d").date()
        except:
            return "review-date-invalid"

        return None
