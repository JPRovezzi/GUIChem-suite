'''This module is used to handle the tools that are selected by the user. It
is used to load the tools and destroy the previous frames.'''
#------------------------------------------------------------
# Importing the required modules:
# frameRoot is a module that provides functions the root frame of the GUI.
# ugroypygui is a module that provides functions to create and manage the
# UGROpyGUI tool.
import addons.ugropygui as ugropygui
#------------------------------------------------------------
# destroy_all_frames is deprecated and will be removed in a future version.
def destroy_all_frames():
    '''This function is used to destroy all the frames except the first two
    which are the menubar and the background.'''
    i = 0
    for widget in frame_root.root.winfo_children():
        if i >= 2:
            widget.destroy()
        i += 1

def save(tool):
    '''This function is used to save the data of the tool that the user is
    using.'''
    match tool:
        case "UgropyGUI":
            ugropygui.frame_save.load()
        case "Flash-Calc":
            None
