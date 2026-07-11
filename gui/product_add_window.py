import tkinter as tk
from tkinter import ttk, messagebox

from modules.products.product_management import add_product
from modules.suppliers.supplier_management import get_all_suppliers


def open_add_product_window(parent,refresh_callback):

    root = tk.Toplevel(parent)

    root.transient(parent)
    root.grab_set()

    root.title("ADD PRODUCT")
    root.geometry("420x380")

    suppliers = get_all_suppliers()
    supplier_map = {s[1]: s[0] for s in suppliers}

    # -----------------------------------
    # FIELDS
    # -----------------------------------
    tk.Label(root, text="Product Name").pack()
    name_entry = tk.Entry(root, width=35)
    name_entry.pack()

    # Focus username automatically
    name_entry.focus()

    tk.Label(root, text="Barcode").pack()
    barcode_entry = tk.Entry(root, width=35)
    barcode_entry.pack()

    tk.Label(root, text="Cost Price").pack()
    cost_entry = tk.Entry(root, width=35)
    cost_entry.pack()

    tk.Label(root, text="Selling Price").pack()
    sell_entry = tk.Entry(root, width=35)
    sell_entry.pack()

    tk.Label(root, text="Quantity").pack()
    qty_entry = tk.Entry(root, width=35)
    qty_entry.pack()

    tk.Label(root, text="Supplier").pack()

    supplier_combo = ttk.Combobox(
        root,
        values=list(supplier_map.keys()),
        state="readonly",
        width=32
    )
    supplier_combo.pack()

    # -----------------------------------
    # SAVE
    # -----------------------------------
    def save():

        try:
            name = name_entry.get().strip()
            barcode = barcode_entry.get().strip()
            cost = cost_entry.get().strip()
            sell = sell_entry.get().strip()
            qty = qty_entry.get().strip()
            supplier_name = supplier_combo.get()

            # -----------------------------
            # VALIDATION (TEXT FIELDS)
            # -----------------------------
            if not name:
                messagebox.showerror("Error", "Product name is required",parent=root)
                return

            if not supplier_name:
                messagebox.showerror("Error", "Select supplier",parent=root)
                return

            # -----------------------------
            # VALIDATION (NUMERIC FIELDS)
            # -----------------------------
            if not cost or not sell or not qty:
                messagebox.showerror("Error", "Cost, Selling Price and Quantity are required",parent=root)
                return

            # -----------------------------
            # SAFE CONVERSION
            # -----------------------------
            try:
                cost_val = float(cost)
                sell_val = float(sell)
                qty_val = int(qty)
            except ValueError:
                messagebox.showerror("Error", "Cost, Selling Price and Quantity must be numbers",parent=root)
                return

            # -----------------------------
            # SAVE TO DB
            # -----------------------------
            add_product(
                name,
                barcode,
                cost_val,
                sell_val,
                qty_val,
                supplier_map[supplier_name]
            )

            refresh_callback()
            messagebox.showinfo("Success", "Product added successfully",parent=root)
            root.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e),parent=root)

    tk.Button(
        root,
        text="Save Product",
        bg="#3498db",
        fg="white",
        width=18,
        command=save
    ).pack(pady=15)

    parent.wait_window(root)