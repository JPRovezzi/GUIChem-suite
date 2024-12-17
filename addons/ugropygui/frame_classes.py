'''This module contains the classes for the frames of the GUIChem-suite application.'''
# Import the required libraries:

# OS module provides functions to interact with the operating system.
import os
import tkinter as tk
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# xml.etree.ElementTree is a module that provides functions to create and parse XML documents.
import xml.etree.ElementTree as ET
# pubchempy is a module that provides functions to interact with the PubChem
import pubchempy
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
import modules.image_handler as image_handler
# svg_handler is a module that provides functions to handle SVG files.
import addons.ugropygui.svg_handler as svg_handler
# pywinstyles is a library that provides functions to set the opacity of a window.
# import the image handler module
import modules.image_handler as imageHandler
# import shutil module to copy files
import shutil
if os.name == 'nt':
    import pywinstyles

class UgropyFrame(ctk.CTkFrame):
    '''Class to create the Ugropy frame.'''
    master = None
    tool = None
    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''
        super().__init__(master=master, corner_radius=50, bg_color="#000000")
        self.master = master
        self.tool = tool
        kwargs

    def save(self):
        '''Save the data to a file by creating the save window and display the image to save'''
        def save_image(file_format):
            '''Implement the logic to save the image in the specified file_format'''
            path = tk.filedialog.asksaveasfilename(
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
            filetypes = []
            for extention in file_format:
                filetypes.append((f"{extention.upper()} files", f"*.{extention}"))
            path = tk.filedialog.asksaveasfilename(
                defaultextension = f".{file_format[0]}",
                filetypes = filetypes)
            if not path:
                return
            shutil.copy("ugropy.session", path)
        save_window = tk.Toplevel(self.master)
        save_window.resizable(0, 0)  # Disable resizing
        save_window.title("Save (last session)")
        save_window.transient(self.master)
        save_window.grab_set()
        # Display the output PNG as a widget
        if os.path.exists("output.png"):
            imageHandler.insert_image(save_window, "output.png")
        else:
            save_window.destroy()
            return

        # Selection box to select if it is a SVG image or a PNG image
        tk.Label(save_window, text="Select picture format:").pack(pady=5)
        format_var = tk.StringVar(value="png")

        # Frame to hold the radio buttons
        radiobutton_frame = tk.Frame(save_window)
        radiobutton_frame.pack(pady=10)

        tk.Radiobutton(
                radiobutton_frame,
                text="PNG",
                variable = format_var,
                value="png"
                ).pack(side=tk.LEFT,padx=0)
        tk.Radiobutton(
                radiobutton_frame,
                text="SVG",
                variable = format_var,
                value = "svg"
                ).pack(side=tk.LEFT,padx=0)

        # Frame to hold the buttons
        button_frame = tk.Frame(save_window)
        button_frame.pack(pady=10)

        # Save button
        tk.Button(
            button_frame,
            text="Save picture",
            command=lambda: save_image(format_var.get())
            ).pack(side=tk.LEFT, padx=5)


        tk.Button(
            button_frame,
            text="Save data",
            command=lambda: save_data(["txt", "xml", "session"])
            ).pack(side=tk.LEFT, padx=5)

        # Cancel button
        tk.Button(
            button_frame,
            text="Close",
            command=lambda: save_window.destroy()
            ).pack(side=tk.LEFT, padx=5)

    def open(self):
        '''Load the data from a file.'''
        pass
    

class WelcomeFrame(UgropyFrame):
    '''Class to create the welcome frame.'''
    master=None
    tool=None
    def __init__(self, master, tool):
        '''Initialize the class.'''
        super().__init__(master, tool)
        self.load(tool)
    
    def load(self, tool):
        '''Load the welcome frame with its widgets.'''
        self.tkraise()
        self.pack_propagate(False)
        widget_classes.TitleLabel(self, text="").pack(pady=0)
        widget_classes.TitleLabel(self, text=f"Welcome to {tool}!").pack(pady=0)
        ctk.CTkButton(
            self,
            text="START",
            cursor="hand2",
            command=lambda: self.master.load_module(tool,"SelectionFrame")
            ).pack(pady=10)
        ctk.CTkButton(
            self,
            text="CLOSE",
            cursor="hand2",
            command=self.master.close_module
            ).pack(pady=10)
        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")
        self.pack(pady=100)
        return None

class SelectionFrame(UgropyFrame):
    '''Class to create the selection frame.'''
    molecule_id_var = None
    error_message = None
    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''
        super().__init__(master, tool, **kwargs)
        self.error_message=kwargs.get('error_message',None)
        self.load(self.error_message)
        
    
    def load(self, error_message = None):
        ''' This function creates the frame_selection frame. This frame allows the 
        user to enter the chemical identifier of the molecule and select the type 
        of identifier (NAME or SMILES). The user can also go back to the UgropyGUI 
        frame. '''
        def select_name(self):
            input_type = 'name'
            molecule_id = self.molecule_id_var.get()
            outcome = svg_handler.get_results(molecule_id,input_type)
            molecule,error = outcome
            if error is None and molecule is not None:
                self.destroy()
                self.master.load_module(self.tool,"ResultFrame",molecule=molecule, name=molecule_id)
                #frame_result.load(molecule, name = molecule_id)
                error_message = ""
            elif error == 1:
                error_message = "The NAME identifier is not valid. Please try again."
                self.master.load_module(self.tool,"SelectionFrame",error_message=error_message)
            elif error == 2:
                error_message = "You must enter a NAME identifier. Please try again."
                self.master.load_module(self.tool,"SelectionFrame",error_message=error_message)
            else:
                error_message = "Unknown error. Please try again."
                self.master.load_module(self.tool,"SelectionFrame",error_message=error_message)
            return

        def select_smiles(self):
            input_type = 'smiles'
            molecule_id = self.molecule_id_var.get()
            outcome = svg_handler.get_results(molecule_id,input_type)
            molecule,error = outcome
            if error is None and molecule is not None:
                self.destroy()
                self.master.load_module(self.tool,"ResultFrame",molecule=molecule, smiles=molecule_id)
                error_message = ""
            elif error == 1:
                error_message = "The SMILES identifier is not valid. Please try again."
                self.master.load_module(self.tool,"SelectionFrame",error_message=error_message)
            elif error == 2:
                error_message = "You must enter a SMILES identifier. Please try again."
                self.master.load_module(self.tool,"SelectionFrame",error_message=error_message)
            else:
                error_message = "Unknown error. Please try again."
                self.master.load_module(self.tool,"SelectionFrame",error_message=error_message)
            return

        self.tkraise()

        # frame_selection widgets
        ctk.CTkLabel(self,
                    text="",
                    ).pack(pady=0)
        widget_classes.TitleLabel(
            self,
            text = "Please enter the Chemical identifier of the molecule:"
            ).pack(pady=0)

        self.molecule_id_var = ctk.StringVar()
        widget_classes.TextEntry(
            self,
            textvariable = self.molecule_id_var
            ).pack(pady=20)

        ctk.CTkLabel(
            self,
            text = self.error_message,
            ).pack(pady=0)

        widget_classes.TitleLabel(
            self,
            text="Select the type of Chemical identifier",
            ).pack(pady=0)

        ctk.CTkButton(
            self,
            text="NAME",
            cursor="hand2",
            command=lambda:select_name(self)
            ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="SMILES",
            cursor="hand2",
            command=lambda:select_smiles(self)
            ).pack(pady=10)

        widget_classes.GoBackButton(
            self,
            command=lambda:self.master.load_module(self.tool,"WelcomeFrame")
        ).pack(pady=50)

        self.pack()
        return None

class   ResultFrame(UgropyFrame):
    '''Class to create the result frame.'''
    molecule = None
    name = None
    smiles = None
    def __init__(self, master, tool, **kwargs):
        '''Initialize the class.'''
        super().__init__(master, tool, **kwargs)
        self.molecule=kwargs.get('molecule',None)
        self.name=kwargs.get('name',None)
        self.smiles=kwargs.get('smiles',None)
        self.load(self.molecule, self.name, self.smiles)
        

    def load(self,
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

        #self.master.destroy_all_frames()
        #frame_result = ctk.CTkFrame(master=frame_root.root)
        self.tkraise()

        ctk.CTkLabel(
            self,
            text="The molecule groups are displayed below.",
            ).pack()

        image_handler.insert_image(self, "output.png")

        result_table = ctk.CTkFrame(master=self)
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
            self,
            command=lambda:self.master.load_module(self.tool,"SelectionFrame")
        ).pack(pady=10)
        self.pack()

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