''' This module contains the class definitions for the custom widgets used in UGROpyGUI. '''
#------------------------------------------------------------
# Import the required libraries:
# Tkinter is a standard GUI library for Python.
import tkinter as tk
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
import modules.main_frame.frame_root as frame_root
import modules.tool_handler as tool_handler
import modules.image_handler as image_handler
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

class TextEntry(ctk.CTkEntry):
    ''' This class is a custom entry widget that is used to get text input from
    the user.'''
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            **kwargs
            )
         # Create labels and commands
        self.bind('<Button-3>',self.popup) # Bind a func to right click
        self.menu = tk.Menu(self,tearoff=0) # Create a menu
        self.menu.add_command(label='Paste',command=self.paste)
        self.menu.add_command(label='Clear',command=self.clear)

    def popup(self,event):
        ''' This function creates a popup menu when the user right-clicks on
        the textbox.'''
        try:
            self.focus_set() # Give focus to the textbox
            self.menu.tk_popup(event.x_root,event.y_root) # Pop the menu up in the given coordinates
        finally:
            self.menu.grab_release() # Release it once an option is selected

    def paste(self):
        ''' This function pastes the text from the clipboard to the textbox.'''
        self.clipboard_get()
        self.insert(tk.END, self.clipboard_get())

    def clear(self):
        ''' This function clears the text in the textbox.'''
        self.delete(0, tk.END)

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
            self.focus_set() # Give focus to the textbox
            self.menu.tk_popup(event.x_root,event.y_root) # Pop the menu up in the given coordinates
        finally:
            self.menu.grab_release() # Release it once an option is selected

    def copy(self):
        ''' This function copies the text in the textbox to the clipboard.'''
        #inp = root.get() # Get the text inside entry widget
        self.clipboard_clear() # Clear the tkinter clipboard
        try:
            text = self.selection_get() # Get the selected text
        except tk.TclError:
            text = self.get(1.0,"end") # if no text is selected, copy all text
        self.clipboard_append(text) # Append to system clipboard
    def select_all(self):
        ''' This function selects all the text in the textbox.'''
        self.tag_add('sel', '1.0', 'end')
        self.mark_set('insert', '1.0')
        self.see('insert')

class FileMenu(ctk.CTkOptionMenu):
    ''' This class is a custom option menu widget that is used to display a list
    of options to the user.'''
    menu = None
    root = None
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            values = self.options(),
            command = self.events,
            **kwargs
            )
        self.menu = parent
        self.root = self.menu.root
        self.set("File")
        self.grid(
            row=0,
            column=0,
            pady=10,
            padx=10)
        
    def events(self, event):
        ''' This function is called when an option is selected from the menu.'''
        self.set("File")
        match event:
            case "New":
                tool_handler.select_tool_event(self.menu.tools_menu.get())
            case "Open":
                print("Open file")
            case "Save":
                tool_handler.save(self.menu.tools_menu.get())
                print("Save file")
            case "Close":
                self.root.destroy_all_frames()
            case "Exit":
                self.root.destroy()
            case _:
                print("Invalid option")

    def options(self):
        ''' This function returns the list of options in the menu.'''
        return ["New", "Open", "Save", "Close","","Exit"]
    
class MenuFrame(ctk.CTkFrame):
    ''' This class is a custom frame widget that is used to create a frame for
    the menu bar.'''
    file_menu = None
    appearance_menu = None
    tools_menu = None
    root = None

    def __init__(self, parent, **kwargs):
        
        super().__init__(
            parent,
            **kwargs
            )
        self.root = parent
        self.file_menu = FileMenu(
            self,
            corner_radius=0,
            )
        self.appearance_menu = ctk.CTkOptionMenu(
            self,
            corner_radius=0,
            values=["Light", "Dark", "System"],
            command = image_handler.change_appearance_mode_event
            )

        self.appearance_menu.set("Theme")
        self.appearance_menu.grid(
            row=0,
            column=2,
            pady=10,
            padx=10)
        self.tools_menu = ctk.CTkOptionMenu(
            self,
            corner_radius=0,
            values=parent.addons
            )
        self.tools_menu.grid(
            row=0,
            column=1,
            pady=10,
            padx=10)
        self.tools_menu.set("Tools")
        self.pack(anchor="w",fill="both",padx=0, pady=0)
        