"""Authentication endpoints: login, profile, change password."""

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.user import User
from app.models.audit import LoginLog
from app.schemas import LoginRequest, TokenResponse, ChangePasswordRequest, UserResponse, RefreshTokenRequest
from app.core.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_refresh_token
from app.core.dependencies import get_current_user
from app.core.exceptions import CredentialsException, BadRequestException

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(request: Request, body: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT tokens (access & refresh)."""
    user = (
        db.query(User)
        .options(joinedload(User.role_rel))
        .filter(User.email == body.email)
        .first()
    )

    ip_addr = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    if not user or not verify_password(body.password, user.hashed_password):
        if user:
            log = LoginLog(user_id=user.id, ip_address=ip_addr, user_agent=user_agent, is_success=False)
            db.add(log)
            db.commit()
        raise CredentialsException()

    if not user.is_active:
        raise BadRequestException("Tài khoản đã bị vô hiệu hóa")

    # Log successful login
    log = LoginLog(user_id=user.id, ip_address=ip_addr, user_agent=user_agent, is_success=True)
    db.add(log)
    db.commit()

    token = create_access_token({"sub": str(user.id), "role": user.role})
    refresh_token = create_refresh_token({"sub": str(user.id)})
    
    return TokenResponse(access_token=token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(body: RefreshTokenRequest, db: Session = Depends(get_db)):
    """Refresh JWT access token using refresh token."""
    payload = decode_refresh_token(body.refresh_token)
    if payload is None:
        raise CredentialsException()

    user_id = payload.get("sub")
    if not user_id:
        raise CredentialsException()

    user = db.query(User).options(joinedload(User.role_rel)).filter(User.id == user_id, User.is_active == True).first()
    if not user:
        raise CredentialsException()

    new_access = create_access_token({"sub": str(user.id), "role": user.role})
    new_refresh = create_refresh_token({"sub": str(user.id)})
    
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


@router.get("/me", response_model=UserResponse)
async def get_profile(current_user: User = Depends(get_current_user)):
    """Get current user's profile."""
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        phone=current_user.phone,
        department_id=current_user.department_id,
        academic_rank=current_user.academic_rank,
        academic_title=current_user.academic_title,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        department_name=current_user.department.name if current_user.department else None,
    )


@router.put("/me/password")
async def change_password(
    body: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Change current user's password."""
    if not verify_password(body.current_password, current_user.hashed_password):
        raise BadRequestException("Mật khẩu hiện tại không đúng")
    if len(body.new_password) < 8:
        raise BadRequestException("Mật khẩu mới phải có ít nhất 8 ký tự")
    current_user.hashed_password = hash_password(body.new_password)
    db.commit()
    return {"message": "Đổi mật khẩu thành công"}
