from modules.products.product_management import (
    get_product_by_id,
    has_sufficient_stock
)

# -----------------------------------
# CART STORAGE
# -----------------------------------
cart_items = {}


# -----------------------------------
# ADD PRODUCT
# -----------------------------------
def add_product(product_id, quantity=1):

    product = get_product_by_id(product_id)

    if not product:
        return False, "Product not found."

    product_name = product[1]
    cost_price = float(product[3])
    unit_price = float(product[4])

    existing_qty = cart_items.get(product_id, {}).get("quantity", 0)
    new_qty = existing_qty + quantity

    if not has_sufficient_stock(product_id, new_qty):
        return False, "Insufficient stock available."

    cart_items[product_id] = {
        "product_id": product_id,
        "product_name": product_name,
        "cost_price": cost_price,
        "quantity": new_qty,
        "unit_price": unit_price,
        "subtotal": new_qty * unit_price
    }

    return True, "Added to cart."


# -----------------------------------
# REMOVE PRODUCT
# -----------------------------------
def remove_product(product_id):

    if product_id in cart_items:
        del cart_items[product_id]
        return True, "Removed."

    return False, "Not in cart."


# -----------------------------------
# UPDATE QUANTITY
# -----------------------------------
def update_quantity(product_id, quantity):

    if product_id not in cart_items:
        return False, "Not in cart."

    if quantity <= 0:
        return remove_product(product_id)

    if not has_sufficient_stock(product_id, quantity):
        return False, "Insufficient stock."

    unit_price = cart_items[product_id]["unit_price"]

    cart_items[product_id]["quantity"] = quantity
    cart_items[product_id]["subtotal"] = quantity * unit_price

    return True, "Updated."


# -----------------------------------
# GET ITEMS
# -----------------------------------
def get_cart_items():
    return list(cart_items.values())


# -----------------------------------
# TOTAL
# -----------------------------------
def get_total():
    return sum(item["subtotal"] for item in cart_items.values())


# -----------------------------------
# CLEAR CART
# -----------------------------------
def clear_cart():
    cart_items.clear()