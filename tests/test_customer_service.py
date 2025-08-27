from __future__ import annotations
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from mini_erp.db.session import Base
from mini_erp.services.customer_service import CustomerService

def make_session():
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    return Session()

def test_create_and_list_customer():
    session = make_session()
    svc = CustomerService(session)
    created = svc.create("Alice", "alice@example.com", "+1 555 1212")
    assert created.id is not None
    items = list(svc.list())
    assert any(c.email == "alice@example.com" for c in items)

def test_validation_email():
    session = make_session()
    svc = CustomerService(session)
    try:
        svc.create("Bob", "bademail", "+1 555 2222")
        assert False, "expected validation error"
    except ValueError:
        assert True