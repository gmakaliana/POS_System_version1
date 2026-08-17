import tkinter as tk
from tkinter import ttk, messagebox

from modules.suppliers.supplier_management import (
    get_all_suppliers,
    delete_supplier
)

from gui.supplier_add_window import (
    open_add_supplier_window
)

from gui.supplier_edit_window import (
    open_edit_supplier_window
)


# ==========================================================
# TOP WINDOW POSITIONING
# ==========================================================

def position_window_top(
    window,
    width,
    height
):
    """
    Positions the window horizontally centered
    and towards the top of the screen.
    """

    screen_width = (
        window.winfo_screenwidth()
    )

    x = (
        screen_width // 2
        -
        width // 2
    )

    y = 40

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )


# ==========================================================
# SUPPLIER MANAGEMENT WINDOW
# ==========================================================

def open_supplier_management_window(
    admin_root
):

    # -----------------------------------
    # HIDE DASHBOARD
    # -----------------------------------

    admin_root.withdraw()


    # -----------------------------------
    # CREATE WINDOW
    # -----------------------------------

    root = tk.Toplevel()

    root.title(
        "SUPPLIER MANAGEMENT"
    )

    root.resizable(
        True,
        True
    )


    # -----------------------------------
    # POSITION TOWARDS TOP
    # -----------------------------------

    position_window_top(
        root,
        800,
        450
    )


    # -----------------------------------
    # CLOSE
    # -----------------------------------

    def close_window():

        root.destroy()

        admin_root.deiconify()


    # -----------------------------------
    # TABLE FRAME
    # -----------------------------------

    table_frame = tk.Frame(
        root
    )

    table_frame.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )


    # -----------------------------------
    # SUPPLIER TABLE
    # -----------------------------------

    tree = ttk.Treeview(
        table_frame,
        columns=(
            "Supplier",
            "Phone",
            "Address"
        ),
        show="headings"
    )


    # -----------------------------------
    # TABLE HEADINGS
    # -----------------------------------

    tree.heading(
        "Supplier",
        text="Supplier Name"
    )

    tree.heading(
        "Phone",
        text="Phone Number"
    )

    tree.heading(
        "Address",
        text="Address"
    )


    # -----------------------------------
    # TABLE COLUMNS
    # -----------------------------------

    tree.column(
        "Supplier",
        width=250
    )

    tree.column(
        "Phone",
        width=180
    )

    tree.column(
        "Address",
        width=280
    )


    # -----------------------------------
    # PACK TABLE
    # -----------------------------------

    tree.pack(
        side="left",
        fill="both",
        expand=True
    )


    # -----------------------------------
    # SCROLLBAR
    # -----------------------------------

    scrollbar = ttk.Scrollbar(
        table_frame,
        orient="vertical",
        command=tree.yview
    )

    tree.configure(
        yscrollcommand=scrollbar.set
    )

    scrollbar.pack(
        side="right",
        fill="y"
    )


    # -----------------------------------
    # LOAD SUPPLIERS
    # -----------------------------------

    def load_suppliers():

        for row in tree.get_children():

            tree.delete(
                row
            )


        suppliers = get_all_suppliers()


        for supplier in suppliers:

            supplier_id = supplier[0]


            tree.insert(
                "",
                "end",
                values=(
                    supplier[1],
                    supplier[2],
                    supplier[3]
                ),
                tags=(
                    supplier_id,
                )
            )


    # -----------------------------------
    # GET SELECTED ID
    # -----------------------------------

    def get_selected_supplier_id():

        selected = tree.focus()


        if not selected:

            return None


        return tree.item(
            selected
        )["tags"][0]


    # -----------------------------------
    # DELETE
    # -----------------------------------

    def delete_selected():

        supplier_id = (
            get_selected_supplier_id()
        )


        if not supplier_id:

            messagebox.showwarning(
                "Warning",
                "Select a supplier.",
                parent=root
            )

            return


        confirm = messagebox.askyesno(
            "Confirm",
            "Delete selected supplier?",
            parent=root
        )


        if confirm:

            try:

                delete_supplier(
                    supplier_id
                )

                load_suppliers()


            except Exception as e:

                messagebox.showerror(
                    "Error",
                    str(e),
                    parent=root
                )


    # -----------------------------------
    # EDIT
    # -----------------------------------

    def edit_selected():

        selected = tree.focus()


        if not selected:

            messagebox.showwarning(
                "Warning",
                "Select a supplier.",
                parent=root
            )

            return


        supplier_id = (
            get_selected_supplier_id()
        )


        values = tree.item(
            selected
        )["values"]


        supplier_data = (

            supplier_id,

            values[0],

            values[1],

            values[2]

        )


        open_edit_supplier_window(
            supplier_data,
            load_suppliers,
            root
        )


    # -----------------------------------
    # BUTTONS
    # -----------------------------------

    btn_frame = tk.Frame(
        root
    )

    btn_frame.pack(
        fill="x",
        padx=10,
        pady=10
    )


    # -----------------------------------
    # ADD SUPPLIER
    # -----------------------------------

    tk.Button(
        btn_frame,
        text="Add Supplier",
        width=14,
        bg="#3498db",
        fg="white",
        command=lambda:
            open_add_supplier_window(
                root,
                load_suppliers
            )
    ).pack(
        side="left",
        padx=5
    )


    # -----------------------------------
    # EDIT SUPPLIER
    # -----------------------------------

    tk.Button(
        btn_frame,
        text="Edit Supplier",
        width=14,
        bg="#f39c12",
        fg="white",
        command=edit_selected
    ).pack(
        side="left",
        padx=5
    )


    # -----------------------------------
    # DELETE SUPPLIER
    # -----------------------------------

    tk.Button(
        btn_frame,
        text="Delete Supplier",
        width=14,
        bg="#e74c3c",
        fg="white",
        command=delete_selected
    ).pack(
        side="left",
        padx=5
    )


    # -----------------------------------
    # CLOSE
    # -----------------------------------

    tk.Button(
        btn_frame,
        text="Close",
        width=14,
        bg="#7f8c8d",
        fg="white",
        command=close_window
    ).pack(
        side="right",
        padx=5
    )


    # -----------------------------------
    # INITIAL LOAD
    # -----------------------------------

    load_suppliers()


    # -----------------------------------
    # WINDOW CLOSE EVENT
    # -----------------------------------

    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )