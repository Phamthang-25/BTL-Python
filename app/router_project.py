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
    current_user: models.User = Depends(get_current_user)
):
    db_project = await crud_project.get_project_by_id(db, project_id=project_id)
    if db_project is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy thông tin đề tài này.")
    return db_project

def check_ownership(project, current_user):
    if current_user.role == models.UserRole.ADMIN:
        return
    if current_user.role == models.UserRole.TEACHER and project.leader_id == current_user.id:
        return
    raise HTTPException(status_code=403, detail="Chỉ ADMIN hoặc Quản lý (Chủ nhiệm) của đề tài này mới được phép thao tác.")

@router.put("/{project_id}", response_model=schemas.ProjectResponse)
async def update_project(
    project_id: UUID, project: schemas.ProjectUpdate,
    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    db_project_info = await crud_project.get_project_by_id(db, project_id)
    if not db_project_info: raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    check_ownership(db_project_info, current_user)

    db_project = await crud_project.update_project(db, project_id, project)
    return db_project

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    project_id: UUID, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    if current_user.role != models.UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Chỉ ADMIN mới được xóa mềm dự án")
    success = await crud_project.delete_project(db, project_id)
    if not success: raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    return None

@router.post("/{project_id}/members", response_model=schemas.ProjectMemberResponse)
async def add_member(
    project_id: UUID, member: schemas.ProjectMemberCreate,
    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    db_project_info = await crud_project.get_project_by_id(db, project_id)
    if not db_project_info: raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    check_ownership(db_project_info, current_user)
    
    return await crud_project.add_project_member(db, project_id, member)

@router.get("/{project_id}/members", response_model=List[schemas.ProjectMemberResponse])
async def read_members(
    project_id: UUID, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return await crud_project.get_project_members(db, project_id)

@router.post("/{project_id}/publications", response_model=schemas.PublicationResponse)
async def add_publication(
    project_id: UUID, pub: schemas.PublicationCreate,
    db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    db_project_info = await crud_project.get_project_by_id(db, project_id)
    if not db_project_info: raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    check_ownership(db_project_info, current_user)
    
    return await crud_project.add_publication(db, project_id, pub)

@router.get("/{project_id}/publications", response_model=List[schemas.PublicationResponse])
async def read_publications(
    project_id: UUID, db: AsyncSession = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return await crud_project.get_project_publications(db, project_id)
