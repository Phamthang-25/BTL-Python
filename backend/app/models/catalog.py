"""Catalog models: Department, ResearchField, ProposalCategory."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Boolean, Integer, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    users = relationship("User", back_populates="department")
    proposals = relationship("Proposal", back_populates="department", foreign_keys="Proposal.department_id")

    def __repr__(self):
        return f"<Department {self.code}>"


class ResearchField(Base):
    __tablename__ = "research_fields"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposals = relationship("Proposal", back_populates="research_field")

    def __repr__(self):
        return f"<ResearchField {self.code}>"


class ProposalCategory(Base):
    """Type/level of research proposal (cấp trường, cấp khoa, cấp bộ)."""
    __tablename__ = "proposal_categories"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(200), unique=True, nullable=False)
    code = Column(String(20), unique=True, nullable=False)
    level = Column(String(50), nullable=False)  # UNIVERSITY, FACULTY, MINISTERIAL
    max_duration_months = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposals = relationship("Proposal", back_populates="category")

    def __repr__(self):
        return f"<ProposalCategory {self.code}>"
