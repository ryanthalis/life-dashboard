from sqlalchemy import (
    BigInteger,
    CheckConstraint,
    ForeignKey,
    Identity,
    Index,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class Exercise(Base):
    __tablename__ = "exercises"

    exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(
            "name = btrim(name) AND name <> ''",
            name="name_trimmed_nonblank",
        ),
        UniqueConstraint(
            "exercise_id",
            "user_id",
            name="exercises_exercise_id_user_id_uq",
        ),
        Index(
            "exercises_user_id_name_lower_uq",
            user_id,
            func.lower(name),
            unique=True,
        ),
    )
