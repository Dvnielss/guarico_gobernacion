import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


from app.config.sql import Base


class Error_report(Base):
    __tablename__ = "error_report"
    __table_args__ = {"schema": "gob"}
    id:Mapped[int] = mapped_column(primary_key=True)
    create_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now )

