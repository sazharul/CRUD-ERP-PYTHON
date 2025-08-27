from __future__ import annotations
from typing import Iterable
from sqlalchemy.orm import Session
from ..repositories.product_repo import ProductRepository
from ..db.models.product import Product


class ProductService:
    def __init__(self, session: Session):
        self.repo = ProductRepository(session)


    def list(self, search: str = "") -> Iterable[Product]:
        return self.repo.list(search)


    def create(self, name: str, price: float, stock: int) -> Product:
        if not name.strip():
            raise ValueError("Name required")
        if price < 0:
            raise ValueError("Price must be >= 0")
        if stock < 0:
            raise ValueError("Stock must be >= 0")
        return self.repo.create(name, price, stock)


    def update(self, pid: int, name: str, price: float, stock: int) -> Product:
        return self.repo.update(pid, name, price, stock)


    def delete(self, pid: int) -> None:
        return self.repo.delete(pid)