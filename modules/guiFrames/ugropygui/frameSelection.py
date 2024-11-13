
"""
    This module provides functions to create and manage a graphical user interface (GUI) for UGROpyGUI.
    Functions:
        load(error_message=None): Load the selection frame with its widgets.
"""
# Import the required libraries:

# CustomTkinter is a custom GUI library for Python.
#import tkinter as tk
import customtkinter as ctk
# Configparser is used to read configuration files.
import configparser
# SvgHandler is a module that provides functions to handle SVG files.
import modules.svgHandler as svgHandler

# widgetClasses is a module that provides classes for GUI widgets.
import modules.widgetClasses as widgetClasses
# FrameRoot is a module that provides functions the root frame of the GUI.
import modules.guiFrames.frameRoot as frameRoot
# Functions is a module that provides common functions to create and manage the GUI.
import modules.guiFrames.functions as functions
# frameResult is a module that provides functions to create and manage the result frame of the GUI.
import modules.guiFrames.ugropygui.frameResult as frameResult
# frameWelcome is a module that provides functions to create and manage the welcome frame of the GUI.
import modules.guiFrames.frameWelcome as frameWelcome
import modules.toolHandler as toolHandler


#------------------------------------------------------------
# Read configuration file
#config = configparser.ConfigParser()
#config.read('config.cfg')

# Get background color from configuration file
#bg_color = config.get('Settings', 'bg_color')

#------------------------------------------------------------

def load(error_message=None):
    def select_name():
        input_type = 'name'
        molecule_id = molecule_id_var.get()
        outcome = svgHandler.get_results(molecule_id,input_type)
        molecule,error = outcome
        if error == None and molecule != None:
            frame_selection.destroy()
            frameResult.load(molecule)
            error_message = ""
        elif error == 1:
            #functions.clear_widgets_except(None, frameRoot.frames)
            error_message = "The NAME identifier is not valid. Please try again."
            load(error_message)
        elif error == 2:
            #functions.clear_widgets_except(None,frameRoot.frames)
            error_message = "You must enter a NAME identifier. Please try again."
            load(error_message)
        else: 
            error_message = "Unknown error. Please try again."
            #functions.clear_widgets_except(None, frameRoot.frames)
            load(error_message)

    def select_smiles():
        input_type = 'smiles'
        molecule_id = molecule_id_var.get()
        outcome = svgHandler.get_results(molecule_id,input_type)
        molecule,error = outcome
        if error == None and molecule != None:
            frame_selection.destroy()
            frameResult.load(molecule)
            error_message = ""
        elif error == 1:
            #functions.clear_widgets_except(None, frameRoot.frames)
            error_message = "The SMILES identifier is not valid. Please try again."
            load(error_message)
        elif error == 2:
            #functions.clear_widgets_except(None, frameRoot.frames)
            error_message = "You must enter a SMILES identifier. Please try again."
            load(error_message)
        else: 
            error_message = "Unknown error. Please try again."
            #functions.clear_widgets_except(None, frameRoot.frames)
            load(error_message)
    toolHandler.destroy_all_frames()
    frame_selection = ctk.CTkFrame(master=frameRoot.root)
    #functions.clear_widgets_except(frame_selection, frameRoot.frames)
    frame_selection.tkraise()

    # frame_selection widgets
    ctk.CTkLabel(frame_selection,
                 text="",
                 #bg=bg_color
                 ).pack(pady=0)
    widgetClasses.TitleLabel(
        frame_selection,
        text = "Please enter the Chemical identifier of the molecule:"
        ).pack(pady=0)

    molecule_id_var = ctk.StringVar()
    ctk.CTkEntry(
        frame_selection, 
        textvariable = molecule_id_var
        ).pack(pady=20)

    ctk.CTkLabel(
        frame_selection, 
        text = error_message,
        #bg=bg_color,
        #fg="red",
        #font=(14)
        ).pack(pady=0)

    widgetClasses.TitleLabel(
        frame_selection,
        text="Select the type of Chemical identifier",
        ).pack(pady=0)

    ctk.CTkButton(
        frame_selection,
        text="NAME",
        #fg="black",
        #font=("TkMenuFont",12),
        #bg="white",
        cursor="hand2",
        #activebackground="gray",
        command=lambda:select_name()
        ).pack(pady=10)

    ctk.CTkButton(
        frame_selection,
        text="SMILES",
        #fg="black",
        #font=("TkMenuFont",12),
        #bg="white",
        cursor="hand2",
        #activebackground="gray",
        command=lambda:select_smiles()
        ).pack(pady=10)

    widgetClasses.GoBackButton(
        frame_selection,
        command=lambda:toolHandler.selectTool_event("UgropyGUI")
    ).pack(pady=50)

    frame_selection.pack()
    return None