'''This module contains the logic to save the image and the data in the specified format'''
import tkinter as tk
import os
# import shutil module to copy files
import shutil
# import filedialog from tkinter module to save files
from tkinter import filedialog
# import the main frame
import modules.main_frame.frame_root as frameRoot
# import the image handler module
import modules.image_handler as imageHandler



def save_image(file_format):
    '''Implement the logic to save the image in the specified file_format'''
    path = filedialog.asksaveasfilename(
        defaultextension = f".{file_format}",
        filetypes = [(f"{file_format.upper()} files", f"*.{file_format}")])
    if not path:
        return
    if file_format == "svg":
        shutil.copy("input.svg", path)
    elif file_format == "png":
        shutil.copy("output.png", path)

def save_data(file_format):
    '''Implement the logic to save the image in the specified file_format'''
    filetypes = []
    for extention in file_format:
        filetypes.append((f"{extention.upper()} files", f"*.{extention}"))
    path = filedialog.asksaveasfilename(
        defaultextension = f".{file_format[0]}",
        filetypes = filetypes)
    if not path:
        return
    shutil.copy("ugropy.session", path)


def load():
    '''Create the save window and display the image to save'''
    save_window = tk.Toplevel(frameRoot.root)
    save_window.resizable(0, 0)  # Disable resizing
    save_window.title("Save")
    save_window.transient(frameRoot.root)
    save_window.grab_set()

    # Display the output PNG as a widget

    if os.path.exists("output.png"):
        imageHandler.insert_image(save_window, "output.png")
    else:
        save_window.destroy()
        return

    # Selection box to select if it is a SVG image or a PNG image
    tk.Label(save_window, text="Select picture format:").pack(pady=5)
    format_var = tk.StringVar(value="png")

    # Frame to hold the radio buttons
    radiobutton_frame = tk.Frame(save_window)
    radiobutton_frame.pack(pady=10)

    tk.Radiobutton(
            radiobutton_frame,
            text="PNG",
            variable = format_var,
            value="png"
            ).pack(side=tk.LEFT,padx=0)
    tk.Radiobutton(
            radiobutton_frame,
            text="SVG",
            variable = format_var,
            value = "svg"
            ).pack(side=tk.LEFT,padx=0)

    # Frame to hold the buttons
    button_frame = tk.Frame(save_window)
    button_frame.pack(pady=10)

    # Save button
    tk.Button(
        button_frame,
        text="Save picture",
        command=lambda: save_image(format_var.get())
        ).pack(side=tk.LEFT, padx=5)


    tk.Button(
        button_frame,
        text="Save data",
        command=lambda: save_data(["txt", "xml", "session"])
        ).pack(side=tk.LEFT, padx=5)

    # Cancel button
    tk.Button(
        button_frame,
        text="Close",
        command=lambda: save_window.destroy()
        ).pack(side=tk.LEFT, padx=5)
