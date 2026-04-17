"""Registration period endpoints."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.period import RegistrationPeriod
from app.models.user import User
from app.schemas import PeriodCreate, PeriodUpdate, PeriodResponse, PeriodListResponse
from app.core.dependencies import get_current_user, require_roles
from app.core.exceptions import NotFoundException, BadRequestException

router = APIRouter(prefix="/periods", tags=["Registration Periods"])


@router.get("/", response_model=PeriodListResponse)
async def list_periods(
    status: str | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    q = db.query(RegistrationPeriod)
    if status:
        q = q.filter(RegistrationPeriod.status == status)
    
    total = q.count()
    items = q.order_by(RegistrationPeriod.created_at.desc()).offset((page - 1) * size).limit(size).all()
    return PeriodListResponse(items=items, total=total, page=page, size=size)


@router.post("/", response_model=PeriodResponse, status_code=201)
async def create_period(body: PeriodCreate, current_user: User = Depends(require_roles("STAFF", "ADMIN")), db: Session = Depends(get_db)):
    if body.end_date <= body.start_date:
        raise BadRequestException("Ngày kết thúc phải sau ngày bắt đầu")
    period = RegistrationPeriod(title=body.title, description=body.description,
                                start_date=body.start_date, end_date=body.end_date, created_by=current_user.id)
    db.add(period); db.commit(); db.refresh(period)
    return period


@router.get("/{period_id}", response_model=PeriodResponse)
async def get_period(period_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    period = db.query(RegistrationPeriod).filter(RegistrationPeriod.id == period_id).first()
    if not period: raise NotFoundException("Đợt đăng ký")
    return period


@router.put("/{period_id}", response_model=PeriodResponse)
async def update_period(period_id: UUID, body: PeriodUpdate, current_user: User = Depends(require_roles("STAFF", "ADMIN")), db: Session = Depends(get_db)):
    period = db.query(RegistrationPeriod).filter(RegistrationPeriod.id == period_id).first()
    if not period: raise NotFoundException("Đợt đăng ký")
    if period.status != "DRAFT": raise BadRequestException("Chỉ có thể chỉnh sửa đợt ở trạng thái Bản nháp")
    for f, v in body.model_dump(exclude_unset=True).items(): setattr(period, f, v)
    db.commit(); db.refresh(period)
    return period


@router.post("/{period_id}/open", response_model=PeriodResponse)
async def open_period(period_id: UUID, current_user: User = Depends(require_roles("STAFF", "ADMIN")), db: Session = Depends(get_db)):
    period = db.query(RegistrationPeriod).filter(RegistrationPeriod.id == period_id).first()
    if not period: raise NotFoundException("Đợt đăng ký")
    if period.status != "DRAFT": raise BadRequestException("Chỉ có thể mở đợt ở trạng thái Bản nháp")
    period.status = "OPEN"; db.commit(); db.refresh(period)
    return period


@router.post("/{period_id}/close", response_model=PeriodResponse)
async def close_period(period_id: UUID, current_user: User = Depends(require_roles("STAFF", "ADMIN")), db: Session = Depends(get_db)):
    period = db.query(RegistrationPeriod).filter(RegistrationPeriod.id == period_id).first()
    if not period: raise NotFoundException("Đợt đăng ký")
    if period.status != "OPEN": raise BadRequestException("Chỉ có thể đóng đợt đang mở")
    period.status = "CLOSED"; db.commit(); db.refresh(period)
    return period
