
"""
    This module provides functions to create and manage a graphical user interface (GUI) for UGROpyGUI.
    Functions:
        create_gui(): Create the main GUI window and frames.
        load_frame_welcome(): Load the welcome frame with its widgets.
        load_frame_selection(error_message=None): Load the selection frame with its widgets.
        load_frame_result(molecule): Load the result frame with its widgets.
        clear_widgets_except(currentFrame): Clear all widgets except those in the specified frame.
"""
# Import the required libraries:

# CustomTkinter is a custom GUI library for Python.
import tkinter as tk
import ctypes as ct
import customtkinter as ctk

# Configparser is used to read configuration files.
import configparser

# frameWelcome is a module that provides functions to create and manage the welcome frame of the GUI.
import modules.guiFrames.frameWelcome as frameWelcome

import modules.imageHandler as imageHandler

import modules.toolHandler as toolHandler

#------------------------------------------------------------
# Read configuration file
config = configparser.ConfigParser()
config.read('config.cfg')

# Get background color from configuration file
bg_color = config.get('Settings', 'bg_color')
ctk.set_appearance_mode("system")
#ctk.set_default_color_theme("dark-blue")

#------------------------------------------------------------


#------------------------------------------------------------
# Function definitions

def create_gui():

    '''Create the main GUI window and frames.'''
    global root, frame_welcome, frame_selection, frame_getName, frame_result, frames, appearance_menu
    root = ctk.CTk()
    root.title("GUIChem suite")
    root.resizable(0, 0)  # Disable resizing
    root.eval("tk::PlaceWindow . center")
    root.geometry("640x480")
    root.after(201, lambda :root.iconbitmap('assets/icons/GUIChem.ico'))
    imageHandler.place_image(root, 0, 0, "assets/backgrounds")


    #Frames
    menuframe = ctk.CTkFrame(master=root)

    # Create a menu bar
    file_menu = ctk.CTkOptionMenu(
        menuframe,
        corner_radius=0, 
        values=["New", "Open", "Save", "Close","","Exit"])
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
        command=imageHandler.change_appearance_mode_event)
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
        command=toolHandler.selectTool_event)
    tools_menu.grid(
        row=0, 
        column=1, 
        pady=10, 
        padx=10)
    tools_menu.set("Tools")

    menuframe.pack(anchor="w",fill="both",padx=0, pady=0)
    

    
    # Create frames
    
    #frame_selection = ctk.CTkFrame(master=root)
    frame_getName = ctk.CTkFrame(master=root)
    #frame_result = ctk.CTkFrame(master=root)
    #frames = (frame_welcome, frame_selection, frame_getName, frame_result)

    
    #Load the welcome frame

    #frameWelcome.load()

    # Start the main loop
    root.mainloop()
    return None





    





    
    