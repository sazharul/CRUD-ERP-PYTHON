from __future__ import annotations
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from ..session import Base


class Customer(Base):
    __tablename__ = "customers"


    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False)
    phone: Mapped[str] = mapped_column(String(40), nullable=False)


    def __repr__(self) -> str:
        return f"<Customer {self.id} {self.name}>"