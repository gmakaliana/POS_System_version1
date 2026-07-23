import tkinter as tk
from tkinter import ttk, messagebox

from modules.products.product_management import update_product
from modules.suppliers.supplier_management import get_all_suppliers

from utils.validation import (
    validate_product_name,
    validate_barcode,
    validate_price,
    validate_quantity
)

def open_edit_product_window(product_data, refresh_callback,parent):

    root = tk.Toplevel(parent)

    root.transient(parent)
    root.grab_set()

    root.title("EDIT PRODUCT")
    root.geometry("420x380")

    product_id = product_data[0]

    suppliers = get_all_suppliers()
    supplier_map = {s[1]: s[0] for s in suppliers}
    reverse_map = {v: k for k, v in supplier_map.items()}

    # -----------------------------------
    # FIELDS
    # -----------------------------------
    tk.Label(root, text="Product Name").pack()
    name_entry = tk.Entry(root, width=35)
    name_entry.pack()
    name_entry.insert(0, product_data[1])

    # Focus username automatically
    name_entry.focus()

    tk.Label(root, text="Barcode").pack()
    barcode_entry = tk.Entry(root, width=35)
    barcode_entry.pack()
    barcode_entry.insert(0, product_data[2])

    tk.Label(root, text="Cost Price").pack()
    cost_entry = tk.Entry(root, width=35)
    cost_entry.pack()
    cost_entry.insert(0, product_data[3])

    tk.Label(root, text="Selling Price").pack()
    sell_entry = tk.Entry(root, width=35)
    sell_entry.pack()
    sell_entry.insert(0, product_data[4])

    tk.Label(root, text="Quantity").pack()
    qty_entry = tk.Entry(root, width=35)
    qty_entry.pack()
    qty_entry.insert(0, product_data[5])

    tk.Label(root, text="Supplier").pack()

    supplier_combo = ttk.Combobox(
        root,
        values=list(supplier_map.keys()),
        state="readonly",
        width=32
    )
    supplier_combo.pack()

    # default supplier not strictly stored in tree, so leave blank or first
    #if suppliers:
    #    supplier_combo.set(suppliers[0][1])

    current_supplier_id = product_data[6]

    if current_supplier_id in reverse_map:

        supplier_combo.set(
            reverse_map[current_supplier_id]
        )


    # -----------------------------------
    # UPDATE
    # -----------------------------------
    def update():

        try:

            name = name_entry.get().strip()
            barcode = barcode_entry.get().strip()
            cost = cost_entry.get().strip()
            sell = sell_entry.get().strip()
            qty = qty_entry.get().strip()
            supplier_name = supplier_combo.get()



            # =============================
            # REQUIRED SUPPLIER
            # =============================

            if not supplier_name:

                messagebox.showerror(
                    "Error",
                    "Select supplier.",
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

                cost_value = float(cost)

                sell_value = float(sell)

                qty_value = int(qty)


            except ValueError:


                messagebox.showerror(
                    "Invalid Input",
                    "Cost price and selling price must be numbers. Quantity must be a whole number.",
                    parent=root
                )

                return



            # =============================
            # NUMERIC VALIDATION
            # =============================

            checks = [

                validate_price(cost_value),

                validate_price(sell_value),

                validate_quantity(qty_value)

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
            # UPDATE DATABASE
            # =============================

            update_product(

                product_id,

                name,

                barcode,

                cost_value,

                sell_value,

                qty_value,

                supplier_map[supplier_name]

            )



            messagebox.showinfo(
                "Success",
                "Product updated successfully.",
                parent=root
            )


            root.destroy()

            refresh_callback()



        except Exception as e:


            messagebox.showerror(
                "Error",
                str(e),
                parent=root
            )

    tk.Button(
        root,
        text="Update Product",
        bg="#f39c12",
        fg="white",
        width=18,
        command=update
    ).pack(pady=15)

    # Press Enter to save settings
    root.bind(
        "<Return>",
        lambda event: update()
    )

    parent.wait_window(root)