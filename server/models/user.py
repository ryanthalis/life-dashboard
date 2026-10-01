from sqlalchemy import BigInteger, CheckConstraint, Identity, Index, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from server.models.base import Base


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    username: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        CheckConstraint(
            "username = btrim(username) AND username <> ''",
            name="username_trimmed_nonblank",
        ),
        CheckConstraint(
            "email = btrim(email) AND email <> ''",
            name="email_trimmed_nonblank",
        ),
        Index("users_username_lower_uq", func.lower(username), unique=True),
        Index("users_email_lower_uq", func.lower(email), unique=True),
    )
