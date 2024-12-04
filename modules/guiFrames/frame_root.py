
"""
    This module provides functions to create and manage the main GUI window
    and frames.
"""
# Import the required libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# ImageHandler is a module that provides functions to handle images.
import modules.image_handler as image_handler
# import the required functions to read the configuration files
from modules.guiFrames.functions import read_appcfg

from modules.widget_classes import FileMenu

#------------------------------------------------------------
# Function definitions


def create_gui():
    '''Create the main GUI window and frames.'''
    global root, appearance_menu, file_menu, tools_menu

    background_path = read_appcfg("PATH","backgrounds")
    icon_path = "/".join((
        read_appcfg("PATH","icons"),
        read_appcfg("FILENAME","icon")
        ))

    root = ctk.CTk()
    root.title("GUIChem suite")
    root.eval("tk::PlaceWindow . center")
    root.geometry("800x600")
    root.resizable(0, 0)  # Disable resizing
    root.after(
        201,
        lambda :root.iconbitmap(icon_path))
    image_handler.place_image(root, 0, 0, background_path)
    #Frames
    menuframe = ctk.CTkFrame(master=root)
    file_menu = FileMenu(
        menuframe,
        corner_radius=0,
        )

    appearance_menu = ctk.CTkOptionMenu(
        menuframe,
        corner_radius=0,
        values=["Light", "Dark", "System"],
        command = image_handler.change_appearance_mode_event
        )
    appearance_menu.grid(
        row=0,
        column=2,
        pady=10,
        padx=10)
    appearance_menu.set("Theme")

    tools_menu = ctk.CTkOptionMenu(
        menuframe,
        corner_radius=0,
        values=["UgropyGUI","Flash-Calc"]
        )
    tools_menu.grid(
        row=0,
        column=1,
        pady=10,
        padx=10)
    tools_menu.set("Tools")
    menuframe.pack(anchor="w",fill="both",padx=0, pady=0)
    ctk.set_appearance_mode("system")
    # Start the main loop
    root.mainloop()
    return root, appearance_menu
