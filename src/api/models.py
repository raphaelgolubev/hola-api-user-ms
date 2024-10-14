from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.sql import expression

from src.database import Base
from src.database.mixins import UuidMixin, TimestampMixin, UuidType


class User(Base, UuidMixin, TimestampMixin):
    __tablename__ = 'users'

    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column(nullable=False)
    user_type: Mapped[str] = mapped_column(nullable=False)
    
    profile: Mapped["Profile"] = relationship(
        "Profile", 
        back_populates="user", 
        uselist=False,
        cascade="all, delete",
        passive_deletes=True
    )
    
    is_email_verified: Mapped[bool] = mapped_column(default=False, server_default=expression.false())
    is_blocked: Mapped[bool] = mapped_column(default=False, server_default=expression.false())


class Profile(Base, UuidMixin, TimestampMixin):
    __tablename__ = 'profiles'

    nickname: Mapped[str] = mapped_column(unique=True, nullable=True)
    birth_date: Mapped[str] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[UuidType] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship(back_populates="profile", single_parent=True)

    __table_args__ = (
        UniqueConstraint("user_id"),
    )