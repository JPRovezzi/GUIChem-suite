'''This module contains the classes for the frames of the GUIChem-suite application.'''
# Import the required libraries:

# OS module provides functions to interact with the operating system.
import os
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
# pywinstyles is a library that provides functions to set the opacity of a window.
if os.name == 'nt':
    import pywinstyles
# frameResult is a module that provides functions to create and manage the
# result frame of the GUI.
# svg_handler is a module that provides functions to handle SVG files.
import addons.ugropygui.svg_handler as svg_handler
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes

class WelcomeFrame(ctk.CTkFrame):
    '''Class to create the welcome frame.'''
    master=None
    tool=None
    def __init__(self, master, tool):
        '''Initialize the class.'''
        super().__init__(master=master, corner_radius=50, bg_color="#000000")
        self.load(tool)
        self.master = master
        self.tool = tool
    
    def load(self, tool):
        '''Load the welcome frame with its widgets.'''
        self.tkraise()
        self.pack_propagate(False)
        widget_classes.TitleLabel(self, text="").pack(pady=0)
        widget_classes.TitleLabel(self, text=f"Welcome to {tool}!").pack(pady=0)
        ctk.CTkButton(
            self,
            text="START",
            cursor="hand2",
            command=lambda: self.master.load_module(tool,"SelectionFrame")
            ).pack(pady=10)
        ctk.CTkButton(
            self,
            text="CLOSE",
            cursor="hand2",
            command=self.destroy
            ).pack(pady=10)
        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")
        self.pack(pady=100)
        return None

class SelectionFrame(ctk.CTkFrame):
    '''Class to create the selection frame.'''
    tool = None
    master = None
    def __init__(self, master, tool):
        '''Initialize the class.'''
        super().__init__(master=master, corner_radius=50, bg_color="#000000")
        self.tool = tool
        self.load()
        self.master = master
    
    def load(self,error_message=None):
        ''' This function creates the frame_selection frame. This frame allows the 
        user to enter the chemical identifier of the molecule and select the type 
        of identifier (NAME or SMILES). The user can also go back to the UgropyGUI 
        frame. '''
        def select_name(self):
            input_type = 'name'
            molecule_id = molecule_id_var.get()
            outcome = svg_handler.get_results(molecule_id,input_type)
            molecule,error = outcome
            if error is None and molecule is not None:
                frame_selection.destroy()
                #frame_result.load(molecule, name = molecule_id)
                error_message = ""
            elif error == 1:
                error_message = "The NAME identifier is not valid. Please try again."
                self.load(error_message)
            elif error == 2:
                error_message = "You must enter a NAME identifier. Please try again."
                self.load(error_message)
            else:
                error_message = "Unknown error. Please try again."
                self.load(error_message)

        def select_smiles(self):
                input_type = 'smiles'
                molecule_id = molecule_id_var.get()
                outcome = svg_handler.get_results(molecule_id,input_type)
                molecule,error = outcome
                if error is None and molecule is not None:
                    frame_selection.destroy()
                    #frame_result.load(molecule, smiles = molecule_id)
                    error_message = ""
                elif error == 1:
                    error_message = "The SMILES identifier is not valid. Please try again."
                    self.load(error_message)
                elif error == 2:
                    error_message = "You must enter a SMILES identifier. Please try again."
                    self.load(error_message)
                else:
                    error_message = "Unknown error. Please try again."
                    self.load(error_message)

        self.master.destroy_all_frames()
        frame_selection = ctk.CTkFrame(master=self.master)
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
            command=lambda:select_name
            ).pack(pady=10)

        ctk.CTkButton(
            frame_selection,
            text="SMILES",
            cursor="hand2",
            command=lambda:select_smiles
            ).pack(pady=10)

        widget_classes.GoBackButton(
            frame_selection,
            command=lambda:self.master.load_module(self.tool,"WelcomeFrame")
        ).pack(pady=50)

        frame_selection.pack()
        return None
