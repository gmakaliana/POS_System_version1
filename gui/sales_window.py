"""
GeoMaka POS Sales Window

File:
modules/sales/sales_window.py

Purpose:
Provide the POS sales interface.

Responsibilities:

- Scan products by barcode.
- Search products.
- Manage shopping cart.
- Calculate totals.
- Apply discounts.
- Accept payment.
- Calculate change.
- Process sales.
- Generate and save receipt.
- Print receipt using XP-80C thermal printer.
- Open BQ400AS cash drawer.
- Manage receipt numbering.
- Handle receipt generation failures safely.
- Handle printer failures safely.
- Handle cash drawer failures safely.
- Never cancel a completed sale because of
  receipt or hardware problems.

Hardware:
Xprinter A160 / XP-80C
80mm Thermal Receipt Printer
BQ400AS Cash Drawer

Windows Printer:
XP-80C

Port:
USB002

Company:
GeoMaka Technologies
"""

import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path


# ==========================================================
# SALES CART
# ==========================================================

from modules.sales.cart import (
    add_product,
    remove_product,
    get_cart_items,
    get_total,
    clear_cart
)


# ==========================================================
# PRODUCT MANAGEMENT
# ==========================================================

from modules.products.product_management import (
    search_products,
    get_product_by_barcode
)


# ==========================================================
# SALES MANAGEMENT
# ==========================================================

from modules.sales.sales_management import (
    process_sale
)


# ==========================================================
# RECEIPT GENERATOR
# ==========================================================

from modules.sales.receipt_generator import (
    generate_receipt
)


# ==========================================================
# HARDWARE
# ==========================================================

from modules.hardware.receipt_printer import (
    open_cash_drawer
)


# ==========================================================
# CENTER WINDOW
# ==========================================================

def center_window(
    window,
    width,
    height
):
    """
    Centers a Tkinter window on the screen.
    """

    x = (
        window.winfo_screenwidth() // 2
        -
        width // 2
    )

    y = (
        window.winfo_screenheight() // 2
        -
        height // 2
    )

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


# ==========================================================
# VALIDATION HELPERS
# ==========================================================

def validate_numeric_input(
    value
):
    """
    Validates numeric Entry input.

    Allows:

    - Empty value
    - Whole numbers
    - Decimal numbers
    """

    if value == "":
        return True

    try:

        if value.count(".") > 1:
            return False

        float(value)

        return True

    except Exception:

        return False


def safe_float(
    value
):
    """
    Safely converts a value to a non-negative float.

    Returns:
        float
    """

    try:

        number = float(value)

        if number >= 0:
            return number

        return 0

    except Exception:

        return 0


# ==========================================================
# SALES WINDOW
# ==========================================================

