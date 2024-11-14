
"""
This module provides functions to create and manage the result frame of the 
GUI.
"""
# Import the required libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# ImageHandler is a module that provides functions to handle images.
import modules.image_handler as image_handler
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
# FrameRoot is a module that provides functions the root frame of the GUI.
import modules.guiFrames.frame_root as frame_root
import modules.tool_handler as tool_handler



#------------------------------------------------------------

#------------------------------------------------------------
def load(molecule):
    ''' This function creates the result frame of the GUI. '''
    tool_handler.destroy_all_frames()
    frame_result = ctk.CTkFrame(master=frame_root.root)
    frame_result.tkraise()

    ctk.CTkLabel(
        frame_result,
        text="The molecule groups are displayed below.",
        #bg=bg_color,
        #fg="white",
        #font=("TkMenuFont",14)
        ).pack(pady=20)

    image_handler.insert_image(frame_result, "output.png")

    ctk.CTkLabel(
        frame_result,
        text = molecule.unifac.subgroups,
        #bg=bg_color,
        #fg="white",
        ).pack()

    widget_classes.GoBackButton(
        frame_result,
        command=lambda:tool_handler.start_tool_event("UgropyGUI")
    ).pack(pady=50)

    frame_result.pack()
    return None
