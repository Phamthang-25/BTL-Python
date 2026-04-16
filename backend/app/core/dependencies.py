"""FastAPI dependencies for authentication and authorization."""

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.core.security import decode_access_token
from app.core.exceptions import CredentialsException, ForbiddenException
from app.core.permissions import has_permission, Permission
from app.models.user import User
from app.models.role import Role

security_scheme = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Extract and validate the current user from the JWT token."""
    payload = decode_access_token(credentials.credentials)
    if payload is None:
        raise CredentialsException()

    user_id: str = payload.get("sub")
    if user_id is None:
        raise CredentialsException()

    user = (
        db.query(User)
        .options(joinedload(User.role_rel), joinedload(User.department))
        .filter(User.id == user_id, User.is_active == True)
        .first()
    )
    if user is None:
        raise CredentialsException()

    return user


def require_roles(*allowed_roles: str):
    """Dependency factory that checks if the current user has one of the allowed roles."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException()
        return current_user
    return role_checker


def require_permission(permission: Permission):
    """Dependency factory that checks if the user's role has the required permission."""
    async def permission_checker(current_user: User = Depends(get_current_user)) -> User:
        if not has_permission(current_user.role, permission):
            raise ForbiddenException()
        return current_user
    return permission_checker
