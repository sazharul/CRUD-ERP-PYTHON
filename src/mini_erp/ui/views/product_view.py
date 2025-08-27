from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from ...services.product_service import ProductService

class ProductView(ttk.Frame):

    def __init__(self, master: tk.Tk, session: Session):
        super().__init__(master, padding=12)

        self.service = ProductService(session)
        self.current_id: int | None = None

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Search
        top = ttk.Frame(self)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top.columnconfigure(0, weight=1)
        self.search_var = tk.StringVar()
        ent = ttk.Entry(top, textvariable=self.search_var)
        ent.grid(row=0, column=0, sticky="ew")
        ent.bind("<Return>", lambda e: self.refresh())
        ttk.Button(top, text="Search", command=self.refresh).grid(row=0, column=1, padx=6)
        ttk.Button(top, text="Clear", command=self._clear_search).grid(row=0, column=2)

        # Tree
        cols = ("id", "name", "price", "stock")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=18)
        self.tree.grid(row=1, column=0, sticky="nsew")
        for c, w in zip(cols, (60, 200, 120, 100)):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=w, anchor="w")
        yscroll = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=1, column=1, sticky="ns")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Form
        form = ttk.LabelFrame(self, text="Product Details")
        form.grid(row=2, column=0, sticky="ew", pady=(10, 0))
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="Name").grid(row=0, column=0)
        self.name_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.name_var).grid(row=0, column=1, sticky="ew")

        ttk.Label(form, text="Price").grid(row=1, column=0)
        self.price_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.price_var).grid(row=1, column=1, sticky="ew")

        ttk.Label(form, text="Stock").grid(row=2, column=0)
        self.stock_var = tk.StringVar()
        ttk.Entry(form, textvariable=self.stock_var).grid(row=2, column=1, sticky="ew")

        # Buttons
        btns = ttk.Frame(form)
        btns.grid(row=3, column=0, columnspan=2, pady=(8, 0))
        for i in range(4):
            btns.columnconfigure(i, weight=1)
        ttk.Button(btns, text="New", command=self.clear_form).grid(row=0, column=0)
        ttk.Button(btns, text="Save", command=self.on_save).grid(row=0, column=1)
        ttk.Button(btns, text="Delete", command=self.on_delete).grid(row=0, column=2)
        ttk.Button(btns, text="Refresh", command=self.refresh).grid(row=0, column=3)

        self.status = tk.StringVar(value="Ready")
        ttk.Label(form, textvariable=self.status, foreground="#666").grid(row=4, column=0, columnspan=2, sticky="w")

        self.refresh()

    def _clear_search(self):
        self.search_var.set("")
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for p in self.service.list(self.search_var.get()):
            self.tree.insert("", "end", iid=str(p.id), values=(p.id, p.name, p.price, p.stock))

    def on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        item = self.tree.item(iid)
        pid, name, price, stock = item["values"]
        self.current_id = int(pid)
        self.name_var.set(name)
        self.price_var.set(str(price))
        self.stock_var.set(str(stock))

    def clear_form(self):
        self.current_id = None
        self.name_var.set("")
        self.price_var.set("")
        self.stock_var.set("")
        self.tree.selection_remove(self.tree.selection())

    def on_save(self):
        try:
            name = self.name_var.get()
            price = float(self.price_var.get())
            stock = int(self.stock_var.get())
            if self.current_id is None:
                obj = self.service.create(name, price, stock)
                self.status.set(f"Created Product {obj.id}")
            else:
                obj = self.service.update(self.current_id, name, price, stock)
                self.status.set(f"Updated Product {obj.id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.refresh()
        self.clear_form()

    def on_delete(self):
        if self.current_id is None:
            messagebox.showinfo("Delete", "Select a product first.")
            return
        if not messagebox.askyesno("Confirm", f"Delete Product {self.current_id}?"):
            return
        try:
            self.service.delete(self.current_id)
            self.status.set(f"Deleted Product {self.current_id}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return
        self.refresh()
        self.clear_form()