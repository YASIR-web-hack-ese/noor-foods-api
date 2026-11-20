"""limit rider_shifts notes to 200 characters

Revision ID: 0003_rider_notes_200
Revises: 0002_rider_notes
"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_rider_notes_200"
down_revision: str | Sequence[str] | None = "0002_rider_notes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column(
        "rider_shifts",
        "notes",
        existing_type=sa.Text(),
        type_=sa.String(length=200),
        existing_nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "rider_shifts",
        "notes",
        existing_type=sa.String(length=200),
        type_=sa.Text(),
        existing_nullable=True,
    )
