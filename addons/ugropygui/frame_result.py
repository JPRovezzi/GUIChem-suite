
"""
This module provides functions to create and manage the result frame of the 
GUI.
"""
# Import the required libraries:
# xml.etree.ElementTree is a module that provides functions to create and parse XML documents.
import xml.etree.ElementTree as ET
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# pubchempy is a module that provides functions to interact with the PubChem
import pubchempy
# ImageHandler is a module that provides functions to handle images.
import modules.image_handler as image_handler
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
# FrameRoot is a module that provides functions the root frame of the GUI.
import modules.main_frame.frame_root as frame_root
# tool_handler is a module that provides functions to handle the tools.
import modules.tool_handler as tool_handler
#------------------------------------------------------------

#------------------------------------------------------------
def load(
        molecule,
        name = None,
        smiles = None,
        formula = None,
        subgroups = None,
        picture = None
        ):
    ''' This function creates the result frame of the GUI. '''

    # Get the informations of the molecule
    mol_data = {
        "name": [name],
        "smiles": [smiles],
        "formula": [formula],
        "UNIFAC Subgroups": subgroups}
    if name is None:
        mol_data["name"] = pubchempy.get_compounds(
            mol_data["smiles"],
            namespace='smiles')[0].iupac_name
    if smiles is None:
        mol_data["smiles"] = pubchempy.get_compounds(
            name,
            namespace='name')[0].canonical_smiles
    if formula is None:
        mol_data["formula"] = pubchempy.get_compounds(
        smiles if smiles is not None else name,
        namespace =
        'smiles' if smiles is not None else "name")[0].molecular_formula

    if subgroups is None:
        mol_data["UNIFAC Subgroups"] = molecule.unifac.subgroups

    tool_handler.destroy_all_frames()
    frame_result = ctk.CTkFrame(master=frame_root.root)
    frame_result.tkraise()

    ctk.CTkLabel(
        frame_result,
        text="The molecule groups are displayed below.",
        ).pack()

    image_handler.insert_image(frame_result, "output.png")

    result_table = ctk.CTkFrame(master=frame_result)
    i = 0
    result_table_info = []
    for key,value in mol_data.items():
        ctk.CTkLabel(
            result_table,
            text=key.capitalize() + ": ",
            ).grid(row=i, column=0, sticky="w")
        widget_classes.CopyTextBox(
            result_table,
            width=300,
            height=10,
            activate_scrollbars=False)
        result_table.winfo_children()[-1].grid(row=i, column=1, sticky="w")
        result_table.winfo_children()[-1].insert("0.0", text=value)
        result_table_info.append(result_table.winfo_children()[-1])
        i += 1
    result_table.pack(fill="both")

    widget_classes.GoBackButton(
        frame_result,
        command=lambda:tool_handler.start_tool_event("UgropyGUI")
    ).pack(pady=10)
    frame_result.pack()

# Save data to a file
    xml_root = ET.Element("MoleculeData")

    xml_name_element = ET.SubElement(xml_root, "Name")
    xml_name_element.text = str(mol_data["name"][0])
    smiles_element = ET.SubElement(xml_root, "SMILES")
    smiles_element.text = str(mol_data["smiles"])
    formula_element = ET.SubElement(xml_root, "MolecularFormula")
    formula_element.text = str(mol_data["formula"])
    subgroups_element = ET.SubElement(xml_root, "UNIFACSubgroups")
    subgroups_element.text = str(mol_data["UNIFAC Subgroups"])
    tree = ET.ElementTree(xml_root)
    tree.write("ugropy.session")
