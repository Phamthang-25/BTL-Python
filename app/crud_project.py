from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import UUID

from app import models, schemas

async def create_project(db: AsyncSession, project: schemas.ProjectCreate, leader_id: UUID):
    # Khởi tạo model SQLAlchemy
    db_project = models.Project(
        **project.model_dump(),
        leader_id=leader_id
    )
    db.add(db_project)
    
    # Flush để có được ID của project trước khi insert thành viên nếu cần thiết
    await db.commit()
    await db.refresh(db_project)
    
    # Thêm Chủ nhiệm đề tài vào bảng ProjectMembers ngay khi tạo
    db_member = models.ProjectMember(
        user_id=leader_id,
        project_id=db_project.id,
        role_in_project=models.ProjectMemberRole.CHAIRMAN
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
