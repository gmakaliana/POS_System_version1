"""
GeoMaka POS Receipt Generator

File:
modules/sales/receipt_generator.py

Purpose:
Generate, save, and print a receipt after a successful sale.

Responsibilities:

- Get the next receipt number.
- Load business receipt settings.
- Get the logged-in cashier/admin.
- Generate receipt text.
- Save receipt to the Windows Documents folder.
- Print the receipt using the configured thermal printer.
- Increase the receipt number after successful receipt saving.
- Return the saved receipt path.

Storage:
Documents/
POS System/
receipts/
receipt_1000.txt
receipt_1001.txt
receipt_1002.txt

Company:
GeoMaka Technologies
"""


from datetime import datetime


# ==========================================================
# SETTINGS
# ==========================================================

from modules.settings.settings import (
    get_settings,
    get_next_receipt_number,
    increase_receipt_number
)


# ==========================================================
# APPLICATION PATHS
# ==========================================================

from modules.system.app_paths import (
    get_receipts_directory
)


# ==========================================================
# RECEIPT PRINTER
# ==========================================================

from modules.hardware.receipt_printer import (
    print_receipt
)


# ==========================================================
# SESSION
# ==========================================================

from auth.session import (
    get_session_user
)


# ==========================================================
# SAFE ROW / DICTIONARY VALUE HELPER
# ==========================================================

def get_value(data, key, default=None):

    """
    Safely get a value from either:

    - dict
    - sqlite3.Row
    - other mapping-like objects

    This prevents errors such as:

        sqlite3.Row object has no attribute 'get'
    """

    if data is None:

        return default


    # ------------------------------------------------------
    # Dictionary
    # ------------------------------------------------------

    if isinstance(data, dict):

        return data.get(
            key,
            default
        )


    # ------------------------------------------------------
    # sqlite3.Row / mapping-style object
    # ------------------------------------------------------

    try:

        return data[key]

    except Exception:

        return default


# ==========================================================
# GENERATE RECEIPT
# ==========================================================

