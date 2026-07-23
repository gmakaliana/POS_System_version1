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
# SETTINGS VALIDATION
# =====================================

def validate_business_name(name):

    if not name:
        return False, "Business name is required."

    if len(name) > 100:
        return False, (
            "Business name cannot exceed 100 characters."
        )

    return True, ""


def validate_email(email):

    if not email:
        return True, ""

    if len(email) > 254:
        return False, (
            "Email cannot exceed 254 characters."
        )

    if not re.match(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$",
        email
    ):
        return False,  (
            "Invalid email address. "
            "Example: name@example.com"
        )

    return True, ""


def validate_receipt_text(text):

    if not text:
        return True, ""

    if len(text) > 255:
        return False, (
            "Receipt text cannot exceed 255 characters."
        )

    return True, ""


def validate_receipt_number(number):

    try:

        number = int(number)

        if number < 1:
            return False, (
                "Receipt number must be greater than zero."
            )

        if number > 999999999:
            return False, (
                "Receipt number is too large."
            )

    except:

        return False, (
            "Invalid receipt number."
        )

    return True, ""


def validate_threshold(value):

    try:

        value = int(value)

        if value < 0:
            return False, (
                "Threshold cannot be negative."
            )

        if value > 100000:
            return False, (
                "Threshold is too large."
            )

    except:

        return False, (
            "Invalid threshold."
        )

    return True, ""


def validate_backup_keep_count(count):

    try:

        count = int(count)

        if count < 1:
            return False, (
                "Backup count must be at least 1."
            )

        if count > 100:
            return False, (
                "Backup count cannot exceed 100."
            )

    except:

        return False, (
            "Invalid backup count."
        )

    return True, ""


def validate_report_time(time_text):

    if not re.match(
        r"^([01]\d|2[0-3]):([0-5]\d)$",
        time_text
    ):
        return False, (
            "Time must be in HH:MM format."
        )

    return True, ""


# =====================================
# GENERAL VALIDATION
# =====================================

# =====================================
# SEARCH VALIDATION
# =====================================

def validate_search_text(text):

    if len(text) > 100:
        return False, (
            "Search text is too long."
        )

    return True, ""

# =====================================
# ID VALIDATION
# =====================================

def validate_id(value, field_name):

    try:

        value = int(value)

        if value <= 0:
            return False, f"{field_name} must be greater than zero."

    except:

        return False, f"Invalid {field_name}."

    return True, ""

# =====================================
# DISCOUNT VALIDATION
# =====================================

def validate_discount(discount):

    try:

        discount = float(discount)

        if discount < 0:
            return False, "Discount cannot be negative."

        if discount > 99999999.99:
            return False, "Discount is too large."

    except:

        return False, "Invalid discount."

    return True, ""