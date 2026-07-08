import tkinter as tk
from tkinter import ttk, messagebox

from modules.products.product_management import (
    get_all_products,
    delete_product
) 

from gui.product_add_window import open_add_product_window
from gui.product_edit_window import open_edit_product_window
from gui.low_stock_window import open_low_stock_window

def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(f"{width}x{height}+{x}+{y}")

# -----------------------------------
# LOW STOCK LIMIT
# -----------------------------------
LOW_STOCK_LIMIT = 5


def open_product_management_window(admin_root):

    admin_root.withdraw()

    root = tk.Toplevel()
    root.title("PRODUCT MANAGEMENT")
    

    root.resizable(True, True)

    center_window(
        root,
        1050,
        500
    )

    # -----------------------------------
    # CLOSE
    # -----------------------------------
    def close_window():
        root.destroy()
        admin_root.deiconify()

    # -----------------------------------
    # TABLE FRAME
    # -----------------------------------
    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    columns = (
        "Name",
        "Barcode",
        "Cost",
        "Selling",
        "Qty",
        "Supplier"
    )

    tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings"
    )

    tree.heading("Name", text="Product Name")
    tree.heading("Barcode", text="Barcode")
    tree.heading("Cost", text="Cost Price (M)")
    tree.heading("Selling", text="Selling Price (M)")
    tree.heading("Qty", text="Quantity")
    tree.heading("Supplier", text="Supplier")

    tree.column("Name", width=200)
    tree.column("Barcode", width=120)
    tree.column("Cost", width=120)
    tree.column("Selling", width=120)
    tree.column("Qty", width=100, anchor="center")
    tree.column("Supplier", width=200)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # -----------------------------------
    # LOAD PRODUCTS
    # -----------------------------------
    def load_products():

        for i in tree.get_children():
            tree.delete(i)

        products = get_all_products()

        for p in products:

            product_id = p[0]
            name = p[1]
            barcode = p[2]
            cost = p[3]
            selling = p[4]
            qty = p[5]
            supplier = p[7]

            tree.insert(
                "",
                "end",
                values=(
                    name,
                    barcode,
                    cost,
                    selling,
                    qty,
                    supplier
                ),
                tags=(product_id,)
            )

    # -----------------------------------
    # GET SELECTED PRODUCT ID
    # -----------------------------------
    def get_selected_id():

        selected = tree.focus()

        if not selected:
            return None

        return tree.item(selected)["tags"][0]

    # -----------------------------------
    # DELETE PRODUCT
    # -----------------------------------
    def delete_selected():

        product_id = get_selected_id()

        if not product_id:
            messagebox.showwarning("Warning", "Select a product")
            return

        if messagebox.askyesno("Confirm", "Delete product?"):
            delete_product(product_id)
            load_products()

    # -----------------------------------
    # EDIT PRODUCT
    # -----------------------------------
    def edit_selected():

        selected = tree.focus()

        if not selected:
            messagebox.showwarning("Warning", "Select a product")
            return

        product_id = get_selected_id()
        values = tree.item(selected)["values"]

        product_data = (
            product_id,
            values[0],  # name
            values[1],  # barcode
            values[2],  # cost
            values[3],  # selling
            values[4],  # qty
            values[5]   # supplier
        )

        open_edit_product_window(product_data, load_products)

    # -----------------------------------
    # LOW STOCK WINDOW
    # -----------------------------------
    def open_low_stock():
        open_low_stock_window(root)

    # -----------------------------------
    # BUTTONS
    # -----------------------------------
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Add Product",
        bg="#3498db",
        fg="white",
        width=14,
        command=lambda: open_add_product_window(load_products)
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Edit Product",
        bg="#f39c12",
        fg="white",
        width=14,
        command=edit_selected
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Low Stock Product",
        bg="#c0392b",
        fg="white",
        width=14,
        command=open_low_stock
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Delete Product",
        bg="#e74c3c",
        fg="white",
        width=14,
        command=delete_selected
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Close",
        bg="#7f8c8d",
        fg="white",
        width=14,
        command=close_window
    ).pack(side="right", padx=5)

    # INITIAL LOAD
    load_products()

    # =====================================
    # WINDOW CONTROL
    # =====================================

    # Handle window X button
    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )