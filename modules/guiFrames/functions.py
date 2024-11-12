import shutil
from tkinter import filedialog


"""
    This module provides functions to create and manage a graphical user interface (GUI) for UGROpyGUI.
    Functions:
        clear_widgets_except(currentFrame): Clear all widgets except those in the specified frame.
"""
def clear_widgets_except(currentFrame,frames):
    for frame in frames:
        if frame != currentFrame:
            for widget in frame.winfo_children():
                widget.destroy()
    return None

def save_image(format):
    # Implement the logic to save the image in the specified format
    path = filedialog.asksaveasfilename(defaultextension=f".{format}", filetypes=[(f"{format.upper()} files", f"*.{format}")])
    if not path:
        return
    print(f"Saving image to {path} as {format}")
    if format == "svg":
        shutil.copy("input.svg", path)
    elif format == "png":
        shutil.copy("output.png", path)

    
        