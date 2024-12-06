"""
    This module creates the frame_selection frame. This frame allows the 
    user to enter the chemical identifier of the molecule and select the type 
    of identifier (NAME or SMILES). The user can also go back to the UgropyGUI 
    frame. 
"""
# Import the required libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# svg_handler is a module that provides functions to handle SVG files.
import modules.tool_frame.ugropygui.svg_handler as svg_handler

# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
# FrameRoot is a module that provides functions the root frame of the GUI.
import modules.main_frame.frame_root as frame_root
# frameResult is a module that provides functions to create and manage the
# result frame of the GUI.
import modules.tool_frame.ugropygui.frame_result as frame_result

import modules.tool_handler as tool_handler


#------------------------------------------------------------
# Read configuration file
#config = configparser.ConfigParser()
#config.read('config.cfg')

# Get background color from configuration file
#bg_color = config.get('Settings', 'bg_color')

#------------------------------------------------------------

def load(error_message=None):
    ''' This function creates the frame_selection frame. This frame allows the 
    user to enter the chemical identifier of the molecule and select the type 
    of identifier (NAME or SMILES). The user can also go back to the UgropyGUI 
    frame. '''
    def select_name():
        input_type = 'name'
        molecule_id = molecule_id_var.get()
        outcome = svg_handler.get_results(molecule_id,input_type)
        molecule,error = outcome
        if error is None and molecule is not None:
            frame_selection.destroy()
            frame_result.load(molecule, name = molecule_id)
            error_message = ""
        elif error == 1:
            error_message = "The NAME identifier is not valid. Please try again."
            load(error_message)
        elif error == 2:
            error_message = "You must enter a NAME identifier. Please try again."
            load(error_message)
        else:
            error_message = "Unknown error. Please try again."
            load(error_message)

    def select_smiles():
        input_type = 'smiles'
        molecule_id = molecule_id_var.get()
        outcome = svg_handler.get_results(molecule_id,input_type)
        molecule,error = outcome
        if error is None and molecule is not None:
            frame_selection.destroy()
            frame_result.load(molecule, smiles = molecule_id)
            error_message = ""
        elif error == 1:
            error_message = "The SMILES identifier is not valid. Please try again."
            load(error_message)
        elif error == 2:
            error_message = "You must enter a SMILES identifier. Please try again."
            load(error_message)
        else:
            error_message = "Unknown error. Please try again."
            load(error_message)

    tool_handler.destroy_all_frames()
    frame_selection = ctk.CTkFrame(master=frame_root.root)
    frame_selection.tkraise()

    # frame_selection widgets
    ctk.CTkLabel(frame_selection,
                 text="",
                 ).pack(pady=0)
    widget_classes.TitleLabel(
        frame_selection,
        text = "Please enter the Chemical identifier of the molecule:"
        ).pack(pady=0)

    molecule_id_var = ctk.StringVar()
    widget_classes.TextEntry(
        frame_selection,
        textvariable = molecule_id_var
        ).pack(pady=20)

    ctk.CTkLabel(
        frame_selection,
        text = error_message,
        ).pack(pady=0)

    widget_classes.TitleLabel(
        frame_selection,
        text="Select the type of Chemical identifier",
        ).pack(pady=0)

    ctk.CTkButton(
        frame_selection,
        text="NAME",
        cursor="hand2",
        #activebackground="gray",
        command=lambda:select_name()
        ).pack(pady=10)

    ctk.CTkButton(
        frame_selection,
        text="SMILES",
        cursor="hand2",
        command=lambda:select_smiles()
        ).pack(pady=10)

    widget_classes.GoBackButton(
        frame_selection,
        command=lambda:tool_handler.select_tool_event("UgropyGUI")
    ).pack(pady=50)

    frame_selection.pack()
    return None
