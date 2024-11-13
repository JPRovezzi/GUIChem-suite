
"""
    This module provides functions to create and manage a graphical user interface (GUI) for UGROpyGUI.
    Functions:
        load_frame_result(molecule): Load the result frame with its widgets.
"""
# Import the required libraries:

# CustomTkinter is a custom GUI library for Python.
#import tkinter as tk
import customtkinter as ctk
# Configparser is used to read configuration files.
import configparser

# ImageHandler is a module that provides functions to handle images.
import modules.imageHandler as imageHandler
# widgetClasses is a module that provides classes for GUI widgets.
import modules.widgetClasses as widgetClasses
# FrameRoot is a module that provides functions the root frame of the GUI.
import modules.guiFrames.frameRoot as frameRoot
# Functions is a module that provides common functions to create and manage the GUI.
import modules.guiFrames.functions as functions
# frameWelcome is a module that provides functions to create and manage the welcome frame of the GUI.
import modules.guiFrames.frameWelcome as frameWelcome
import modules.toolHandler as toolHandler



#------------------------------------------------------------
# Read configuration file
config = configparser.ConfigParser()
config.read('config.cfg')

# Get background color from configuration file
bg_color = config.get('Settings', 'bg_color')

#------------------------------------------------------------
def load(molecule):
    toolHandler.destroy_all_frames()
    frame_result = ctk.CTkFrame(master=frameRoot.root)
    #functions.clear_widgets_except(frame_result,frameRoot.frames)
    frame_result.tkraise()
    
    ctk.CTkLabel(
        frame_result,
        text="The molecule groups are displayed below.",
        #bg=bg_color,
        #fg="white",
        #font=("TkMenuFont",14)
        ).pack(pady=20)
    
    imageHandler.insert_image(frame_result, "output.png")

    ctk.CTkLabel(
        frame_result,
        text = molecule.unifac.subgroups,
        #bg=bg_color,
        #fg="white",
        ).pack()

    widgetClasses.GoBackButton(
        frame_result,
        command=lambda:toolHandler.startTool_event("UgropyGUI")
    ).pack(pady=50)

    frame_result.pack()
    
    return None