def open_sales_window(
    user_id,
    role="cashier",
    parent=None
):

    root = tk.Toplevel(
        parent
    )

    root.title(
        "Sales"
    )

    # ======================================================
    # RESIZABLE WINDOW
    # ======================================================

    root.resizable(
        True,
        True
    )

    # ======================================================
    # INITIAL WINDOW SIZE
    # ======================================================

    center_window(
        root,
        1200,
        800
    )

    # ======================================================
    # MINIMUM WINDOW SIZE
    # ======================================================

    root.minsize(
        950,
        650
    )

    # ======================================================
    # FONT SETTINGS
    # ======================================================

    FONT_LABEL = (
        "Arial",
        12
    )

    FONT_ENTRY = (
        "Arial",
        14
    )

    FONT_BUTTON = (
        "Arial",
        12,
        "bold"
    )

    # ------------------------------------------------------
    # CART TABLE FONT
    # ------------------------------------------------------

    FONT_TABLE = (
        "Arial",
        14
    )

    FONT_TABLE_HEADING = (
        "Arial",
        14,
        "bold"
    )

    FONT_TOTAL_LABEL = (
        "Arial",
        13,
        "bold"
    )

    FONT_TOTAL_VALUE = (
        "Arial",
        15,
        "bold"
    )

    FONT_TITLE = (
        "Arial",
        22,
        "bold"
    )

    # ======================================================
    # TREEVIEW STYLE
    # ======================================================

    style = ttk.Style(
        root
    )

    try:

        style.configure(
            "Sales.Treeview",
            font=FONT_TABLE,
            rowheight=38
        )

        style.configure(
            "Sales.Treeview.Heading",
            font=FONT_TABLE_HEADING,
            padding=6
        )

    except Exception:

        pass

    # ======================================================
    # VALIDATION SETUP
    # ======================================================

    vcmd = (
        root.register(
            validate_numeric_input
        ),
        "%P"
    )

    # ======================================================
    # VARIABLES
    # ======================================================

    barcode_var = tk.StringVar()

    search_var = tk.StringVar()

    discount_var = tk.StringVar(
        value="0"
    )

    paid_var = tk.StringVar(
        value="0"
    )

    barcode_entry = None

    # ======================================================
    # TOTALS
    # ======================================================

    def update_totals():

        total = get_total()

        discount = safe_float(
            discount_var.get()
        )

        paid = safe_float(
            paid_var.get()
        )

        # --------------------------------------------------
        # PREVENT DISCOUNT FROM EXCEEDING TOTAL
        # --------------------------------------------------

        if discount > total:

            discount = total

        final = max(
            0,
            total - discount
        )

        change = paid - final

        # --------------------------------------------------
        # TOTAL
        # --------------------------------------------------

        total_label.config(
            text=f"M{total:.2f}"
        )

        # --------------------------------------------------
        # FINAL TOTAL
        # --------------------------------------------------

        final_label.config(
            text=f"M{final:.2f}"
        )

        # --------------------------------------------------
        # CHANGE
        # --------------------------------------------------

        change_label.config(
            text=f"M{change:.2f}",
            fg=(
                "green"
                if paid >= final
                else "red"
            )
        )

    # ======================================================
    # FORCE TOTAL UPDATE
    # ======================================================

    def force_update(
        *args
    ):

        update_totals()

    discount_var.trace_add(
        "write",
        force_update
    )

    paid_var.trace_add(
        "write",
        force_update
    )

    # ======================================================
    # REFRESH CART
    # ======================================================

    def refresh_cart():

        for row in tree.get_children():

            tree.delete(
                row
            )

        for item in get_cart_items():

            tree.insert(
                "",
                "end",
                values=(
                    item["product_name"],
                    item["quantity"],
                    f"M{float(item['unit_price']):.2f}",
                    f"M{float(item['subtotal']):.2f}"
                )
            )

        update_totals()

    # ======================================================
    # ADD PRODUCT BY BARCODE
    # ======================================================

    def add_by_barcode():

        code = barcode_var.get().strip()

        if not code:

            barcode_entry.focus_set()

            return

        product = get_product_by_barcode(
            code
        )

        if not product:

            messagebox.showerror(
                "Product Not Found",
                "Product not found.",
                parent=root
            )

            barcode_var.set("")

            barcode_entry.focus_set()

            return

        success, msg = add_product(
            product[0],
            1
        )

        if not success:

            messagebox.showerror(
                "Error",
                msg,
                parent=root
            )

            barcode_var.set("")

            barcode_entry.focus_set()

            return

        barcode_var.set("")

        refresh_cart()

        barcode_entry.focus_set()

    # ======================================================
    # SEARCH AND ADD PRODUCT
    # ======================================================

    def search_and_add():

        text = search_var.get().strip()

        if not text:

            return

        results = search_products(
            text
        )

        if not results:

            messagebox.showinfo(
                "Product Search",
                "No product found.",
                parent=root
            )

            return

        product = results[0]

        success, msg = add_product(
            product[0],
            1
        )

        if not success:

            messagebox.showerror(
                "Error",
                msg,
                parent=root
            )

            return

        search_var.set("")

        refresh_cart()

        barcode_entry.focus_set()

    # ======================================================
    # REMOVE SELECTED PRODUCT
    # ======================================================

    def remove_selected():

        selected = tree.selection()

        if not selected:

            messagebox.showerror(
                "Error",
                "No product selected.",
                parent=root
            )

            return

        values = tree.item(
            selected[0]
        )["values"]

        product_name = values[0]

        for item in get_cart_items():

            if (
                item["product_name"]
                ==
                product_name
            ):

                remove_product(
                    item["product_id"]
                )

                break

        refresh_cart()

        barcode_entry.focus_set()

    # ======================================================
    # CLEAR AFTER COMPLETED SALE
    # ======================================================

    def reset_sale_screen():

        clear_cart()

        discount_var.set(
            "0"
        )

        paid_var.set(
            "0"
        )

        barcode_var.set("")

        search_var.set("")

        refresh_cart()

        update_totals()

        barcode_entry.focus_set()

    # ======================================================
    # EXIT SALES
    # ======================================================

    def exit_sales():

        clear_cart()

        root.destroy()

        if (
            parent
            and
            parent.winfo_exists()
        ):

            parent.deiconify()

    root.protocol(
        "WM_DELETE_WINDOW",
        exit_sales
    )

    # ======================================================
    # PAY / COMPLETE SALE
    # ======================================================

    def pay():

        # ==================================================
        # GET CART
        # ==================================================

        cart = get_cart_items()

        if not cart:

            messagebox.showerror(
                "Error",
                "Cart is empty.",
                parent=root
            )

            return

        # ==================================================
        # CALCULATE AMOUNTS
        # ==================================================

        total = get_total()

        discount = safe_float(
            discount_var.get()
        )

        paid = safe_float(
            paid_var.get()
        )

        # ==================================================
        # LIMIT DISCOUNT
        # ==================================================

        if discount > total:

            discount = total

            discount_var.set(
                f"{discount:.2f}"
            )

        final = max(
            0,
            total - discount
        )

        change = paid - final

        # ==================================================
        # VALIDATE PAYMENT
        # ==================================================

        if paid <= 0:

            messagebox.showerror(
                "Payment Error",
                "Invalid payment amount.",
                parent=root
            )

            paid_entry.focus()

            return

        if paid < final:

            messagebox.showerror(
                "Insufficient Payment",
                (
                    f"Insufficient payment.\n\n"
                    f"Required: M{final:.2f}\n"
                    f"Paid: M{paid:.2f}"
                ),
                parent=root
            )

            paid_entry.focus()

            return

        # ==================================================
        # CONFIRM SALE
        # ==================================================

        confirm = messagebox.askyesno(
            "Confirm Sale",
            (
                "Complete this sale?\n\n"
                f"Total: M{total:.2f}\n"
                f"Discount: M{discount:.2f}\n"
                f"Final Total: M{final:.2f}\n"
                f"Amount Paid: M{paid:.2f}\n"
                f"Change: M{change:.2f}"
            ),
            parent=root
        )

        if not confirm:

            return

        # ==================================================
        # PROCESS SALE
        # ==================================================

        success, sale_id = process_sale(
            user_id,
            cart,
            discount
        )

        # ==================================================
        # SALE FAILED
        # ==================================================

        if not success:

            messagebox.showerror(
                "Sale Error",
                sale_id,
                parent=root
            )

            return

        # ==================================================
        # SALE IS NOW COMPLETED
        # ==================================================

        receipt_result = None

        receipt_error = None

        # ==================================================
        # GENERATE / SAVE / PRINT RECEIPT
        # ==================================================

        try:

            receipt_result = generate_receipt(
                sale_id=sale_id,
                items=cart,
                total=total,
                discount=discount,
                paid=paid
            )

        except Exception as e:

            receipt_error = str(
                e
            )

        # ==================================================
        # RECEIPT GENERATION / SAVING FAILED
        # ==================================================

        if receipt_error is not None:

            reset_sale_screen()

            messagebox.showwarning(
                "Sale Completed - Receipt Error",
                (
                    "SALE COMPLETED SUCCESSFULLY.\n\n"
                    "However, the receipt could not "
                    "be generated or saved.\n\n"
                    f"Receipt error:\n"
                    f"{receipt_error}\n\n"
                    "The sale has NOT been cancelled."
                ),
                parent=root
            )

            return

        # ==================================================
        # GET SAVED RECEIPT PATH
        # ==================================================

        receipt_path = None

        receipt_saved = False

        if isinstance(
            receipt_result,
            dict
        ):

            receipt_path = (
                receipt_result.get(
                    "path"
                )
                or
                receipt_result.get(
                    "receipt_path"
                )
            )

            receipt_saved = bool(
                receipt_result.get(
                    "saved",
                    receipt_result.get(
                        "success",
                        False
                    )
                )
            )

        elif isinstance(
            receipt_result,
            (str, Path)
        ):

            receipt_path = str(
                receipt_result
            )

        # ==================================================
        # VERIFY RECEIPT FILE
        # ==================================================

        if receipt_path:

            try:

                receipt_saved = (
                    Path(
                        receipt_path
                    ).is_file()
                )

            except Exception:

                receipt_saved = False

        # ==================================================
        # RECEIPT WAS NOT SAVED
        # ==================================================

        if not receipt_saved:

            reset_sale_screen()

            messagebox.showwarning(
                "Sale Completed - Receipt Error",
                (
                    "SALE COMPLETED SUCCESSFULLY.\n\n"
                    "However, the receipt file could "
                    "not be verified.\n\n"
                    "The sale has NOT been cancelled."
                ),
                parent=root
            )

            return

        # ==================================================
        # CASH DRAWER
        # ==================================================

        try:

            open_cash_drawer()

        except Exception:

            pass

        # ==================================================
        # CLEAR COMPLETED SALE
        # ==================================================

        reset_sale_screen()

        # ==================================================
        # SALE COMPLETION MESSAGE
        # ==================================================

        result_message = (
            "Sale completed successfully.\n\n"
            f"Sale ID: {sale_id}\n"
            f"Total: M{final:.2f}\n"
            f"Paid: M{paid:.2f}\n"
            f"Change: M{change:.2f}\n\n"
            "Receipt saved successfully.\n\n"
            f"Saved Receipt:\n"
            f"{receipt_path}"
        )

        messagebox.showinfo(
            "Sale Completed",
            result_message,
            parent=root
        )

    # ======================================================
    # UI HEADER
    # ======================================================

    tk.Label(
        root,
        text="SALES",
        font=FONT_TITLE
    ).pack(
        pady=8
    )

    # ======================================================
    # MAIN CONTENT FRAME
    # ======================================================

    main_frame = tk.Frame(
        root
    )

    main_frame.pack(
        fill="both",
        expand=True,
        padx=15
    )

    # ======================================================
    # INPUT AREA
    # ======================================================

    input_frame = tk.Frame(
        main_frame
    )

    input_frame.pack(
        fill="x",
        pady=8
    )

    # ======================================================
    # INPUT GRID CONFIGURATION
    # ======================================================

    input_frame.columnconfigure(
        1,
        weight=1
    )

    input_frame.columnconfigure(
        4,
        weight=1
    )

    # ======================================================
    # BARCODE LABEL
    # ======================================================

    tk.Label(
        input_frame,
        text="Barcode:",
        font=FONT_LABEL
    ).grid(
        row=0,
        column=0,
        padx=(5, 8),
        pady=5
    )

    # ======================================================
    # BARCODE INPUT
    # ======================================================

    barcode_entry = tk.Entry(
        input_frame,
        textvariable=barcode_var,
        width=28,
        font=FONT_ENTRY
    )

    barcode_entry.grid(
        row=0,
        column=1,
        padx=5,
        pady=5,
        ipady=8,
        sticky="ew"
    )

    barcode_entry.bind(
        "<Return>",
        lambda e: add_by_barcode()
    )

    # ======================================================
    # BARCODE ADD BUTTON
    # ======================================================

    tk.Button(
        input_frame,
        text="ADD",
        bg="#3498db",
        fg="white",
        font=FONT_BUTTON,
        command=add_by_barcode,
        width=8,
        height=1
    ).grid(
        row=0,
        column=2,
        padx=(5, 20),
        pady=5,
        ipadx=5,
        ipady=5
    )

    # ======================================================
    # PRODUCT SEARCH LABEL
    # ======================================================

    tk.Label(
        input_frame,
        text="Search Product:",
        font=FONT_LABEL
    ).grid(
        row=0,
        column=3,
        padx=(5, 8),
        pady=5
    )

    # ======================================================
    # PRODUCT SEARCH INPUT
    # ======================================================

    search_entry = tk.Entry(
        input_frame,
        textvariable=search_var,
        width=28,
        font=FONT_ENTRY
    )

    search_entry.grid(
        row=0,
        column=4,
        padx=5,
        pady=5,
        ipady=8,
        sticky="ew"
    )

    search_entry.bind(
        "<Return>",
        lambda e: search_and_add()
    )

    # ======================================================
    # PRODUCT SEARCH ADD BUTTON
    # ======================================================

    tk.Button(
        input_frame,
        text="ADD",
        bg="#3498db",
        fg="white",
        font=FONT_BUTTON,
        command=search_and_add,
        width=8,
        height=1
    ).grid(
        row=0,
        column=5,
        padx=(5, 5),
        pady=5,
        ipadx=5,
        ipady=5
    )

    # ======================================================
    # CART TABLE CONTAINER
    # ======================================================

    table_frame = tk.Frame(
        main_frame
    )

    table_frame.pack(
        fill="x",
        pady=5
    )

    # ======================================================
    # CART TABLE
    # ======================================================

    tree = ttk.Treeview(
        table_frame,
        columns=(
            "Product",
            "Qty",
            "Price",
            "Subtotal"
        ),
        show="headings",
        height=6,
        style="Sales.Treeview"
    )

    # ======================================================
    # TABLE HEADINGS
    # ======================================================

    tree.heading(
        "Product",
        text="Product"
    )

    tree.heading(
        "Qty",
        text="Quantity"
    )

    tree.heading(
        "Price",
        text="Unit Price"
    )

    tree.heading(
        "Subtotal",
        text="Subtotal"
    )

    # ======================================================
    # TABLE COLUMN CONFIGURATION
    # ======================================================

    tree.column(
        "Product",
        width=430,
        minwidth=250,
        anchor="w",
        stretch=True
    )

    tree.column(
        "Qty",
        width=110,
        minwidth=80,
        anchor="center",
        stretch=False
    )

    tree.column(
        "Price",
        width=170,
        minwidth=120,
        anchor="e",
        stretch=False
    )

    tree.column(
        "Subtotal",
        width=190,
        minwidth=140,
        anchor="e",
        stretch=False
    )

    tree.pack(
        side="left",
        fill="x",
        expand=True
    )

    # ======================================================
    # VERTICAL SCROLLBAR
    # ======================================================

    tree_scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree_scrollbar.pack(
        side="right",
        fill="y"
    )

    tree.configure(
        yscrollcommand=tree_scrollbar.set
    )

    # ======================================================
    # REMOVE BUTTON
    # ======================================================

    tk.Button(
        main_frame,
        text="REMOVE SELECTED PRODUCT",
        bg="#f39c12",
        fg="white",
        font=FONT_BUTTON,
        command=remove_selected,
        width=28,
        height=1
    ).pack(
        pady=(12, 14),
        ipadx=5,
        ipady=5
    )

    # ======================================================
    # SEPARATOR
    # ======================================================

    ttk.Separator(
        main_frame,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=15,
        pady=6
    )

    # ======================================================
    # TOTAL SECTION
    # ======================================================

    total_frame = tk.Frame(
        main_frame
    )

    total_frame.pack(
        fill="x",
        pady=(10, 12)
    )

    # ======================================================
    # TOTAL
    # ======================================================

    tk.Label(
        total_frame,
        text="Total:",
        font=FONT_TOTAL_LABEL
    ).grid(
        row=0,
        column=0,
        padx=(15, 10),
        pady=8
    )

    total_label = tk.Label(
        total_frame,
        width=16,
        relief="solid",
        font=FONT_TOTAL_VALUE,
        anchor="e",
        padx=8
    )

    total_label.grid(
        row=0,
        column=1,
        padx=(0, 45),
        ipady=7
    )

    # ======================================================
    # DISCOUNT
    # ======================================================

    tk.Label(
        total_frame,
        text="Discount:",
        font=FONT_TOTAL_LABEL
    ).grid(
        row=0,
        column=2,
        padx=(10, 10),
        pady=8
    )

    discount_entry = tk.Entry(
        total_frame,
        textvariable=discount_var,
        width=16,
        font=FONT_ENTRY,
        justify="right"
    )

    discount_entry.grid(
        row=0,
        column=3,
        padx=(0, 45),
        ipady=7
    )

    discount_entry.config(
        validate="key",
        validatecommand=vcmd
    )

    # ======================================================
    # FINAL TOTAL
    # ======================================================

    tk.Label(
        total_frame,
        text="Final Total:",
        font=FONT_TOTAL_LABEL
    ).grid(
        row=0,
        column=4,
        padx=(10, 10),
        pady=8
    )

    final_label = tk.Label(
        total_frame,
        width=16,
        relief="solid",
        font=FONT_TOTAL_VALUE,
        anchor="e",
        padx=8
    )

    final_label.grid(
        row=0,
        column=5,
        padx=(0, 15),
        ipady=7
    )

    # ======================================================
    # PAYMENT SEPARATOR
    # ======================================================

    ttk.Separator(
        main_frame,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=15,
        pady=6
    )

    # ======================================================
    # PAYMENT SECTION
    # ======================================================

    pay_frame = tk.Frame(
        main_frame
    )

    pay_frame.pack(
        fill="x",
        pady=(10, 12)
    )

    # ======================================================
    # AMOUNT PAID
    # ======================================================

    tk.Label(
        pay_frame,
        text="Amount Paid:",
        font=FONT_TOTAL_LABEL
    ).grid(
        row=0,
        column=0,
        padx=(15, 12),
        pady=8
    )

    paid_entry = tk.Entry(
        pay_frame,
        textvariable=paid_var,
        width=25,
        font=FONT_ENTRY,
        justify="right"
    )

    paid_entry.grid(
        row=0,
        column=1,
        padx=(0, 80),
        ipady=8
    )

    paid_entry.config(
        validate="key",
        validatecommand=vcmd
    )

    # ======================================================
    # CHANGE
    # ======================================================

    tk.Label(
        pay_frame,
        text="Change:",
        font=FONT_TOTAL_LABEL
    ).grid(
        row=0,
        column=2,
        padx=(10, 12),
        pady=8
    )

    change_label = tk.Label(
        pay_frame,
        width=20,
        relief="solid",
        font=FONT_TOTAL_VALUE,
        anchor="e",
        padx=8
    )

    change_label.grid(
        row=0,
        column=3,
        padx=(0, 15),
        ipady=7
    )

    # ======================================================
    # ACTION SEPARATOR
    # ======================================================

    ttk.Separator(
        main_frame,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=15,
        pady=6
    )

    # ======================================================
    # ACTION BUTTONS
    # ======================================================

    button_frame = tk.Frame(
        main_frame
    )

    button_frame.pack(
        pady=(14, 10)
    )

    # ======================================================
    # PAY
    # ======================================================

    tk.Button(
        button_frame,
        text="PAY",
        bg="green",
        fg="white",
        font=(
            "Arial",
            16,
            "bold"
        ),
        command=pay,
        width=18,
        height=2
    ).grid(
        row=0,
        column=0,
        padx=15
    )

    # ======================================================
    # EXIT
    # ======================================================

    tk.Button(
        button_frame,
        text="EXIT",
        bg="red",
        fg="white",
        font=(
            "Arial",
            16,
            "bold"
        ),
        command=exit_sales,
        width=10,
        height=2
    ).grid(
        row=0,
        column=1,
        padx=15
    )

    # ======================================================
    # INITIALIZE WINDOW
    # ======================================================

    refresh_cart()

    update_totals()

    root.after(
        100,
        lambda: barcode_entry.focus_set()
    )

    return root