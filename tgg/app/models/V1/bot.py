import datetime

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column


from app.config.sql import Base


class Bot_report(Base):
    __tablename__ = "bot_report"
    __table_args__ = {"schema": "gob"}
    id:Mapped[int] = mapped_column(primary_key=True)
    user_id:Mapped[str] = mapped_column(String(30),nullable= True)
    create_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now )

