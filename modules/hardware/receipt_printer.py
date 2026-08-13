"""
GeoMaka POS Receipt Printer

File:
modules/hardware/receipt_printer.py

Purpose:
Handle the GeoMaka POS thermal receipt printer
and cash drawer.

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
- Send receipt data to the configured Windows printer.
- Open the cash drawer through the receipt printer.
- Handle printer errors safely.
- Handle cash drawer errors safely.
- Never allow hardware failure to cancel a completed sale.

IMPORTANT:

This module intentionally does NOT perform
printer status checking.

It does NOT check:

- Printer availability.
- Printer port availability.
- Printer online/offline status.
- Printer paper status.
- Printer door status.
- Printer Windows status flags.
- Windows printer attributes.
- Print-job status.
- Physical printer power state.
- Cash drawer status.

The application simply sends the ESC/POS command
to the configured Windows printer queue.

If Windows/PyWin32 raises an error while performing
an operation, that error is returned safely.

A successful Windows spooler submission means that
Windows accepted the print command.

It does NOT guarantee that the physical printer
has printed the paper.

Company:
GeoMaka Technologies
"""

import win32print


# ==========================================================
# PRINTER CONFIGURATION
# ==========================================================

PRINTER_NAME = "XP-80C"

PRINTER_PORT = "USB002"


# ==========================================================
# ESC/POS COMMANDS
# ==========================================================

ESC = b"\x1b"

GS = b"\x1d"


# ----------------------------------------------------------
# Initialize printer
# ----------------------------------------------------------

INIT = (
    ESC
    + b"@"
)


# ----------------------------------------------------------
# Alignment
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# Bold
# ----------------------------------------------------------

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


# ----------------------------------------------------------
# Cash drawer pulse
#
# Pin 2 / Drawer connector 1
# ----------------------------------------------------------

OPEN_DRAWER = (
    ESC
    + b"p"
    + b"\x00"
    + b"\x19"
    + b"\xfa"
)


# ----------------------------------------------------------
# Paper cut
# ----------------------------------------------------------

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

    No printer ON/OFF or readiness check is performed.

    Returns:

        Printer handle

    Raises:

        Exception:
            If Windows cannot open the printer.
    """

    printer = win32print.OpenPrinter(
        PRINTER_NAME
    )


    if not printer:

        raise Exception(
            (
                f"Printer '{PRINTER_NAME}' "
                "could not be opened."
            )
        )


    return printer


# ==========================================================
# WRITE RAW DATA
# ==========================================================

def write_raw(
    printer,
    data
):
    """
    Sends raw ESC/POS bytes directly
    to the Windows printer.

    No printer status check is performed.

    Raises:

        Exception:
            If Windows cannot send the data.
    """

    result = win32print.WritePrinter(
        printer,
        data
    )


    if not result:

        raise Exception(
            (
                "Windows failed to send data "
                "to the receipt printer."
            )
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
        +
        quantity_text
        +
        amount_text
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

    No printer readiness, ON/OFF, port, status,
    or print-job verification is performed.

    The receipt is simply sent to the configured
    Windows printer queue.

    Printer failure does NOT cancel the sale.

    Returns:

        True, success message

        or

        False, error message
    """

    printer = None

    document_started = False

    page_started = False


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


        document_started = True


        # ==================================================
        # START PAGE
        # ==================================================

        win32print.StartPagePrinter(
            printer
        )


        page_started = True


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
            ).encode(
                "utf-8",
                errors="replace"
            )
        )


        write_raw(
            printer,
            (
                f"Date       : {date_str}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )


        write_raw(
            printer,
            (
                f"Time       : {time_str}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
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
                    +
                    "\n"
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
            ).encode(
                "utf-8",
                errors="replace"
            )
        )


        write_raw(
            printer,
            (
                f"DISCOUNT        : M{discount:.2f}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )


        write_raw(
            printer,
            (
                f"FINAL TOTAL     : M{final_total:.2f}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )


        write_raw(
            printer,
            (
                f"AMOUNT PAID     : M{paid:.2f}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
        )


        write_raw(
            printer,
            (
                f"CHANGE          : M{change:.2f}\n"
            ).encode(
                "utf-8",
                errors="replace"
            )
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

        if page_started:

            win32print.EndPagePrinter(
                printer
            )

            page_started = False


        # ==================================================
        # END DOCUMENT
        # ==================================================

        if document_started:

            win32print.EndDocPrinter(
                printer
            )

            document_started = False


        # ==================================================
        # SUCCESS
        # ==================================================

        return (
            True,
            "Receipt sent to printer successfully."
        )


    except Exception as e:

        return (
            False,
            (
                "Receipt printing failed.\n\n"
                f"Printer: {PRINTER_NAME}\n"
                f"Port: {PRINTER_PORT}\n"
                f"Error: {e}"
            )
        )


    finally:

        # --------------------------------------------------
        # Safely close unfinished print page
        # --------------------------------------------------

        if printer is not None:

            if page_started:

                try:

                    win32print.EndPagePrinter(
                        printer
                    )

                except Exception:

                    pass


            if document_started:

                try:

                    win32print.EndDocPrinter(
                        printer
                    )

                except Exception:

                    pass


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
    Opens the BQ400AS cash drawer through
    the XP-80C printer.

    No printer readiness, ON/OFF, port,
    status, or job-status checks are performed.

    The drawer pulse is simply sent to the
    configured Windows printer.

    Cash drawer failure does NOT cancel
    the completed sale.

    Returns:

        True, success message

        or

        False, error message
    """

    printer = None

    document_started = False

    page_started = False


    try:

        # ==================================================
        # OPEN PRINTER
        # ==================================================

        printer = open_printer()


        # ==================================================
        # START DRAWER JOB
        # ==================================================

        win32print.StartDocPrinter(
            printer,
            1,
            (
                "GeoMaka POS Cash Drawer",
                None,
                "RAW"
            )
        )


        document_started = True


        # ==================================================
        # START PAGE
        # ==================================================

        win32print.StartPagePrinter(
            printer
        )


        page_started = True


        # ==================================================
        # SEND DRAWER PULSE
        # ==================================================

        write_raw(
            printer,
            OPEN_DRAWER
        )


        # ==================================================
        # END PAGE
        # ==================================================

        if page_started:

            win32print.EndPagePrinter(
                printer
            )

            page_started = False


        # ==================================================
        # END DOCUMENT
        # ==================================================

        if document_started:

            win32print.EndDocPrinter(
                printer
            )

            document_started = False


        # ==================================================
        # SUCCESS
        # ==================================================

        return (
            True,
            "Cash drawer command sent successfully."
        )


    except Exception as e:

        return (
            False,
            (
                "Cash drawer could not be opened.\n\n"
                f"Printer: {PRINTER_NAME}\n"
                f"Port: {PRINTER_PORT}\n"
                f"Error: {e}"
            )
        )


    finally:

        if printer is not None:

            if page_started:

                try:

                    win32print.EndPagePrinter(
                        printer
                    )

                except Exception:

                    pass


            if document_started:

                try:

                    win32print.EndDocPrinter(
                        printer
                    )

                except Exception:

                    pass


            try:

                win32print.ClosePrinter(
                    printer
                )

            except Exception:

                pass