import tkinter as tk
from tkinter import messagebox

from modules.suppliers.supplier_management import (
    update_supplier
)



def center_window(window, width, height):

    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)

    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )



def open_edit_supplier_window(
        supplier_data,
        refresh_callback,
        parent
):

    supplier_id = supplier_data[0]


    # -----------------------------------
    # CREATE WINDOW
    # -----------------------------------

    root = tk.Toplevel(parent)

    root.title(
        "EDIT SUPPLIER"
    )

    root.resizable(
        False,
        False
    )


    center_window(
        root,
        400,
        320
    )


    root.transient(
        parent
    )


    root.grab_set()



    # -----------------------------------
    # CLOSE WINDOW
    # -----------------------------------

    def close_window():

        root.grab_release()

        root.destroy()



    root.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )



    # -----------------------------------
    # FONTS
    # -----------------------------------

    label_font = (
        "Arial",
        11
    )


    entry_font = (
        "Arial",
        11
    )


    button_font = (
        "Arial",
        11,
        "bold"
    )



    # -----------------------------------
    # MAIN FRAME
    # -----------------------------------

    frame = tk.Frame(
        root,
        padx=20,
        pady=15
    )

    frame.pack(
        fill="both",
        expand=True
    )



    # -----------------------------------
    # NAME
    # -----------------------------------

    tk.Label(
        frame,
        text="Supplier Name",
        font=label_font
    ).pack(
        anchor="w"
    )


    supplier_entry = tk.Entry(
        frame,
        width=35,
        font=entry_font
    )


    supplier_entry.pack(
        pady=(5,10)
    )


    supplier_entry.insert(
        0,
        supplier_data[1]
    )

    # Focus username automatically
    supplier_entry.focus()

    # -----------------------------------
    # PHONE
    # -----------------------------------

    tk.Label(
        frame,
        text="Phone Number",
        font=label_font
    ).pack(
        anchor="w"
    )


    phone_entry = tk.Entry(
        frame,
        width=35,
        font=entry_font
    )


    phone_entry.pack(
        pady=(5,10)
    )


    phone_entry.insert(
        0,
        supplier_data[2]
    )



    # -----------------------------------
    # ADDRESS
    # -----------------------------------

    tk.Label(
        frame,
        text="Address",
        font=label_font
    ).pack(
        anchor="w"
    )


    address_entry = tk.Entry(
        frame,
        width=35,
        font=entry_font
    )


    address_entry.pack(
        pady=(5,10)
    )


    address_entry.insert(
        0,
        supplier_data[3]
    )



    # -----------------------------------
    # UPDATE FUNCTION
    # -----------------------------------

    def update():


        supplier_name = supplier_entry.get().strip()



        phone = phone_entry.get().strip()

        address = address_entry.get().strip()



        if not supplier_name:


            messagebox.showerror(
                "Error",
                "Supplier name is required.",
                parent=root
            )

            return



        update_button.config(
            state="disabled"
        )



        try:


            update_supplier(

                supplier_id,

                supplier_name,

                phone,

                address

            )



            refresh_callback()



            messagebox.showinfo(
                "Success",
                "Supplier updated successfully.",
                parent=root
            )



            close_window()



        except Exception as e:


            update_button.config(
                state="normal"
            )


            messagebox.showerror(
                "Error",
                str(e),
                parent=root
            )



    # -----------------------------------
    # BUTTONS
    # -----------------------------------

    button_frame = tk.Frame(
        frame
    )

    button_frame.pack(
        pady=15,
        fill="x"
    )



    update_button = tk.Button(
        button_frame,
        text="UPDATE SUPPLIER",
        bg="#f39c12",
        fg="white",
        font=button_font,
        width=18,
        command=update
    )


    update_button.pack(
        side="left",
        padx=5
    )

    # Press Enter to save settings
    root.bind(
        "<Return>",
        lambda event: update()
    )


    tk.Button(
        button_frame,
        text="CLOSE",
        bg="#7f8c8d",
        fg="white",
        font=button_font,
        width=12,
        command=close_window
    ).pack(
        side="right",
        padx=5
    )