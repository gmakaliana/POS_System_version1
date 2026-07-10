import tkinter as tk
from tkinter import ttk, messagebox

from modules.inventory.stock_alerts import get_low_stock_product_details

from modules.settings.settings import get_low_stock_threshold

# -----------------------------------
# LOW STOCK WINDOW
# -----------------------------------
def open_low_stock_window(parent):

    parent.withdraw()

    root = tk.Toplevel()
    root.title("LOW STOCK PRODUCTS")
    
    threshold = get_low_stock_threshold()

    ttk.Label(
        root,
        text=f"Low Stock Threshold: {threshold}",
        font=("Arial", 10, "bold")
    ).pack(
        pady=5
    )
    
    root.geometry("900x450")
    root.resizable(False, False)

    # -----------------------------------
    # CLOSE WINDOW
    # -----------------------------------
    def close_window():
        root.destroy()
        parent.deiconify()

    root.protocol("WM_DELETE_WINDOW", close_window)

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

    # -----------------------------------
    # HEADERS
    # -----------------------------------
    tree.heading("Name", text="Product Name")
    tree.heading("Barcode", text="Barcode")
    tree.heading("Cost", text="Cost Price (M)")
    tree.heading("Selling", text="Selling Price (M)")
    tree.heading("Qty", text="Quantity")
    tree.heading("Supplier", text="Supplier")

    # -----------------------------------
    # COLUMN SIZES
    # -----------------------------------
    tree.column("Name", width=200)
    tree.column("Barcode", width=130)
    tree.column("Cost", width=120)
    tree.column("Selling", width=120)
    tree.column("Qty", width=90, anchor="center")
    tree.column("Supplier", width=200)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # -----------------------------------
    # TAGS (RED FOR LOW STOCK)
    # -----------------------------------
    tree.tag_configure("low_stock", foreground="red")

    # -----------------------------------
    # LOAD DATA
    # -----------------------------------
    def load_low_stock_products():

        for item in tree.get_children():
            tree.delete(item)

        products = get_low_stock_product_details()

        if not products:
            messagebox.showinfo("Low Stock", "No low stock products found.",parent=root)
            return

        for p in products:

            product_id = p[0]
            name = p[1]
            barcode = p[2]
            cost = p[3]
            selling = p[4]
            qty = p[5]
            supplier = p[6]

            tags = ("low_stock",)

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
                tags=tags
            )

    # -----------------------------------
    # BUTTONS
    # -----------------------------------
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", padx=10, pady=10)

    tk.Button(
        btn_frame,
        text="Refresh",
        bg="#3498db",
        fg="white",
        width=12,
        command=load_low_stock_products
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Close",
        bg="#7f8c8d",
        fg="white",
        width=12,
        command=close_window
    ).pack(side="right", padx=5)

    # -----------------------------------
    # INITIAL LOAD
    # -----------------------------------
    load_low_stock_products()

    