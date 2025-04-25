from typing import Iterable
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from cinemaapi.container import Container
from cinemaapi.core.domain.repertoire import Repertoire, RepertoireIn, RepertoireBroker
from cinemaapi.infrastructure.services.irepertoire import IRepertoireService

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from cinemaapi.infrastructure.utils import consts
from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES

bearer_scheme = HTTPBearer()

router = APIRouter()

@router.get("/all", response_model=Iterable[Repertoire], status_code=200)
@inject
async def get_all_repertoires(
    service: IRepertoireService = Depends(Provide[Container.repertoire_service]),
) -> Iterable:
    """An endpoint for getting all repertoires.

    Args:
        service (IRepertoireService, optional): The injected service dependency.

    Returns:
        Iterable: The repertoire attributes collection.
    """

    repertoires = await service.get_all_repertoires()

    return repertoires


@router.get("/{repertoire_id}", response_model=Repertoire, status_code=200)
@inject
async def get_repertoire_by_id(
    repertoire_id: int,
    service: IRepertoireService = Depends(Provide[Container.repertoire_service]),
) -> dict | None:
    """An endpoint for getting repertoire by id.

    Args:
        repertoire_id (int): The id of the repertoire.
        service (IRepertoireService, optional): The injected service dependency.

    Returns:
        dict | None: The repertoire details.
    """

    if repertoire := await service.get_repertoire_by_id(repertoire_id=repertoire_id):
        return repertoire.model_dump()

    raise HTTPException(status_code=404, detail="Repertoire not found")

@router.post("/create", response_model=Repertoire, status_code=201)
@inject
async def create_repertoire(
        repertoire: RepertoireIn,
        service: IRepertoireService = Depends(Provide[Container.repertoire_service]),
        credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for adding new repertoire.

    Args:
        repertoire (RepertoireIn): The repertoire data.
        service (IRepertoireService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The new repertoire attributes.

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

    extended_repertoire_data = RepertoireBroker(
        user_id=user_uuid,
        **repertoire.model_dump(),
    )

    new_repertoire = await service.add_repertoire(extended_repertoire_data)

    return new_repertoire.model_dump() if new_repertoire else {}


@router.put("/{repertoire_id}", response_model=Repertoire, status_code=201)
@inject
async def update_repertoire(
    repertoire_id: int,
    updated_repertoire: RepertoireIn,
    service: IRepertoireService = Depends(Provide[Container.repertoire_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """An endpoint for updating repertoire data.

    Args:
        repertoire_id (int): The id of the repertoire.
        updated_repertoire(RepertoireIn): The updated repertoire details.
        service (IMovieService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if repertoire does not exist.

    Returns:
        dict: The updated repertoire details.

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

    if repertoire_data := await service.get_repertoire_by_id(repertoire_id):
        extended_updated_repertoire = RepertoireBroker(
            user_id=user_uuid,
            **updated_repertoire.model_dump(),
        )
        updated_repertoire_data = await service.update_repertoire(
            repertoire_id=repertoire_id,
            data=extended_updated_repertoire,
        )

        return updated_repertoire_data.model_dump() if updated_repertoire_data else {}

    raise HTTPException(status_code=404, detail="Repertoire not found")


@router.delete("/{repertoire_id}", status_code=204)
@inject
async def delete_repertoire(
    repertoire_id: int,
    service: IRepertoireService = Depends(Provide[Container.repertoire_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> None:
    """An endpoint for deleting repertoire.

    Args:
        repertoire_id (int): The id of the repertoire.
        service (IRepertoireService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 403 if user is not authorized.
        HTTPException: 404 if repertoire does not exist.

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

    if await service.get_repertoire_by_id(repertoire_id=repertoire_id):
        await service.delete_repertoire(repertoire_id)
        return

    raise HTTPException(status_code=404, detail="Repertoire not found")