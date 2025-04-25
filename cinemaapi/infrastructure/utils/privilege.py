from cinemaapi.infrastructure.utils.consts import (
    SUPER_ADMIN_ONE_TIME_KEY,
    AVAILABLE_ROLES
)

def check_privilege_code(authorization_code: str) -> str | None:
    """A function checking authorization code.

    Args:
        authorization_code (str): Provided code.

    Returns:
        str: Given super_admin role.
    """

    if authorization_code == SUPER_ADMIN_ONE_TIME_KEY:
        return AVAILABLE_ROLES[2]

    return None

