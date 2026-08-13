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

def center_window(window, width, height):

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

def validate_numeric_input(value):

    if value == "":
        return True

    try:

        if value.count(".") > 1:
            return False

        float(value)

        return True

    except Exception:

        return False


def safe_float(value):

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

    root = tk.Toplevel(parent)

    root.title("Sales")

    root.resizable(
        False,
        False
    )

    center_window(
        root,
        950,
        650
    )


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

    def force_update(*args):

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

            tree.delete(row)


        for item in get_cart_items():

            tree.insert(
                "",
                "end",
                values=(
                    item["product_name"],
                    item["quantity"],
                    item["unit_price"],
                    item["subtotal"]
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
                "Error",
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
                "Info",
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
                "Error",
                "Invalid payment amount.",
                parent=root
            )

            paid_entry.focus_set()

            return


        if paid < final:

            messagebox.showerror(
                "Error",
                (
                    f"Insufficient payment.\n\n"
                    f"Required: M{final:.2f}\n"
                    f"Paid: M{paid:.2f}"
                ),
                parent=root
            )

            paid_entry.focus_set()

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
        # GENERATE, SAVE AND PRINT RECEIPT
        # ==================================================
        #
        # IMPORTANT:
        #
        # process_sale() has already committed the sale.
        #
        # generate_receipt() is now responsible for:
        #
        # 1. Getting the receipt directory.
        # 2. Creating Documents/POS System/receipts/.
        # 3. Getting the next receipt number.
        # 4. Creating the receipt text file.
        # 5. Saving the receipt.
        # 6. Sending the receipt to the printer.
        # 7. Increasing the receipt number.
        #
        # The sales window must NOT separately handle
        # receipt numbering.
        # ==================================================

        try:

            receipt_path = generate_receipt(
                sale_id=sale_id,
                items=cart,
                total=total,
                discount=discount,
                paid=paid
            )


        except Exception as e:

            # ------------------------------------------------
            # IMPORTANT:
            #
            # The sale has already been committed.
            #
            # Therefore the sale must NOT be cancelled
            # because of a receipt problem.
            # ------------------------------------------------

            messagebox.showwarning(
                "Receipt Error",
                (
                    "Sale completed successfully.\n\n"
                    "However, the receipt could not be "
                    "generated or saved.\n\n"
                    f"Receipt error:\n{e}\n\n"
                    "The sale has NOT been cancelled."
                ),
                parent=root
            )

            clear_cart()

            discount_var.set("0")

            paid_var.set("0")

            barcode_var.set("")

            refresh_cart()

            barcode_entry.focus_set()

            return


        # ==================================================
        # VERIFY RECEIPT PATH
        # ==================================================
        #
        # generate_receipt() should return the actual path
        # of the saved receipt.
        #
        # We verify it here before telling the cashier
        # that the receipt was saved.
        # ==================================================

        receipt_saved = False

        try:

            if receipt_path:

                receipt_saved = (
                    __import__("pathlib")
                    .Path(receipt_path)
                    .is_file()
                )

        except Exception:

            receipt_saved = False


        # ==================================================
        # RECEIPT WAS NOT FOUND
        # ==================================================

        if not receipt_saved:

            messagebox.showwarning(
                "Receipt Warning",
                (
                    "Sale completed successfully.\n\n"
                    "However, the receipt file could not "
                    "be verified in the Documents folder.\n\n"
                    f"Receipt path returned:\n"
                    f"{receipt_path}\n\n"
                    "The sale has NOT been cancelled."
                ),
                parent=root
            )

            clear_cart()

            discount_var.set("0")

            paid_var.set("0")

            barcode_var.set("")

            refresh_cart()

            barcode_entry.focus_set()

            return


        # ==================================================
        # OPEN CASH DRAWER
        # ==================================================

        drawer_success, drawer_message = (
            open_cash_drawer()
        )


        # ==================================================
        # CLEAR CART
        # ==================================================

        clear_cart()

        discount_var.set("0")

        paid_var.set("0")

        barcode_var.set("")


        refresh_cart()

        update_totals()

        barcode_entry.focus_set()


        # ==================================================
        # SUCCESS MESSAGE
        # ==================================================

        if drawer_success:

            messagebox.showinfo(
                "Sale Completed",
                (
                    "Sale completed successfully.\n\n"
                    f"Sale ID: {sale_id}\n"
                    f"Total: M{final:.2f}\n"
                    f"Paid: M{paid:.2f}\n"
                    f"Change: M{change:.2f}\n\n"
                    "Receipt saved and printed successfully.\n\n"
                    f"Saved Receipt:\n"
                    f"{receipt_path}\n\n"
                    "Cash drawer opened."
                ),
                parent=root
            )

        else:

            messagebox.showwarning(
                "Sale Completed",
                (
                    "Sale completed successfully.\n\n"
                    f"Sale ID: {sale_id}\n"
                    f"Total: M{final:.2f}\n"
                    f"Paid: M{paid:.2f}\n"
                    f"Change: M{change:.2f}\n\n"
                    "Receipt saved successfully.\n\n"
                    f"Saved Receipt:\n"
                    f"{receipt_path}\n\n"
                    "WARNING:\n"
                    "Cash drawer could not be opened.\n\n"
                    f"{drawer_message}"
                ),
                parent=root
            )


    # ======================================================
    # UI HEADER
    # ======================================================

    tk.Label(
        root,
        text="SALES",
        font=(
            "Arial",
            18,
            "bold"
        )
    ).pack(
        pady=8
    )


    # ======================================================
    # INPUT AREA
    # ======================================================

    input_frame = tk.Frame(root)

    input_frame.pack(
        pady=10
    )


    # ======================================================
    # BARCODE
    # ======================================================

    tk.Label(
        input_frame,
        text="Barcode:"
    ).grid(
        row=0,
        column=0,
        padx=5
    )


    barcode_entry = tk.Entry(
        input_frame,
        textvariable=barcode_var,
        width=25
    )

    barcode_entry.grid(
        row=0,
        column=1
    )


    barcode_entry.bind(
        "<Return>",
        lambda e: add_by_barcode()
    )


    tk.Button(
        input_frame,
        text="Add",
        bg="#3498db",
        fg="white",
        command=add_by_barcode
    ).grid(
        row=0,
        column=2
    )


    # ======================================================
    # PRODUCT SEARCH
    # ======================================================

    tk.Label(
        input_frame,
        text="Search Product:"
    ).grid(
        row=0,
        column=3,
        padx=10
    )


    search_entry = tk.Entry(
        input_frame,
        textvariable=search_var,
        width=25
    )

    search_entry.grid(
        row=0,
        column=4
    )


    search_entry.bind(
        "<Return>",
        lambda e: search_and_add()
    )


    tk.Button(
        input_frame,
        text="Add",
        bg="#3498db",
        fg="white",
        command=search_and_add
    ).grid(
        row=0,
        column=5
    )


    # ======================================================
    # CART TABLE
    # ======================================================

    tree = ttk.Treeview(
        root,
        columns=(
            "Product",
            "Qty",
            "Price",
            "Subtotal"
        ),
        show="headings",
        height=10
    )


    for column in (
        "Product",
        "Qty",
        "Price",
        "Subtotal"
    ):

        tree.heading(
            column,
            text=column
        )

        tree.column(
            column,
            width=180
        )


    tree.pack(
        pady=10
    )


    # ======================================================
    # REMOVE BUTTON
    # ======================================================

    tk.Button(
        root,
        text="Remove Selected Product",
        bg="#f39c12",
        fg="white",
        command=remove_selected
    ).pack(
        pady=5
    )


    ttk.Separator(
        root,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=20,
        pady=10
    )


    # ======================================================
    # TOTAL SECTION
    # ======================================================

    total_frame = tk.Frame(root)

    total_frame.pack(
        pady=5
    )


    # ======================================================
    # TOTAL
    # ======================================================

    tk.Label(
        total_frame,
        text="Total:"
    ).grid(
        row=0,
        column=0
    )


    total_label = tk.Label(
        total_frame,
        width=20,
        relief="solid"
    )

    total_label.grid(
        row=0,
        column=1
    )


    # ======================================================
    # DISCOUNT
    # ======================================================

    tk.Label(
        total_frame,
        text="Discount:"
    ).grid(
        row=1,
        column=0
    )


    discount_entry = tk.Entry(
        total_frame,
        textvariable=discount_var
    )

    discount_entry.grid(
        row=1,
        column=1
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
        text="Final Total:"
    ).grid(
        row=2,
        column=0
    )


    final_label = tk.Label(
        total_frame,
        width=20,
        relief="solid"
    )

    final_label.grid(
        row=2,
        column=1
    )


    ttk.Separator(
        root,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=20,
        pady=10
    )


    # ======================================================
    # PAYMENT SECTION
    # ======================================================

    pay_frame = tk.Frame(root)

    pay_frame.pack(
        pady=5
    )


    # ======================================================
    # AMOUNT PAID
    # ======================================================

    tk.Label(
        pay_frame,
        text="Amount Paid:"
    ).grid(
        row=0,
        column=0,
        padx=10
    )


    paid_entry = tk.Entry(
        pay_frame,
        textvariable=paid_var,
        width=22
    )

    paid_entry.grid(
        row=0,
        column=1,
        padx=10
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
        text="Change:"
    ).grid(
        row=1,
        column=0,
        padx=10
    )


    change_label = tk.Label(
        pay_frame,
        width=20,
        relief="solid"
    )

    change_label.grid(
        row=1,
        column=1,
        padx=10
    )


    ttk.Separator(
        root,
        orient="horizontal"
    ).pack(
        fill="x",
        padx=20,
        pady=10
    )


    # ======================================================
    # ACTION BUTTONS
    # ======================================================

    button_frame = tk.Frame(root)

    button_frame.pack(
        pady=15
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
            14,
            "bold"
        ),
        command=pay,
        width=15
    ).grid(
        row=0,
        column=0,
        padx=10
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
            14,
            "bold"
        ),
        command=exit_sales,
        width=8
    ).grid(
        row=0,
        column=1,
        padx=10
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
