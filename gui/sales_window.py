import tkinter as tk
from tkinter import ttk, messagebox

from modules.sales.cart import (
    add_product,
    remove_product,
    get_cart_items,
    get_total,
    clear_cart
)

from modules.products.product_management import (
    search_products,
    get_product_by_barcode
)

from modules.sales.sales_management import process_sale

from modules.sales.receipt_generator import generate_receipt


# -----------------------------------
# CENTER WINDOW
# -----------------------------------
def center_window(window, width, height):
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")


# -----------------------------------
# VALIDATION HELPERS
# -----------------------------------
def validate_numeric_input(value):
    if value == "":
        return True
    try:
        if value.count(".") > 1:
            return False
        float(value)
        return True
    except:
        return False


def safe_float(value):
    try:
        v = float(value)
        return v if v >= 0 else 0
    except:
        return 0


# -----------------------------------
# SALES WINDOW
# -----------------------------------
def open_sales_window(user_id, role="cashier",parent=None):

    root = tk.Toplevel(parent)
    root.title("Sales")
    root.resizable(False, False)

    center_window(root, 950, 650)

    # ===============================
    # VALIDATION SETUP (IMPORTANT FIX)
    # ===============================
    vcmd = (root.register(validate_numeric_input), "%P")

    # -------------------------------
    # VARIABLES
    # -------------------------------
    barcode_var = tk.StringVar()
    search_var = tk.StringVar()
    discount_var = tk.StringVar(value="0")
    paid_var = tk.StringVar(value="0")

    barcode_entry = None

    # ===============================
    # TOTALS
    # ===============================
    def update_totals():

        total = get_total()
        discount = safe_float(discount_var.get())
        paid = safe_float(paid_var.get())

        final = max(0, total - discount)
        change = paid - final

        total_label.config(text=f"M{total:.2f}")
        final_label.config(text=f"M{final:.2f}")

        change_label.config(
            text=f"M{change:.2f}",
            fg="green" if paid >= final else "red"
        )

    def force_update(*args):
        update_totals()

    discount_var.trace_add("write", force_update)
    paid_var.trace_add("write", force_update)

    # -------------------------------
    # REFRESH CART
    # -------------------------------
    def refresh_cart():

        for row in tree.get_children():
            tree.delete(row)

        for item in get_cart_items():
            tree.insert("", "end", values=(
                item["product_name"],
                item["quantity"],
                item["unit_price"],
                item["subtotal"]
            ))

        update_totals()

    # -------------------------------
    # ADD BY BARCODE
    # -------------------------------
    def add_by_barcode():

        code = barcode_var.get().strip()

        if not code:
            barcode_entry.focus_set()
            return

        product = get_product_by_barcode(code)

        if not product:
            messagebox.showerror("Error", "Product not found")
            barcode_var.set("")
            barcode_entry.focus_set()
            return

        success, msg = add_product(product[0], 1)

        if not success:
            messagebox.showerror("Error", msg)

        barcode_var.set("")
        refresh_cart()
        barcode_entry.focus_set()

    # -------------------------------
    # SEARCH
    # -------------------------------
    def search_and_add():

        text = search_var.get().strip()

        if not text:
            return

        results = search_products(text)

        if not results:
            messagebox.showinfo("Info", "No product found")
            return

        product = results[0]

        success, msg = add_product(product[0], 1)

        if not success:
            messagebox.showerror("Error", msg)

        search_var.set("")
        refresh_cart()
        barcode_entry.focus_set()

    # -------------------------------
    # REMOVE
    # -------------------------------
    def remove_selected():

        selected = tree.selection()

        if not selected:
            messagebox.showerror("Error", "No product selected")
            return

        values = tree.item(selected[0])["values"]
        product_name = values[0]

        for item in get_cart_items():
            if item["product_name"] == product_name:
                remove_product(item["product_id"])
                break

        refresh_cart()
        barcode_entry.focus_set()

    # -------------------------------
    # EXIT
    # -------------------------------
    def exit_sales():
        clear_cart()
        root.destroy()

        if parent and parent.winfo_exists():
            parent.deiconify()   # Show dashboard again

    root.protocol(
    "WM_DELETE_WINDOW",
    exit_sales
    )    

    # -------------------------------
    # PAY + RECEIPT
    # -------------------------------
    def pay():

        cart = get_cart_items()

        if not cart:
            messagebox.showerror("Error", "Cart is empty")
            return

        total = get_total()
        discount = safe_float(discount_var.get())
        paid = safe_float(paid_var.get())

        final = max(0, total - discount)

        if paid <= 0:
            messagebox.showerror("Error", "Invalid payment amount")
            return

        if paid < final:
            messagebox.showerror(
                "Error",
                f"Insufficient payment. Required: M{final:.2f}"
            )
            return

        success, sale_id = process_sale(user_id, cart, discount)

        if not success:
            messagebox.showerror("Error", sale_id)
            return

        receipt_file = generate_receipt(
            sale_id,
            cart,
            total,
            discount,
            paid
        )

        messagebox.showinfo(
            "Success",
            f"Sale completed successfully!\nReceipt saved:\n{receipt_file}"
        )

        clear_cart()
        discount_var.set("0")
        paid_var.set("0")
        barcode_var.set("")

        refresh_cart()
        update_totals()
        barcode_entry.focus_set()

    # ===============================
    # UI HEADER
    # ===============================
    tk.Label(root, text="SALES", font=("Arial", 18, "bold")).pack(pady=8)

    tk.Button(
        root,
        text="EXIT",
        bg="red",
        fg="white",
        command=exit_sales
    ).place(x=880, y=10)

    # ===============================
    # INPUT AREA
    # ===============================
    input_frame = tk.Frame(root)
    input_frame.pack(pady=10)

    tk.Label(input_frame, text="Barcode:").grid(row=0, column=0, padx=5)

    barcode_entry = tk.Entry(input_frame, textvariable=barcode_var, width=25)
    barcode_entry.grid(row=0, column=1)
    barcode_entry.bind("<Return>", lambda e: add_by_barcode())

    tk.Button(input_frame, text="Add", command=add_by_barcode).grid(row=0, column=2)

    tk.Label(input_frame, text="Search Product:").grid(row=0, column=3, padx=10)

    search_entry = tk.Entry(input_frame, textvariable=search_var, width=25)
    search_entry.grid(row=0, column=4)
    search_entry.bind("<Return>", lambda e: search_and_add())

    tk.Button(input_frame, text="Add", command=search_and_add).grid(row=0, column=5)

    # ===============================
    # TABLE
    # ===============================
    tree = ttk.Treeview(
        root,
        columns=("Product", "Qty", "Price", "Subtotal"),
        show="headings",
        height=10
    )

    for c in ("Product", "Qty", "Price", "Subtotal"):
        tree.heading(c, text=c)
        tree.column(c, width=180)

    tree.pack(pady=10)

    tk.Button(root, text="Remove Selected Product", command=remove_selected).pack(pady=5)

    ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=10)

    # ===============================
    # TOTAL SECTION
    # ===============================
    total_frame = tk.Frame(root)
    total_frame.pack(pady=5)

    tk.Label(total_frame, text="Total:").grid(row=0, column=0)
    total_label = tk.Label(total_frame, width=20, relief="solid")
    total_label.grid(row=0, column=1)

    tk.Label(total_frame, text="Discount:").grid(row=1, column=0)

    discount_entry = tk.Entry(total_frame, textvariable=discount_var)
    discount_entry.grid(row=1, column=1)
    discount_entry.config(validate="key", validatecommand=vcmd)

    tk.Label(total_frame, text="Final Total:").grid(row=2, column=0)
    final_label = tk.Label(total_frame, width=20, relief="solid")
    final_label.grid(row=2, column=1)

    ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=10)

    # ===============================
    # PAYMENT
    # ===============================
    pay_frame = tk.Frame(root)
    pay_frame.pack(pady=5)

    tk.Label(pay_frame, text="Amount Paid:").grid(row=0, column=0, padx=10)

    paid_entry = tk.Entry(pay_frame, textvariable=paid_var, width=22)
    paid_entry.grid(row=0, column=1, padx=10)
    paid_entry.config(validate="key", validatecommand=vcmd)

    tk.Label(pay_frame, text="Change:").grid(row=1, column=0, padx=10)

    change_label = tk.Label(pay_frame, width=20, relief="solid")
    change_label.grid(row=1, column=1, padx=10)

    ttk.Separator(root, orient="horizontal").pack(fill="x", padx=20, pady=10)

    # ===============================
    # PAY BUTTON
    # ===============================
    tk.Button(
        root,
        text="PAY",
        bg="green",
        fg="white",
        font=("Arial", 14, "bold"),
        command=pay,
        width=15
    ).pack(pady=15)

    root.after(100, lambda: barcode_entry.focus_set())

    return root