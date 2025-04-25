from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from cinemaapi.container import Container
from cinemaapi.core.domain.hall import Hall, HallIn, HallBroker
from cinemaapi.infrastructure.services.ihall import IHallService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from cinemaapi.infrastructure.utils import consts
from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/all", response_model=Iterable[Hall], status_code=200)
@inject
async def get_all_halls(
    service: IHallService = Depends(Provide[Container.hall_service]),
) -> Iterable:
    """An endpoint for getting all halls.

    Args:
        service (IHallService, optional): The injected service dependency.

    Returns:
        Iterable: The hall attributes collection.
    """

    halls = await service.get_all_halls()

    return halls


@router.get("/{hall_id}", response_model=Hall, status_code=200)
@inject
async def get_hall_by_id(
    hall_id: int,
    service: IHallService = Depends(Provide[Container.hall_service]),
) -> dict | None:
    """An endpoint for getting hall by id.

    Args:
        hall_id (int): The id of the hall.
        service (IHallService, optional): The injected service dependency.

    Returns:
        dict | None: The hall details.
    """

    if hall := await service.get_hall_by_id(hall_id=hall_id):
        return hall.model_dump()

    raise HTTPException(status_code=404, detail="Hall not found")


@router.get("/alias/{alias}", response_model=Hall, status_code=200)
@inject
async def get_hall_by_alias(
    alias: str,
    service: IHallService = Depends(Provide[Container.hall_service]),
) -> dict | None:
    """An endpoint for getting hall by alias.

    Args:
        alias (str): The alias of the hall.
        service (IHallService, optional): The injected service dependency.

    Returns:
        dict | None: The hall details.
    """

    if hall := await service.get_hall_by_alias(alias=alias):
        return hall.model_dump()

    raise HTTPException(status_code=404, detail="Hall not found")

@router.post("/create", response_model=Hall, status_code=201)
@inject
async def create_hall(
        hall: HallIn,
        service: IHallService = Depends(Provide[Container.hall_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new hall.

    Args:
        hall (HallIn): The hall data.
        service (IHallService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The new hall attributes.

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

    extended_hall_data = HallBroker(
        user_id=user_uuid,
        **hall.model_dump(),
    )

    match await service.validate_hall(extended_hall_data):
        case "hall-seat-row-invalid":
            raise HTTPException(status_code=400, detail="Given seat or row length is invalid.")
        case "hall-alias-occupied":
            raise HTTPException(status_code=400, detail="Hall of that alias already exists!")

    new_hall = await service.add_hall(extended_hall_data)

    return new_hall.model_dump() if new_hall else {}


@router.put("/{hall_id}", response_model=Hall, status_code=201)
@inject
async def update_hall(
    hall_id: int,
    updated_hall: HallIn,
    service: IHallService = Depends(Provide[Container.hall_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating hall data.

    Args:
        hall_id (int): The id of the hall.
        updated_hall (HallIn): The updated hall details.
        service (IHallService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if hall does not exist.

    Returns:
        dict: The updated hall details.

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

    if hall_data := await service.get_hall_by_id(hall_id=hall_id):
        extended_updated_hall = HallBroker(
            user_id=user_uuid,
            **updated_hall.model_dump(),
        )

        updated_hall_data = await service.update_hall(
            hall_id=hall_id,
            data=extended_updated_hall,
        )
        return updated_hall_data.model_dump() if updated_hall_data \
            else {}

    raise HTTPException(status_code=404, detail="Hall not found")


@router.delete("/{hall_id}", status_code=204)
@inject
async def delete_hall(
    hall_id: int,
    service: IHallService = Depends(Provide[Container.hall_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting halls.

    Args:
        hall_id (int): The id of the hall.
        service (IHallService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if hall does not exist.

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

    if await service.get_hall_by_id(hall_id=hall_id):
        await service.delete_hall(hall_id)
        return

    raise HTTPException(status_code=404, detail="Hall not found")