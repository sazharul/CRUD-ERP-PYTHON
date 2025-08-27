# Mini ERP (Tkinter)


A layered desktop app in Python with GUI + SQLite via SQLAlchemy.


## Quickstart
```bash
python -m venv venv
# PowerShell: .\venv\Scripts\Activate ; Git Bash: source venv/Scripts/activate
pip install -e .
mini-erp # or: python -m mini_erp


---


### `src/mini_erp/__init__.py`
```python
__all__ = ["__version__"]
__version__ = "0.1.0"