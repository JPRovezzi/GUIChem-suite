
'''This module contains the classes for the frames of the flashcalc addon.'''

# Import the required standard libraries:
# OS module provides functions to interact with the operating system.
import os
# tkinter is a module that provides functions to create GUI applications.
import tkinter as tk
# xml.etree.ElementTree is a module that provides functions to create and parse XML documents.
import xml.etree.ElementTree as ET
from PIL import Image

# Import the required third-party libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes

if os.name == 'nt':
    import pywinstyles

class FlashCalcFrame(ctk.CTkFrame):
    '''Class to create the FlashCalc frame. It has the following methods: 
    save, open.'''
    master = None
    tool = None
    def __init__(self, master, tool, **kwargs):
        '''This method initializes an instance of the FlashCalcFrame class.'''
        if os.name == 'nt':
            super().__init__(master=master, corner_radius=50, bg_color="#000000")
        else:
            super().__init__(master=master, corner_radius=0, bg_color="#000000")
        self.master = master
        self.tool = tool
        kwargs
    def save(self):
        '''Not implemented: Save the data'''
        pass
    def open(self):
        '''Load the data from a file.'''
        file_path = tk.filedialog.askopenfilename(
            title="Open File",
            filetypes=[("All Files", "*.*"),
                       ("Flashcalc savefile", "*.session")])
        if not file_path:
            return
        with open(file_path, 'r') as file:
            data = file.read()
        return

class WelcomeFrame(FlashCalcFrame):
    '''Class to create the welcome frame. It has the following methods: 
    load.'''

    master=None
    tool=None

    def __init__(self, master, tool):
        '''Initialize the class.'''

        super().__init__(master, tool)
        self.load(tool)

    def load(self, tool):
        '''Load the welcome frame with its widgets.'''

        self.tkraise()
        self.pack_propagate(False)
        widget_classes.TitleLabel(self, text="").pack(pady=0)
        widget_classes.TitleLabel(self, text=f"Welcome to {tool}!").pack(pady=0)
        
        script_dir = os.path.dirname(__file__)
        image_path = script_dir+"/res/flashcalc.jpeg"
        image = Image.open(image_path)
        self.image = ctk.CTkImage(image, size=(80,80))
        ctk.CTkLabel(self, image=self.image, text="").pack(pady=10)
        ctk.CTkButton(
            self,
            text="NEW",
            cursor="hand2",
            command=lambda: self.master.load_module(tool,"WorkSheetFrame1")
            ).pack(pady=10)
        ctk.CTkButton(
            self,
            text="OPEN",
            cursor="hand2",
            command=lambda: self.open()
            ).pack(pady=10)
        ctk.CTkButton(
            self,
            text="CLOSE",
            cursor="hand2",
            command=self.master.close_module
            ).pack(pady=10)

        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")
        self.pack(pady=100, expand=True, fill="y")
        return None

class WorkSheetFrame1(FlashCalcFrame):
    '''Class to create the worksheet frame. It has the following methods:
    load, save, open, close.'''
    error_message = None
    problem_name = None
    model = None
    parameter_table = None

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
        open_button = ctk.CTkButton(
            buttonrow1_frame, text="Open", cursor="hand2", command=self.open)
        reset_button = ctk.CTkButton(
            buttonrow1_frame, text="Reset", cursor="hand2", command=lambda: self.master.load_module(self.tool, "WorkSheetFrame1"))

        # First row of configuration widgets: 
        # Problem name, model, parameter table
        cfg1_frame = ctk.CTkFrame(self)
        problem_name_label = ctk.CTkLabel(cfg1_frame, text="Problem name:")
        problem_name_entry = widget_classes.TextEntry(cfg1_frame)
        #if self.problem_name is not None:
            #problem_name_entry.insert(0, self.problem_name)
        model_label = ctk.CTkLabel(cfg1_frame, text="Model:")
        model_option = ctk.CTkOptionMenu(cfg1_frame, values=["UNIFAC", "A-UNIFAC"])
        #if self.model is not None:
            #model_option.set(self.model)
        parameter_table_label = ctk.CTkLabel(cfg1_frame, text="Parameter table:")
        parameter_table_option = ctk.CTkOptionMenu(cfg1_frame, values=["Vapor-Liquid", "Liquid-Liquid", "Infinity Dil."], variable=self.parameter_table)
        #if self.parameter_table is not None:
            #parameter_table_option.set(self.parameter_table)

        # Last row of buttons: Back, Next
        buttonrow3_frame = ctk.CTkFrame(self)
        next_button = ctk.CTkButton(
            buttonrow3_frame, text="Next", cursor="hand2",
            command = 
                lambda: [
                self.master.load_module(
                    self.tool,
                    "WorkSheetFrame2",
                    error_message="",
                    problem_name = problem_name_entry.get()[:18],
                    model = model_option.get(),
                    parameter_table = parameter_table_option.get())]
            )
        back_button = ctk.CTkButton(
            buttonrow3_frame, text = "Back", cursor = "hand2",
            command = lambda: self.master.load_module(
                self.tool, "WelcomeFrame"))

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
        parameter_table_option.grid(row=0, column=5, padx=5)
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
    

