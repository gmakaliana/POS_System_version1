"""
GeoMaka POS Receipt Printer Hardware

File:
    hardware/receipt_printer.py

Purpose:
    Communicate directly with the Xprinter A160
    using USB ESC/POS commands.

Hardware:
    Xprinter A160 / XP-80
    BQ400AS Cash Drawer

Connection:
    USB

Responsibilities:
    - Detect the Xprinter USB device.
    - Print ESC/POS receipts.
    - Open the cash drawer.
    - Provide printer hardware testing.

Company:
    GeoMaka Technologies
"""


from escpos.printer import Usb


# ==========================================================
# XPRINTER USB IDENTIFICATION
# ==========================================================

VENDOR_ID = 0x0483
PRODUCT_ID = 0x5743


# ==========================================================
# PRINTER CONNECTION
# ==========================================================

def get_printer():

    """
    Connect directly to the Xprinter A160.

    Returns:
        ESC/POS USB printer object
        or None if connection fails.
    """

    try:

        printer = Usb(
            VENDOR_ID,
            PRODUCT_ID
        )

        return printer

    except Exception as e:

        print(
            f"Printer connection failed: {e}"
        )

        return None


# ==========================================================
# OPEN CASH DRAWER
# ==========================================================

def open_cash_drawer(printer):

    """
    Send the ESC/POS drawer-open pulse
    through the receipt printer.

    The BQ400AS is connected to the
    printer's RJ11 cash-drawer port.
    """

    try:

        printer.cashdraw(
            2
        )

        return True, "Cash drawer opened."

    except Exception as e:

        return False, str(e)


# ==========================================================
# TEST PRINT
# ==========================================================

def test_print():

    """
    Print a simple hardware test receipt
    and open the cash drawer.
    """

    printer = get_printer()

    if printer is None:

        return False, "Could not connect to Xprinter."


    try:

        # ==============================================
        # INITIALIZE PRINTER
        # ==============================================

        printer.set(
            align="center",
            bold=True
        )

        printer.text(
            "GEOMAKA POS\n"
        )

        printer.text(
            "HARDWARE TEST\n"
        )

        printer.text(
            "==============================\n"
        )


        # ==============================================
        # PRINTER INFORMATION
        # ==============================================

        printer.set(
            align="left",
            bold=False
        )

        printer.text(
            "Printer : Xprinter A160\n"
        )

        printer.text(
            "Driver  : XP-80\n"
        )

        printer.text(
            "USB     : 0483:5743\n"
        )

        printer.text(
            "Status  : TEST\n"
        )


        printer.text(
            "==============================\n"
        )


        printer.set(
            align="center",
            bold=True
        )

        printer.text(
            "PRINT TEST SUCCESSFUL\n"
        )

        printer.text(
            "\n"
        )

        printer.text(
            "GeoMaka Technologies\n"
        )

        printer.text(
            "\n\n"
        )


        # ==============================================
        # CUT PAPER
        # ==============================================

        printer.cut()


        # ==============================================
        # OPEN CASH DRAWER
        # ==============================================

        success, message = open_cash_drawer(
            printer
        )


        printer.close()


        if not success:

            return False, (
                "Receipt printed, but cash drawer "
                f"failed: {message}"
            )


        return True, (
            "Printer test successful "
            "and cash drawer opened."
        )


    except Exception as e:

        try:

            printer.close()

        except Exception:

            pass


        return False, str(e)