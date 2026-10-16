from datetime import datetime

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Identity,
    Index,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class WorkoutType(Base):
    __tablename__ = "workout_types"

    workout_type_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(Text)
    archived_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        CheckConstraint(
            "name = btrim(name) AND name <> ''",
            name="name_trimmed_nonblank",
        ),
        UniqueConstraint(
            "workout_type_id",
            "user_id",
            name="workout_types_workout_type_id_user_id_uq",
        ),
        Index(
            "workout_types_user_id_name_lower_uq",
            user_id,
            func.lower(name),
            unique=True,
        ),
    )
