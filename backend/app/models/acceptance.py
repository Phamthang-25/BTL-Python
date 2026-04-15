"""Acceptance dossier and acceptance review models."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Numeric, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class AcceptanceDossier(Base):
    __tablename__ = "acceptance_dossiers"
    __table_args__ = (
        UniqueConstraint("proposal_id", name="uq_acceptance_per_proposal"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="RESTRICT"), nullable=False)
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    final_report = Column(Text, nullable=False)
    achievements = Column(Text, nullable=False)
    deliverables = Column(Text, nullable=True)  # Products, software, prototypes
    status = Column(String(30), nullable=False, default="SUBMITTED")
    revision_reason = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="acceptance_dossiers")
    acceptance_reviews = relationship("AcceptanceReview", back_populates="dossier")

    def __repr__(self):
        return f"<AcceptanceDossier ({self.status})>"


class AcceptanceReview(Base):
    __tablename__ = "acceptance_reviews"
    __table_args__ = (
        UniqueConstraint("dossier_id", "reviewer_id", name="uq_acceptance_review"),
        CheckConstraint("score BETWEEN 0 AND 100", name="ck_acc_score"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dossier_id = Column(UUID(as_uuid=True), ForeignKey("acceptance_dossiers.id", ondelete="CASCADE"), nullable=False)
    council_id = Column(UUID(as_uuid=True), ForeignKey("councils.id", ondelete="RESTRICT"), nullable=False)
    reviewer_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    score = Column(Numeric(5, 2), nullable=True)
    comments = Column(Text, nullable=True)
    verdict = Column(String(20), nullable=True)  # PASS, FAIL
    status = Column(String(20), nullable=False, default="PENDING")  # PENDING, SUBMITTED
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    dossier = relationship("AcceptanceDossier", back_populates="acceptance_reviews")
    council = relationship("Council", back_populates="acceptance_reviews")
    reviewer = relationship("User", back_populates="acceptance_reviews")

    def __repr__(self):
        return f"<AcceptanceReview ({self.status})>"
