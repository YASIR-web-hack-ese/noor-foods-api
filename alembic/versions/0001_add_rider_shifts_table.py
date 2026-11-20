"""add rider_shifts table

Revision ID: 0001_rider_shifts
Revises: None
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0001_rider_shifts"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "rider_shifts",
        sa.Column("shift_id", sa.Integer(), nullable=False),
        sa.Column("rider_id", sa.Integer(), nullable=False),
        sa.Column("shift_date", sa.Date(), nullable=False),
        sa.Column("starts_at", sa.Time(), nullable=False),
        sa.Column("ends_at", sa.Time(), nullable=False),
        sa.ForeignKeyConstraint(["rider_id"], ["riders.rider_id"]),
        sa.PrimaryKeyConstraint("shift_id"),
    )


def downgrade() -> None:
    op.drop_table("rider_shifts")
