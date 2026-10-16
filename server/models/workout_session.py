from datetime import date

from sqlalchemy import (
    BigInteger,
    Date,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
    Index,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class WorkoutSession(Base):
    __tablename__ = "workout_sessions"

    workout_session_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
    )
    workout_type_id: Mapped[int] = mapped_column(BigInteger)
    session_date: Mapped[date] = mapped_column(Date)

    __table_args__ = (
        ForeignKeyConstraint(
            ["workout_type_id", "user_id"],
            ["workout_types.workout_type_id", "workout_types.user_id"],
            name="workout_sessions_workout_type_owner_fk",
        ),
        UniqueConstraint(
            "workout_session_id",
            "user_id",
            name="workout_sessions_workout_session_id_user_id_uq",
        ),
        Index(
            "workout_sessions_user_id_session_date_ix",
            user_id,
            session_date,
        ),
    )