class WorkSheetFrame2(FlashCalcFrame):
    '''Class to create the worksheet frame. It has the following methods:
    load, save, open, close.'''
    error_message = None
    problem_name = None
    model = None
    parameter_table = None

    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''

        super().__init__(master, tool, **kwargs)
        self.error_message=kwargs.get('error_message',None)
        self.problem_name=kwargs.get('problem_name',None)
        self.model=kwargs.get('model',None)
        self.parameter_table=kwargs.get('parameter_table',None)
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
        open_button = ctk.CTkButton(
            buttonrow1_frame, text="Open", cursor="hand2", command=self.open)
        reset_button = ctk.CTkButton(
            buttonrow1_frame, text="Reset", cursor="hand2", command=lambda: self.master.load_module(self.tool, "WorkSheetFrame1"))

        # First row of configuration widgets: 
        # Problem name, model, parameter table
        cfg1_frame = ctk.CTkFrame(self)
        problem_name_label = ctk.CTkLabel(
            cfg1_frame, text=f"Problem name: {self.problem_name}")
        model_label = ctk.CTkLabel(
            cfg1_frame, text=f"Model: {self.model}")
        parameter_table_label = ctk.CTkLabel(
            cfg1_frame, text=f"Parameter table: {self.parameter_table}")

        # Second row of configuration widgets: 
        # number of components, number of flash calculations
        cfg2_frame = ctk.CTkFrame(self)
        nc_label = ctk.CTkLabel(
            cfg2_frame, text="Number of components:")
        nc_spinbox = tk.Spinbox(cfg2_frame, from_=1, to=10, width=5)
        nf_label = ctk.CTkLabel(
            cfg2_frame, text="Number of flash calculations:")
        nf_spinbox = tk.Spinbox(cfg2_frame, from_=1, to=10, width=5)

        # Second row of buttons: Show Composition Table, Show Flash Table
        buttonrow2_frame = ctk.CTkFrame(self)
        showct_button = ctk.CTkButton(
            buttonrow2_frame, text="Show the composition table", cursor="hand2")
        showft_button = ctk.CTkButton(
            buttonrow2_frame, text="Show the flash table", cursor="hand2")

        # Comment frame
        comment_frame = ctk.CTkFrame(self)
        comment_label = ctk.CTkLabel(comment_frame, text="Comments:")
        comment_text = widget_classes.TextEntry(comment_frame, width=400, height=5) 

        # Last row of buttons: Save, Run, Back, Close
        buttonrow3_frame = ctk.CTkFrame(self)
        save_button = ctk.CTkButton(
            buttonrow3_frame, text="Save", cursor="hand2", command=self.save)
        close_button = ctk.CTkButton(
            buttonrow3_frame, text="Close", cursor="hand2", command=self.master.close_module)
        back_button = ctk.CTkButton(
            buttonrow3_frame, text="Back", cursor="hand2", command=lambda: 
            self.master.load_module(
                self.tool,
                "WorkSheetFrame1",
                error_message="",
                problem_name = self.problem_name,
                model = self.model,
                parameter_table = self.parameter_table))
        run_button = ctk.CTkButton(
            buttonrow3_frame, text="Run", cursor="hand2", command=lambda: self.master.load_module(self.tool, "ResultsFrame"))

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
        problem_name_label.pack(side="left", padx=5)
        model_label.pack(side="left", padx=5)
        parameter_table_label.pack(side="left", padx=5)
        cfg1_frame.pack(pady=10,fill="x")

        # Second row of configuration widgets:
        # number of components, number of flash calculations
        nc_label.pack(side="left", padx=5)
        nc_spinbox.pack(side="left", padx=5)
        nf_label.pack(side="left", padx=5)
        nf_spinbox.pack(side="left", padx=5)
        cfg2_frame.pack(pady=10,fill="x")
        
        # Second row of buttons: Show Composition Table, Show Flash Table
        showct_button.pack(side="left", padx=5)
        showft_button.pack(side="left", padx=5)
        buttonrow2_frame.pack(pady=10,fill="x")

        # Comment frame
        comment_label.pack(padx=5, side = "left")
        comment_text.pack(padx=5,side="left")
        comment_frame.pack(pady=10,fill="x")

        # Third and last row of buttons: Save, Run, Back, Close
        back_button.pack(side="left", padx=5)
        ctk.CTkLabel(buttonrow3_frame, text="  |  ").pack(side="left", padx=10)
        save_button.pack(side="left", padx=5)
        run_button.pack(side="left", padx=5)
        ctk.CTkLabel(buttonrow3_frame, text="  |  ").pack(side="left", padx=10)
        close_button.pack(side="left", padx=5)
        buttonrow3_frame.pack(pady=50, side="bottom",fill="x")

        # Pack the worksheet frame
        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")

        self.pack(pady=0, expand=True, fill="both")
        return None
    
class WorkSheetFrame3(FlashCalcFrame):
    '''Class to create the worksheet frame. It has the following methods:
    load, save, open, close.'''
    error_message = None
    problem_name = None
    model = None
    parameter_table = None

    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''

        super().__init__(master, tool, **kwargs)
        self.error_message=kwargs.get('error_message',None)
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
        open_button = ctk.CTkButton(
            buttonrow1_frame, text="Open", cursor="hand2", command=self.open)
        reset_button = ctk.CTkButton(
            buttonrow1_frame, text="Reset", cursor="hand2", command=lambda: self.master.load_module(self.tool, "WorkSheetFrame1"))

        # First row of configuration widgets: 
        # Problem name, model, parameter table
        cfg1_frame = ctk.CTkFrame(self)
        problem_name_label = ctk.CTkLabel(cfg1_frame, text="Problem name:")
        problem_name_entry = widget_classes.TextEntry(cfg1_frame)
        model_label = ctk.CTkLabel(cfg1_frame, text="Model:")
        model_option = ctk.CTkOptionMenu(cfg1_frame, values=["UNIFAC", "A-UNIFAC"])
        parameter_table_label = ctk.CTkLabel(cfg1_frame, text="Parameter table:")
        parameter_table_option = ctk.CTkOptionMenu(cfg1_frame, values=["Vapor-Liquid", "Liquid-Liquid", "Infinity Dil."])

        # Second row of configuration widgets: 
        # number of components, number of flash calculations
        cfg2_frame = ctk.CTkFrame(self)
        nc_label = ctk.CTkLabel(
            cfg2_frame, text="Number of components:")
        nc_spinbox = tk.Spinbox(cfg2_frame, from_=1, to=10, width=5)
        nf_label = ctk.CTkLabel(
            cfg2_frame, text="Number of flash calculations:")
        nf_spinbox = tk.Spinbox(cfg2_frame, from_=1, to=10, width=5)

        # Second row of buttons: Show Composition Table, Show Flash Table
        buttonrow2_frame = ctk.CTkFrame(self)
        showct_button = ctk.CTkButton(
            buttonrow2_frame, text="Show the composition table", cursor="hand2")
        showft_button = ctk.CTkButton(
            buttonrow2_frame, text="Show the flash table", cursor="hand2")

        # Comment frame
        comment_frame = ctk.CTkFrame(self)
        comment_label = ctk.CTkLabel(comment_frame, text="Comments:")
        comment_text = widget_classes.TextEntry(comment_frame, width=400, height=5) 

        # Third and last row of buttons: Save, Run, Back, Close
        buttonrow3_frame = ctk.CTkFrame(self)
        save_button = ctk.CTkButton(
            buttonrow3_frame, text="Save", cursor="hand2", command=self.save)
        close_button = ctk.CTkButton(
            buttonrow3_frame, text="Close", cursor="hand2", command=self.master.close_module)
        back_button = ctk.CTkButton(
            buttonrow3_frame, text="Back", cursor="hand2", command=lambda: self.master.load_module(self.tool, "WelcomeFrame"))
        run_button = ctk.CTkButton(
            buttonrow3_frame, text="Run", cursor="hand2", command=lambda: self.master.load_module(self.tool, "ResultsFrame"))

        # Add the widgets to the frame with the pack method
        # Title and picture
        title.pack(side="left", padx = 5)
        flashcalc_picture.pack(side="left", padx = 5)
        title_frame.pack(pady=20)

        # First row of buttons: Open, Reset
        open_button.pack(side="left", padx=5)
        reset_button.pack(side="left", padx=5)
        buttonrow1_frame.pack(pady=10)

        # First row of configuration widgets: 
        # problem name, model, parameter table
        problem_name_label.pack(side="left", padx=5)
        problem_name_entry.pack(side="left", padx=5)
        model_label.pack(side="left", padx=5)
        model_option.pack(side="left", padx=5)
        parameter_table_label.pack(side="left", padx=5)
        parameter_table_option.pack(side="left", padx=5)
        cfg1_frame.pack(pady=10)

        # Second row of configuration widgets:
        # number of components, number of flash calculations
        nc_label.pack(side="left", padx=5)
        nc_spinbox.pack(side="left", padx=5)
        nf_label.pack(side="left", padx=5)
        nf_spinbox.pack(side="left", padx=5)
        cfg2_frame.pack(pady=10)
        
        # Second row of buttons: Show Composition Table, Show Flash Table
        showct_button.pack(side="left", padx=5)
        showft_button.pack(side="left", padx=5)
        buttonrow2_frame.pack(pady=10)

        # Comment frame
        comment_label.pack(padx=5, side = "left")
        comment_text.pack(padx=5,side="left")
        comment_frame.pack(pady=10)

        # Third and last row of buttons: Save, Run, Back, Close
        back_button.pack(side="left", padx=5)
        ctk.CTkLabel(buttonrow3_frame, text="  |  ").pack(side="left", padx=10)
        save_button.pack(side="left", padx=5)
        run_button.pack(side="left", padx=5)
        ctk.CTkLabel(buttonrow3_frame, text="  |  ").pack(side="left", padx=10)
        close_button.pack(side="left", padx=5)
        buttonrow3_frame.pack(pady=50, side="bottom")

        # Pack the worksheet frame
        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")

        self.pack(pady=0, expand=True, fill="both")
        return None
    