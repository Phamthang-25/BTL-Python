"""Publication model — scientific outputs linked to proposals."""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Column, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Publication(Base):
    __tablename__ = "publications"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    proposal_id = Column(UUID(as_uuid=True), ForeignKey("proposals.id", ondelete="SET NULL"), nullable=True, index=True)
    author_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    journal_name = Column(String(300), nullable=True)  # Journal or conference name
    doi = Column(String(100), unique=True, nullable=True)
    pub_type = Column(String(30), nullable=False)  # JOURNAL, CONFERENCE, BOOK_CHAPTER, PATENT
    published_date = Column(Date, nullable=True)
    issn_isbn = Column(String(30), nullable=True)
    indexing = Column(String(50), nullable=True)  # SCOPUS, WOS, OTHER, DOMESTIC
    authors_text = Column(Text, nullable=True)  # Full author list as text
    status = Column(String(20), nullable=False, default="DRAFT")  # DRAFT, PUBLISHED, VERIFIED
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationships
    proposal = relationship("Proposal", back_populates="publications")
    author = relationship("User", back_populates="publications")

    def __repr__(self):
        return f"<Publication {self.title[:50]}>"
