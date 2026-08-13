"""
GeoMaka POS Receipt Printer

Hardware:
    Xprinter A160 / XP-80C
    80mm Thermal Receipt Printer
    BQ400AS Cash Drawer

Windows Printer:
    XP-80C

Port:
    USB002

Connection:
    USB printer queue

Responsibilities:
    - Print ESC/POS receipts.
    - Open cash drawer.
    - Handle printer errors safely.

Company:
    GeoMaka Technologies
"""

import win32print


# ==========================================================
# PRINTER CONFIGURATION
# ==========================================================

PRINTER_NAME = "XP-80C"


# ==========================================================
# ESC/POS COMMANDS
# ==========================================================

ESC = b"\x1b"
GS = b"\x1d"


# Initialize printer
INIT = (
    ESC
    + b"@"
)


# Alignment
ALIGN_LEFT = (
    ESC
    + b"a"
    + b"\x00"
)

ALIGN_CENTER = (
    ESC
    + b"a"
    + b"\x01"
)


# Bold
BOLD_ON = (
    ESC
    + b"E"
    + b"\x01"
)

BOLD_OFF = (
    ESC
    + b"E"
    + b"\x00"
)


# Cash drawer pulse
#
# Pin 2 / Drawer connector 1
#
OPEN_DRAWER = (
    ESC
    + b"p"
    + b"\x00"
    + b"\x19"
    + b"\xfa"
)


# Paper cut
CUT_PAPER = (
    GS
    + b"V"
    + b"\x00"
)


# ==========================================================
# OPEN PRINTER
# ==========================================================

def open_printer():

    """
    Opens the configured Windows printer.

    Returns:
        Printer handle
    """

    return win32print.OpenPrinter(
        PRINTER_NAME
    )


# ==========================================================
# WRITE RAW DATA
# ==========================================================

def write_raw(
    printer,
    data
):

    """
    Sends raw ESC/POS bytes
    directly to the printer.
    """

    win32print.WritePrinter(
        printer,
        data
    )


# ==========================================================
# FORMAT RECEIPT LINE
# ==========================================================

def format_item_line(
    product_name,
    quantity,
    amount
):

    """
    Creates an 80mm receipt item line.

    Approximate width:
        48 characters
    """

    product_name = str(
        product_name
    )

    if len(product_name) > 28:

        product_name = (
            product_name[:28]
        )

    product_name = product_name.ljust(
        28
    )

    quantity_text = str(
        quantity
    ).rjust(
        5
    )

    amount_text = (
        f"M{amount:.2f}"
    ).rjust(
        15
    )

    return (
        product_name
        + quantity_text
        + amount_text
    )


# ==========================================================
# PRINT RECEIPT
# ==========================================================

