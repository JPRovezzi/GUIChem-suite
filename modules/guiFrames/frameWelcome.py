
"""
    This module provides functions to create and manage a graphical user interface (GUI) for UGROpyGUI.
    Functions:
        load_frame_welcome(): Load the welcome frame with its widgets.
"""
# Import the required libraries:

# CustomTkinter is a custom GUI library for Python.
#import tkinter as tk
import customtkinter as ctk
import pywinstyles


# widgetClasses is a module that provides classes for GUI widgets.
import modules.widgetClasses as widgetClasses

# frameRoot is a module that provides functions the root frame of the GUI.
import modules.guiFrames.frameRoot as frameRoot
# frameSelection is a module that provides functions to create and manage the selection frame of the GUI.
#import modules.guiFrames.frameSelection as frameSelection
# functions is a module that provides common functions to create and manage the GUI.
import modules.guiFrames.functions as functions
import modules.imageHandler as imageHandler
import modules.toolHandler as toolHandler

#------------------------------------------------------------
bg_color = "#000000"

def load(tool):
    global frame_welcome
    frame_welcome = ctk.CTkFrame(
        master=frameRoot.root,
        corner_radius=50, 
        #border_color="black", 
        #border_width=2, 
        #fg_color="transparent",
        bg_color=bg_color,
        )
     # just add this line
    #functions.clear_widgets_except(frame_welcome,frameRoot.frames)
    frame_welcome.tkraise()
    frame_welcome.pack_propagate(False)
    
    
    # frame_welcome widgets
    # Add image file 
    #imageHandler.place_image(frameRoot.frame_welcome, 0, 0, imageHandler.random_image("assets/backgrounds"))
    #imageHandler.place_image(frameRoot.frame_welcome, 0, 0, "assets/backgrounds/gray_lines.png")
    widgetClasses.TitleLabel(
        frame_welcome,
        text=""
        ).pack(pady=0)
    widgetClasses.TitleLabel(
        frame_welcome,
        text=f"Welcome to {tool}!"
        ).pack(pady=0)

    ctk.CTkButton(
        frame_welcome,
        text="START",
        #fg="black",
        #font=("TkMenuFont",12),
        #bg_color=bg_color,
        cursor="hand2",
        #activebackground="gray",
        command=lambda:toolHandler.startTool_event(tool)
        ).pack(pady=10)
    
    ctk.CTkButton(
    frame_welcome,
    text="CLOSE",
    #fg="black",
    #font=("TkMenuFont",12),
    #bg="white",
    cursor="hand2",
    #activebackground="gray",
    command=lambda:frame_welcome.destroy()
    ).pack(pady=10)
    
    pywinstyles.set_opacity(frame_welcome, color=bg_color)
    
    
    frame_welcome.pack(pady=100)


    return None

