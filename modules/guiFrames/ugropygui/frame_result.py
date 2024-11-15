
"""
This module provides functions to create and manage the result frame of the 
GUI.
"""
# Import the required libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# pubchempy is a module that provides functions to interact with the PubChem
import pubchempy
# ImageHandler is a module that provides functions to handle images.
import modules.image_handler as image_handler
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
# FrameRoot is a module that provides functions the root frame of the GUI.
import modules.guiFrames.frame_root as frame_root
import modules.tool_handler as tool_handler



#------------------------------------------------------------

#------------------------------------------------------------
def load(molecule, name = None, smiles = None):
    ''' This function creates the result frame of the GUI. '''
    tool_handler.destroy_all_frames()
    frame_result = ctk.CTkFrame(master=frame_root.root)
    frame_result.tkraise()

    ctk.CTkLabel(
        frame_result,
        text="The molecule groups are displayed below.",
        ).pack()

    image_handler.insert_image(frame_result, "output.png")

    result_table = ctk.CTkFrame(master=frame_result)

    ctk.CTkLabel(
        result_table,
        text="Name: ",
        ).grid(row=0, column=0, sticky="w")

    ctk.CTkLabel(
        result_table,
        text =str(name if name is not None
                              else pubchempy.get_compounds(
                                  smiles,
                                  namespace='smiles')[0].iupac_name)
        ).grid(row=0, column=1, sticky="w")

    ctk.CTkLabel(
        result_table,
        text="SMILES: "
        ).grid(row=1, column=0, sticky="w")

    ctk.CTkLabel(
        result_table,
        text = str(smiles if smiles is not None 
                              else pubchempy.get_compounds(
                                  name,
                                  namespace='name')[0].canonical_smiles)
        ).grid(row=1, column=1, sticky="w")

    ctk.CTkLabel(
        result_table,
        text = molecule.unifac.subgroups,
        ).grid(row=2, column=1, sticky="w")

    result_table.pack(fill="both")

    widget_classes.GoBackButton(
        frame_result,
        command=lambda:tool_handler.start_tool_event("UgropyGUI")
    ).pack(pady=10)
    frame_result.pack()
    return None
