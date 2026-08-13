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

from datetime import datetime


# ==========================================================
# SESSION
# ==========================================================

from auth.session import (
    get_session_user
)


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
# SETTINGS
# ==========================================================

from modules.settings.settings import (
    get_setting_value,
    get_next_receipt_number,
    increase_receipt_number
)


# ==========================================================
# HARDWARE
# ==========================================================

from modules.hardware.receipt_printer import (
    print_receipt,
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
# GET CURRENT USER DISPLAY NAME
# ==========================================================

def get_served_by(user_id):

    """
    Gets the name of the currently logged-in user.

    Falls back to the user ID if the session does not
    contain a suitable name field.
    """

    try:

        user = get_session_user()

        if isinstance(user, dict):

            for key in (
                "full_name",
                "username",
                "user_name",
                "name"
            ):

                value = user.get(key)

                if value:

                    return str(value)

        elif user:

            return str(user)

    except Exception:

        pass

    return str(user_id)


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


        # ----------------------------------------------
        # Prevent discount from exceeding total
        # ----------------------------------------------

        if discount > total:

            discount = total


        final = max(
            0,
            total - discount
        )


        change = paid - final


        # ----------------------------------------------
        # TOTAL
        # ----------------------------------------------

        total_label.config(
            text=f"M{total:.2f}"
        )


        # ----------------------------------------------
        # FINAL TOTAL
        # ----------------------------------------------

        final_label.config(
            text=f"M{final:.2f}"
        )


        # ----------------------------------------------
        # CHANGE
        # ----------------------------------------------

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

        # --------------------------------------------------
        # GET CART
        # --------------------------------------------------

        cart = get_cart_items()


        if not cart:

            messagebox.showerror(
                "Error",
                "Cart is empty.",
                parent=root
            )

            return


        # --------------------------------------------------
        # CALCULATE AMOUNTS
        # --------------------------------------------------

        total = get_total()

        discount = safe_float(
            discount_var.get()
        )

        paid = safe_float(
            paid_var.get()
        )


        # --------------------------------------------------
        # LIMIT DISCOUNT
        # --------------------------------------------------

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


        # --------------------------------------------------
        # VALIDATE PAYMENT
        # --------------------------------------------------

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


        # --------------------------------------------------
        # CONFIRM SALE
        # --------------------------------------------------

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


        # --------------------------------------------------
        # PROCESS SALE
        # --------------------------------------------------

        success, sale_id = process_sale(
            user_id,
            cart,
            discount
        )


        if not success:

            messagebox.showerror(
                "Sale Error",
                sale_id,
                parent=root
            )

            return


        # ==================================================
        # GET RECEIPT INFORMATION
        # ==================================================

        try:

            business_name = (
                get_setting_value(
                    "business_name"
                )
                or
                "GeoMaka POS"
            )


            business_address = (
                get_setting_value(
                    "business_address"
                )
                or
                ""
            )


            business_phone = (
                get_setting_value(
                    "business_phone"
                )
                or
                ""
            )


            business_email = (
                get_setting_value(
                    "business_email"
                )
                or
                ""
            )


            receipt_header = (
                get_setting_value(
                    "receipt_header"
                )
                or
                "SALES RECEIPT"
            )


            receipt_footer = (
                get_setting_value(
                    "receipt_footer"
                )
                or
                "Thank you for shopping with us."
            )


            # --------------------------------------------------
            # RECEIPT NUMBER
            # --------------------------------------------------

            receipt_number = (
                get_next_receipt_number()
            )


            # --------------------------------------------------
            # DATE AND TIME
            # --------------------------------------------------

            now = datetime.now()

            date_str = now.strftime(
                "%Y-%m-%d"
            )

            time_str = now.strftime(
                "%H:%M:%S"
            )


            # --------------------------------------------------
            # SERVED BY
            # --------------------------------------------------

            served_by = get_served_by(
                user_id
            )


        except Exception as e:

            messagebox.showerror(
                "Receipt Error",
                (
                    "Sale was completed, "
                    "but receipt information "
                    f"could not be loaded.\n\n{e}"
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
        # PRINT RECEIPT
        # ==================================================

        print_success, print_message = print_receipt(

            business_name=business_name,

            business_address=business_address,

            business_phone=business_phone,

            business_email=business_email,

            receipt_header=receipt_header,

            receipt_footer=receipt_footer,

            served_by=served_by,

            receipt_number=receipt_number,

            date_str=date_str,

            time_str=time_str,

            items=cart,

            total=total,

            discount=discount,

            final_total=final,

            paid=paid,

            change=change
        )


        # ==================================================
        # HANDLE PRINT FAILURE
        # ==================================================

        if not print_success:

            messagebox.showwarning(
                "Receipt Printing Error",
                (
                    "Sale completed successfully.\n\n"
                    "However, the receipt could not be "
                    "printed.\n\n"
                    f"Printer error:\n{print_message}\n\n"
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
        # INCREASE RECEIPT NUMBER
        # ==================================================

        try:

            increase_receipt_number()

        except Exception:

            # Receipt was already printed.
            # Do not tell the cashier that the sale failed.

            pass


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
                    f"Receipt No: {receipt_number}\n"
                    f"Total: M{final:.2f}\n"
                    f"Paid: M{paid:.2f}\n"
                    f"Change: M{change:.2f}\n\n"
                    "Receipt printed successfully.\n"
                    "Cash drawer opened."
                ),
                parent=root
            )

        else:

            messagebox.showwarning(
                "Sale Completed",
                (
                    "Sale completed successfully.\n\n"
                    f"Receipt No: {receipt_number}\n"
                    f"Total: M{final:.2f}\n"
                    f"Paid: M{paid:.2f}\n"
                    f"Change: M{change:.2f}\n\n"
                    "Receipt printed successfully.\n\n"
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


    # ------------------------------------------------------
    # BARCODE
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # PRODUCT SEARCH
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # TOTAL
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # DISCOUNT
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # FINAL TOTAL
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # AMOUNT PAID
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # CHANGE
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # PAY
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # EXIT
    # ------------------------------------------------------

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