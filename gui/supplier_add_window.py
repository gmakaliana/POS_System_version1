import tkinter as tk
from tkinter import messagebox

from modules.suppliers.supplier_management import add_supplier


def open_add_supplier_window(refresh_callback):

    root = tk.Toplevel()
    root.title("ADD SUPPLIER")
    root.geometry("400x280")
    root.resizable(False, False)

    # -----------------------------------
    # LABELS
    # -----------------------------------
    tk.Label(root, text="Supplier Name").pack(pady=(15, 0))
    supplier_entry = tk.Entry(root, width=35)
    supplier_entry.pack()

    # Focus username automatically
    supplier_entry.focus()

    tk.Label(root, text="Phone Number").pack(pady=(10, 0))
    phone_entry = tk.Entry(root, width=35)
    phone_entry.pack()

    tk.Label(root, text="Address").pack(pady=(10, 0))
    address_entry = tk.Entry(root, width=35)
    address_entry.pack()

    # -----------------------------------
    # SAVE
    # -----------------------------------
    def save_supplier():

        supplier_name = supplier_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()

        if not supplier_name:
            messagebox.showerror(
                "Error",
                "Supplier name is required.",parent=root
            )
            return

        try:

            add_supplier(
                supplier_name,
                phone,
                address
            )

            refresh_callback()

            messagebox.showinfo(
                "Success",
                "Supplier added successfully.",parent=root
            )

            root.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e),parent=root
            )

    tk.Button(
        root,
        text="Save Supplier",
        bg="#3498db",
        fg="white",
        width=18,
        command=save_supplier
    ).pack(pady=20)