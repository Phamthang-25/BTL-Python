"""Role model — defines system roles for RBAC.

MVP roles: ADMIN, STAFF, LEADERSHIP, FACULTY, REVIEWER.
Stored in DB for extensibility; seeded on first startup.
"""

import uuid

from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Role(Base):
    __tablename__ = "roles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String(20), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)  # Vietnamese display name
    description = Column(Text, nullable=True)
    sort_order = Column(Integer, nullable=False, default=0)

    # Relationships
    users = relationship("User", back_populates="role_rel")

    def __repr__(self):
        return f"<Role {self.code}>"
