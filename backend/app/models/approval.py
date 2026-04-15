"""Approval models — configurable workflow steps and decision history."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Integer, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ApprovalStep(Base):
    """Configured workflow step definitions.

    MVP seed:
      1. STAFF_VALIDATE  — S&T Staff checks completeness
      2. COUNCIL_REVIEW  — Review council scores
      3. LEADERSHIP_APPROVE — Leadership makes final decision
    """
    __tablename__ = "approval_steps"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    step_code = Column(String(30), unique=True, nullable=False)
    step_name = Column(String(100), nullable=False)  # Vietnamese display name
    required_role = Column(String(20), nullable=False)  # Role code needed to act
    step_order = Column(Integer, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    history_entries = relationship("ApprovalHistory", back_populates="step")

    def __repr__(self):
        return f"<ApprovalStep {self.step_code} (order={self.step_order})>"


class ApprovalHistory(Base):
    """Actual decisions made at each approval step for a proposal."""
    __tablename__ = "approval_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False, index=True)
    step_id = Column(UUID(as_uuid=True), ForeignKey("approval_steps.id", ondelete="RESTRICT"), nullable=False)
    decided_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    decision = Column(String(20), nullable=False)  # APPROVED, REJECTED, RETURNED
    reason = Column(Text, nullable=True)
    decided_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="approval_history")
    step = relationship("ApprovalStep", back_populates="history_entries")
    decided_by_user = relationship("User", back_populates="approval_decisions")

    def __repr__(self):
        return f"<ApprovalHistory {self.decision}>"
