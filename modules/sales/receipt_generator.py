"""
GeoMaka POS Receipt Generator

File:
modules/sales/receipt_generator.py

Purpose:
Generate and save a receipt after a successful sale.

Responsibilities:

- Get the next receipt number.
- Load business receipt settings.
- Get the logged-in cashier/admin.
- Generate receipt text.
- Save receipt to the Windows Documents folder.
- Send the receipt to the configured thermal printer.
- Increase the receipt number after successful receipt saving.
- Never allow printer failure to cancel a completed sale.

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
# ROW / DICTIONARY HELPER
# ==========================================================

def get_value(
    data,
    key,
    default=None
):
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


    # ======================================================
    # DICTIONARY
    # ======================================================

    if isinstance(
        data,
        dict
    ):

        return data.get(
            key,
            default
        )


    # ======================================================
    # SQLITE3.ROW / MAPPING-LIKE OBJECT
    # ======================================================

    try:

        return data[key]

    except (
        KeyError,
        IndexError,
        TypeError
    ):

        return default

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
    Generate, save, and send a receipt to the printer.

    The receipt is saved first in:

        Documents/POS System/receipts/

    After the receipt file has been successfully saved,
    the receipt number is increased.

    The receipt is then sent to the configured thermal
    printer.

    IMPORTANT:

    The sale has already been successfully completed
    before this function is called.

    Printer problems MUST NEVER cancel the sale.

    Printer status is deliberately NOT returned to the
    sales window.

    The receipt file is the authoritative receipt record.

    Returns:

        dict:
            {
                "success": True,
                "saved": True,
                "path": "...",
                "receipt_path": "...",
                "receipt_number": ...
            }

    Raises:

        Exception:
            Only when the receipt itself cannot be
            generated or saved.
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


    # ------------------------------------------------------
    # Create directory if it does not exist
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Receipt filename
    # ------------------------------------------------------

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

        business_name = get_value(
            settings,
            "business_name",
            "GeoMaka POS"
        )


        business_address = get_value(
            settings,
            "business_address",
            ""
        )


        business_phone = get_value(
            settings,
            "business_phone",
            ""
        )


        business_email = get_value(
            settings,
            "business_email",
            ""
        )


        receipt_header = get_value(
            settings,
            "receipt_header",
            "SALES RECEIPT"
        )


        receipt_footer = get_value(
            settings,
            "receipt_footer",
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
    # PROTECT AGAINST NULL SETTINGS
    # ======================================================

    business_name = (
        business_name
        or
        "GeoMaka POS"
    )


    business_address = (
        business_address
        or
        ""
    )


    business_phone = (
        business_phone
        or
        ""
    )


    business_email = (
        business_email
        or
        ""
    )


    receipt_header = (
        receipt_header
        or
        "SALES RECEIPT"
    )


    receipt_footer = (
        receipt_footer
        or
        "Thank you for shopping with us."
    )


    # ======================================================
    # LOGGED-IN USER
    # ======================================================

    user = get_session_user()


    served_by = "Unknown"


    if user:

        served_by = (
            get_value(
                user,
                "full_name"
            )
            or
            get_value(
                user,
                "username"
            )
            or
            get_value(
                user,
                "user_name"
            )
            or
            get_value(
                user,
                "name"
            )
            or
            "Unknown"
        )


        if served_by == "Unknown":

            served_by = str(
                user
            )


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


                # ------------------------------------------
                # Safely convert numeric values
                # ------------------------------------------

                try:

                    quantity = float(
                        quantity
                    )

                except Exception:

                    quantity = 0


                try:

                    subtotal = float(
                        subtotal
                    )

                except Exception:

                    subtotal = 0


                # ------------------------------------------
                # Display quantity
                # ------------------------------------------

                if quantity.is_integer():

                    quantity_display = str(
                        int(quantity)
                    )

                else:

                    quantity_display = str(
                        quantity
                    )


                name = (
                    product_name[:30]
                    .ljust(30)
                )


                qty = (
                    quantity_display.rjust(6)
                )


                amount = (
                    f"M{subtotal:.2f}"
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
                f"TOTAL COST      : M{total:.2f}\n"
            )


            file.write(
                f"DISCOUNT        : M{discount:.2f}\n"
            )


            file.write(
                f"FINAL TOTAL     : M{final_total:.2f}\n"
            )


            file.write(
                f"AMOUNT PAID     : M{paid:.2f}\n"
            )


            file.write(
                f"CHANGE          : M{change:.2f}\n"
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
        # Receipt already exists.
        #
        # Do not fail the completed sale.
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
    #
    # IMPORTANT:
    #
    # The receipt file has already been saved successfully.
    #
    # Printing is OPTIONAL hardware functionality.
    #
    # print_receipt() returns:
    #
    #     (True, message)
    #
    # or
    #
    #     (False, error message)
    #
    # We deliberately ignore BOTH results here.
    #
    # This means:
    #
    # - Printer connected     -> sale remains successful.
    # - Printer disconnected  -> sale remains successful.
    # - Printer powered off   -> sale remains successful.
    # - Printer error         -> sale remains successful.
    # - Windows spooler error -> sale remains successful.
    #
    # The saved TXT receipt remains the permanent receipt
    # record.
    #
    # ======================================================

    try:

        print_receipt(

            business_name,
            business_address,
            business_phone,
            business_email,

            receipt_header,
            receipt_footer,

            served_by,

            receipt_number,

            date_str,
            time_str,

            items,

            total,
            discount,
            final_total,

            paid,
            change
        )

    except Exception:

        # --------------------------------------------------
        # Hardware failure must NEVER affect the completed
        # sale or the saved receipt.
        # --------------------------------------------------

        pass


    # ======================================================
    # RETURN RESULT
    # ======================================================
    #
    # IMPORTANT:
    #
    # Do NOT return:
    #
    #     printed
    #     print_success
    #     print_message
    #
    # because the sales window should not display printer
    # warnings from this function.
    #
    # ======================================================

    return {
        "success": True,
        "saved": True,
        "path": str(
            filename
        ),
        "receipt_path": str(
            filename
        ),
        "receipt_number": receipt_number
    }