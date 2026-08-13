"""
GeoMaka POS Hardware Test

Hardware:
    Xprinter A160 / XP-80C
    BQ400AS Cash Drawer

Printer:
    XP-80C

Connection:
    USB002
"""

import win32print


# ==========================================================
# PRINTER
# ==========================================================

PRINTER_NAME = "XP-80C"


# ==========================================================
# ESC/POS COMMANDS
# ==========================================================

ESC = b"\x1b"
GS = b"\x1d"


INIT = ESC + b"@"


CENTER = (
    ESC
    + b"a"
    + b"\x01"
)


LEFT = (
    ESC
    + b"a"
    + b"\x00"
)


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
# Connector 1
#
DRAWER_OPEN = (
    ESC
    + b"p"
    + b"\x00"
    + b"\x19"
    + b"\xfa"
)


# Paper cut
CUT = (
    GS
    + b"V"
    + b"\x00"
)


# ==========================================================
# PRINT TEST
# ==========================================================

def test_printer():

    printer = None

    try:

        print()
        print("=" * 50)
        print("GeoMaka POS Hardware Test")
        print("=" * 50)


        # ==================================================
        # OPEN PRINTER
        # ==================================================

        print(
            "Opening printer..."
        )

        printer = win32print.OpenPrinter(
            PRINTER_NAME
        )

        print(
            "Printer opened successfully."
        )


        # ==================================================
        # START PRINT JOB
        # ==================================================

        win32print.StartDocPrinter(
            printer,
            1,
            (
                "GeoMaka POS Hardware Test",
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

        win32print.WritePrinter(
            printer,
            INIT
        )


        # ==================================================
        # HEADER
        # ==================================================

        win32print.WritePrinter(
            printer,
            CENTER
        )

        win32print.WritePrinter(
            printer,
            BOLD_ON
        )

        win32print.WritePrinter(
            printer,
            b"GEOMAKA POS\n"
        )

        win32print.WritePrinter(
            printer,
            b"HARDWARE TEST\n"
        )

        win32print.WritePrinter(
            printer,
            BOLD_OFF
        )

        win32print.WritePrinter(
            printer,
            b"================================\n"
        )


        # ==================================================
        # PRINTER INFORMATION
        # ==================================================

        win32print.WritePrinter(
            printer,
            LEFT
        )

        win32print.WritePrinter(
            printer,
            b"Printer : XP-80C\n"
        )

        win32print.WritePrinter(
            printer,
            b"Model   : Xprinter A160\n"
        )

        win32print.WritePrinter(
            printer,
            b"Port    : USB002\n"
        )

        win32print.WritePrinter(
            printer,
            b"Status  : ONLINE\n"
        )

        win32print.WritePrinter(
            printer,
            b"--------------------------------\n"
        )


        # ==================================================
        # RECEIPT TEST
        # ==================================================

        win32print.WritePrinter(
            printer,
            CENTER
        )

        win32print.WritePrinter(
            printer,
            BOLD_ON
        )

        win32print.WritePrinter(
            printer,
            b"RECEIPT PRINT TEST\n"
        )

        win32print.WritePrinter(
            printer,
            BOLD_OFF
        )

        win32print.WritePrinter(
            printer,
            b"\n"
        )

        win32print.WritePrinter(
            printer,
            b"Receipt printer is working.\n"
        )

        win32print.WritePrinter(
            printer,
            b"GeoMaka POS hardware test.\n"
        )

        win32print.WritePrinter(
            printer,
            b"\n"
        )


        # ==================================================
        # CASH DRAWER TEST
        # ==================================================

        win32print.WritePrinter(
            printer,
            b"Testing cash drawer...\n"
        )

        win32print.WritePrinter(
            printer,
            b"\n\n"
        )


        print(
            "Sending cash drawer command..."
        )

        win32print.WritePrinter(
            printer,
            DRAWER_OPEN
        )


        print(
            "Cash drawer command sent."
        )


        # ==================================================
        # FEED PAPER
        # ==================================================

        win32print.WritePrinter(
            printer,
            b"\n\n\n"
        )


        # ==================================================
        # CUT PAPER
        # ==================================================

        win32print.WritePrinter(
            printer,
            CUT
        )


        # ==================================================
        # END PRINT JOB
        # ==================================================

        win32print.EndPagePrinter(
            printer
        )

        win32print.EndDocPrinter(
            printer
        )


        print()
        print(
            "Receipt data sent successfully."
        )

        print(
            "Check the receipt printer."
        )

        print(
            "Check whether the cash drawer opened."
        )

        print("=" * 50)

        return True


    except Exception as e:

        print()
        print(
            "ERROR:"
        )

        print(
            str(e)
        )

        print("=" * 50)

        return False


    finally:

        if printer is not None:

            try:

                win32print.ClosePrinter(
                    printer
                )

            except Exception:

                pass


# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    test_printer()