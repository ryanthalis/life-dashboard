from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Identity,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class WorkoutSet(Base):
    __tablename__ = "sets"

    set_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    session_exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("session_exercises.session_exercise_id", ondelete="CASCADE"),
    )
    set_number: Mapped[int] = mapped_column(Integer)
    repetitions: Mapped[int] = mapped_column(Integer)
    rir: Mapped[int | None] = mapped_column(Integer)
    load_lbs: Mapped[Decimal | None] = mapped_column(Numeric(8, 2))

    __table_args__ = (
        CheckConstraint("set_number > 0", name="set_number_positive"),
        CheckConstraint("repetitions >= 0", name="repetitions_nonnegative"),
        CheckConstraint(
            "rir IS NULL OR rir BETWEEN 0 AND 10",
            name="rir_range",
        ),
        CheckConstraint(
            "load_lbs IS NULL OR load_lbs >= 0",
            name="load_lbs_nonnegative",
        ),
        UniqueConstraint(
            "session_exercise_id",
            "set_number",
            name="sets_session_exercise_id_set_number_uq",
        ),
    )
