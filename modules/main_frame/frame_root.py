
"""
    This module provides functions to create and manage the main GUI window
    and frames.
"""
# Import the required libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# ImageHandler is a module that provides functions to handle images.
import modules.image_handler as image_handler
# import the required functions to read the configuration files
from modules.main_frame.functions import read_json
from modules.widget_classes import MenuFrame

#------------------------------------------------------------

class Root(ctk.CTk):
    '''Class to create the main GUI window and frames.'''
    
    def __init__(self):
        '''Initialize the class.'''
        super().__init__()
        #self.root, self.appearance_menu = self.create_gui()
        print(self.background_path)
    
    # Read the configuration file to get the constants
    background_path = read_json(section = "PATH", key = "backgrounds")
    icon_path = "/".join((
        read_json(section = "PATH", key = "icons"),
        read_json(section = "FILENAME", key = "icon")
        ))
    window_width = read_json(section = "WINDOW", key = "width")
    window_height = read_json(section = "WINDOW", key = "height")
    is_resizable = read_json(section = "WINDOW", key = "resizable")
    window_title = read_json(section = "WINDOW", key = "title")
    addons = read_json(filename = "user", section = "ADDONS", key = "enabled")
    menuframe = None

    def create_gui(self):
        '''Create the main GUI window and frames.'''

        # Create the main window
        self.title(self.window_title)
        self.eval("tk::PlaceWindow . center")
        self.geometry("x".join((self.window_width, self.window_height)))
        if self.is_resizable == "false":
            self.resizable(0, 0)  # Disable resizing
        self.after(
            201,
            lambda :self.iconbitmap(self.icon_path))
        image_handler.place_image(self, 0, 0, self.background_path)
        #Frames
        self.create_menu()
        ctk.set_appearance_mode("system")
        # Start the main loop
        self.mainloop()
        return
    
    def create_menu(self):
        '''Create the menu bar.'''
        self.menuframe = MenuFrame(self)

    def destroy_all_frames(self):
        '''This function is used to destroy all the frames except the first two
        which are the menubar and the background.'''
        i = 0
        for widget in self.winfo_children():
            if i >= 2:
                widget.destroy()
            i += 1
        
        
