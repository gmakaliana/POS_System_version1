import os
from datetime import datetime

from modules.settings.settings import (
    get_settings,
    get_next_receipt_number,
    increase_receipt_number
)

from auth.session import get_session_user

def generate_receipt(
        sale_id,
        items,
        total,
        discount,
        paid
):

    os.makedirs(
        "receipts",
        exist_ok=True
    )


    # =====================================
    # GET RECEIPT NUMBER
    # =====================================

    receipt_number = get_next_receipt_number()



    filename = (
        f"receipts/receipt_{receipt_number}.txt"
    )



    # =====================================
    # BUSINESS INFORMATION
    # =====================================

    settings = get_settings()


    if settings:

        business_name = settings["business_name"]

        business_address = settings["business_address"]

        business_phone = settings["business_phone"]

        business_email = settings["business_email"]

        receipt_header = settings["receipt_header"]

        receipt_footer = settings["receipt_footer"]


    else:

        business_name = "POS SYSTEM"

        business_address = ""

        business_phone = ""

        business_email = ""

        receipt_header = "RECEIPT"

        receipt_footer = "THANK YOU"

    # =====================================
    # LOGGED-IN USER
    # =====================================

    user = get_session_user()

    if user:
        served_by = user["username"]
    else:
        served_by = "Unknown"


    now = datetime.now()

    date_str = now.strftime("%Y-%m-%d")

    time_str = now.strftime("%H:%M")



    final_total = max(
        0,
        total - discount
    )


    change = paid - final_total



    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as file:



        # =====================================
        # HEADER
        # =====================================

        file.write(
            "=================================\n"
        )


        file.write(
            f"{business_name.center(33)}\n"
        )


        file.write(
            f"{business_address.center(33)}\n"
        )


        file.write(
            f"Tel: {business_phone}".center(33)
            + "\n"
        )


        file.write(
            f"{business_email}".center(33)
            + "\n"
        )


        file.write(
            "---------------------------------\n"
        )


        file.write(
            f"{receipt_header.center(33)}\n"
        )

        file.write(
            "=================================\n"
        )

        file.write(
            f"Served By : {served_by}\n"
        )

        file.write("\n")



        # =====================================
        # RECEIPT DETAILS
        # =====================================

        file.write(
            f"Receipt No : {receipt_number}\n"
        )


        file.write(
            f"Date       : {date_str}\n"
        )


        file.write(
            f"Time       : {time_str}\n\n"
        )



        # =====================================
        # PRODUCTS
        # =====================================

        file.write(
            "---------------------------------\n"
        )


        file.write(
            "PRODUCTS        QTY     AMOUNT (M)\n"
        )


        file.write(
            "---------------------------------\n"
        )



        for item in items:

            name = (
                item["product_name"][:12]
                .ljust(14)
            )


            qty = (
                str(item["quantity"])
                .ljust(6)
            )


            amount = (
                f"M{item['subtotal']:.2f}"
            )


            file.write(
                f"{name}{qty}{amount}\n"
            )



        file.write(
            "---------------------------------\n"
        )



        # =====================================
        # PAYMENT
        # =====================================

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



        # =====================================
        # FOOTER
        # =====================================

        file.write(
            "=================================\n"
        )

        file.write(
            f"{receipt_footer.center(33)}\n\n"
        )

        file.write(
            "Developed By:"
        )

        file.write(
            "Mpho George Makaliana\n"
        )

        file.write(
            "Phone : +266 53239121\n"
        )

        file.write(
            "Email : makalianamphogeorge@gmail.com\n"
        )

        file.write(
            "=================================\n"
        )



    # =====================================
    # UPDATE NEXT RECEIPT NUMBER
    # =====================================

    increase_receipt_number()



    return filename