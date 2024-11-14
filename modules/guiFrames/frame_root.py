
"""
    This module provides functions to create and manage the main GUI window
    and frames.
"""
# Import the required libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# ImageHandler is a module that provides functions to handle images.
import modules.image_handler as image_handler
# ToolHandler is a module that provides functions to handle tools.
import modules.tool_handler as tool_handler
# FileMenuHandler is a module that provides functions to handle the file menu.
import modules.guiFrames.file_menu_handler as file_menu_handler

#------------------------------------------------------------
# Function definitions
def create_gui():
    '''Create the main GUI window and frames.'''
    global root, appearance_menu, file_menu, tools_menu
    root = ctk.CTk()
    root.title("GUIChem suite")
    root.resizable(0, 0)  # Disable resizing
    root.eval("tk::PlaceWindow . center")
    root.geometry("640x480")
    root.after(201, lambda :root.iconbitmap('assets/icons/GUIChem.ico'))
    image_handler.place_image(root, 0, 0, "assets/backgrounds")
    #Frames
    menuframe = ctk.CTkFrame(master=root)
    # Create a menu bar
    file_menu = ctk.CTkOptionMenu(
        menuframe,
        corner_radius=0,
        values=["New", "Open", "Save", "Close","","Exit"],
        command = file_menu_handler.file_menu_event
        )
    file_menu.grid(
        row=0,
        column=0,
        pady=10,
        padx=10)
    file_menu.set("File")

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
        values=["UgropyGUI","Flash-Calc"],
        command = tool_handler.select_tool_event)
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
