import re


# =====================================
# USER VALIDATION
# =====================================

def validate_username(username):

    if not username:
        return False, "Username is required."

    if len(username) < 3:
        return False, "Username must be at least 3 characters."

    if len(username) > 30:
        return False, "Username cannot exceed 30 characters."

    if not re.match(
        r"^[A-Za-z0-9_]+$",
        username
    ):
        return False, (
            "Username can only contain "
            "letters, numbers and underscore."
        )

    return True, ""



# =====================================
# PASSWORD VALIDATION
# =====================================

def validate_password_length(password):

    if not password:
        return False, "Password is required."

    if len(password) > 128:
        return False, "Password cannot exceed 128 characters."

    return True, ""



# =====================================
# PRODUCT VALIDATION
# =====================================

def validate_product_name(product_name):

    if not product_name:
        return False, "Product name is required."

    if len(product_name) > 100:
        return False, (
            "Product name cannot exceed 100 characters."
        )

    return True, ""



def validate_barcode(barcode):

    if not barcode:
        return True, ""

    if len(barcode) > 50:
        return False, (
            "Barcode cannot exceed 50 characters."
        )

    if not re.match(
        r"^[A-Za-z0-9_-]+$",
        barcode
    ):
        return False, (
            "Barcode contains invalid characters."
        )

    return True, ""



def validate_price(price):

    try:

        value = float(price)

        if value < 0:
            return False, "Price cannot be negative."

        if value > 99999999.99:
            return False, "Price is too large."

    except:

        return False, "Invalid price."


    return True, ""



def validate_quantity(quantity):

    try:

        value = int(quantity)

        if value < 0:
            return False, "Quantity cannot be negative."

        if value > 999999:
            return False, "Quantity is too large."

    except:

        return False, "Invalid quantity."


    return True, ""



# =====================================
# SUPPLIER VALIDATION
# =====================================

def validate_supplier_name(name):

    if not name:
        return False, "Supplier name is required."

    if len(name) > 100:
        return False, (
            "Supplier name cannot exceed 100 characters."
        )

    return True, ""



def validate_phone(phone):

    if not phone:
        return True, ""

    if len(phone) > 20:
        return False, (
            "Phone number cannot exceed 20 characters."
        )

    if not re.match(
        r"^[0-9+\-\s()]+$",
        phone
    ):
        return False, (
            "Phone number contains invalid characters."
        )

    return True, ""



def validate_address(address):

    if not address:
        return True, ""

    if len(address) > 255:
        return False, (
            "Address cannot exceed 255 characters."
        )

    return True, ""



# =====================================
# SEARCH VALIDATION
# =====================================

def validate_search_text(text):

    if len(text) > 100:
        return False, (
            "Search text is too long."
        )

    return True, ""