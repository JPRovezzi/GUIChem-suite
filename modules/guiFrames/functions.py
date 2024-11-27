"""This module provides functions to create and manage a graphical user
interface (GUI) for UGROpyGUI.
Functions:
    clear_widgets_except(currentFrame): Clear all widgets except those in the
    specified frame.
"""
# Import the required modules:
# import shutil module to copy files
import shutil
# import filedialog from tkinter module to save files
from tkinter import filedialog
#---------------------------------------------------------

def save_image(file_format):
    '''Implement the logic to save the image in the specified file_format'''
    path = filedialog.asksaveasfilename(
        defaultextension = f".{file_format}",
        filetypes = [(f"{file_format.upper()} files", f"*.{file_format}")])
    if not path:
        return
    if file_format == "svg":
        shutil.copy("input.svg", path)
    elif file_format == "png":
        shutil.copy("output.png", path)

def save_data(file_format):
    '''Implement the logic to save the image in the specified file_format'''
    path = filedialog.asksaveasfilename(
        defaultextension = f".{file_format}",
        filetypes = [(f"{file_format.upper()} files", f"*.{file_format}")])
    if not path:
        return
    if file_format == "svg":
        shutil.copy("input.svg", path)
    elif file_format == "png":
        shutil.copy("output.png", path)