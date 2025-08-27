from __future__ import annotations
from pathlib import Path


APP_NAME = "Mini ERP"
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INSTANCE_DIR = BASE_DIR / "instance"
INSTANCE_DIR.mkdir(parents=True, exist_ok=True)


DB_URL = f"sqlite:///{(INSTANCE_DIR / 'mini_erp.db').as_posix()}"