def generate_receipt(
    sale_id,
    items,
    total,
    discount,
    paid
):

    """
    Generate, save, and print a receipt.

    The receipt is saved first in:

        Documents/POS System/receipts/

    After the receipt file has been successfully saved,
    the receipt number is increased.

    The receipt is then sent to the configured thermal
    receipt printer.

    Important:

    The sale has already been successfully completed
    before this function is called.

    Therefore, a receipt saving or printing failure
    must NOT cancel the completed sale.

    Returns:

        str:
            Full path to the saved receipt file.

    Raises:

        Exception:
            If the receipt cannot be generated or saved.
    """


    # ======================================================
    # VALIDATE BASIC RECEIPT DATA
    # ======================================================

    if not sale_id:

        raise ValueError(
            "Sale ID is required to generate a receipt."
        )


    if not items:

        raise ValueError(
            "Receipt cannot be generated because "
            "the sale contains no items."
        )


    # ======================================================
    # RECEIPT STORAGE LOCATION
    # ======================================================

    receipt_directory = (
        get_receipts_directory()
    )


    receipt_directory.mkdir(
        parents=True,
        exist_ok=True
    )


    # ======================================================
    # GET RECEIPT NUMBER
    # ======================================================

    receipt_number = (
        get_next_receipt_number()
    )


    # ======================================================
    # RECEIPT FILE
    # ======================================================

    filename = (
        receipt_directory
        /
        f"receipt_{receipt_number}.txt"
    )


    # ======================================================
    # BUSINESS INFORMATION
    # ======================================================

    settings = get_settings()


    if settings:

        business_name = (
            get_value(
                settings,
                "business_name",
                "GeoMaka POS"
            )
            or
            "GeoMaka POS"
        )


        business_address = (
            get_value(
                settings,
                "business_address",
                ""
            )
            or
            ""
        )


        business_phone = (
            get_value(
                settings,
                "business_phone",
                ""
            )
            or
            ""
        )


        business_email = (
            get_value(
                settings,
                "business_email",
                ""
            )
            or
            ""
        )


        receipt_header = (
            get_value(
                settings,
                "receipt_header",
                "SALES RECEIPT"
            )
            or
            "SALES RECEIPT"
        )


        receipt_footer = (
            get_value(
                settings,
                "receipt_footer",
                "Thank you for shopping with us."
            )
            or
            "Thank you for shopping with us."
        )


    else:

        business_name = "GeoMaka POS"

        business_address = ""

        business_phone = ""

        business_email = ""

        receipt_header = "SALES RECEIPT"

        receipt_footer = (
            "Thank you for shopping with us."
        )


    # ======================================================
    # LOGGED-IN USER
    # ======================================================

    user = get_session_user()


    served_by = "Unknown"


    if isinstance(user, dict):

        served_by = (
            user.get("full_name")
            or
            user.get("username")
            or
            user.get("user_name")
            or
            user.get("name")
            or
            "Unknown"
        )


    else:

        try:

            served_by = (
                user["full_name"]
                or
                user["username"]
                or
                user["user_name"]
                or
                user["name"]
                or
                "Unknown"
            )

        except Exception:

            if user:

                served_by = str(user)


    # ======================================================
    # DATE AND TIME
    # ======================================================

    now = datetime.now()


    date_str = now.strftime(
        "%Y-%m-%d"
    )


    time_str = now.strftime(
        "%H:%M:%S"
    )


    # ======================================================
    # CALCULATIONS
    # ======================================================

    final_total = max(
        0,
        total - discount
    )


    change = max(
        0,
        paid - final_total
    )


    # ======================================================
    # SAVE TEXT RECEIPT
    # ======================================================

    try:

        with open(
            filename,
            "w",
            encoding="utf-8"
        ) as file:

            # ==============================================
            # HEADER
            # ==============================================

            file.write(
                "======================================================\n"
            )


            file.write(
                f"{str(business_name).center(54)}\n"
            )


            if business_address:

                file.write(
                    f"{str(business_address).center(54)}\n"
                )


            if business_phone:

                file.write(
                    f"Tel: {business_phone}".center(54)
                    +
                    "\n"
                )


            if business_email:

                file.write(
                    f"{business_email}".center(54)
                    +
                    "\n"
                )


            file.write(
                "------------------------------------------------------\n"
            )


            file.write(
                f"{str(receipt_header).center(54)}\n"
            )


            file.write(
                "======================================================\n"
            )


            # ==============================================
            # SALE INFORMATION
            # ==============================================

            file.write(
                f"Receipt No : {receipt_number}\n"
            )


            file.write(
                f"Sale ID    : {sale_id}\n"
            )


            file.write(
                f"Date       : {date_str}\n"
            )


            file.write(
                f"Time       : {time_str}\n"
            )


            file.write(
                f"Served By  : {served_by}\n"
            )


            file.write(
                "\n"
            )


            # ==============================================
            # PRODUCTS
            # ==============================================

            file.write(
                "------------------------------------------------------\n"
            )


            file.write(
                "PRODUCT                         QTY      AMOUNT (M)\n"
            )


            file.write(
                "------------------------------------------------------\n"
            )


            for item in items:

                product_name = str(
                    get_value(
                        item,
                        "product_name",
                        "Unknown Product"
                    )
                )


                quantity = get_value(
                    item,
                    "quantity",
                    0
                )


                subtotal = get_value(
                    item,
                    "subtotal",
                    0
                )


                name = (
                    product_name[:30]
                    .ljust(30)
                )


                qty = (
                    str(quantity)
                    .rjust(6)
                )


                amount = (
                    f"M{float(subtotal):.2f}"
                    .rjust(12)
                )


                file.write(
                    f"{name}{qty}{amount}\n"
                )


            file.write(
                "------------------------------------------------------\n"
            )


            # ==============================================
            # PAYMENT INFORMATION
            # ==============================================

            file.write(
                f"TOTAL COST      : M{float(total):.2f}\n"
            )


            file.write(
                f"DISCOUNT        : M{float(discount):.2f}\n"
            )


            file.write(
                f"FINAL TOTAL     : M{float(final_total):.2f}\n"
            )


            file.write(
                f"AMOUNT PAID     : M{float(paid):.2f}\n"
            )


            file.write(
                f"CHANGE          : M{float(change):.2f}\n"
            )


            file.write(
                "======================================================\n"
            )


            # ==============================================
            # FOOTER
            # ==============================================

            file.write(
                f"{str(receipt_footer).center(54)}\n\n"
            )


            file.write(
                "Developed By: Mpho George Makaliana\n"
            )


            file.write(
                "Phone : +266 53239121\n"
            )


            file.write(
                "Email : makalianamphogeorge@gmail.com\n"
            )


            file.write(
                "======================================================\n"
            )


    except Exception as e:

        raise Exception(
            "Unable to save receipt file.\n\n"
            f"Receipt path:\n{filename}\n\n"
            f"Error:\n{e}"
        )


    # ======================================================
    # VERIFY RECEIPT FILE EXISTS
    # ======================================================

    if not filename.exists():

        raise Exception(
            "Receipt generation completed without "
            "creating the receipt file."
        )


    # ======================================================
    # INCREASE RECEIPT NUMBER
    # ======================================================

    try:

        increase_receipt_number()


    except Exception as e:

        # --------------------------------------------------
        # Receipt has already been saved successfully.
        # Do not treat the sale as failed.
        # --------------------------------------------------

        print(
            "WARNING: Receipt number could not be increased."
        )

        print(
            f"Receipt number: {receipt_number}"
        )

        print(
            f"Error: {e}"
        )


    # ======================================================
    # PRINT RECEIPT
    # ======================================================

    try:

        print_success, print_message = (
            print_receipt(

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

                items=items,

                total=total,

                discount=discount,

                final_total=final_total,

                paid=paid,

                change=change
            )
        )


    except Exception as e:

        print_success = False

        print_message = str(e)


    # ======================================================
    # PRINT RESULT
    # ======================================================

    if not print_success:

        print(
            "WARNING: Receipt saved but printing failed."
        )

        print(
            f"Receipt: {filename}"
        )

        print(
            f"Printer error: {print_message}"
        )


    # ======================================================
    # RETURN SAVED RECEIPT PATH
    # ======================================================

    return str(filename)