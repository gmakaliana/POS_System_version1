import tkinter as tk
from tkinter import ttk, messagebox

from modules.products.product_management import update_product
from modules.suppliers.supplier_management import get_all_suppliers


def open_edit_product_window(product_data, refresh_callback):

    root = tk.Toplevel()
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
    if suppliers:
        supplier_combo.set(suppliers[0][1])

    # -----------------------------------
    # UPDATE
    # -----------------------------------
    def update():

        update_product(
            product_id,
            name_entry.get(),
            barcode_entry.get(),
            float(cost_entry.get()),
            float(sell_entry.get()),
            int(qty_entry.get()),
            supplier_map[supplier_combo.get()]
        )

        refresh_callback()
        messagebox.showinfo("Success", "Product updated",parent=root)
        root.destroy()

    tk.Button(
        root,
        text="Update Product",
        bg="#f39c12",
        fg="white",
        width=18,
        command=update
    ).pack(pady=15)