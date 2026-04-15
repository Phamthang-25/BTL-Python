"""001 - Initial schema: All 18 MVP tables.

Revision ID: 001_initial
Revises: None
Create Date: 2026-04-15
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

revision: str = "001_initial"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ── 1. roles ──────────────────────────────────────────────
    op.create_table(
        "roles",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("name", sa.String(100), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_roles_code", "roles", ["code"])

    # ── 2. departments ────────────────────────────────────────
    op.create_table(
        "departments",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(200), unique=True, nullable=False),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── 3. research_fields ────────────────────────────────────
    op.create_table(
        "research_fields",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(200), unique=True, nullable=False),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── 4. proposal_categories ────────────────────────────────
    op.create_table(
        "proposal_categories",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(200), unique=True, nullable=False),
        sa.Column("code", sa.String(20), unique=True, nullable=False),
        sa.Column("level", sa.String(50), nullable=False),
        sa.Column("max_duration_months", sa.Integer(), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    # ── 5. approval_steps ─────────────────────────────────────
    op.create_table(
        "approval_steps",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("step_code", sa.String(30), unique=True, nullable=False),
        sa.Column("step_name", sa.String(100), nullable=False),
        sa.Column("required_role", sa.String(20), nullable=False),
        sa.Column("step_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
    )

    # ── 6. users ──────────────────────────────────────────────
    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("email", sa.String(255), unique=True, nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("full_name", sa.String(200), nullable=False),
        sa.Column("phone", sa.String(20), nullable=True),
        sa.Column("department_id", UUID(as_uuid=True), sa.ForeignKey("departments.id", ondelete="SET NULL"), nullable=True),
        sa.Column("academic_rank", sa.String(50), nullable=True),
        sa.Column("academic_title", sa.String(50), nullable=True),
        sa.Column("role_id", UUID(as_uuid=True), sa.ForeignKey("roles.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_users_email", "users", ["email"])
    op.create_index("ix_users_role_id", "users", ["role_id"])
    op.create_index("ix_users_department_id", "users", ["department_id"])

    # ── 7. registration_periods ───────────────────────────────
    op.create_table(
        "registration_periods",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("title", sa.String(300), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
        sa.Column("created_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.CheckConstraint("end_date > start_date", name="ck_period_dates"),
    )

    # ── 8. proposals ──────────────────────────────────────────
    op.create_table(
        "proposals",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("objectives", sa.Text(), nullable=True),
        sa.Column("methodology", sa.Text(), nullable=True),
        sa.Column("expected_outcomes", sa.Text(), nullable=True),
        sa.Column("duration_months", sa.Integer(), nullable=True),
        sa.Column("budget_estimated", sa.Numeric(15, 2), nullable=True),
        sa.Column("pi_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("department_id", UUID(as_uuid=True), sa.ForeignKey("departments.id", ondelete="SET NULL"), nullable=True),
        sa.Column("field_id", UUID(as_uuid=True), sa.ForeignKey("research_fields.id", ondelete="SET NULL"), nullable=True),
        sa.Column("category_id", UUID(as_uuid=True), sa.ForeignKey("proposal_categories.id", ondelete="SET NULL"), nullable=True),
        sa.Column("period_id", UUID(as_uuid=True), sa.ForeignKey("registration_periods.id", ondelete="SET NULL"), nullable=True),
        sa.Column("status", sa.String(40), nullable=False, server_default="DRAFT"),
        sa.Column("revision_reason", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("title", "period_id", name="uq_proposal_title_period"),
        sa.CheckConstraint("duration_months BETWEEN 1 AND 36", name="ck_duration"),
    )
    op.create_index("ix_proposals_pi_id", "proposals", ["pi_id"])
    op.create_index("ix_proposals_status", "proposals", ["status"])
    op.create_index("ix_proposals_period_id", "proposals", ["period_id"])
    op.create_index("ix_proposals_category_id", "proposals", ["category_id"])

    # ── 9. proposal_members ───────────────────────────────────
    op.create_table(
        "proposal_members",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role_in_proposal", sa.String(30), nullable=False, server_default="CO_INVESTIGATOR"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("proposal_id", "user_id", name="uq_proposal_member"),
    )

    # ── 10. proposal_status_history ───────────────────────────
    op.create_table(
        "proposal_status_history",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("from_status", sa.String(40), nullable=True),
        sa.Column("to_status", sa.String(40), nullable=False),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("actor_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("note", sa.Text(), nullable=True),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_status_history_proposal", "proposal_status_history", ["proposal_id"])

    # ── 11. councils ──────────────────────────────────────────
    op.create_table(
        "councils",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(300), nullable=False),
        sa.Column("council_type", sa.String(30), nullable=False),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="FORMING"),
        sa.Column("scheduled_date", sa.Date(), nullable=True),
        sa.Column("location", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_councils_proposal_id", "councils", ["proposal_id"])

    # ── 12. council_members ───────────────────────────────────
    op.create_table(
        "council_members",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("council_id", UUID(as_uuid=True), sa.ForeignKey("councils.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("role_in_council", sa.String(30), nullable=False, server_default="REVIEWER"),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.UniqueConstraint("council_id", "user_id", name="uq_council_member"),
    )

    # ── 13. reviews ───────────────────────────────────────────
    op.create_table(
        "reviews",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("council_id", UUID(as_uuid=True), sa.ForeignKey("councils.id", ondelete="CASCADE"), nullable=False),
        sa.Column("reviewer_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("verdict", sa.String(20), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("council_id", "reviewer_id", name="uq_review_per_council"),
        sa.CheckConstraint("score BETWEEN 0 AND 100", name="ck_review_score"),
    )
    op.create_index("ix_reviews_reviewer_id", "reviews", ["reviewer_id"])
    op.create_index("ix_reviews_status", "reviews", ["status"])

    # ── 14. approval_history ──────────────────────────────────
    op.create_table(
        "approval_history",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("step_id", UUID(as_uuid=True), sa.ForeignKey("approval_steps.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("decided_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("decision", sa.String(20), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column("decided_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_approval_proposal_id", "approval_history", ["proposal_id"])

    # ── 15. progress_reports ──────────────────────────────────
    op.create_table(
        "progress_reports",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="CASCADE"), nullable=False),
        sa.Column("submitted_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("report_order", sa.Integer(), nullable=False),
        sa.Column("report_period", sa.String(50), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("completion_pct", sa.Numeric(5, 2), nullable=False),
        sa.Column("issues", sa.Text(), nullable=True),
        sa.Column("next_steps", sa.Text(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="SUBMITTED"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("proposal_id", "report_order", name="uq_progress_order"),
        sa.CheckConstraint("completion_pct BETWEEN 0 AND 100", name="ck_completion"),
    )
    op.create_index("ix_progress_proposal_id", "progress_reports", ["proposal_id"])

    # ── 16. acceptance_dossiers ───────────────────────────────
    op.create_table(
        "acceptance_dossiers",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("submitted_by", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("final_report", sa.Text(), nullable=False),
        sa.Column("achievements", sa.Text(), nullable=False),
        sa.Column("deliverables", sa.Text(), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="SUBMITTED"),
        sa.Column("revision_reason", sa.Text(), nullable=True),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("proposal_id", name="uq_acceptance_per_proposal"),
    )

    # ── 17. acceptance_reviews ────────────────────────────────
    op.create_table(
        "acceptance_reviews",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("dossier_id", UUID(as_uuid=True), sa.ForeignKey("acceptance_dossiers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("council_id", UUID(as_uuid=True), sa.ForeignKey("councils.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("reviewer_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=True),
        sa.Column("comments", sa.Text(), nullable=True),
        sa.Column("verdict", sa.String(20), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="PENDING"),
        sa.Column("reviewed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("dossier_id", "reviewer_id", name="uq_acceptance_review"),
        sa.CheckConstraint("score BETWEEN 0 AND 100", name="ck_acc_score"),
    )

    # ── 18. publications ──────────────────────────────────────
    op.create_table(
        "publications",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()")),
        sa.Column("proposal_id", UUID(as_uuid=True), sa.ForeignKey("proposals.id", ondelete="SET NULL"), nullable=True),
        sa.Column("author_id", UUID(as_uuid=True), sa.ForeignKey("users.id", ondelete="RESTRICT"), nullable=False),
        sa.Column("title", sa.String(500), nullable=False),
        sa.Column("journal_name", sa.String(300), nullable=True),
        sa.Column("doi", sa.String(100), unique=True, nullable=True),
        sa.Column("pub_type", sa.String(30), nullable=False),
        sa.Column("published_date", sa.Date(), nullable=True),
        sa.Column("issn_isbn", sa.String(30), nullable=True),
        sa.Column("indexing", sa.String(50), nullable=True),
        sa.Column("authors_text", sa.Text(), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="DRAFT"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_publications_proposal_id", "publications", ["proposal_id"])
    op.create_index("ix_publications_author_id", "publications", ["author_id"])


def downgrade() -> None:
    op.drop_table("publications")
    op.drop_table("acceptance_reviews")
    op.drop_table("acceptance_dossiers")
    op.drop_table("progress_reports")
    op.drop_table("approval_history")
    op.drop_table("reviews")
    op.drop_table("council_members")
    op.drop_table("councils")
    op.drop_table("proposal_status_history")
    op.drop_table("proposal_members")
    op.drop_table("proposals")
    op.drop_table("registration_periods")
    op.drop_table("users")
    op.drop_table("approval_steps")
    op.drop_table("proposal_categories")
    op.drop_table("research_fields")
    op.drop_table("departments")
    op.drop_table("roles")
