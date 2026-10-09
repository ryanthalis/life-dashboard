"""Create exercises.

Revision ID: 20261009_01
Revises: f5a123306151
Create Date: 2026-10-09
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20261009_01"
down_revision: str | Sequence[str] | None = "f5a123306151"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "exercises",
        sa.Column(
            "exercise_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("name", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "name = btrim(name) AND name <> ''",
            name=op.f("ck_exercises_name_trimmed_nonblank"),
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.user_id"],
            name=op.f("fk_exercises_user_id_users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("exercise_id", name=op.f("pk_exercises")),
        sa.UniqueConstraint(
            "exercise_id",
            "user_id",
            name="exercises_exercise_id_user_id_uq",
        ),
    )
    op.create_index(
        "exercises_user_id_name_lower_uq",
        "exercises",
        ["user_id", sa.text("lower(name)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("exercises_user_id_name_lower_uq", table_name="exercises")
    op.drop_table("exercises")
