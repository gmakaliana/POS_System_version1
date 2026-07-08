import tkinter as tk
from tkinter import ttk, messagebox

from modules.users.user_management import (
    get_all_users,
    delete_user
)

from gui.user_edit_window import open_edit_user_window
from gui.user_add_window import open_add_user_window


def open_user_management_window(admin_root):

    # -----------------------------------
    # HIDE ADMIN DASHBOARD
    # -----------------------------------
    admin_root.withdraw()

    root = tk.Toplevel()
    root.title("USER MANAGEMENT")
    root.geometry("750x450")

    # -----------------------------------
    # CLOSE FUNCTION (RETURN TO ADMIN)
    # -----------------------------------
    def close_window():
        root.destroy()
        admin_root.deiconify()

    # -----------------------------------
    # TABLE FRAME
    # -----------------------------------
    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    tree = ttk.Treeview(
        table_frame,
        columns=("Username", "Role", "Status"),
        show="headings"
    )

    tree.heading("Username", text="Username")
    tree.heading("Role", text="Role")
    tree.heading("Status", text="Password Status")

    tree.column("Username", width=250)
    tree.column("Role", width=150)
    tree.column("Status", width=150)

    tree.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # -----------------------------------
    # LOAD USERS (STORE ID IN TAGS)
    # -----------------------------------
    def load_users():
        for i in tree.get_children():
            tree.delete(i)

        users = get_all_users()

        for u in users:
            user_id = u[0]
            username = u[1]
            role = u[2]
            status = "Temporary" if u[3] == 1 else "Set"

            tree.insert(
                "",
                "end",
                values=(username, role, status),
                tags=(user_id,)
            )

    # -----------------------------------
    # GET SELECTED USER ID
    # -----------------------------------
    def get_selected_user_id():
        selected = tree.focus()
        if not selected:
            return None

        return tree.item(selected)["tags"][0]

    # -----------------------------------
    # DELETE USER
    # -----------------------------------
    def delete_selected():

        user_id = get_selected_user_id()

        if not user_id:
            messagebox.showwarning("Warning", "Select a user")
            return

        confirm = messagebox.askyesno("Confirm", "Delete this user?")

        if confirm:
            try:
                delete_user(user_id)
                load_users()

            except Exception as e:
                messagebox.showerror("Error", str(e))

    # -----------------------------------
    # EDIT USER
    # -----------------------------------
    def edit_selected():

        selected = tree.focus()

        if not selected:
            messagebox.showwarning("Warning", "Select a user")
            return

        user_id = get_selected_user_id()
        values = tree.item(selected)["values"]

        user_data = (user_id, values[0], values[1], values[2])

        open_edit_user_window(user_data, load_users)

    # -----------------------------------
    # BUTTON PANEL
    # -----------------------------------
    btn_frame = tk.Frame(root)
    btn_frame.pack(fill="x", padx=10, pady=10)

    # ADD USER (BLUE)
    tk.Button(
        btn_frame,
        text="Add User",
        width=12,
        bg="#3498db",
        fg="white",
        command=lambda: open_add_user_window(load_users)
    ).pack(side="left", padx=5)

    # EDIT USER (ORANGE)
    tk.Button(
        btn_frame,
        text="Edit User",
        width=12,
        bg="#f39c12",
        fg="white",
        command=edit_selected
    ).pack(side="left", padx=5)

    # DELETE USER (RED)
    tk.Button(
        btn_frame,
        text="Delete User",
        width=12,
        bg="#e74c3c",
        fg="white",
        command=delete_selected
    ).pack(side="left", padx=5)

    # CLOSE (DARK GRAY)
    tk.Button(
        btn_frame,
        text="Close",
        width=12,
        bg="#7f8c8d",
        fg="white",
        command=close_window
    ).pack(side="right", padx=5)

    # -----------------------------------
    # INIT
    # -----------------------------------
    load_users()

    # Handle window X button
    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )

    root.mainloop()