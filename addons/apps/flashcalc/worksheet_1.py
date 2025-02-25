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


class WorkSheetFrame1(frame_classes.FlashCalcFrame):
    '''Class to create the worksheet frame. It has the following methods:
    load, save, open, close.'''
    error_message = None
    problem_name = None
    model = None
    parameter_table = None

    # Dictionary with models as keys and parameter tables as values
    model_parameter_table = {
        "UNIFAC": ["Vapor-Liquid", "Liquid-Liquid", "Infinity Dil."],
        "A-UNIFAC": ["(A) Vapor-Liquid", "(A) Liquid-Liquid", "(A) Infinity Dil."]
    }

    parameter_table_option = None

    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''

        super().__init__(master, tool, **kwargs)
        self.error_message = kwargs.get('error_message',None)
        self.problem_name = kwargs.get('problem_name',None)
        self.model = kwargs.get('model',None)
        self.parameter_table = kwargs.get('parameter_table',None)
        self.load(self.error_message)

    def load(self, error_message = None):
        '''Load the worksheet frame with its widgets.'''

        self.tkraise()
        self.pack_propagate(False)

        def set_parameter_table(*args):
            '''Set the parameter table options.'''
            self.parameter_table_option.set(self.model_parameter_table[model_option.get()][0])
            self.parameter_table_option.configure(values=self.model_parameter_table[model_option.get()])

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
            buttonrow1_frame, text="Reset", cursor="hand2", command=lambda: self.master.load_module(self.tool,"WorkSheetFrame1",location="worksheet_1")
            )

        # First row of configuration widgets: 
        # Problem name, model, parameter table
        cfg1_frame = ctk.CTkFrame(self)
        problem_name_label = ctk.CTkLabel(cfg1_frame, text="Problem name:")
        problem_name_entry = widget_classes.TextEntry(cfg1_frame)
        if self.problem_name is not None:
            problem_name_entry.insert(0, self.problem_name)

        print("Building model list...")
        model_label = ctk.CTkLabel(cfg1_frame, text="Model:")
        model_option = ctk.CTkOptionMenu(
            cfg1_frame,
            values=list(self.model_parameter_table.keys()),
            command=lambda value:set_parameter_table(value))

        if self.model is not None:
            model_option.set(self.model)
            print(f"Using preloaded model: {self.model}")
        else:
            model_option.set(list(self.model_parameter_table.keys())[0])
            print("Using default model: ",
                  list(self.model_parameter_table.keys())[0])

        print("Building parameter list...")
        parameter_table_label = ctk.CTkLabel(cfg1_frame, text="Parameter table:")
        self.parameter_table_option = ctk.CTkOptionMenu(
            cfg1_frame,
            values=self.model_parameter_table[model_option.get()])

        if self.parameter_table is not None:
            self.parameter_table_option.set(self.parameter_table)
            print(f"Using preloaded parameter: {self.parameter_table}")
        else:
            self.parameter_table_option.set(self.model_parameter_table[model_option.get()][0])
            print(f"Using default parameter: {self.model_parameter_table[model_option.get()][0]}")

        # Last row of buttons: Back, Next
        buttonrow3_frame = ctk.CTkFrame(self)
        next_button = ctk.CTkButton(
            buttonrow3_frame, text="Next", cursor="hand2",
            command =
                lambda: [
                self.master.load_module(
                    self.tool,
                    "WorkSheetFrame2",
                    location="worksheet_2",
                    error_message="",
                    problem_name = problem_name_entry.get()[:16],
                    model = model_option.get(),
                    parameter_table = self.parameter_table_option.get())]
            )
        back_button = ctk.CTkButton(
            buttonrow3_frame, text = "Back", cursor = "hand2",
            command = lambda: self.master.load_module(
                self.tool,"WelcomeFrame",location="frame_classes", error_message=""))

        # Add the widgets to the frame with the pack method
        # Title and picture
        title.pack(side="left", padx = 5)
        flashcalc_picture.pack(side="left", padx = 5)
        title_frame.pack(pady=20)

        # First row of buttons: Open, Reset
        #open_button.pack(side="left", padx=5)
        reset_button.pack(side="left", padx=5)
        buttonrow1_frame.pack(pady=10)
        # First row of configuration widgets: 
        # problem name, model, parameter table
        problem_name_label.grid(row=0, column=0, padx=5)
        problem_name_entry.grid(row=0, column=1, padx=5)
        model_label.grid(row=0, column=2, padx=5)
        model_option.grid(row=0, column=3, padx=5)
        parameter_table_label.grid(row=0, column=4, padx=5)
        self.parameter_table_option.grid(row=0, column=5, padx=5)
        cfg1_frame.pack(pady=10)

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

#------------------------------------------------------------------------------