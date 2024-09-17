
import datetime

from sqlalchemy import Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column


from app.config.sql import Base



class Cron_update(Base):
    __tablename__ = "cron"
    __table_args__ = {"schema": "gob"}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    success: Mapped[bool] = mapped_column(Boolean)
    create_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now)
