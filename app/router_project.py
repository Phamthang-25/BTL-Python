from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.database import get_db
from app.auth import get_current_user
from app import schemas, crud_project, models

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"]
)

@router.post("/", response_model=schemas.ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    project: schemas.ProjectCreate,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Chỉ định vai trò: Chỉ ADMIN hoặc TEACHER (Giảng viên) mới được phép tạo đề tài
    if current_user.role not in [models.UserRole.TEACHER, models.UserRole.ADMIN]:
         raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Bạn không có quyền tạo đề tài. Chức năng này chỉ dành cho Giảng viên."
        )
    return await crud_project.create_project(db=db, project=project, leader_id=current_user.id)

@router.get("/", response_model=List[schemas.ProjectResponse])
async def read_projects(
    skip: int = 0, limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Bắt buộc phải là user đã đăng nhập
):
    return await crud_project.get_projects(db, skip=skip, limit=limit)

@router.get("/{project_id}", response_model=schemas.ProjectResponse)
async def read_project(
    project_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(get_current_user) # Bắt buộc phải là user đã đăng nhập
):
    db_project = await crud_project.get_project_by_id(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin đề tài này.")
    return db_project
