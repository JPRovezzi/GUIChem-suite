''' This module contains the class definitions for the custom widgets used in UGROpyGUI. '''
#------------------------------------------------------------
# Import the required libraries:
# Tkinter is a standard GUI library for Python.
import tkinter as tk
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

class CopyTextBox(ctk.CTkTextbox):
    ''' This class is a custom textbox widget that is allowed to copy the text'''
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            **kwargs
            )
         # Create labels and commands
        self.bind('<Button-3>',self.popup) # Bind a func to right click
        self.menu = tk.Menu(self,tearoff=0) # Create a menu
        self.menu.add_command(label='Select all',command=self.select_all)
        self.menu.add_command(label='Copy',command=self.copy)
    def popup(self,event):
        ''' This function creates a popup menu when the user right-clicks on
        the textbox.'''
        try:
            self.menu.tk_popup(event.x_root,event.y_root) # Pop the menu up in the given coordinates
        finally:
            self.menu.grab_release() # Release it once an option is selected

    def copy(self):
        ''' This function copies the text in the textbox to the clipboard.'''
        #inp = root.get() # Get the text inside entry widget
        self.clipboard_clear() # Clear the tkinter clipboard
        text = self.selection_get()
        self.clipboard_append(text) # Append to system clipboard
    def select_all(self):
        ''' This function selects all the text in the textbox.'''
        self.tag_add('sel', '1.0', 'end')
        self.mark_set('insert', '1.0')
        self.see('insert')