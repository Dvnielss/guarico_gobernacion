import datetime

from typing import List
from sqlalchemy import String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config.sql import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = {"schema": "gob"}

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50),unique=True)
    password: Mapped[str] = mapped_column(String(100))
    rol: Mapped[str] = mapped_column(String(5), default="GUEST")
    status:Mapped[bool] = mapped_column(Boolean,default=True)
    create_at: Mapped[DateTime] = mapped_column(
        DateTime, default=datetime.datetime.now
    )
    user_update:Mapped[List["Users_update"]] = relationship("Users_update")



class Users_update(Base):
    __tablename__ = "user_update"
    __table_args__ = {"schema": "gob"}
    id: Mapped[int] = mapped_column(primary_key=True)
    users:Mapped[int] = mapped_column(ForeignKey(User.id),)
    success: Mapped[bool] = mapped_column(Boolean)
    create_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now)
