''' This module contains the class definitions for the custom widgets used in UGROpyGUI. '''
#------------------------------------------------------------
# Import the required standard libraries:
# Tkinter is a standard GUI library for Python.
import tkinter as tk
# random is a standard library for generating random numbers.
import random
# PIL is a standard library for image processing.
from PIL import Image
# Import the required 3rd party libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk

import modules.image_handler as image_handler
from modules.main_frame.functions import read_json
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
    ''' This class is a custom option menu widget that is used to display a 
    list of options to the user.'''
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
                self.start_tool_event(action = "new")
            case "Open":
                self.start_tool_event(action = "open")
            case "Save":
                if self.root.module_frame is not None:
                    self.root.module_frame.save()
            case "Close":
                self.root.close_module()
            case "Exit":
                self.root.destroy()
            case _:
                print("Invalid option")

    def options(self):
        ''' This function returns the list of options in the menu.'''
        return ["New", "Open", "Save", "Close","","Exit"]

    def select_tool_event(self, tool: str, action = "new"):
        '''This function is used to select the tool that the user wants to use.'''
        if action == "new":
            if tool != "Tools":
                self.root.destroy_all_frames()
                self.root.load_module(tool,'WelcomeFrame')
        if action == "open":
            if tool != "Tools":
                self.root.load_module(tool,'WelcomeFrame')

    def open_tool_event(self):
        '''This function is used to open a file of the tool that the user wants to use.'''
        open_window = tk.Toplevel(self.master)
        open_window.resizable(0, 0)  # Disable resizing
        open_window.title("Open file")
        open_window.transient(self.master)
        open_window.grab_set()

        # Selection box to select if it is a SVG image or a PNG image
        tk.Label(open_window, text="Select tool:").pack(pady=5)

        # Frame to hold the buttons
        button_frame = tk.Frame(open_window)
        button_frame.pack(pady=10)

        # Save button
        tk.Button(
            button_frame,
            text="Open",
            command=lambda: None
            ).pack(side=tk.LEFT, padx=5)

        # Cancel button
        tk.Button(
            button_frame,
            text="Close",
            command=lambda: open_window.destroy()
            ).pack(side=tk.LEFT, padx=5)
        return

    def start_tool_event(self,action: str):
        '''This function is used to create a new file of the tool that the user wants to use.'''

        match action:
            case "new":
                title = "New file"
                button_text = "Create"
            case "open":
                title = "Open file"
                button_text = "Open"
            case _:
                pass
        select_window = ctk.CTkToplevel(self.master)
        select_window.resizable(0, 0)  # Disable resizing
        select_window.title(title)
        select_window.transient(self.master)
        select_window.grab_set()

        # Selection box to select if it is a SVG image or a PNG image
        ctk.CTkLabel(select_window, text="Select tool:").pack(pady=5)
        # Create a scrollable listbox to display the values of parent.addons
        listbox_frame = ctk.CTkFrame(select_window)
        listbox_frame.pack(pady=10)

        scrollbar = tk.Scrollbar(listbox_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(listbox_frame, yscrollcommand=scrollbar.set)
        for addon in self.root.addons:
            listbox.insert(tk.END, addon)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        if listbox.size() > 0:
            listbox.select_set(0)  # Auto-select the first item

        scrollbar.config(command=listbox.yview)
        # Frame to hold the buttons
        button_frame = ctk.CTkFrame(select_window)
        button_frame.pack(pady=10)

        # New button
        ctk.CTkButton(
            button_frame,
            text=button_text,
            command=lambda: (self.select_tool_event(
                listbox.get(
                    listbox.curselection()), action), select_window.destroy())
            ).pack(side=tk.LEFT, padx=5)

        # Cancel button
        ctk.CTkButton(
            button_frame,
            text="Close",
            command=lambda: select_window.destroy()
            ).pack(side=tk.LEFT, padx=5)
        return

class MenuFrame(ctk.CTkFrame):
    ''' This class is a custom frame widget that is used to create a frame for
    the menu bar.'''
    file_menu = None
    appearance_menu = None
    tools_menu = None
    root = None

    def __init__(self, parent, **kwargs):
        ''' This function initializes the menu frame.'''
        super().__init__(
            parent,
            **kwargs
            )
        self.root = parent
        self.file_menu = FileMenu(
            self,
            corner_radius=0,
            )
        self.appearance_menu = AppearanceMenu(
            self,
            )

        self.appearance_menu.set("Theme")
        self.appearance_menu.grid(
            row=0,
            column=2,
            pady=10,
            padx=10)
        self.pack(anchor="w",fill="both",padx=0, pady=0)

class AppearanceMenu(ctk.CTkOptionMenu):
    ''' This class is a custom option menu widget that is used to display a list
    of options to the user.'''
    menu = None
    root = None
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            corner_radius=0,
            values = ["Light", "Dark", "System"],
            command = self.change_appearance_mode_event,
            **kwargs
            )
        self.set("Theme")
        self.menu = parent
        self.root = self.menu.root
    def change_appearance_mode_event(self, new_appearance_mode: str):
        '''Change the appearance mode of the GUI.'''

        backgrounds_path = read_json(section = "PATH",key = "backgrounds")

        # Reset the appearance menu label
        self.set("Theme")
        # Change the appearance mode
        ctk.set_appearance_mode(new_appearance_mode)
            # Change the default color theme
        if new_appearance_mode == "Light":
            ctk.set_default_color_theme("blue")
        else:
            ctk.set_default_color_theme("dark-blue")
        # Change light and dark mode images
        light_image=Image.open(
            image_handler.random_image(f"{backgrounds_path}/light")
                ).rotate(random.choice([0,90,180,270]))
        dark_image=Image.open(
            image_handler.random_image(f"{backgrounds_path}/dark")
                ).rotate(random.choice([0,90,180,270]))
        image = ctk.CTkImage(
            light_image=light_image,
            dark_image=dark_image,
            size=(800,800))
        # Change the image of the main frame
        self.root.winfo_children()[0].configure(image=image)
        return None
