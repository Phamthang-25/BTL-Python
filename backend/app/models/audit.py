"""Audit models — tracking user login activities."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class LoginLog(Base):
    __tablename__ = "login_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    ip_address = Column(String(50), nullable=True)
    user_agent = Column(String(500), nullable=True)
    is_success = Column(Boolean, default=True, nullable=False)
    login_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationship
    user = relationship("User", backref="login_logs")

    def __repr__(self):
        return f"<LoginLog {self.user_id} - {self.login_time}>"
