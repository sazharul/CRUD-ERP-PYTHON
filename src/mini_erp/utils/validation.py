from __future__ import annotations
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9+()\-\s]{6,}$")
SKU_RE = re.compile(r"^[A-Z0-9_-]{3,}$")

def validate_customer(name: str, email: str, phone: str) -> tuple[bool, str]:
    if not name.strip():
        return False, "Name is required."
    if not EMAIL_RE.match(email.strip()):
        return False, "Invalid email address."
    if not PHONE_RE.match(phone.strip()):
        return False, "Invalid phone number."
    return True, ""


def validate_product(name: str, sku: str, price: float, stock: int) -> tuple[bool, str]:
    if not name.strip():
        return False, "Name is required."
    if not SKU_RE.match(sku.strip()):
        return False, "SKU must be A–Z, 0–9, _ or -, length ≥ 3."
    try:
        price = float(price)
    except Exception:
        return False, "Price must be a number."
    if price < 0:
        return False, "Price cannot be negative."
    try:
        stock = int(stock)
    except Exception:
        return False, "Stock must be an integer."
    if stock < 0:
        return False, "Stock cannot be negative."
    return True, ""
