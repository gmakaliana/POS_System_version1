# auth/permissions.py


# =====================================================
# ROLE CHECKS
# =====================================================

def get_role(user):

    if not user:
        return None

    return user.get("role")



def is_system_admin(user):

    return get_role(user) == "System Admin"



def is_default_admin(user):

    return get_role(user) == "Default Admin"



def is_admin(user):

    return get_role(user) == "Admin"



def is_cashier(user):

    return get_role(user) == "Cashier"





# =====================================================
# DASHBOARD PERMISSIONS
# =====================================================

def can_access_admin_dashboard(user):

    return (
        is_system_admin(user)
        or is_default_admin(user)
        or is_admin(user)
    )



def can_access_cashier_dashboard(user):

    return is_cashier(user)





# =====================================================
# USER VISIBILITY
# =====================================================

def can_view_user(viewer, target_role):


    if is_system_admin(viewer):

        return True



    if is_default_admin(viewer):

        return target_role != "System Admin"



    if is_admin(viewer):

        return target_role in [
            "Admin",
            "Cashier"
        ]



    return False





# =====================================================
# CREATE USER
# =====================================================

def can_create_user(creator, new_role):


    if is_system_admin(creator):

        return new_role in [
            "Default Admin",
            "Admin",
            "Cashier"
        ]



    if is_default_admin(creator):

        return new_role in [
            "Admin",
            "Cashier"
        ]



    if is_admin(creator):

        return new_role == "Cashier"



    return False





# =====================================================
# EDIT USER BASIC INFORMATION
# =====================================================

def can_edit_user(editor, target_user):


    target_role = target_user.get("role")



    # System Admin is locked

    if target_role == "System Admin":

        return False



    # Cannot edit yourself

    if (
        editor.get("user_id")
        ==
        target_user.get("user_id")
    ):

        return False



    if is_system_admin(editor):

        return True



    if is_default_admin(editor):

        return target_role in [
            "Default Admin",
            "Admin",
            "Cashier"
        ]



    if is_admin(editor):

        return target_role in [
            "Admin",
            "Cashier"
        ]



    return False





# =====================================================
# CHANGE USER ROLE
# =====================================================

def can_change_role(editor, target_user, new_role):


    target_role = target_user.get("role")



    # System Admin cannot change

    if target_role == "System Admin":

        return False



    # Cannot change own role

    if (
        editor.get("user_id")
        ==
        target_user.get("user_id")
    ):

        return False



    # System Admin

    if is_system_admin(editor):

        return new_role in [
            "Default Admin",
            "Admin",
            "Cashier"
        ]



    # Default Admin

    if is_default_admin(editor):

        # Cannot modify Default Admin roles

        if target_role == "Default Admin":

            return False


        return new_role in [
            "Admin",
            "Cashier"
        ]



    # Admin

    if is_admin(editor):

        # Admin cannot change Admin roles

        if target_role == "Admin":

            return False


        return new_role == "Cashier"



    return False





# =====================================================
# USER DELETION
# =====================================================

def can_delete_user(deleter, target_user):


    target_role = target_user.get("role")



    if target_role == "System Admin":

        return False



    if is_system_admin(deleter):

        return target_role in [
            "Default Admin",
            "Admin",
            "Cashier"
        ]



    if is_default_admin(deleter):

        return target_role in [
            "Admin",
            "Cashier"
        ]



    if is_admin(deleter):

        return target_role == "Cashier"



    return False





# =====================================================
# PASSWORD RESET
# =====================================================

def can_reset_password(resetter, target_user):


    target_role = target_user.get("role")



    # System Admin can reset own password only

    if target_role == "System Admin":

        return (
            resetter.get("user_id")
            ==
            target_user.get("user_id")
        )



    if is_system_admin(resetter):

        return True



    if is_default_admin(resetter):

        return target_role in [
            "Default Admin",
            "Admin",
            "Cashier"
        ]



    if is_admin(resetter):

        return target_role in [
            "Admin",
            "Cashier"
        ]



    return False





# =====================================================
# SETTINGS
# =====================================================

def can_manage_settings(user):

    return (
        is_system_admin(user)
        or
        is_default_admin(user)
    )





# =====================================================
# MODULE ACCESS
# =====================================================

def can_manage_products(user):

    return not is_cashier(user)



def can_manage_suppliers(user):

    return not is_cashier(user)



def can_manage_reports(user):

    return not is_cashier(user)



def can_manage_sales(user):

    return user is not None