def print_receipt(
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
):

    """
    Prints a completed receipt.

    Returns:
        True, message
        or
        False, error message
    """

    printer = None

    try:

        # ==================================================
        # OPEN PRINTER
        # ==================================================

        printer = open_printer()


        # ==================================================
        # START PRINT JOB
        # ==================================================

        win32print.StartDocPrinter(
            printer,
            1,
            (
                "GeoMaka POS Receipt",
                None,
                "RAW"
            )
        )

        win32print.StartPagePrinter(
            printer
        )


        # ==================================================
        # INITIALIZE
        # ==================================================

        write_raw(
            printer,
            INIT
        )


        # ==================================================
        # HEADER
        # ==================================================

        write_raw(
            printer,
            ALIGN_CENTER
        )

        write_raw(
            printer,
            BOLD_ON
        )

        write_raw(
            printer,
            (
                f"{business_name}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )

        write_raw(
            printer,
            BOLD_OFF
        )


        # ==================================================
        # BUSINESS INFORMATION
        # ==================================================

        if business_address:

            write_raw(
                printer,
                (
                    f"{business_address}\n"
                ).encode(
                    "utf-8",
                    errors="replace"
                )
            )


        if business_phone:

            write_raw(
                printer,
                (
                    f"Tel: {business_phone}\n"
                ).encode(
                    "utf-8",
                    errors="replace"
                )
            )


        if business_email:

            write_raw(
                printer,
                (
                    f"{business_email}\n"
                ).encode(
                    "utf-8",
                    errors="replace"
                )
            )


        write_raw(
            printer,
            b"-----------------------------------------------\n"
        )


        # ==================================================
        # RECEIPT HEADER
        # ==================================================

        write_raw(
            printer,
            BOLD_ON
        )

        write_raw(
            printer,
            (
                f"{receipt_header}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )

        write_raw(
            printer,
            BOLD_OFF
        )


        write_raw(
            printer,
            b"-----------------------------------------------\n"
        )


        # ==================================================
        # SALE INFORMATION
        # ==================================================

        write_raw(
            printer,
            ALIGN_LEFT
        )

        write_raw(
            printer,
            (
                f"Receipt No : {receipt_number}\n"
            ).encode()
        )

        write_raw(
            printer,
            (
                f"Date       : {date_str}\n"
            ).encode()
        )

        write_raw(
            printer,
            (
                f"Time       : {time_str}\n"
            ).encode()
        )

        write_raw(
            printer,
            (
                f"Served By  : {served_by}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )


        # ==================================================
        # PRODUCTS
        # ==================================================

        write_raw(
            printer,
            b"-----------------------------------------------\n"
        )

        write_raw(
            printer,
            b"PRODUCT                      QTY          AMOUNT\n"
        )

        write_raw(
            printer,
            b"-----------------------------------------------\n"
        )


        for item in items:

            line = format_item_line(
                item["product_name"],
                item["quantity"],
                item["subtotal"]
            )

            write_raw(
                printer,
                (
                    line
                    + "\n"
                ).encode(
                    "utf-8",
                    errors="replace"
                )
            )


        # ==================================================
        # PAYMENT
        # ==================================================

        write_raw(
            printer,
            b"-----------------------------------------------\n"
        )

        write_raw(
            printer,
            (
                f"TOTAL COST      : M{total:.2f}\n"
            ).encode()
        )

        write_raw(
            printer,
            (
                f"DISCOUNT        : M{discount:.2f}\n"
            ).encode()
        )

        write_raw(
            printer,
            (
                f"FINAL TOTAL     : M{final_total:.2f}\n"
            ).encode()
        )

        write_raw(
            printer,
            (
                f"AMOUNT PAID     : M{paid:.2f}\n"
            ).encode()
        )

        write_raw(
            printer,
            (
                f"CHANGE          : M{change:.2f}\n"
            ).encode()
        )


        # ==================================================
        # FOOTER
        # ==================================================

        write_raw(
            printer,
            b"\n"
        )

        write_raw(
            printer,
            ALIGN_CENTER
        )

        write_raw(
            printer,
            (
                f"{receipt_footer}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )

        write_raw(
            printer,
            b"\n"
        )

        write_raw(
            printer,
            b"Developed By: Mpho George Makaliana\n"
        )

        write_raw(
            printer,
            b"Phone : +266 53239121\n"
        )

        write_raw(
            printer,
            b"Email : makalianamphogeorge@gmail.com\n"
        )


        # ==================================================
        # FEED PAPER
        # ==================================================

        write_raw(
            printer,
            b"\n\n\n\n\n"
        )


        # ==================================================
        # CUT PAPER
        # ==================================================

        write_raw(
            printer,
            CUT_PAPER
        )


        # ==================================================
        # END PAGE
        # ==================================================

        win32print.EndPagePrinter(
            printer
        )


        # ==================================================
        # END DOCUMENT
        # ==================================================

        win32print.EndDocPrinter(
            printer
        )


        return True, "Receipt printed successfully."


    except Exception as e:

        return False, str(e)


    finally:

        if printer is not None:

            try:

                win32print.ClosePrinter(
                    printer
                )

            except Exception:

                pass


# ==========================================================
# OPEN CASH DRAWER
# ==========================================================

def open_cash_drawer():

    """
    Opens the BQ400AS cash drawer
    through the XP-80C printer.

    Returns:
        True, message
        or
        False, error message
    """

    printer = None

    try:

        printer = open_printer()


        win32print.StartDocPrinter(
            printer,
            1,
            (
                "GeoMaka POS Cash Drawer",
                None,
                "RAW"
            )
        )

        win32print.StartPagePrinter(
            printer
        )


        # Send drawer pulse

        write_raw(
            printer,
            OPEN_DRAWER
        )


        win32print.EndPagePrinter(
            printer
        )

        win32print.EndDocPrinter(
            printer
        )


        return True, "Cash drawer opened successfully."


    except Exception as e:

        return False, str(e)


    finally:

        if printer is not None:

            try:

                win32print.ClosePrinter(
                    printer
                )

            except Exception:

                pass