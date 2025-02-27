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
    # Class variables:
    table = []
    parameter_table = None
    groups = []
    number_of_components = 3

    #Constants for the table
    temp_min = 273
    temp_max = 473
    temp_increment = 1
    pressure_min = 1
    pressure_max = 10
    pressure_increment = 0.1
    z_min = 0
    z_max = 1
    z_increment = 0.05
    
    fixed_rows = 2 # Minimum number of rows in the table
     
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
        buttons_row = []

        self.row_count_label = ctk.CTkLabel(
            self.table_frame,
            text=self.number_of_flashes())
        self.row_count_label.grid(row=0, column=0, padx=5, pady=5)
        buttons_row.append(self.row_count_label)

        self.auto_fill_button = ctk.CTkButton(
            self.table_frame,
            text="Auto Fill",
            cursor="hand2",
            command=lambda: self.auto_fill())
        self.auto_fill_button.grid(row=0, column=1, padx=5, pady=5)
        buttons_row.append(self.auto_fill_button)

        self.add_row_button = ctk.CTkButton(
            self.table_frame, text="Add \n Flash", cursor="hand2", command=self.add_row)
        self.add_row_button.grid(row=0, column=2, padx=5, pady=5)
        buttons_row.append(self.add_row_button)
        
        self.subtract_row_button = ctk.CTkButton(
            self.table_frame, text="Subtract \n Flash", cursor="hand2", command=self.subtract_row)
        self.subtract_row_button.grid(row=0, column=3, padx=5, pady=5)
        buttons_row.append(self.subtract_row_button)

        self.save_button = ctk.CTkButton(
            self.table_frame, text="Save", cursor="hand2")
        self.save_button.grid(row=0, column=4, padx=5, pady=5)
        buttons_row.append(self.save_button)

        self.close_button = ctk.CTkButton(
            self.table_frame, text="Close", cursor="hand2", command=self.destroy)
        self.close_button.grid(row=0, column=5, padx=5, pady=5)
        buttons_row.append(self.close_button)

        self.table.append(buttons_row)

        line_row = []
        for col in range(13):  # Assuming 13 columns for the table
            separator = ctk.CTkLabel(self.table_frame, text="_"*25)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0,sticky="n")
            line_row.append(separator)
        
        self.table.append(line_row)


        #self.add_row()

    def load_from_json(self, json_file):
        '''Load a table from a json file.'''
        with open(json_file) as f:
            data = json.load(f)
        self.load_table(data)

    
    def load_table(self,table):
        '''Load a table from a file.'''
        self.table = table
        for row in table:
            for entry in row:
                entry.grid()
        self.row_count_label.configure(
            text=self.number_of_flashes())

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

        if len(self.table) > (self.fixed_rows + 3) :
            prev_box = self.table[-3][0]
            temp_box.delete(0,tk.END)
            temp_box.insert(0,prev_box.get())

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
        if len(self.table) > (self.fixed_rows + 3) :
            prev_box = self.table[-3][1]
            pressure_box.delete(0,tk.END)
            pressure_box.insert(0,prev_box.get())

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
            if len(self.table) > (self.fixed_rows + 3) :
                prev_box = self.table[-3][col-1]
                z_box.delete(0,tk.END)
                z_box.insert(0,prev_box.get())
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
        '''Subtract rows from the table.'''
        rows_to_substract = 3 # Number of rows to subtract
        
        if self.table:
            for i in range(rows_to_substract):
                if len(self.table) > self.fixed_rows:
                    row = self.table.pop()
                    for entry in row:
                        entry.destroy()
        self.row_count_label.configure(
            text = self.number_of_flashes())
    
    def auto_fill(self):
        '''Fill the table with values.'''
        # Remove all rows below the fixed ones
        while len(self.table) > self.fixed_rows:
            row = self.table.pop()
            for entry in row:
                entry.destroy()

        # Add the label row:
        label_row = []

        labels = ["Settings", "Temperature", "Pressure"]
        for i in range(self.number_of_components):
            labels.append(f"z{i+1}")
        for label in labels:
            label_label = ctk.CTkLabel(self.table_frame, text=label)
            label_label.grid(row=len(self.table) + 1, column=labels.index(label), padx=5, pady=5)
            label_row.append(label_label)

        self.table.append(label_row)

        # Add the row with starting values
        starting_value_row = []

        starting_label = ctk.CTkLabel(self.table_frame, text="Starting Value:")
        starting_label.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        starting_value_row.append(starting_label)

        from_values = [self.temp_min, self.pressure_min]
        for i in range(self.number_of_components): 
            from_values.append(self.z_min)

        to_values = [self.temp_max, self.pressure_max]
        for i in range(self.number_of_components):
            to_values.append(self.z_max)

        increment_values = [self.temp_increment, self.pressure_increment]
        for i in range(self.number_of_components):
            increment_values.append(self.z_increment)
        
        for i, from_value in enumerate(from_values):
            initial_box = tk.Spinbox(
                self.table_frame,
                from_=from_value,
                to=to_values[i],
                increment=increment_values[i],
                width=5)
            initial_box.grid(
                row=len(self.table) + 1,
                column= i + 1,
                padx=5,
                pady=5)
            starting_value_row.append(initial_box)

        self.table.append(starting_value_row)

        # Add the row with final values
        final_value_row = []
        
        final_label = ctk.CTkLabel(self.table_frame, text="Final Value:")
        final_label.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        final_value_row.append(final_label)
        temp_final_box = tk.Spinbox(self.table_frame, from_=self.temp_min, to=self.temp_max, increment=self.temp_increment, width=5)
        temp_final_box.grid(row=len(self.table) + 1, column=1, padx=5, pady=5)
        final_value_row.append(temp_final_box)

        self.table.append(final_value_row)

        # Add the row with increment values
        increment_value_row = []
        increment_label = ctk.CTkLabel(self.table_frame, text="Increment:")
        increment_label.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        increment_value_row.append(increment_label)
        temp_increment_box = tk.Spinbox(self.table_frame, from_=self.temp_increment, to=self.temp_max, increment=self.temp_increment, width=5)
        temp_increment_box.grid(row=len(self.table) + 1, column=1, padx=5, pady=5)
        increment_value_row.append(temp_increment_box)

        
        self.table.append(increment_value_row)

        

        

        '''
        pressure_initial_box = tk.Spinbox(self.table_frame, from_=self.pressure_min, to=self.pressure_max, increment=self.pressure_increment, width=5)
        pressure_initial_box.grid(row=len(self.table) + 1, column=4, padx=5, pady=5)
        settings_row.append(pressure_initial_box)

        pressure_final_box = tk.Spinbox(self.table_frame, from_=self.pressure_min, to=self.pressure_max, increment=self.pressure_increment, width=5)
        pressure_final_box.grid(row=len(self.table) + 1, column=5, padx=5, pady=5)
        settings_row.append(pressure_final_box)

        pressure_increment_box = tk.Spinbox(self.table_frame, from_=self.pressure_increment, to=self.pressure_max, increment=self.pressure_increment, width=5)
        pressure_increment_box.grid(row=len(self.table) + 1, column=6, padx=5, pady=5)
        settings_row.append(pressure_increment_box)

        for col in range(self.number_of_components):
            z_initial_box = tk.Spinbox(self.table_frame, from_=self.z_min, to=self.z_max, increment=self.z_increment, width=5)
            z_initial_box.grid(row=len(self.table) + 1, column=7 + col * 3, padx=5, pady=5)
            settings_row.append(z_initial_box)

            z_final_box = tk.Spinbox(self.table_frame, from_=self.z_min, to=self.z_max, increment=self.z_increment, width=5)
            z_final_box.grid(row=len(self.table) + 1, column=8 + col * 3, padx=5, pady=5)
            settings_row.append(z_final_box)

            z_increment_box = tk.Spinbox(self.table_frame, from_=self.z_increment, to=self.z_max, increment=self.z_increment, width=5)
            z_increment_box.grid(row=len(self.table) + 1, column=9 + col * 3, padx=5, pady=5)
            settings_row.append(z_increment_box)

        self.table.append(settings_row)'''