import tkinter as tk
from tkinter import ttk, messagebox

from modules.settings.settings import (
    get_low_stock_threshold,
    update_low_stock_threshold
)



def open_inventory_settings(parent):

    parent.withdraw()


    window = tk.Toplevel()

    window.title("Inventory Settings")

    window.geometry("400x250")

    window.resizable(False, False)



    def close_window():

        window.destroy()

        parent.deiconify()



    ttk.Label(
        window,
        text="INVENTORY SETTINGS",
        font=("Arial",16,"bold")
    ).pack(pady=20)



    frame = ttk.Frame(window)

    frame.pack()



    ttk.Label(
        frame,
        text="Low Stock Threshold"
    ).grid(
        row=0,
        column=0,
        padx=10,
        pady=20
    )


    entry = ttk.Entry(
        frame,
        width=15
    )

    entry.grid(
        row=0,
        column=1
    )


    entry.insert(
        0,
        get_low_stock_threshold()
    )



    def save():

        try:

            value = int(entry.get())


            update_low_stock_threshold(value)


            messagebox.showinfo(
                "Saved",
                "Inventory settings saved."
            )


        except ValueError:

            messagebox.showerror(
                "Error",
                "Enter a valid number."
            )



    ttk.Button(
        window,
        text="Save",
        width=15,
        command=save
    ).pack(pady=20)



    ttk.Button(
        window,
        text="Close",
        width=15,
        command=close_window
    ).pack()



    window.protocol(
        "WM_DELETE_WINDOW",
        close_window
    )