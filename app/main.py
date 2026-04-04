from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine, AsyncSessionLocal
from app.models import User, Project, ProjectMember, Publication, UserRole, ProjectStatus
from app.router_auth import router as auth_router
from app.router_project import router as project_router
from app.auth import get_password_hash
from sqlalchemy.future import select
import uuid

app = FastAPI(
    title="Science Manager API",
    description="Hệ thống Quản lý Hoạt động Khoa học - Khoa ATTT (PTIT)",
    version="1.0.0"
)

# Kích hoạt CORS cực kỳ quan trọng: Cho phép Frontend (React) gọi lệnh API xuyên Domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Đăng ký các router
app.include_router(auth_router)
app.include_router(project_router)

# Khởi tạo bảng tự động và Seed Data (Chuẩn bị hệ sinh thái MVP 1 Run)
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
    # Tạo Seed Data nếu DB chưa có ai
    async with AsyncSessionLocal() as db:
        result = await db.execute(select(User).limit(1))
        if not result.scalars().first():
            print("--- BẮT ĐẦU CHẠY SEED DATA CHO MVP ---")
            admin_id = uuid.uuid4()
            admin = User(
                id=admin_id,
                username="admin",
                hashed_password=get_password_hash("admin123"), # Mật khẩu sẽ đăng nhập ở Frontend
                role=UserRole.ADMIN,
                email="admin@ptit.edu.vn",
                department="Ban Quản trị Khoa"
            )
            db.add(admin)
            
            project1 = Project(
                title="Ứng dụng Blockchain trong quản lý văn bằng hệ thống PTIT",
                research_field="Blockchain Security",
                budget=50000000,
                start_date="2024-01-01",
                end_date="2024-12-31",
                status=ProjectStatus.APPROVED,
                leader_id=admin_id
            )
            db.add(project1)
            
            project2 = Project(
                title="Nghiên cứu và đánh giá rủi ro hệ thống kiểm thử tự động Penetration Test",
                research_field="Pentest",
                start_date="2024-06-01",
                status=ProjectStatus.DRAFT,
                leader_id=admin_id
            )
            db.add(project2)
            
            await db.commit()
            print("--- SEED DATA HOÀN TẤT: Đã có sẵn tài khoản: admin | Mật khẩu: admin123")

@app.get("/")
async def root():
    return {"message": "Welcome to Science Manager API - Hệ thống đang hoạt động với Database Postgres"}
