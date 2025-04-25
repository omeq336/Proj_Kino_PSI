import string
from typing import Iterable

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from cinemaapi.container import Container
from cinemaapi.core.domain.reservation import Reservation, ReservationIn, ReservationBroker
from cinemaapi.infrastructure.dto.reservationdto import ReservationDTO
from cinemaapi.infrastructure.services.ireservation import IReservationService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from cinemaapi.infrastructure.utils import consts
from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/all", response_model=Iterable[ReservationDTO], status_code=200)
@inject
async def get_all_reservations(
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """An endpoint for getting all reservations.

    Args:
        service (IReservationService, optional): The injected service dependency.

    Returns:
        Iterable: The reservation attributes collection.
    """

    reservations = await service.get_all()

    return reservations

@router.get("/{reservation_id}",response_model=ReservationDTO,status_code=200)
@inject
async def get_reservation_by_id(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> dict | None:
    """An endpoint for getting reservation by id.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.

    Returns:
        dict | None: The reservation details.
    """

    if reservation := await service.get_by_id(reservation_id=reservation_id):
        return reservation.model_dump()

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.get("/movie/title/{title}",response_model=Iterable[Reservation],status_code=200)
@inject
async def get_reservation_by_movie_title(
    title: str,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """An endpoint for getting reservations by movie title.

    Args:
        title (str): The title of the movie.
        service (IReservationService, optional): The injected service dependency.

    Returns:
        Iterable: The reservation details collection.
    """

    reservations = await service.get_by_title(title)
    return reservations

@router.get("/showing/showing_id/{showing_id}",response_model=Iterable[Reservation],status_code=200)
@inject
async def get_reservation_by_showing(
    showing_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """An endpoint for getting reservations by showing id.

    Args:
        showing_id (int): The id of the showing.
        service (IReservationService, optional): The injected service dependency.

    Returns:
        Iterable: The showing details collection.
    """

    reservations = await service.get_by_showing(showing_id)
    return reservations

@router.get("/user_id/{user_id}",response_model=Iterable[ReservationDTO],status_code=200)
@inject
async def get_reservation_by_user(
    user_id: str,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
) -> Iterable:
    """An endpoint for getting reservations by user who added them.

    Args:
        user_id (UUID4): The id of the user.
        service (IReservationService, optional): The injected service dependency.

    Returns:
        Iterable: The reservation details collection.
    """

    try:
        UUID4(user_id)
    except:
        raise HTTPException(status_code=400, detail="Given user_id is invalid.")

    reservations = await service.get_by_user(UUID4(user_id))
    return reservations

@router.post("/create", response_model=Reservation, status_code=201)
@inject
async def create_reservation(
    reservation: ReservationIn,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new reservation.

    Args:
        reservation (ReservationIn): The reservation data.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The new reservation attributes.

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

    extended_reservation_data = ReservationBroker(
        user_id=user_uuid,
        **reservation.model_dump(),
    )

    match await service.validate_reservation(extended_reservation_data):
        case "seat-status-error":
            raise HTTPException(status_code=400, detail="This seat is already taken!")
        case "seat-row-error":
            raise HTTPException(status_code=400, detail="Invalid seat row was given")
        case "seat-num-error":
            raise HTTPException(status_code=400, detail="Invalid seat number was given")

    new_reservation = await service.add_reservation(extended_reservation_data)

    return new_reservation.model_dump() if new_reservation else {}


@router.put("/{reservation_id}", response_model=Reservation, status_code=201)
@inject
async def update_reservation(
    reservation_id: int,
    updated_reservation: ReservationIn,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating reservation data.

    Args:
        reservation_id (int): The id of the reservation.
        updated_reservation(ReservationIn): The updated reservation details.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if reservation does not exist.

    Returns:
        dict: The updated reservation details.

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

    if not user_uuid:
        raise HTTPException(status_code=403, detail="Unauthorized")

    if reservation_data := await service.get_by_id(reservation_id):
        if str(reservation_data.user_id) != user_uuid and user_role not in AVAILABLE_ROLES[1:3]:
            raise HTTPException(status_code=403, detail="Unauthorized")

        extended_reservation_data = ReservationBroker(
            user_id=user_uuid,
            **updated_reservation.model_dump(),
        )

        match await service.validate_reservation(extended_reservation_data):
            case "showing-availability-error":
                raise HTTPException(status_code=400, detail="Invalid showing, it might not exist.")
            case "seat-status-error":
                raise HTTPException(status_code=400, detail="This seat is already taken!")
            case "seat-row-error":
                raise HTTPException(status_code=400, detail="Invalid seat row was given")
            case "seat-num-error":
                raise HTTPException(status_code=400, detail="Invalid seat number was given")

        updated_reservation_data = await service.update_reservation(
            reservation_id=reservation_id,
            data=extended_reservation_data,
        )
        return updated_reservation_data.model_dump() if updated_reservation_data \
            else {}

    raise HTTPException(status_code=404, detail="Reservation not found")


@router.delete("/{reservation_id}", status_code=204)
@inject
async def delete_reservation(
    reservation_id: int,
    service: IReservationService = Depends(Provide[Container.reservation_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting reservation.

    Args:
        reservation_id (int): The id of the reservation.
        service (IReservationService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if reservation does not exist.

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

    if await service.get_by_id(reservation_id=reservation_id):
        await service.delete_reservation(reservation_id)
        return

    raise HTTPException(status_code=404, detail="Reservation not found")