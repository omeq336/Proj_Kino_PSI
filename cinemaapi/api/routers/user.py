from typing import Iterable, Optional

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt
from pydantic import UUID4

from cinemaapi.container import Container
from cinemaapi.core.domain.user import UserIn
from cinemaapi.infrastructure.dto.tokendto import TokenDTO
from cinemaapi.infrastructure.dto.userdto import UserDTO
from cinemaapi.infrastructure.services.iuser import IUserService
from cinemaapi.infrastructure.utils import consts
from cinemaapi.infrastructure.utils.consts import AVAILABLE_ROLES

router = APIRouter()

bearer_scheme = HTTPBearer()


@router.post("/register", response_model=UserDTO, status_code=201)
@inject
async def register_user(
    user: UserIn,
    authorization_code: Optional[str] = None,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for registering new user

    Args:
        user (UserIn): The user input data.
        authorization_code (Optional[str]): The user's authorization code.
        service (IUserService, optional): The injected user service.

    Returns:
        dict: The user DTO details.
    """

    if new_user := await service.register_user(user, authorization_code):
        return UserDTO(**dict(new_user)).model_dump()

    raise HTTPException(
        status_code=400,
        detail="The user with provided e-mail already exists",
    )

@router.post("/register_admin", response_model=UserDTO, status_code=201)
@inject
async def register_admin(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict:
    """A router coroutine for registering new admin

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Raises:
        HTTPException: 400 if data is not valid.
        HTTPException: 403 if user is not authorized.

    Returns:
        dict: The user DTO details.

    Requires:
        super_admin privileges.
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

    if user_role != AVAILABLE_ROLES[2]:
        raise HTTPException(status_code=403, detail="Unauthorized, not enough privileges")

    if new_user := await service.register_admin(user):
        return UserDTO(**dict(new_user)).model_dump()

    raise HTTPException(
        status_code=400,
        detail="The user with provided e-mail already exists",
    )

@router.post("/token", response_model=TokenDTO, status_code=200)
@inject
async def authenticate_user(
    user: UserIn,
    service: IUserService = Depends(Provide[Container.user_service]),
) -> dict:
    """A router coroutine for authenticating users.

    Args:
        user (UserIn): The user input data.
        service (IUserService, optional): The injected user service.

    Raises:
        HTTPException: 401 if credentials are not valid.

    Returns:
        dict: The token DTO details.
    """


    if token_details := await service.authenticate_user(user):
        print("user confirmed")
        return token_details.model_dump()

    raise HTTPException(
        status_code=401,
        detail="Provided incorrect credentials",
    )

@router.get("/movie/uuid/{uuid}", response_model=Iterable[dict], status_code=200)
@inject
async def view_recommended_movies(uuid: str, service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> Iterable:
    """An endpoint for getting recommending movies to user.

    Args:
        uuid (UUID4): The id of the user.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        Iterable: The movie details collection.
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

    try:
        UUID4(uuid)
    except:
        raise HTTPException(status_code=400, detail="Given user_id is invalid.")

    match await service.validate_user(uuid):
        case "user-genre-not-found":
            raise HTTPException(status_code=400, detail="No movie recommendations, review some movies first.")

    recommendations = await service.view_recommended_movies(uuid)

    return recommendations

@router.get("/genre/{uuid}", response_model=dict, status_code=200)
@inject
async def get_recommended_genre(uuid: str, service: IUserService = Depends(Provide[Container.user_service]),
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> dict | None:
    """An endpoint for recommending genre to user.

    Args:
        uuid (UUID4): The id of the user.
        service (IUserService, optional): The injected service dependency.
        credentials (HTTPAuthorizationCredentials, optional): The credentials.

    Returns:
        dict | None: The genre name.
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

    try:
        UUID4(uuid)
    except:
        raise HTTPException(status_code=400, detail="Given user_id is invalid.")

    match await service.validate_user(uuid):
        case "user-genre-not-found":
            raise HTTPException(status_code=404, detail="Cannot recommend genre, review some movies first.")

    if recommendation := await service.view_recommended_genre(uuid=uuid):
        return recommendation

    raise HTTPException(status_code=404, detail="Cannot recommend genre, review some movies first.")