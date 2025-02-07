
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
            command=lambda: self.master.load_module(tool,"WorkSheetFrame")
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

class WorkSheetFrame(FlashCalcFrame):
    '''Class to create the worksheet frame. It has the following methods:
    load, save, open, close.'''
    error_message = None

    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''

        super().__init__(master, tool, **kwargs)
        self.error_message=kwargs.get('error_message',None)
        self.load(self.error_message)

    def load(self, error_message = None):
        '''Load the worksheet frame with its widgets.'''

        self.tkraise()
        self.pack_propagate(False)
        
        script_dir = os.path.dirname(__file__)
        image_path = script_dir+"/res/flashcalc.jpeg"
        image = Image.open(image_path)
        self.image = ctk.CTkImage(image, size=(80, 80))

        title_frame = ctk.CTkFrame(self)
        title= widget_classes.TitleLabel(title_frame, text="Flash-Calc")
        flashcalc_picture=ctk.CTkLabel(title_frame, image=self.image, text="")

        cfg1_frame = ctk.CTkFrame(self)
        problem_name_label = ctk.CTkLabel(cfg1_frame, text="Problem name:")
        problem_name_entry = widget_classes.TextEntry(cfg1_frame)
        model_label = ctk.CTkLabel(cfg1_frame, text="Model:")
        model_option = ctk.CTkOptionMenu(cfg1_frame, values=["UNIFAC", "A-UNIFAC"])
        parameter_table_label = ctk.CTkLabel(cfg1_frame, text="Parameter table:")
        parameter_table_option = ctk.CTkOptionMenu(cfg1_frame, values=["Vapor-Liquid", "Liquid-Liquid", "Infinity Dil."])

        cfg2_frame = ctk.CTkFrame(self)
        nc_label = ctk.CTkLabel(
            cfg2_frame, text="Number of components:")
        nc_spinbox = tk.Spinbox(cfg2_frame, from_=1, to=10, width=5)
        nf_label = ctk.CTkLabel(
            cfg2_frame, text="Number of flash calculations:")
        nf_spinbox = tk.Spinbox(cfg2_frame, from_=1, to=10, width=5)

        buttonrow1_frame = ctk.CTkFrame(self)
        showct_button = ctk.CTkButton(
            buttonrow1_frame, text="Show the composition table", cursor="hand2")
        showft_button = ctk.CTkButton(
            buttonrow1_frame, text="Show the flash table", cursor="hand2")

        comment_frame = ctk.CTkFrame(self)
        comment_label = ctk.CTkLabel(comment_frame, text="Comments:")
        comment_text = widget_classes.TextEntry(comment_frame, width=400, height=5)

        buttonrow2_frame = ctk.CTkFrame(self)
        save_button = ctk.CTkButton(
            buttonrow2_frame, text="Save", cursor="hand2", command=self.save)
        open_button = ctk.CTkButton(
            buttonrow2_frame, text="Open", cursor="hand2", command=self.open)
        close_button = ctk.CTkButton(
            buttonrow2_frame, text="Close", cursor="hand2", command=self.master.close_module)
        back_button = ctk.CTkButton(
            buttonrow2_frame, text="Back", cursor="hand2", command=lambda: self.master.load_module(self.tool, "WelcomeFrame"))
        reset_button = ctk.CTkButton(
            buttonrow2_frame, text="Reset", cursor="hand2", command=lambda: self.master.load_module(self.tool, "WorkSheetFrame"))

        title.pack(side="left")
        flashcalc_picture.pack()
        title_frame.pack()


        problem_name_label.pack(side="left", padx=5)
        problem_name_entry.pack(side="left", padx=5)
        model_label.pack(side="left", padx=5)
        model_option.pack(side="left", padx=5)
        parameter_table_label.pack(side="left", padx=5)
        parameter_table_option.pack(side="left", padx=5)
        cfg1_frame.pack()

        nc_label.pack(side="left", padx=5)
        nc_spinbox.pack(side="left", padx=5)
        nf_label.pack(side="left", padx=5)
        nf_spinbox.pack(side="left", padx=5)
        cfg2_frame.pack()
        
        showct_button.pack(side="left", padx=5)
        showft_button.pack(side="left", padx=5)
        buttonrow1_frame.pack()

        
        comment_label.pack(padx=5, side = "left")
        comment_text.pack(padx=5,side="left")
        comment_frame.pack()

        save_button.pack(side="left", padx=5)
        open_button.pack(side="left", padx=5)
        close_button.pack(side="left", padx=5)
        back_button.pack(side="left", padx=5)
        reset_button.pack(side="left", padx=5)
        buttonrow2_frame.pack(pady=50, side="bottom")

        # Add other widgets here as needed
        
        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")
        self.pack(pady=0, expand=True, fill="both")
        return None
    

    