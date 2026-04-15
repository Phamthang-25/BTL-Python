"""Progress report model — periodic updates by PI."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Integer, Numeric, DateTime, ForeignKey, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class ProgressReport(Base):
    __tablename__ = "progress_reports"
    __table_args__ = (
        UniqueConstraint("proposal_id", "report_order", name="uq_progress_order"),
        CheckConstraint("completion_pct BETWEEN 0 AND 100", name="ck_completion"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False, index=True)
    submitted_by = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    report_order = Column(Integer, nullable=False)  # Auto-incremented per proposal
    report_period = Column(String(50), nullable=True)  # e.g., "Tháng 3-4/2026"
    content = Column(Text, nullable=False)
    completion_pct = Column(Numeric(5, 2), nullable=False)  # 0.00 - 100.00
    issues = Column(Text, nullable=True)
    next_steps = Column(Text, nullable=False)
    status = Column(String(20), nullable=False, default="SUBMITTED")  # SUBMITTED (MVP)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="progress_reports")
    submitted_by_user = relationship("User", back_populates="progress_reports")

    def __repr__(self):
        return f"<ProgressReport #{self.report_order} ({self.completion_pct}%)>"
