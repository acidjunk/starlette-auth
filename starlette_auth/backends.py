from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    UnauthenticatedUser,
)
from starlette.requests import HTTPConnection

from .tables import User


class ModelAuthBackend(AuthenticationBackend):
    def get_user(self, conn: HTTPConnection):
        user_id = conn.session.get("user")
        if user_id:
            return User.query.get(user_id)

    async def authenticate(self, conn: HTTPConnection):
        user = self.get_user(conn)
        if user and user.is_authenticated:
            scopes = ["authenticated"] + sorted([str(s) for s in user.scopes])
            return AuthCredentials(scopes), user
        scopes = ["unauthenticated"]
        return AuthCredentials(scopes), UnauthenticatedUser()
