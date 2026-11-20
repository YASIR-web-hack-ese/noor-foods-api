"""add notes to rider_shifts

Revision ID: 0002_rider_notes
Revises: 0001_rider_shifts
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_rider_notes"
down_revision: str | Sequence[str] | None = "0001_rider_shifts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "rider_shifts",
        sa.Column("notes", sa.Text(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("rider_shifts", "notes")
