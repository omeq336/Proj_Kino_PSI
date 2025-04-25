"""A module containing movie endpoints."""

from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from cinemaapi.container import Container
from cinemaapi.core.domain.movie import Movie, MovieIn, MovieBroker
from cinemaapi.infrastructure.dto.moviedto import MovieDTO
from cinemaapi.infrastructure.services.imovie import IMovieService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from cinemaapi.infrastructure.utils import consts
from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/all", response_model=Iterable[Movie], status_code=200)
@inject
async def get_all_movies(
    service: IMovieService = Depends(Provide[Container.movie_service]),
) -> Iterable:
    """An endpoint for getting all movies.

    Args:
        service (IMovieService, optional): The injected service dependency.

    Returns:
        Iterable: The movie attributes collection.
    """

    movies = await service.get_all()

    return movies

@router.get(
        "/{movie_id}", response_model=MovieDTO, status_code=200,)
@inject
async def get_movie_by_id(
    movie_id: int,
    service: IMovieService = Depends(Provide[Container.movie_service]),
) -> dict | None:
    """An endpoint for getting movie by id.

    Args:
        movie_id (int): The id of the movie.
        service (IMovieService, optional): The injected service dependency.

    Returns:
        dict | None: The movie details.
    """

    if movie := await service.get_by_id(movie_id=movie_id):
        return movie.model_dump()

    raise HTTPException(status_code=404, detail="Movie not found")

@router.get(
        "/title/{title}", response_model=Movie, status_code=200,)
@inject
async def get_movie_by_title(
    title: str,
    service: IMovieService = Depends(Provide[Container.movie_service]),
) -> dict | None:
    """An endpoint for getting movie by title.

    Args:
        title (str): The title of the movie.
        service (IMovieService, optional): The injected service dependency.

    Returns:
        dict | None: The movie details.
    """

    if movie := await service.get_by_title(title):
        return movie.model_dump()

    raise HTTPException(status_code=404, detail="Movie not found")


@router.get(
        "/genre/{genre}", response_model=Iterable[MovieDTO], status_code=200,)
@inject
async def get_movie_by_genre(
    genre: str,
    service: IMovieService = Depends(Provide[Container.movie_service]),
) -> Iterable:
    """An endpoint for getting movies by genre.

    Args:
        genre (str): The genre of the movie.
        service (IMovieService, optional): The injected service dependency.

    Returns:
        Iterable: The movie details collection.
    """

    movies = await service.get_by_genre(genre)

    return movies

@router.get(
        "/age_restriction/{age}", response_model=Iterable[MovieDTO], status_code=200,)
@inject
async def get_movie_by_age_restriction(
    age: int,
    service: IMovieService = Depends(Provide[Container.movie_service]),
) -> Iterable:
    """An endpoint for getting movies with below or equal age restriction.

    Args:
        age (int): The age restriction of the movie.
        service (IMovieService, optional): The injected service dependency.

    Returns:
        Iterable: The movie details collection.
    """

    movies = await service.get_by_age_restriction(age)

    return movies


@router.get(
        "/rating/{rating}", response_model=Iterable[MovieDTO], status_code=200,)
@inject
async def get_movie_by_rating(
    rating: int,
    service: IMovieService = Depends(Provide[Container.movie_service]),
) -> Iterable:
    """An endpoint for getting movies with higher or equal rating.

    Args:
        rating (int): The rating of the movie.
        service (IMovieService, optional): The injected service dependency.

    Returns:
        Iterable: The movie details collection.
    """

    movies = await service.get_by_rating(rating)

    return movies

@router.post("/create", response_model=Movie, status_code=201)
@inject
async def create_movie(
    movie: MovieIn,
    service: IMovieService = Depends(Provide[Container.movie_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new movie.

    Args:
        movie (MovieIn): The movie data.
        service (IMovieService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The new movie attributes.

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

    extended_movie_data = MovieBroker(
        user_id=user_uuid,
        **movie.model_dump(),
    )

    match await service.validate_movie(extended_movie_data):
        case "movie-title-occupied":
            raise HTTPException(status_code=400, detail="Movie of that title already exists!")
        case "movie-age_restriction-invalid":
            raise HTTPException(status_code=400, detail="Given age restriction is invalid")
        case "movie-duration-invalid":
            raise HTTPException(status_code=400, detail="Given duration is invalid")

    new_movie = await service.add_movie(extended_movie_data)

    return new_movie.model_dump() if new_movie else {}

@router.put("/{movie_id}", response_model=Movie, status_code=201)
@inject
async def update_movie(
    movie_id: int,
    updated_movie: MovieIn,
    service: IMovieService = Depends(Provide[Container.movie_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating movie data.

    Args:
        movie_id (int): The id of the movie.
        updated_movie (MovieIn): The updated movie details.
        service (IMovieService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if movie does not exist.

    Returns:
        dict: The updated movie details.

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

    if movie_data := await service.get_by_id(movie_id):
        extended_updated_movie = MovieBroker(
            user_id=user_uuid,
            **updated_movie.model_dump(),
        )

        match await service.validate_movie(extended_updated_movie):
            case "movie-age_restriction-invalid":
                raise HTTPException(status_code=400, detail="Given age restriction is invalid")
            case "movie-duration-invalid":
                raise HTTPException(status_code=400, detail="Given duration is invalid")

        updated_movie_data = await service.update_movie(
            movie_id=movie_id,
            data=extended_updated_movie,
        )

        return updated_movie_data.model_dump() if updated_movie_data \
            else {}

    raise HTTPException(status_code=404, detail="Movie not found")


@router.delete("/{movie_id}", status_code=204)
@inject
async def delete_movie(
    movie_id: int,
    service: IMovieService = Depends(Provide[Container.movie_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)

) -> None:
    """An endpoint for deleting movies.

    Args:
        movie_id (int): The id of the movie.
        service (IMovieService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if movie does not exist.

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

    if await service.get_by_id(movie_id=movie_id):
        await service.delete_movie(movie_id)
        return

    raise HTTPException(status_code=404, detail="Movie not found")