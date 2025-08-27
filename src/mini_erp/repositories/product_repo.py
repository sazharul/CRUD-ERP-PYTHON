from __future__ import annotations
from typing import Iterable, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from ..db.models.product import Product


class ProductRepository:
    def __init__(self, session: Session):
        self.session = session

    def list(self, search: str = "") -> Iterable[Product]:
        stmt = select(Product).order_by(Product.id.desc())
        if search := search.strip():
            like = f"%{search}%"
            stmt = stmt.where(Product.name.like(like))
        return self.session.scalars(stmt).all()


    def get(self, pid: int) -> Optional[Product]:
        return self.session.get(Product, pid)


    def create(self, name: str, price: float, stock: int) -> Product:
        obj = Product(name=name.strip(), price=float(price), stock=int(stock))
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj


    def update(self, pid: int, name: str, price: float, stock: int) -> Product:
        obj = self.session.get(Product, pid)
        if not obj:
            raise ValueError("Product not found")
        obj.name, obj.price, obj.stock = name.strip(), float(price), int(stock)
        self.session.commit()
        self.session.refresh(obj)
        return obj


    def delete(self, pid: int) -> None:
        obj = self.session.get(Product, pid)
        if not obj:
            raise ValueError("Product not found")
        self.session.delete(obj)
        self.session.commit()