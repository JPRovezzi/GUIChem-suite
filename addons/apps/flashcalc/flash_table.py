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

class FlashTableWindow(ctk.CTkToplevel):
    '''Class to create the composition table window.'''
    table = []
    parameter_table = None
    groups = []
    temp_min = 273
    temp_max = 473
    temp_increment = 1
    pressure_min = 1
    pressure_max = 10
    pressure_increment = 0.01
    z_min = 0
    z_max = 1
    z_increment = 0.05
    number_of_components = 3
     
    def __init__(self, master,partable=None, **kwargs):
        '''Initialize the class.'''
        super().__init__(master, **kwargs)
        self.title("Flash Config Table")
        self.geometry("600x400")
        self.parameter_table = partable

        self.table = []
        self.table_frame = CTkXYFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Firt row of the table: Number of flashes, add and subtract buttons, save button and close button
        self.row_count_label = ctk.CTkLabel(
            self.table_frame,
            text=self.number_of_flashes())
        self.row_count_label.grid(row=0, column=0, padx=5, pady=5)
        self.add_row_button = ctk.CTkButton(
            self.table_frame, text="Add \n Flash", cursor="hand2", command=self.add_row)
        self.add_row_button.grid(row=0, column=1, padx=5, pady=5)
        
        self.subtract_row_button = ctk.CTkButton(
            self.table_frame, text="Subtract \n Flash", cursor="hand2", command=self.subtract_row)
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

    def number_of_flashes(self):
        '''Return the number of flashes in the table.'''
        return f"Number of flashes:\n {int(len(self.table)/3)}"
    

    def add_row(self):
        '''Add a pair of rows to the table.'''
        row1 = []
        
        flash_label = ctk.CTkLabel(
            self.table_frame, text=f"Flash {int(len(self.table)/3)+1}:")
        flash_label.grid(
            row=len(self.table) + 1, column=0, padx=0, pady=5)
        row1.append(flash_label)

        temp_label = ctk.CTkLabel(
            self.table_frame, text="Temperature (K):")
        temp_label.grid(
            row=len(self.table) + 1, column=1, padx=0, pady=5)
        row1.append(temp_label)


        pressure_label = ctk.CTkLabel(
            self.table_frame, text="Pressure (bar):")
        pressure_label.grid(
            row=len(self.table) + 1, column=2, padx=0, pady=5)
        row1.append(pressure_label)

        z_colmin = 3
        z_colmax = z_colmin + self.number_of_components # Assuming 3 componets for the table
        for col in range(z_colmin,z_colmax):  
            comp_label = ctk.CTkLabel(self.table_frame, text=f"z{col-z_colmin+1}", width=10)
            comp_label.grid(row=len(self.table) + 1, column=col, padx=5, pady=5)
            row1.append(comp_label)
        
        self.table.append(row1)

        row2 = []
        
        temp_box = tk.Spinbox(self.table_frame,
                              from_= self.temp_min,
                              to = self.temp_max,
                              increment = self.temp_increment,
                              width = 5)
        temp_box.grid(row = len(self.table) + 1,
                      column = 1,
                      padx = 5,
                      pady = 5)
        row2.append(temp_box)

        pressure_box = tk.Spinbox(self.table_frame,
                              from_= self.pressure_min,
                              to = self.pressure_max,
                              increment = self.pressure_increment,
                              width = 5)
        pressure_box.grid(row = len(self.table) + 1,
                      column = 2,
                      padx = 5,
                      pady = 5)
        row2.append(pressure_box)

        for col in range(z_colmin,z_colmax):
            z_box = tk.Spinbox(self.table_frame,
                                    from_=self.z_min,
                                    to=self.z_max,
                                    increment=self.z_increment,
                                    width=5)
            z_box.grid(row=len(self.table) + 1, column=col, padx=5, pady=5)
            row2.append(z_box)
        
        self.table.append(row2)
        self.row_count_label.configure(
            text=self.number_of_flashes())
        
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
            text=self.number_of_flashes())