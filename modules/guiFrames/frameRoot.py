
"""
    This module provides functions to create and manage a graphical user interface (GUI) for UGROpyGUI.
    Functions:
        create_gui(): Create the main GUI window and frames.
        load_frame_welcome(): Load the welcome frame with its widgets.
        load_frame_selection(error_message=None): Load the selection frame with its widgets.
        load_frame_result(molecule): Load the result frame with its widgets.
        clear_widgets_except(currentFrame): Clear all widgets except those in the specified frame.
"""
# Import the required libraries:

# Tkinter is a standard GUI library for Python.
import tkinter as tk
import ctypes as ct
# Configparser is used to read configuration files.
import configparser

# frameWelcome is a module that provides functions to create and manage the welcome frame of the GUI.
import modules.guiFrames.frameWelcome as frameWelcome

#import modules.guiFrames.frameSavePicture as frameSavePicture

#------------------------------------------------------------
# Read configuration file
config = configparser.ConfigParser()
config.read('config.cfg')

# Get background color from configuration file
bg_color = config.get('Settings', 'bg_color')

#------------------------------------------------------------


#------------------------------------------------------------
# Function definitions

def dark_title_bar(window):
    """
    MORE INFO:
    https://learn.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    window.update()
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(window.winfo_id())
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, 20, ct.byref(value),
                         4)

def create_gui():

    '''Create the main GUI window and frames.'''
    global root, frame_welcome, frame_selection, frame_getName, frame_result, frames
    root = tk.Tk()
    root.title("UGROpyGUI")
    root.resizable(0, 0)  # Disable resizing
    #dark_title_bar(root)
    root.eval("tk::PlaceWindow . center")

    # Create a menu bar
    menu_bar = tk.Menu(root)
    
    # Create a file menu
    file_menu = tk.Menu(menu_bar, tearoff=0)
    #file_menu.add_command(label="Save last picture", command=lambda: frameSavePicture.load())
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=root.quit)
    menu_bar.add_cascade(label="File", menu=file_menu)
    # Create an options menu
    options_menu = tk.Menu(menu_bar, tearoff=0)
    options_menu.add_command(label="Preferences", command=lambda: print("Option 1 selected"))
    menu_bar.add_cascade(label="Settings", menu=options_menu)
    # Add the menu bar to the root window
    root.config(menu=menu_bar)

    # Create frames
    frame_welcome = tk.Frame(root, width=640, height=480, bg=bg_color)



    frame_selection = tk.Frame(root, width=640, height=480, bg=bg_color)
    frame_getName = tk.Frame(root, width=640, height=480, bg=bg_color)
    frame_result = tk.Frame(root, width=640, height=480, bg=bg_color)
    frames = (frame_welcome, frame_selection, frame_getName, frame_result)

    for frame in frames:
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid(row=0, column=0, sticky="nesw")

    #Load the welcome frame
    

    

    frameWelcome.load()

    # Start the main loop
    root.mainloop()
    return None





    





    
    