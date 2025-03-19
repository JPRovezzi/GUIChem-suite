import tkinter as tk
import os
from PIL import Image

import customtkinter as ctk

if os.name == 'nt':
    import pywinstyles

# Import the required third-party libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# CTkXYFrame is a custom frame with XY scrollbars for Python.
from modules.ctk_xyframe import CTkXYFrame
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
from . import frame_classes
from . import flash_table
class WorkSheetFrame3(frame_classes.FlashCalcFrame):
    '''Class to create the worksheet frame. It has the following methods:
    load, save, open, close.'''
    error_message = None
    problem_name = None
    model = None
    parameter_table = None

    flash_list = []
    composition_dict = {}

    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''

        super().__init__(master, tool, **kwargs)
        self.error_message=kwargs.get('error_message',None)
        self.problem_name=kwargs.get('problem_name',None)
        self.model=kwargs.get('model',None)
        self.parameter_table=kwargs.get('parameter_table',None)
        

        self.flash_list = kwargs.get('flash_list',None)
        self.composition_dict = kwargs.get('composition_dict',None)

        self.load(self.error_message)

    def load(self, error_message = None):
        '''Load the worksheet frame with its widgets.'''

        self.tkraise()
        self.pack_propagate(False)

        # Get the path of the image for the title
        script_dir = os.path.dirname(__file__)
        image_path = script_dir+"/res/flashcalc.jpeg"
        image = Image.open(image_path)
        self.image = ctk.CTkImage(image, size=(80, 80))

        # Create the widgets
        # Title and picture
        title_frame = ctk.CTkFrame(self)
        title= widget_classes.TitleLabel(title_frame, text="Flash-Calc")
        flashcalc_picture=ctk.CTkLabel(title_frame, image=self.image, text="")

        # First row of buttons: Open, Reset
        buttonrow1_frame = ctk.CTkFrame(self)
        reset_button = ctk.CTkButton(
            buttonrow1_frame, text="Reset", cursor="hand2", command=lambda: self.master.load_module(self.tool, "WorkSheetFrame1", location="worksheet_1"))

        # First row of configuration widgets: 
        # Problem name, model, parameter table
        cfg1_frame = ctk.CTkFrame(self)
        problem_name_label = ctk.CTkLabel(
            cfg1_frame, text=f"Problem name: {self.problem_name}")
        model_label = ctk.CTkLabel(
            cfg1_frame, text=f"Model: {self.model}")
        parameter_table_label = ctk.CTkLabel(
            cfg1_frame, text=f"Parameter table: {self.parameter_table}")

        # Second row of buttons: Show Composition Table, Show Flash Table
        buttonrow2_frame = ctk.CTkFrame(self)
        showct_button = ctk.CTkButton(
            buttonrow2_frame, text="Show the composition table", cursor="hand2",
            command=lambda : print("WiP: Show the composition table"))
        showft_button = ctk.CTkButton(
            buttonrow2_frame, text="Edit the flash config table", cursor="hand2",
            command=lambda : flash_table.FlashTableWindow(self))

        # Last row of buttons: Save, Run, Back, Close
        buttonrow3_frame = ctk.CTkFrame(self)
        next_button = ctk.CTkButton(
            buttonrow3_frame, text="Next", cursor="hand2", command=lambda: 
            self.master.load_module(
                self.tool,
                "WorkSheetFrame4",
                location="worksheet_4",
                error_message="",
                problem_name = self.problem_name,
                model = self.model,
                parameter_table = self.parameter_table,

                flash_list = self.flash_list,
                composition_dict = self.composition_dict))
                
        back_button = ctk.CTkButton(
            buttonrow3_frame, text="Back", cursor="hand2", command=lambda: 
            self.master.load_module(
                self.tool,
                "WorkSheetFrame2",
                location="worksheet_2",
                error_message="",
                problem_name = self.problem_name,
                model = self.model,
                parameter_table = self.parameter_table,
                
                composition_dict = self.composition_dict))
        
        # Add the widgets to the frame with the pack method
        # Title and picture
        title.pack(side="left", padx = 5)
        flashcalc_picture.pack(side="left", padx = 5)
        title_frame.pack(pady=20)

        # First row of buttons: Reset
        reset_button.pack(side="left", padx=5)
        buttonrow1_frame.pack(pady=10)

        # First row of configuration widgets: 
        # problem name, model, parameter table
        problem_name_label.grid(row=0, column=0, padx=5)
        model_label.grid(row=0, column=1, padx=5)
        parameter_table_label.grid(row=0, column=2, padx=5)
        cfg1_frame.pack(pady=10)

        # Second row of buttons: Show Composition Table, Show Flash Table
        showct_button.grid(row=0, column=0, padx=5)
        showft_button.grid(row=0, column=1, padx=5)
        buttonrow2_frame.pack(pady=10)

        # Last row of buttons: Back, Next
        back_button.grid(row=0, column=0, padx=5)
        ctk.CTkLabel(buttonrow3_frame, text="  |  ").grid(row=0, column=1, padx=5)
        ctk.CTkButton(
            buttonrow3_frame,text="",hover=False).grid(row=0, column=2, padx=5)
        ctk.CTkButton(
            buttonrow3_frame,text="",hover=False).grid(row=0, column=3, padx=5)
        ctk.CTkLabel(buttonrow3_frame, text="  |  ").grid(row=0, column=4, padx=5)
        next_button.grid(row=0, column=5, padx=5)
        buttonrow3_frame.pack(pady=50, side="bottom")

        # Pack the worksheet frame
        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")

        self.pack(pady=0, expand=True, fill="both")
        return None