"""User management endpoints (Admin only)."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.models.role import Role
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserListResponse
from app.core.security import hash_password
from app.core.dependencies import require_roles
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/users", tags=["User Management"])


def _user_to_response(user: User) -> UserResponse:
    """Convert User model to response schema."""
    return UserResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        department_id=user.department_id,
        academic_rank=user.academic_rank,
        academic_title=user.academic_title,
        role=user.role,
        is_active=user.is_active,
        created_at=user.created_at,
        department_name=user.department.name if user.department else None,
    )


@router.get("/", response_model=UserListResponse)
async def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    role: str | None = None,
    search: str | None = None,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """List all users with pagination and optional filters."""
    query = db.query(User).options(joinedload(User.role_rel), joinedload(User.department))

    if role:
        query = query.join(User.role_rel).filter(Role.code == role)
    if search:
        query = query.filter(
            (User.full_name.ilike(f"%{search}%")) | (User.email.ilike(f"%{search}%"))
        )

    total = query.count()
    users = query.order_by(User.created_at.desc()).offset((page - 1) * size).limit(size).all()

    return UserListResponse(
        items=[_user_to_response(u) for u in users],
        total=total, page=page, size=size,
    )


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Create a new user."""
    existing = db.query(User).filter(User.email == body.email).first()
    if existing:
        raise BadRequestException("Email đã tồn tại trong hệ thống")

    # Resolve role code to role_id
    role_obj = db.query(Role).filter(Role.code == body.role).first()
    if not role_obj:
        raise BadRequestException(f"Vai trò '{body.role}' không hợp lệ")

    user = User(
        email=body.email,
        hashed_password=hash_password(body.password),
        full_name=body.full_name,
        phone=body.phone,
        department_id=body.department_id,
        academic_rank=body.academic_rank,
        academic_title=body.academic_title,
        role_id=role_obj.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Reload with relationships
    user = db.query(User).options(joinedload(User.role_rel), joinedload(User.department)).filter(User.id == user.id).first()
    return _user_to_response(user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Get user by ID."""
    user = (
        db.query(User)
        .options(joinedload(User.role_rel), joinedload(User.department))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise NotFoundException("Người dùng")
    return _user_to_response(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    body: UserUpdate,
    current_user: User = Depends(require_roles("ADMIN")),
    db: Session = Depends(get_db),
):
    """Update an existing user."""
    user = (
        db.query(User)
        .options(joinedload(User.role_rel), joinedload(User.department))
        .filter(User.id == user_id)
        .first()
    )
    if not user:
        raise NotFoundException("Người dùng")

    update_data = body.model_dump(exclude_unset=True)

    # Handle role update specially — convert role code to role_id
    if "role" in update_data:
        role_code = update_data.pop("role")
        role_obj = db.query(Role).filter(Role.code == role_code).first()
        if not role_obj:
            raise BadRequestException(f"Vai trò '{role_code}' không hợp lệ")
        user.role_id = role_obj.id

    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    # Reload relationships
    user = db.query(User).options(joinedload(User.role_rel), joinedload(User.department)).filter(User.id == user.id).first()
    return _user_to_response(user)
