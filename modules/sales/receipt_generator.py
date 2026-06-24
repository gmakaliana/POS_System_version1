import os
from datetime import datetime


def generate_receipt(sale_id, items, total, discount, paid):

    os.makedirs("receipts", exist_ok=True)

    filename = f"receipts/receipt_{sale_id}.txt"

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    final_total = max(0, total - discount)
    change = paid - final_total

    with open(filename, "w", encoding="utf-8") as file:

        # ==============================
        # HEADER
        # ==============================
        file.write("=================================\n")
        file.write("        POS SYSTEM RECEIPT\n")
        file.write("=================================\n\n")

        file.write(f"Receipt No : {sale_id}\n")
        file.write(f"Date       : {date_str}\n")
        file.write(f"Time       : {time_str}\n\n")

        # ==============================
        # TABLE HEADER
        # ==============================
        file.write("---------------------------------\n")
        file.write("PRODUCTS        QTY     AMOUNT (M)\n")
        file.write("---------------------------------\n")

        # ==============================
        # ITEMS
        # ==============================
        for item in items:
            name = item["product_name"][:12].ljust(14)
            qty = str(item["quantity"]).ljust(6)
            amount = f"M{item['subtotal']:.2f}"

            file.write(f"{name}{qty}{amount}\n")

        file.write("---------------------------------\n")

        # ==============================
        # SUMMARY
        # ==============================
        file.write(f"TOTAL COST      : M{total:.2f}\n")
        file.write(f"DISCOUNT        : M{discount:.2f}\n")
        file.write(f"FINAL TOTAL     : M{final_total:.2f}\n")
        file.write(f"AMOUNT PAID     : M{paid:.2f}\n")
        file.write(f"CHANGE          : M{change:.2f}\n")

        file.write("=================================\n")
        file.write("      THANK YOU FOR SHOPPING\n")
        file.write("=================================\n")

    return filename