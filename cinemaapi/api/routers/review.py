from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from cinemaapi.container import Container
from cinemaapi.core.domain.review import Review, ReviewIn, ReviewBroker
from cinemaapi.infrastructure.dto.reviewdto import ReviewDTO
from cinemaapi.infrastructure.services.ireview import IReviewService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from cinemaapi.infrastructure.utils import consts
from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/all", response_model=Iterable[ReviewDTO], status_code=200)
@inject
async def get_all_reviews(
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting all reviews.

    Args:
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review attributes collection.
    """

    reviews = await service.get_all()

    return reviews

@router.get(
        "/movie_id/{movie_id}",
        response_model=Iterable[Review],
        status_code=200,
)
@inject
async def get_reviews_by_movie_id(
    movie_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting reviews by movie id.

    Args:
        movie_id (int): The id of the movie.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """

    reviews = await service.get_by_movie_id(movie_id)

    return reviews

@router.get(
        "/movie_title/{title}",
        response_model=Iterable[Review],
        status_code=200,
)
@inject
async def get_reviews_by_movie_title(
    title: str,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting reviews by movie title.

    Args:
        title (str): The title of the movie.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """

    reviews = await service.get_by_movie_title(title)

    return reviews


@router.get("/{review_id}",response_model=ReviewDTO,status_code=200)
@inject
async def get_review_by_id(
    review_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> dict | None:
    """An endpoint for getting review by id.

    Args:
        review_id (int): The id of the review.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        dict | None: The review details.
    """

    if review := await service.get_by_id(review_id=review_id):
        return review.model_dump()

    raise HTTPException(status_code=404, detail="Review not found")


@router.get(
    "/movie_title/{title}/review_date/{date}",
    response_model=Iterable[Review],
    status_code=200
)
@inject
async def get_by_date_in_movie(title: str,
                               date: str,
                               service: IReviewService = Depends(Provide[Container.review_service])) -> Iterable:
    """An endpoint for getting reviews by title and date.

    Args:
        title (str): The title of the movie.
        date (str): The date of the review.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """
    reviews = await service.get_by_date(title,date)
    return reviews

@router.get(
    "/movie_title/{title}/review_rating/{rating}",
    response_model=Iterable[Review],
    status_code=200
)
@inject
async def get_reviews_by_rating_in_movie(title: str,
                                rating: int,
                               service: IReviewService = Depends(Provide[Container.review_service])
                               ) -> Iterable:
    """An endpoint for getting reviews by movie title and review rating.

    Args:
        title (str): The title of the movie.
        rating (int): The rating of the reviews.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """
    reviews = await service.get_by_rating(title, rating)
    return reviews

@router.get("/user_id/{user_id}",response_model=Iterable[ReviewDTO],status_code=200)
@inject
async def get_review_by_user(
    user_id: str,
    service: IReviewService = Depends(Provide[Container.review_service]),
) -> Iterable:
    """An endpoint for getting reviews by user who added them.

    Args:
        user_id (UUID4): The id of the user.
        service (IReviewService, optional): The injected service dependency.

    Returns:
        Iterable: The review details collection.
    """

    try:
        UUID4(user_id)
    except:
        raise HTTPException(status_code=400, detail="Given user_id is invalid.")

    reviews = await service.get_by_user(UUID4(user_id))
    return reviews

@router.post("/create", response_model=Review, status_code=201)
@inject
async def create_review(
    review: ReviewIn,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new review.

    Args:
        review (ReviewIn): The review data.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.
        
    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The new review attributes.

    Requires:
        User privileges or above.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    extended_review_data = ReviewBroker(
        user_id=user_uuid,
        **review.model_dump(),
    )

    match await service.validate_review(extended_review_data):
        case "review-exists":
            raise HTTPException(status_code=400, detail="You have already reviewed this movie!")
        case "review-rating-invalid":
            raise HTTPException(status_code=400, detail="Given rating is invalid. Valid range is: 1-5")
        case "review-date-invalid":
            raise HTTPException(status_code=400, detail="Given date is invalid. Valid syntax is: Year-Month-Day")

    new_review = await service.add_review(extended_review_data)

    return new_review.model_dump() if new_review else {}


@router.put("/{review_id}", response_model=Review, status_code=201)
@inject
async def update_review(
    review_id: int,
    updated_review: ReviewIn,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating review data.

    Args:
        review_id (int): The id of the review.
        updated_review (ReviewIn): The updated review details.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if review does not exist.

    Returns:
        dict: The updated review details.

    Requires:
        User privileges or above.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")
    user_role = token_payload.get("role")

    if review_data := await service.get_by_id(review_id):
        if str(review_data.user_id) != user_uuid and user_role not in AVAILABLE_ROLES[1:3]:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_review_data = ReviewBroker(
            user_id=user_uuid,
            **updated_review.model_dump(),
        )

        match await service.validate_review(extended_review_data):
            case "review-rating-invalid":
                raise HTTPException(status_code=400, detail="Given rating is invalid. Valid range is: 1-5")
            case "review-date-invalid":
                raise HTTPException(status_code=400, detail="Given date is invalid. Valid syntax is: Year-Month-Day")

        updated_review_data = await service.update_review(
            review_id=review_id,
            data=extended_review_data,
        )
        return updated_review_data.model_dump() if updated_review_data \
            else {}

    raise HTTPException(status_code=404, detail="Review not found")


@router.delete("/{review_id}", status_code=204)
@inject
async def delete_review(
    review_id: int,
    service: IReviewService = Depends(Provide[Container.review_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting reviews.

    Args:
        review_id (int): The id of the review.
        service (IReviewService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if review does not exist.

    Requires:
        Admin privileges or above.
    """

    token = credentials.credentials
    token_payload = jwt.decode(
        token,
        key=consts.SECRET_KEY,
        algorithms=[consts.ALGORITHM],
    )
    user_uuid = token_payload.get("sub")
    user_role = token_payload.get("role")

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")
    if user_role not in AVAILABLE_ROLES[1:3]:
        raise HTTPException(status_code=403, detail="Unauthorized, not enough privileges")

    if await service.get_by_id(review_id=review_id):
        await service.delete_review(review_id)
        return

    raise HTTPException(status_code=404, detail="Review not found")