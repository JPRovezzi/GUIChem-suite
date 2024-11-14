'''
    This module provides functions to handle the file menu. Such as opening, 
    saving, and closing files.
'''
# Import the required libraries:
import customtkinter as ctk
import modules.guiFrames.frame_root as frame_root
#------------------------------------------------------------

def file_menu_event(file_option:str):
    '''Handle the file menu events.'''
    match file_option:
        case "New":
            print("New file")
        case "Open":
            print("Open file")
        case "Save":
            print("Save file")
        case "Close":
            print("Close file")
        case "Exit":
            frame_root.root.destroy()
        case _:
            print("Invalid option")
