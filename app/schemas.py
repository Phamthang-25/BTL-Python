from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date, datetime
from uuid import UUID
from app.models import ProjectStatus

class ProjectBase(BaseModel):
    title: str
    research_field: str
    budget: float = 0.0
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass
    # Không cần truyền leader_id vì hệ thống sẽ lấy id của người dùng đang đăng nhập

class ProjectResponse(ProjectBase):
    id: UUID
    status: ProjectStatus
    leader_id: UUID
    created_at: datetime
    updated_at: datetime
    
    # Từ Pydantic v2, sử dụng model_config (from_attributes=True) để tương thích với SQLAlchemy model (thay cho orm_mode=True của v1)
    model_config = ConfigDict(from_attributes=True)
