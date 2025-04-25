"""A module containing constant values for infrastructure layer."""

EXPIRATION_MINUTES = 60
SECRET_KEY = "s3cr3t"  # TODO: -> random generation - it's safe
ALGORITHM = "HS256"
SUPER_ADMIN_ONE_TIME_KEY = "n4m4a"
AVAILABLE_ROLES = ["user", "admin", "super_admin"]