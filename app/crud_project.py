from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from uuid import UUID

from app import models, schemas

async def create_project(db: AsyncSession, project: schemas.ProjectCreate, leader_id: UUID):
    db_project = models.Project(**project.model_dump(), leader_id=leader_id)
    db.add(db_project)
    await db.commit()
    await db.refresh(db_project)
    
    db_member = models.ProjectMember(
        user_id=leader_id, project_id=db_project.id, role_in_project=models.ProjectMemberRole.CHAIRMAN
    )
    db.add(db_member)
    await db.commit()
    return db_project

async def get_projects(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(models.Project).offset(skip).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()

async def get_project_by_id(db: AsyncSession, project_id: UUID):
    stmt = select(models.Project).where(models.Project.id == project_id)
    result = await db.execute(stmt)
    return result.scalars().first()

async def update_project(db: AsyncSession, project_id: UUID, project_update: schemas.ProjectUpdate):
    db_project = await get_project_by_id(db, project_id)
    if not db_project: return None
    update_data = project_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_project, key, value)
    await db.commit()
    await db.refresh(db_project)
    return db_project

async def delete_project(db: AsyncSession, project_id: UUID):
    db_project = await get_project_by_id(db, project_id)
    if db_project:
        await db.delete(db_project)
        await db.commit()
        return True
    return False

async def add_project_member(db: AsyncSession, project_id: UUID, member_data: schemas.ProjectMemberCreate):
    db_member = models.ProjectMember(
        project_id=project_id, user_id=member_data.user_id, role_in_project=member_data.role_in_project
    )
    db.add(db_member)
    try:
        await db.commit()
        await db.refresh(db_member)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Lỗi: Khóa dữ liệu (ID Thành viên không tồn tại hoặc đã có trong danh sách).")
        
    stmt = select(models.ProjectMember).options(selectinload(models.ProjectMember.user)).where(
        models.ProjectMember.project_id == project_id, models.ProjectMember.user_id == member_data.user_id
    )
    result = await db.execute(stmt)
    return result.scalars().first()

async def get_project_members(db: AsyncSession, project_id: UUID):
    stmt = select(models.ProjectMember).options(selectinload(models.ProjectMember.user)).where(models.ProjectMember.project_id == project_id)
    result = await db.execute(stmt)
    return result.scalars().all()

async def add_publication(db: AsyncSession, project_id: UUID, pub_data: schemas.PublicationCreate):
    db_pub = models.Publication(**pub_data.model_dump(), project_id=project_id)
    db.add(db_pub)
    try:
        await db.commit()
        await db.refresh(db_pub)
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Lỗi CSDL: Khai báo ấn phẩm không thành công.")
    return db_pub

async def get_project_publications(db: AsyncSession, project_id: UUID):
    stmt = select(models.Publication).where(models.Publication.project_id == project_id)
    result = await db.execute(stmt)
    return result.scalars().all()
