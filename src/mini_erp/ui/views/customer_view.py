from __future__ import annotations
import tkinter as tk
from tkinter import ttk, messagebox
from sqlalchemy.orm import Session
from ...services.customer_service import CustomerService


class CustomerView(ttk.Frame):
    def __init__(self, master: tk.Tk, session: Session):
        super().__init__(master, padding=12)
        self.service = CustomerService(session)
        self.current_id: int | None = None

        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=1)

        self._build_left()
        self._build_right()
        self.refresh()

    # Left side: search + table
    def _build_left(self):
        left = ttk.Frame(self)

        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        left.columnconfigure(0, weight=1)
        left.rowconfigure(1, weight=1)

        top = ttk.Frame(left)
        top.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top.columnconfigure(0, weight=1)
        self.search_var = tk.StringVar()
        ent = ttk.Entry(top, textvariable=self.search_var)
        ent.grid(row=0, column=0, sticky="ew")
        ent.bind("<Return>", lambda e: self.refresh())
        ttk.Button(top, text="Search", command=self.refresh).grid(row=0, column=1, padx=6)
        ttk.Button(top, text="Clear", command=self._clear_search).grid(row=0, column=2)

        cols = ("id", "name", "email", "phone")
        self.tree = ttk.Treeview(left, columns=cols, show="headings", height=18)
        self.tree.grid(row=1, column=0, sticky="nsew")
        for c, w in zip(cols, (60, 200, 260, 160)):
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, width=w, anchor="w")
        yscroll = ttk.Scrollbar(left, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=yscroll.set)
        yscroll.grid(row=1, column=1, sticky="ns")
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    # Right side: form + buttons
    def _build_right(self):
        right = ttk.LabelFrame(self, text="Customer Details")
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(1, weight=1)


        ttk.Label(right, text="Name").grid(row=0, column=0, sticky="w", pady=(6, 2))
        self.name_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.name_var).grid(row=0, column=1, sticky="ew", padx=(0, 6))


        ttk.Label(right, text="Email").grid(row=1, column=0, sticky="w", pady=2)
        self.email_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.email_var).grid(row=1, column=1, sticky="ew", padx=(0, 6))


        ttk.Label(right, text="Phone").grid(row=2, column=0, sticky="w", pady=2)
        self.phone_var = tk.StringVar()
        ttk.Entry(right, textvariable=self.phone_var).grid(row=2, column=1, sticky="ew", padx=(0, 6))


        btns = ttk.Frame(right)
        btns.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(12, 0))
        for i in range(4):
            btns.columnconfigure(i, weight=1)
        ttk.Button(btns, text="New", command=self.clear_form).grid(row=0, column=0, padx=4)
        ttk.Button(btns, text="Save", command=self.on_save).grid(row=0, column=1, padx=4)
        ttk.Button(btns, text="Delete", command=self.on_delete).grid(row=0, column=2, padx=4)
        ttk.Button(btns, text="Refresh", command=self.refresh).grid(row=0, column=3, padx=4)


        self.status = tk.StringVar(value="Ready")
        ttk.Label(right, textvariable=self.status, foreground="#666").grid(row=5, column=0, columnspan=2, sticky="w", pady=(10, 0))

    def _clear_search(self):
        self.search_var.set("")
        self.refresh()

    def refresh(self):
        self.tree.delete(*self.tree.get_children())

        for c in self.service.list(self.search_var.get()):
            self.tree.insert("", "end", iid=str(c.id), values=(c.id, c.name, c.email, c.phone))
        if s := self.search_var.get().strip():
            self.status.set(f"Loaded customers (filter: {s})")
        else:
            self.status.set("Loaded customers")

    def on_select(self, event=None):
        sel = self.tree.selection()
        if not sel:
            return
        iid = sel[0]
        item = self.tree.item(iid)
        cid, name, email, phone = item["values"]
        self.current_id = int(cid)
        self.name_var.set(name)
        self.email_var.set(email)
        self.phone_var.set(phone)
        self.status.set(f"Selected ID {cid}")

    def clear_form(self):
        self.current_id = None
        self.name_var.set("")
        self.email_var.set("")
        self.phone_var.set("")
        self.tree.selection_remove(self.tree.selection())
        self.status.set("New record")

    def on_save(self):
        name, email, phone = self.name_var.get(), self.email_var.get(), self.phone_var.get()

        try:
            if self.current_id is None:
                obj = self.service.create(name, email, phone)
                self.status.set(f"Created ID {obj.id}")
            else:
                obj = self.service.update(self.current_id, name, email, phone)
                self.status.set(f"Updated ID {obj.id}")
        except ValueError as e:
            messagebox.showerror("Validation", str(e))
            return
        self.refresh()
        self.clear_form()

    def on_delete(self):
        if self.current_id is None:
            messagebox.showinfo("Delete", "Select a customer to delete.")
            return
        from tkinter import messagebox as m
        if not m.askyesno("Confirm", f"Delete customer ID {self.current_id}?"):
            return
        try:
            self.service.delete(self.current_id)
            self.status.set(f"Deleted ID {self.current_id}")
        except ValueError as e:
            messagebox.showerror("Delete", str(e))
            return
        self.refresh()
        self.clear_form()