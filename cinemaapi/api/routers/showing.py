from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from cinemaapi.container import Container
from cinemaapi.core.domain.showing import Showing, ShowingIn, ShowingBroker
from cinemaapi.infrastructure.dto.showingdto import ShowingDTO
from cinemaapi.infrastructure.services.ishowing import IShowingService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from cinemaapi.infrastructure.utils import consts
from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/all", response_model=Iterable[ShowingDTO], status_code=200)
@inject
async def get_all_showings(
    service: IShowingService = Depends(Provide[Container.showing_service]),
) -> Iterable:
    """An endpoint for getting all showings.

    Args:
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing attributes collection.
    """

    showings = await service.get_all()

    return showings


@router.get("/{showing_id}",response_model=ShowingDTO,status_code=200)
@inject
async def get_showing_by_id(
    showing_id: int,
    service: IShowingService = Depends(Provide[Container.showing_service]),
) -> dict | None:
    """An endpoint for getting showing by id.

    Args:
        showing_id (int): The id of the showing.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        dict | None: The showing details.
    """

    if showing := await service.get_by_id(showing_id=showing_id):
        return showing.model_dump()

    raise HTTPException(status_code=404, detail="Showing not found")

@router.get(
        "/repertoire/repertoire_id/{repertoire_id}",
        response_model=Iterable[ShowingDTO],
        status_code=200,
)
@inject
async def get_showings_by_repertoire(
    repertoire_id: int,
    service: IShowingService = Depends(Provide[Container.showing_service]),
) -> Iterable:
    """An endpoint for getting showings by repertoire.

    Args:
        repertoire_id (int): The id of the repertoire.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    showings = await service.get_by_repertoire(repertoire_id)

    return showings

@router.get(
    "/showing_date/{showing_date}",
    response_model=Iterable[ShowingDTO],
    status_code=200
)
@inject
async def get_showings_by_date(showing_date: str,
                              service: IShowingService = Depends(Provide[Container.showing_service])
                              ) -> Iterable:
    """An endpoint for getting showings by date.

    Args:
        showing_date (str): The date of the showing.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    showings = await service.get_showings_by_date(showing_date)
    return showings

@router.get(
    "/showing_time/{showing_time}",
    response_model=Iterable[ShowingDTO],
    status_code=200
)
@inject
async def get_showings_by_time(showing_time: str,
                               service: IShowingService = Depends(Provide[Container.showing_service])
                               ) -> Iterable:
    """An endpoint for getting showings with time equal to showing_time or above.

    Args:
        showing_time (str): The time of the showing.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    showings = await service.get_showings_by_time(showing_time)
    return showings

@router.get(
    "/language_version/{language_ver}",
    response_model=Iterable[ShowingDTO],
    status_code=200
)
@inject
async def get_showings_by_language_ver(language_ver: str,
                                       service: IShowingService = Depends(Provide[Container.showing_service])
                                       ) -> Iterable:
    """An endpoint for getting showings by language version.

    Args:
        language_ver (str): The language version of the showing.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    showings = await service.get_showings_by_language_ver(language_ver)
    return showings

@router.get(
    "/movie/genre/{genre}",
    response_model=Iterable[ShowingDTO],
    status_code=200
)
@inject
async def get_showings_by_movie_genre(genre: str,
                                      service: IShowingService = Depends(Provide[Container.showing_service])
                                      ) -> Iterable:
    """An endpoint for getting showings by movie genre.

    Args:
        genre (str): The genre of the movie.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    showings = await service.get_showings_by_movie_genre(genre)
    return showings

@router.get("/movie/title/{title}",response_model=Iterable[ShowingDTO],status_code=200)
@inject
async def get_showing_by_movie_title(
    title: str,
    service: IShowingService = Depends(Provide[Container.showing_service]),
) -> Iterable:
    """An endpoint for getting showings by movie title.

    Args:
        title (str): The title of the movie.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    showings = await service.get_showing_by_movie_title(title)
    return showings

@router.get(
    "/movie/age_restriction/{age_restriction}",
    response_model=Iterable[ShowingDTO],
    status_code=200
)
@inject
async def get_showings_by_age_restriction(age_restriction: int,
                               service: IShowingService = Depends(Provide[Container.showing_service])
                               ) -> Iterable:
    """An endpoint for getting showings that are equal or below given age restriction.

    Args:
        age_restriction (int): The age restriction of the movie.
        service (IShowingService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    showings = await service.get_showings_by_age_restriction(age_restriction)
    return showings

@router.post("/create", response_model=Showing, status_code=201)
@inject
async def create_showing(
    showing: ShowingIn,
    service: IShowingService = Depends(Provide[Container.showing_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new showing.

    Args:
        showing (ShowingIn): The showing data.
        service (IShowingService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The new showing attributes.

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

    extended_showing_data = ShowingBroker(
        user_id=user_uuid,
        **showing.model_dump(),
    )

    match await service.validate_showing(extended_showing_data):
        case "showing-language_version-invalid":
            raise HTTPException(status_code=400, detail="Given language version is invalid.")
        case "showing-price-invalid":
            raise HTTPException(status_code=400, detail="Given price is invalid.")
        case "showing-time-invalid":
            raise HTTPException(status_code=400, detail="Given time is invalid. Valid syntax is: hour:minute.")
        case "showing-date-invalid":
            raise HTTPException(status_code=400, detail="Given date is invalid. Valid syntax is: year-month-day.")
        case "showing-hall-occupied":
            raise HTTPException(status_code=400, detail="At this time the hall is already occupied.")

    new_showing = await service.add_showing(extended_showing_data)

    return new_showing.model_dump() if new_showing else {}


@router.put("/{showing_id}", response_model=Showing, status_code=201)
@inject
async def update_showing(
    showing_id: int,
    updated_showing: ShowingIn,
    service: IShowingService = Depends(Provide[Container.showing_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating showing data.

    Args:
        showing_id (int): The id of the showing.
        updated_showing (ShowingIn): The updated showing details.
        service (IShowingService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if showing does not exist.

    Returns:
        dict: The updated showing details.

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

    if showing_data := await service.get_by_id(showing_id):

        extended_showing_data = ShowingBroker(
            user_id=user_uuid,
            **updated_showing.model_dump(),
        )

        match await service.validate_showing(extended_showing_data):
            case "showing-language_version-invalid":
                raise HTTPException(status_code=400, detail="Given language version is invalid.")
            case "showing-price-invalid":
                raise HTTPException(status_code=400, detail="Given price is invalid.")
            case "showing-time-invalid":
                raise HTTPException(status_code=400, detail="Given time is invalid. Valid syntax is: hour:minute.")
            case "showing-date-invalid":
                raise HTTPException(status_code=400, detail="Given date is invalid. Valid syntax is: year-month-day")
            case "showing-hall-occupied":
                raise HTTPException(status_code=400, detail="At this time the hall is already occupied.")

        updated_showing_data = await service.update_showing(
            showing_id=showing_id,
            data=extended_showing_data,
        )
        return updated_showing_data.model_dump() if updated_showing_data \
            else {}

    raise HTTPException(status_code=404, detail="Showing not found")


@router.delete("/{showing_id}", status_code=204)
@inject
async def delete_showing(
    showing_id: int,
    service: IShowingService = Depends(Provide[Container.showing_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting showings.

    Args:
        showing_id (int): The id of the showing.
        service (IShowingService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if showing does not exist.

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

    if await service.get_by_id(showing_id=showing_id):
        await service.delete_showing(showing_id)
        return

    raise HTTPException(status_code=404, detail="Showing not found")