
"""
    This module provides functions to load the welcome frame with its widgets.
"""
# Import the required libraries:

# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# pywinstyles is a library that provides functions to set the opacity of a window.
import os
if os.name == 'nt':
    import pywinstyles

# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
# frameRoot is a module that provides functions the root frame of the GUI.
import modules.guiFrames.frame_root as frame_root
# tool_handler is a module that provides functions to handle the tools.
import modules.tool_handler as tool_handler

#------------------------------------------------------------
BG_COLOR = "#000000"

def load(tool):
    '''This function loads the welcome frame with its widgets.'''
    #global frame_welcome
    frame_welcome = ctk.CTkFrame(
        master=frame_root.root,
        corner_radius=50,
        bg_color=BG_COLOR,
        )
    frame_welcome.tkraise()
    frame_welcome.pack_propagate(False)
    widget_classes.TitleLabel(
        frame_welcome,
        text=""
        ).pack(pady=0)
    widget_classes.TitleLabel(
        frame_welcome,
        text=f"Welcome to {tool}!"
        ).pack(pady=0)
    ctk.CTkButton(
        frame_welcome,
        text="START",
        cursor="hand2",
        command=lambda:tool_handler.start_tool_event(tool)
        ).pack(pady=10)

    ctk.CTkButton(
    frame_welcome,
    text="CLOSE",
    cursor="hand2",
    command=frame_welcome.destroy
    ).pack(pady=10)
    if os.name == 'nt':  # Check if the OS is Windows
        pywinstyles.set_opacity(frame_welcome, color=BG_COLOR)
    frame_welcome.pack(pady=100)
    return None
