import tkinter as tk
import os
from PIL import Image
import json

import customtkinter as ctk

if os.name == 'nt':
    import pywinstyles

# Import the required third-party libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# CTkXYFrame is a custom frame with XY scrollbars for Python.
from modules.ctk_xyframe import CTkXYFrame
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes
from . import frame_classes

class CompositionTableWindow(ctk.CTkToplevel):
    '''Class to create the composition table window.'''
    table = []
    parameter_table = None
    groups = []
     
    def __init__(self, master,partable=None, **kwargs):
        '''Initialize the class.'''
        super().__init__(master, **kwargs)
        self.title("Composition Table")
        self.geometry("600x400")
        self.parameter_table = partable
        
        
        self.groups = self.load_groups(self.parameter_table)
                
        self.table = []
        self.table_frame = CTkXYFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Firt row of the table: Number of components, add and subtract buttons, save button and close button
        self.row_count_label = ctk.CTkLabel(
            self.table_frame,
            text=self.number_of_components())
        self.row_count_label.grid(row=0, column=0, padx=5, pady=5)
        self.add_row_button = ctk.CTkButton(
            self.table_frame, text="Add \n Component", cursor="hand2", command=self.add_row)
        self.add_row_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.subtract_row_button = ctk.CTkButton(
            self.table_frame, text="Subtract \n Component", cursor="hand2", command=self.subtract_row)
        self.subtract_row_button.grid(row=0, column=2, padx=5, pady=5)

        self.save_button = ctk.CTkButton(
            self.table_frame, text="Save", cursor="hand2")
        self.save_button.grid(row=0, column=3, padx=5, pady=5)

        self.close_button = ctk.CTkButton(
            self.table_frame, text="Close", cursor="hand2", command=self.destroy)
        self.close_button.grid(row=0, column=4, padx=5, pady=5)

        line_row = []
        for col in range(13):  # Assuming 13 columns for the table
            separator = ctk.CTkLabel(self.table_frame, text="_"*25)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0,sticky="n")
            line_row.append(separator)
        
        self.table.append(line_row)

        # Add the first pair of rows: 
        # Import, Component, Group, 10 groups
        # Export, Name,Number, 10 numbers
        self.add_row()

    def load_groups(self, parameter_table):
        '''Load the group list from the JSON file.'''
        script_dir = os.path.dirname(__file__)
        print(script_dir)
        for i in range (2):
                script_dir = os.path.dirname(script_dir)
        json_path = script_dir+"/models/FlashCalcUNIFAC/gruposram.json"
        print(json_path)
        with open(json_path, 'r') as file:
            data = json.load(file)
        return data.get(parameter_table, [])

    def number_of_components(self):
        '''Return the number of components in the table.'''
        return f"Number of components:\n {int(len(self.table)/3)}"
    

    def add_row(self):
        '''Add a pair of rows to the table.'''
        row1 = []
        
        import_button = ctk.CTkButton(
            self.table_frame, text="Import from file", cursor="hand2")
        import_button.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        row1.append(import_button)

        component_label = ctk.CTkLabel(
            self.table_frame, text=f"Component {int(len(self.table)/3)+1}:")
        component_label.grid(
            row=len(self.table) + 1, column=1, padx=0, pady=5)
        row1.append(component_label)

        group_label = ctk.CTkLabel(
            self.table_frame, text="Group:")
        group_label.grid(
            row=len(self.table) + 1, column=2, padx=0, pady=5)
        row1.append(group_label)

        for col in range(3,13):  # Assuming 11 columns for the table
            group_box = tk.Spinbox(self.table_frame, values=[f"{i}: {group}" for i, group in enumerate(self.groups)], width=10)
            group_box.grid(row=len(self.table) + 1, column=col, padx=5, pady=5)
            row1.append(group_box)
        
        self.table.append(row1)

        row2 = []
        export_button = ctk.CTkButton(
            self.table_frame, text="Export to file", cursor="hand2")
        export_button.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        row2.append(export_button)

        component_entry = widget_classes.TextEntry(self.table_frame)
        component_entry.grid(
            row=len(self.table) + 1, column=1, padx=5, pady=5)
        row2.append(component_entry)

        number_label = ctk.CTkLabel(
            self.table_frame, text="Number:")
        number_label.grid(
            row=len(self.table) + 1, column=2, padx=0, pady=5)
        row2.append(number_label)

        for col in range(3,13):  # Assuming 11 columns for the table
            #number_box = ctk.CTkLabel(self.table_frame, text="0")
            number_box = tk.Spinbox(self.table_frame, from_=0, to=10, width=5)
            number_box.grid(row=len(self.table) + 1, column=col, padx=5, pady=5)
            row2.append(number_box)
        
        self.table.append(row2)
        self.row_count_label.configure(
            text=self.number_of_components())
        
        # Add a separator row
        separator_row = []
        for col in range(13):  # Assuming 13 columns for the table
            separator = ctk.CTkLabel(self.table_frame, text="·"*37)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0,)
            separator_row.append(separator)
        
        self.table.append(separator_row)
    
    def subtract_row(self):
        '''Subtract a pair of rows from the table.'''
        if self.table:
            for i in range(3):
                if len(self.table) > 1:
                    row = self.table.pop()
                    for entry in row:
                        entry.destroy()
        self.row_count_label.configure(
            text=self.number_of_components())