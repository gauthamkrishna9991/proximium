__all__ = ["User", "AuthenticationLog"]

from proximium.database import sync_table

from .user import User
from .authentication_log import AuthenticationLog

sync_table(User)
sync_table(AuthenticationLog)
