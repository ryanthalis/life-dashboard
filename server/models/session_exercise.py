from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    ForeignKeyConstraint,
    Identity,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class SessionExercise(Base):
    __tablename__ = "session_exercises"

    session_exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    workout_session_id: Mapped[int] = mapped_column(BigInteger)
    exercise_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
    )
    exercise_order: Mapped[int] = mapped_column(Integer)

    __table_args__ = (
        ForeignKeyConstraint(
            ["workout_session_id", "user_id"],
            ["workout_sessions.workout_session_id", "workout_sessions.user_id"],
            name="session_exercises_workout_session_owner_fk",
            ondelete="CASCADE",
        ),
        ForeignKeyConstraint(
            ["exercise_id", "user_id"],
            ["exercises.exercise_id", "exercises.user_id"],
            name="session_exercises_exercise_owner_fk",
        ),
        CheckConstraint(
            "exercise_order > 0",
            name="exercise_order_positive",
        ),
        UniqueConstraint(
            "workout_session_id",
            "exercise_order",
            name="session_exercises_workout_session_id_exercise_order_uq",
        ),
    )
