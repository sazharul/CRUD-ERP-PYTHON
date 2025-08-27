from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from ..config import DB_URL


class Base(DeclarativeBase):
    pass


engine = create_engine(DB_URL, echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def init_db() -> None:
    from .models import customer  # noqa: F401
    Base.metadata.create_all(bind=engine)
