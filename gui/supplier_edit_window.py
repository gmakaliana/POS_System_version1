import tkinter as tk
from tkinter import messagebox

from modules.suppliers.supplier_management import (
    update_supplier
)


def open_edit_supplier_window(
        supplier_data,
        refresh_callback
):

    supplier_id = supplier_data[0]

    root = tk.Toplevel()
    root.title("EDIT SUPPLIER")
    root.geometry("400x280")
    root.resizable(False, False)

    # -----------------------------------
    # NAME
    # -----------------------------------
    tk.Label(root, text="Supplier Name").pack(pady=(15, 0))

    supplier_entry = tk.Entry(root, width=35)
    supplier_entry.pack()
    supplier_entry.insert(0, supplier_data[1])

    # -----------------------------------
    # PHONE
    # -----------------------------------
    tk.Label(root, text="Phone Number").pack(pady=(10, 0))

    phone_entry = tk.Entry(root, width=35)
    phone_entry.pack()
    phone_entry.insert(0, supplier_data[2])

    # -----------------------------------
    # ADDRESS
    # -----------------------------------
    tk.Label(root, text="Address").pack(pady=(10, 0))

    address_entry = tk.Entry(root, width=35)
    address_entry.pack()
    address_entry.insert(0, supplier_data[3])

    # -----------------------------------
    # UPDATE
    # -----------------------------------
    def update():

        supplier_name = supplier_entry.get().strip()
        phone = phone_entry.get().strip()
        address = address_entry.get().strip()

        if not supplier_name:
            messagebox.showerror(
                "Error",
                "Supplier name is required."
            )
            return

        try:

            update_supplier(
                supplier_id,
                supplier_name,
                phone,
                address
            )

            refresh_callback()

            messagebox.showinfo(
                "Success",
                "Supplier updated successfully."
            )

            root.destroy()

        except Exception as e:
            messagebox.showerror(
                "Error",
                str(e)
            )

    tk.Button(
        root,
        text="Update Supplier",
        bg="#f39c12",
        fg="white",
        width=18,
        command=update
    ).pack(pady=20)