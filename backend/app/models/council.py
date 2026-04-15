"""Council and CouncilMember models for review/acceptance panels."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, Date, DateTime, Text, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Council(Base):
    __tablename__ = "councils"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(300), nullable=False)
    council_type = Column(String(30), nullable=False)  # PROPOSAL_REVIEW, ACCEPTANCE
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="RESTRICT"), nullable=False, index=True)
    status = Column(String(20), nullable=False, default="FORMING")  # FORMING, ACTIVE, COMPLETED
    scheduled_date = Column(Date, nullable=True)  # Council meeting date
    location = Column(Text, nullable=True)  # Meeting location
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="councils")
    members = relationship("CouncilMember", back_populates="council", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="council")
    acceptance_reviews = relationship("AcceptanceReview", back_populates="council")

    def __repr__(self):
        return f"<Council {self.name} ({self.status})>"


class CouncilMember(Base):
    __tablename__ = "council_members"
    __table_args__ = (
        UniqueConstraint("council_id", "user_id", name="uq_council_member"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    council_id = Column(UUID(as_uuid=True), ForeignKey("councils.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_in_council = Column(String(30), nullable=False, default="REVIEWER")  # CHAIR, SECRETARY, REVIEWER
    sort_order = Column(Integer, nullable=False, default=0)

    # Relationships
    council = relationship("Council", back_populates="members")
    user = relationship("User", back_populates="council_memberships")
