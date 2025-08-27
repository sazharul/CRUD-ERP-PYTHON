from __future__ import annotations
from typing import Iterable
from sqlalchemy.orm import Session
from ..repositories.customer_repo import CustomerRepository
from ..utils.validation import validate_customer
from ..db.models.customer import Customer


class CustomerService:
    def __init__(self, session: Session):
        self.repo = CustomerRepository(session)


    def list(self, search: str = "") -> Iterable[Customer]:
        return self.repo.list(search)


    def create(self, name: str, email: str, phone: str) -> Customer:
        ok, msg = validate_customer(name, email, phone)
        if not ok:
            raise ValueError(msg)
        return self.repo.create(name, email, phone)


    def update(self, cid: int, name: str, email: str, phone: str) -> Customer:
        ok, msg = validate_customer(name, email, phone)
        if not ok:
            raise ValueError(msg)
        return self.repo.update(cid, name, email, phone)


    def delete(self, cid: int) -> None:
        return self.repo.delete(cid)