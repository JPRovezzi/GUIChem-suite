
'''This module contains the classes for the frames of the flashcalc addon.'''

# Import the required standard libraries:
# OS module provides functions to interact with the operating system.
import os
# tkinter is a module that provides functions to create GUI applications.
import tkinter as tk
# xml.etree.ElementTree is a module that provides functions to create and parse XML documents.
import xml.etree.ElementTree as ET

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
        ctk.CTkButton(
            self,
            text="NEW",
            cursor="hand2",
            command=lambda: self.master.load_module(tool,"SelectionFrame")
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
        self.pack(pady=100)
        return None