"""Create users.

Revision ID: 20261001_01
Revises:
Create Date: 2026-10-01
"""
from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa


revision: str = "20261001_01"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column(
            "user_id",
            sa.BigInteger(),
            sa.Identity(always=True),
            nullable=False,
        ),
        sa.Column("username", sa.Text(), nullable=False),
        sa.Column("email", sa.Text(), nullable=False),
        sa.CheckConstraint(
            "email = btrim(email) AND email <> ''",
            name=op.f("ck_users_email_trimmed_nonblank"),
        ),
        sa.CheckConstraint(
            "username = btrim(username) AND username <> ''",
            name=op.f("ck_users_username_trimmed_nonblank"),
        ),
        sa.PrimaryKeyConstraint("user_id", name=op.f("pk_users")),
    )
    op.create_index(
        "users_email_lower_uq",
        "users",
        [sa.text("lower(email)")],
        unique=True,
    )
    op.create_index(
        "users_username_lower_uq",
        "users",
        [sa.text("lower(username)")],
        unique=True,
    )


def downgrade() -> None:
    op.drop_index("users_username_lower_uq", table_name="users")
    op.drop_index("users_email_lower_uq", table_name="users")
    op.drop_table("users")
