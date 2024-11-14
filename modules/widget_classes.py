''' This module contains the class definitions for the custom widgets used in UGROpyGUI. '''
#------------------------------------------------------------
# Import the required libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
#------------------------------------------------------------

# Class definitions
class GoBackButton(ctk.CTkButton):
    ''' This class is a custom button widget that is used to navigate back to
    the previous screen. '''
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            text="BACK",
            cursor="hand2",
            **kwargs)

class TitleLabel(ctk.CTkLabel):
    ''' This class is a custom label widget that is used to display the 
    title'''
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            font=("TkMenuFont",14),
            **kwargs
            )
        