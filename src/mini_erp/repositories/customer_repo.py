from __future__ import annotations
from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db.models.customer import Customer


class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self, search: str = "") -> Iterable[Customer]:
        stmt = select(Customer).order_by(Customer.id.desc())
        if search := search.strip():
            like = f"%{search}%"
            stmt = select(Customer).where(
                (Customer.name.like(like)) | (Customer.email.like(like)) | (Customer.phone.like(like))
            ).order_by(Customer.id.desc())
        return self.session.scalars(stmt).all()


    def get(self, cid: int) -> Optional[Customer]:
        return self.session.get(Customer, cid)


    def create(self, name: str, email: str, phone: str) -> Customer:
        obj = Customer(name=name.strip(), email=email.strip(), phone=phone.strip())
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj


    def update(self, cid: int, name: str, email: str, phone: str) -> Customer:
        obj = self.session.get(Customer, cid)
        if not obj:
            raise ValueError("Customer not found")
        obj.name, obj.email, obj.phone = name.strip(), email.strip(), phone.strip()
        self.session.commit()
        self.session.refresh(obj)
        return obj


    def delete(self, cid: int) -> None:
        obj = self.session.get(Customer, cid)
        if not obj:
            raise ValueError("Customer not found")
        self.session.delete(obj)
        self.session.commit()
