def is_admin(user):
    return user and user.get("role") == "Admin"


def is_cashier(user):
    return user and user.get("role") == "Cashier"