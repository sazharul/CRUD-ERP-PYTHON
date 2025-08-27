from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mini_erp.db.session import Base
from mini_erp.services.product_service import ProductService




def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return Session()




def test_create_and_list_product():
    s = make_session()
    svc = ProductService(s)
    obj = svc.create("Test Product", 9.99, 10)
    assert obj.id is not None
    items = list(svc.list())
    assert any(p.name == "Test Product" for p in items)

def test_validate_price_and_stock():
    s = make_session()
    svc = ProductService(s)
    # negative price
    try:
        svc.create("Invalid Price", -1.0, 0)
        assert False, "expected validation error for negative price"
    except ValueError:
        assert True
    # negative stock
    try:
        svc.create("Invalid Stock", 1.0, -5)
        assert False, "expected validation error for negative stock"
    except ValueError:
        assert True