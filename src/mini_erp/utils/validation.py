from __future__ import annotations
import re

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9+()\-\s]{6,}$")


def validate_customer(name: str, email: str, phone: str) -> tuple[bool, str]:
    if not name.strip():
        return False, "Name is required."
    if not EMAIL_RE.match(email.strip()):
        return False, "Invalid email address."
    if not PHONE_RE.match(phone.strip()):
        return False, "Invalid phone number."
    return True, ""
