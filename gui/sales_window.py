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
# WINDOW POSITIONING
# ==========================================================

def position_sales_window(
    window,
    width,
    height
):
    """
    Positions the Sales window horizontally centered
    and near the top of the screen.

    This gives the POS window a consistent opening
    position instead of placing it vertically in the
    middle of the screen.
    """

    screen_width = (
        window.winfo_screenwidth()
    )

    # ------------------------------------------------------
    # Horizontal center
    # ------------------------------------------------------

    x = (
        screen_width // 2
        -
        width // 2
    )

    # ------------------------------------------------------
    # Small top margin
    # ------------------------------------------------------

    y = 40

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
    # WINDOW SIZE / POSITION
    # ======================================================

    # The window is intentionally wide enough for the
    # barcode/search area and totals section.
    #
    # The height is reduced so there is no large unused
    # area below the PAY / EXIT buttons.

    SALES_WIDTH = 1100
    SALES_HEIGHT = 610

    position_sales_window(
        root,
        SALES_WIDTH,
        SALES_HEIGHT
    )

    # ======================================================
    # RESIZABLE WINDOW
    # ======================================================

    root.resizable(
        True,
        True
    )

    # ======================================================
    # MINIMUM WINDOW SIZE
    # ======================================================

    root.minsize(
        900,
        580
    )

    # ======================================================
    # FONT SETTINGS
    # ======================================================

    FONT_LABEL = (
        "Arial",
        10
    )

    FONT_ENTRY = (
        "Arial",
        11
    )

    FONT_BUTTON = (
        "Arial",
        10,
        "bold"
    )

    FONT_TABLE = (
        "Arial",
        10
    )

    FONT_TABLE_HEADING = (
        "Arial",
        10,
        "bold"
    )

    FONT_TOTAL_LABEL = (
        "Arial",
        11,
        "bold"
    )

    FONT_TOTAL_VALUE = (
        "Arial",
        12,
        "bold"
    )

    FONT_TITLE = (
        "Arial",
        17,
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
            rowheight=25
        )

        style.configure(
            "Sales.Treeview.Heading",
            font=FONT_TABLE_HEADING,
            padding=3
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
        # SALE COMPLETED
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
        pady=(8, 6)
    )

    # ======================================================
    # MAIN CONTENT FRAME
    # ======================================================

    main_frame = tk.Frame(
        root
    )

    main_frame.pack(
        fill="x",
        padx=10,
        pady=(0, 2)
    )

    # ======================================================
    # INPUT AREA
    # ======================================================

    input_frame = tk.Frame(
        main_frame
    )

    input_frame.pack(
        fill="x",
        pady=(2, 8)
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
    # BARCODE
    # ======================================================

    tk.Label(
        input_frame,
        text="Barcode:",
        font=FONT_LABEL
    ).grid(
        row=0,
        column=0,
        padx=(3, 5),
        pady=3
    )

    barcode_entry = tk.Entry(
        input_frame,
        textvariable=barcode_var,
        width=20,
        font=FONT_ENTRY
    )

    barcode_entry.grid(
        row=0,
        column=1,
        padx=3,
        pady=3,
        ipady=4,
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
        width=5,
        height=1
    ).grid(
        row=0,
        column=2,
        padx=(3, 18),
        pady=3,
        ipadx=2,
        ipady=2
    )

    # ======================================================
    # SEARCH
    # ======================================================

    tk.Label(
        input_frame,
        text="Search:",
        font=FONT_LABEL
    ).grid(
        row=0,
        column=3,
        padx=(3, 5),
        pady=3
    )

    search_entry = tk.Entry(
        input_frame,
        textvariable=search_var,
        width=20,
        font=FONT_ENTRY
    )

    search_entry.grid(
        row=0,
        column=4,
        padx=3,
        pady=3,
        ipady=4,
        sticky="ew"
    )

    search_entry.bind(
        "<Return>",
        lambda e: search_and_add()
    )

    # ======================================================
    # SEARCH ADD BUTTON
    # ======================================================

    tk.Button(
        input_frame,
        text="ADD",
        bg="#3498db",
        fg="white",
        font=FONT_BUTTON,
        command=search_and_add,
        width=5,
        height=1
    ).grid(
        row=0,
        column=5,
        padx=(3, 3),
        pady=3,
        ipadx=2,
        ipady=2
    )

    # ======================================================
    # CART TABLE
    # ======================================================

    table_frame = tk.Frame(
        main_frame
    )

    table_frame.pack(
        fill="x",
        pady=(2, 6)
    )

    tree = ttk.Treeview(
        table_frame,
        columns=(
            "Product",
            "Qty",
            "Price",
            "Subtotal"
        ),
        show="headings",
        height=8,
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
        width=390,
        minwidth=220,
        anchor="w",
        stretch=True
    )

    tree.column(
        "Qty",
        width=80,
        minwidth=60,
        anchor="center",
        stretch=False
    )

    tree.column(
        "Price",
        width=130,
        minwidth=100,
        anchor="e",
        stretch=False
    )

    tree.column(
        "Subtotal",
        width=150,
        minwidth=110,
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
    # REMOVE SELECTED
    # ======================================================

    tk.Button(
        main_frame,
        text="REMOVE SELECTED",
        bg="#f39c12",
        fg="white",
        font=FONT_BUTTON,
        command=remove_selected,
        width=20,
        height=1
    ).pack(
        pady=(8, 0),
        ipadx=3,
        ipady=4
    )

    # ======================================================
    # HORIZONTAL LINE BELOW REMOVE SELECTED
    # ======================================================

    ttk.Separator(
        main_frame,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=5,
        pady=(14, 10)
    )

    # ======================================================
    # TOTAL / DISCOUNT / FINAL TOTAL
    # ======================================================

    total_center = tk.Frame(
        main_frame
    )

    total_center.pack(
        pady=0
    )

    total_frame = tk.Frame(
        total_center
    )

    total_frame.pack()

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
        padx=(10, 8),
        pady=5
    )

    total_label = tk.Label(
        total_frame,
        width=12,
        relief="solid",
        font=FONT_TOTAL_VALUE,
        anchor="e",
        padx=6
    )

    total_label.grid(
        row=0,
        column=1,
        padx=(0, 35),
        ipady=4
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
        padx=(5, 8),
        pady=5
    )

    discount_entry = tk.Entry(
        total_frame,
        textvariable=discount_var,
        width=12,
        font=FONT_ENTRY,
        justify="right"
    )

    discount_entry.grid(
        row=0,
        column=3,
        padx=(0, 35),
        ipady=4
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
        padx=(5, 8),
        pady=5
    )

    final_label = tk.Label(
        total_frame,
        width=12,
        relief="solid",
        font=FONT_TOTAL_VALUE,
        anchor="e",
        padx=6
    )

    final_label.grid(
        row=0,
        column=5,
        padx=(0, 10),
        ipady=4
    )

    # ======================================================
    # HORIZONTAL LINE BELOW TOTAL SECTION
    # ======================================================

    ttk.Separator(
        main_frame,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=5,
        pady=(14, 10)
    )

    # ======================================================
    # AMOUNT PAID / CHANGE
    # ======================================================

    pay_center = tk.Frame(
        main_frame
    )

    pay_center.pack(
        pady=0
    )

    pay_frame = tk.Frame(
        pay_center
    )

    pay_frame.pack()

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
        padx=(10, 8),
        pady=5
    )

    paid_entry = tk.Entry(
        pay_frame,
        textvariable=paid_var,
        width=14,
        font=FONT_ENTRY,
        justify="right"
    )

    paid_entry.grid(
        row=0,
        column=1,
        padx=(0, 25),
        ipady=4
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
        padx=(5, 8),
        pady=5
    )

    change_label = tk.Label(
        pay_frame,
        width=14,
        relief="solid",
        font=FONT_TOTAL_VALUE,
        anchor="e",
        padx=6
    )

    change_label.grid(
        row=0,
        column=3,
        padx=(0, 10),
        ipady=4
    )

    # ======================================================
    # HORIZONTAL LINE ABOVE PAY / EXIT
    # ======================================================

    ttk.Separator(
        main_frame,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=5,
        pady=(16, 10)
    )

    # ======================================================
    # PAY / EXIT BUTTONS
    # ======================================================

    button_frame = tk.Frame(
        main_frame
    )

    button_frame.pack(
        pady=(0, 0)
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
            12,
            "bold"
        ),
        command=pay,
        width=14,
        height=1
    ).grid(
        row=0,
        column=0,
        padx=5,
        ipadx=3,
        ipady=4
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
            12,
            "bold"
        ),
        command=exit_sales,
        width=8,
        height=1
    ).grid(
        row=0,
        column=1,
        padx=5,
        ipadx=3,
        ipady=4
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