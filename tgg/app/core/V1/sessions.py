from sqlalchemy.orm import Session
from app.config.sql import SessionLocal


def get_db() -> Session:
    with SessionLocal() as db:
        yield db
