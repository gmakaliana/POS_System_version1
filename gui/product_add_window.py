import tkinter as tk
from tkinter import ttk, messagebox

from modules.products.product_management import add_product
from modules.suppliers.supplier_management import get_all_suppliers

from utils.validation import (
    validate_product_name,
    validate_barcode,
    validate_price,
    validate_quantity
)


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



            # =============================
            # REQUIRED FIELDS
            # =============================

            if not supplier_name:

                messagebox.showerror(
                    "Error",
                    "Select supplier.",
                    parent=root
                )

                return



            if not cost or not sell or not qty:

                messagebox.showerror(
                    "Error",
                    "Cost price, selling price and quantity are required.",
                    parent=root
                )

                return



            # =============================
            # TEXT VALIDATION
            # =============================

            checks = [

                validate_product_name(name),

                validate_barcode(barcode)

            ]


            for valid, message in checks:

                if not valid:

                    messagebox.showerror(
                        "Validation Error",
                        message,
                        parent=root
                    )

                    return



            # =============================
            # NUMBER CONVERSION
            # =============================

            try:

                cost_val = float(cost)

                sell_val = float(sell)

                qty_val = int(qty)


            except ValueError:


                messagebox.showerror(
                    "Invalid Input",
                    "Price must be numbers and quantity must be a whole number.",
                    parent=root
                )

                return



            # =============================
            # NUMERIC VALIDATION
            # =============================

            checks = [

                validate_price(cost_val),

                validate_price(sell_val),

                validate_quantity(qty_val)

            ]


            for valid, message in checks:

                if not valid:

                    messagebox.showerror(
                        "Validation Error",
                        message,
                        parent=root
                    )

                    return



            # =============================
            # SAVE
            # =============================

            add_product(
                name,
                barcode,
                cost_val,
                sell_val,
                qty_val,
                supplier_map[supplier_name]
            )


            refresh_callback()


            messagebox.showinfo(
                "Success",
                "Product added successfully.",
                parent=root
            )


            root.destroy()



        except Exception as e:


            messagebox.showerror(
                "Error",
                str(e),
                parent=root
            )

    tk.Button(
        root,
        text="Save Product",
        bg="#3498db",
        fg="white",
        width=18,
        command=save
    ).pack(pady=15)

    # Press Enter to save settings
    root.bind(
        "<Return>",
        lambda event: save()
    )

    parent.wait_window(root)