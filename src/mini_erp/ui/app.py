from __future__ import annotations
import tkinter as tk
from tkinter import ttk
from ..config import APP_NAME
from ..db.session import SessionLocal, init_db
from .views.customer_view import CustomerView




def mainloop() -> None:
    init_db()
    root = tk.Tk()
    root.title(APP_NAME)
    root.geometry("980x560")
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass


    # One session for the app (single-threaded GUI)
    session = SessionLocal()


    app = CustomerView(root, session)
    app.pack(fill="both", expand=True)


    def on_close():
        try:
            session.close()
        finally:
            root.destroy()


    root.protocol("WM_DELETE_WINDOW", on_close)
    root.mainloop()