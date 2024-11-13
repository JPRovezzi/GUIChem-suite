''' This module contains the class definitions for the custom widgets used in UGROpyGUI. '''
# Tkinter is a standard GUI library for Python.
import tkinter as tk
import customtkinter as ctk
# Configparser is used to read configuration files.
import configparser

#------------------------------------------------------------
# Read configuration file
config = configparser.ConfigParser()
config.read('config.cfg')

# Get background color from configuration file
bg_color = config.get('Settings', 'bg_color')

# Class definitions


class GoBackButton(tk.Button):
        def __init__(self, parent, **kwargs):
            super().__init__(
                parent, 
                text="BACK", 
                fg="black", 
                font=("TkMenuFont", 12), 
                bg="white", 
                cursor="hand2", 
                activebackground="gray", 
                **kwargs
                )

class TitleLabel(ctk.CTkLabel):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            #bg=bg_color,
            #fg="white",
            font=("TkMenuFont",14),
            **kwargs
            )