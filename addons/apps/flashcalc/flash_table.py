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
    # The values are intergers
    temp_min = 27300 # 273 K
    temp_max = 47300 # 473 K
    temp_increment = 100 # 1 K
    pressure_min = 100 # 1 bar
    pressure_max = 1000 # 1000 bar
    pressure_increment = 10 # 0.1 bar
    z_min = 0 # 0 
    z_max = 100 # 1
    z_increment = 5 # 0.05
    
    fixed_rows = 2 # Minimum number of rows in the table
    max_columns = 13 # Maximum number of columns in the table
     
    #Text for the table
    title_text = "Flash Config Table"
    number_of_flashes_text = "Number of flashes:"
    auto_fill_text = "Auto Fill"
    add_flash_text = "Add\nFlash"
    subtract_flash_text = "Subtract\nFlash"
    save_text = "Save"
    close_text = "Close"
    flash_text = "Flash"
    temperature_text = "Temperature (K):"
    pressure_text = "Pressure (bar):"
    setting_text = "Settings"
    increment_text = "Increment"
    starting_value_text = "Starting Value"
    final_value_text = "Final Value"


    def __init__(self, master,partable=None, **kwargs):
        '''Initialize the class.'''
        super().__init__(master, **kwargs)
        self.title(self.title_text)
        self.geometry("600x400")
        self.parameter_table = partable

        self.table = []
        self.table_frame = CTkXYFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # First row of the table: Number of flashes, add and subtract buttons, save button and close button
        buttons_row = []

        self.row_count_label = ctk.CTkLabel(
            self.table_frame,
            text=self.number_of_flashes())
        self.row_count_label.grid(row=0, column=0, padx=5, pady=5)
        buttons_row.append(self.row_count_label)

        self.auto_fill_checkbox = ctk.CTkCheckBox(
            self.table_frame,
            text=self.auto_fill_text,
            variable=tk.BooleanVar(),
            command=lambda: self.auto_fill() if self.auto_fill_checkbox.get()  else self.clear_table()
            )
        self.auto_fill_checkbox.grid(row=0, column=1, padx=5, pady=5)
        buttons_row.append(self.auto_fill_checkbox)

        self.add_row_button = ctk.CTkButton(
            self.table_frame,
            text=self.add_flash_text,
            cursor="hand2",
            command=lambda: None if self.auto_fill_checkbox.get() else self.add_row())
        self.add_row_button.grid(row=0, column=2, padx=5, pady=5)
        buttons_row.append(self.add_row_button)
        
        self.subtract_row_button = ctk.CTkButton(
            self.table_frame,
            text=self.subtract_flash_text,
            cursor="hand2",
            command=lambda: None if self.auto_fill_checkbox.get() else self.subtract_row())
        self.subtract_row_button.grid(row=0, column=3, padx=5, pady=5)
        buttons_row.append(self.subtract_row_button)

        self.save_button = ctk.CTkButton(
            self.table_frame,
            text=self.save_text,
            cursor="hand2")
        self.save_button.grid(row=0, column=4, padx=5, pady=5)
        buttons_row.append(self.save_button)

        self.close_button = ctk.CTkButton(
            self.table_frame,
            text=self.close_text,
            cursor="hand2",
            command=lambda: self.destroy())
        self.close_button.grid(row=0, column=5, padx=5, pady=5)
        buttons_row.append(self.close_button)

        self.table.append(buttons_row)

        line_row = []
        for col in range(self.max_columns):
            separator = ctk.CTkLabel(self.table_frame, text="_"*25)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0,sticky="n")
            line_row.append(separator)
        
        self.table.append(line_row)

    def clear_table(self):
        '''Clear the table.'''
        while len(self.table) > self.fixed_rows:
            row = self.table.pop()
            for entry in row:
                entry.destroy()
        self.row_count_label.configure(
        text = self.number_of_flashes())

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
        return f"{self.number_of_flashes_text}\n {int(len(self.table)/3)}"
    

    def add_row(self):
        '''Add a pair of rows to the table.'''
        row1 = []
        
        flash_label = ctk.CTkLabel(
            self.table_frame, text=f"Flash {int(len(self.table)/3)+1}:")
        flash_label.grid(
            row=len(self.table) + 1, column=0, padx=0, pady=5)
        row1.append(flash_label)

        temp_label = ctk.CTkLabel(
            self.table_frame, text=self.temperature_text)
        temp_label.grid(
            row=len(self.table) + 1, column=1, padx=0, pady=5)
        row1.append(temp_label)


        pressure_label = ctk.CTkLabel(
            self.table_frame, text=self.pressure_text)
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
        for col in range(self.max_columns):
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
        def float_to_intx100(value):
            '''Convert a value to an integer multiplied by 100.'''
            return int(float(value)*100)
        def intx100_to_float(value):
            '''Convert an integer multiplied by 100 to a float.'''
            return float(value)/100
        def auto_fill_values():
            '''Fill the table with values.'''
            # Check if input values are correct:
            check_values()
            # Clear the table below the separator row
            while len(self.table) > self.fixed_rows + 5:
                row = self.table.pop()
                for entry in row:
                    entry.destroy()
            auto_list = []
            print(auto_list)
            # Add the auto-filled values into rows
            for index,label in enumerate(labels):
                print(f"index={index}, label={label}")
                if index == 0:
                    continue
                auto_list.append([])
                auto_values=label

                # If the increment value is not zero, 
                # fill the list with the values
                if int(float(increment_value_row[index].get())*100) != 0:
                    for value in range(
                        float_to_intx100(starting_value_row[index].get()),
                        float_to_intx100(final_value_row[index].get())+1,
                        float_to_intx100(increment_value_row[index].get())):
                        auto_list[index-1].append(float(value)/100)

                else:
                    auto_list[index-1] = [float(starting_value_row[index].get())]

                print(auto_list)
                for value in list(auto_list[index-1]):
                    auto_values += f" {value};"

                row = []
                label = ctk.CTkLabel(self.table_frame, text=auto_values)
                label.grid(
                    row=len(self.table) + 1,
                    column=0,
                    padx=5,
                    pady=5,
                    columnspan=self.max_columns,
                    sticky="w")
                row.append(label)
                self.table.append(row)
            return  None
        def check_values():
            '''Check the values in the table.'''
            for index,label in enumerate(labels):
                print(f"index={index}, label={label}")
                if index == 0:
                    continue
                # Check if the values are numbers:
                try:
                    float(starting_value_row[index].get())
                except ValueError:
                    print(f"{starting_value_row[index].get()} is not a number!")
                    starting_value_row[index].delete(0, tk.END)
                    starting_value_row[index].insert(
                        0, intx100_to_float(from_values[index-1]))
                try:
                    float(final_value_row[index].get())
                except ValueError:
                    print(f"{final_value_row[index].get()} is not a number!")
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, intx100_to_float(from_values[index-1]))
                try:
                    float(increment_value_row[index].get())
                except ValueError:
                    print(f"{increment_value_row[index].get()} is not a number!")
                    increment_value_row[index].delete(0, tk.END)
                    increment_value_row[index].insert(
                        0, intx100_to_float(0))

                # Check if the values are within the limits:
                if float_to_intx100(starting_value_row[index].get()) < from_values[index-1] or float_to_intx100(starting_value_row[index].get()) > to_values[index-1]:
                    print(f"{starting_value_row[index].get()} is out of range!")
                    starting_value_row[index].delete(0, tk.END)
                    starting_value_row[index].insert(
                        0, intx100_to_float(from_values[index-1]))
                if float_to_intx100(final_value_row[index].get()) > to_values[index-1] or float_to_intx100(final_value_row[index].get()) < from_values[index-1]:
                    print(f"{final_value_row[index].get()} is out of range!")
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, intx100_to_float(to_values[index-1]))
                
                #if float(increment_value_row[index].get()) > to_values[index-1]:
                    #increment_value_row[index].delete(0, tk.END)
                    #increment_value_row[index].insert(0, increment_values[index-1])

                if float_to_intx100(increment_value_row[index].get()) < 0:
                    print(f"{increment_value_row[index].get()} is negative!")
                    increment_value_row[index].delete(0, tk.END)
                    increment_value_row[index].insert(
                        0, intx100_to_float(0))
                  
                if float_to_intx100(increment_value_row[index].get()) < increment_values[index-1]:
                    print(f"{increment_value_row[index].get()} is less than {intx100_to_float(increment_values[index-1])}!")
                    increment_value_row[index].delete(0, tk.END)
                    increment_value_row[index].insert(0, intx100_to_float(increment_values[index-1]))

                # Check if the final value is greater than the starting value:
                if float_to_intx100(final_value_row[index].get()) < float_to_intx100(starting_value_row[index].get()):
                    print(f"{final_value_row[index].get()} is less than {starting_value_row[index].get()}!")
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, starting_value_row[index].get())
                # Check if the increment value is greater than the difference between the final and starting values:
                if float_to_intx100(increment_value_row[index].get()) > (float_to_intx100(final_value_row[index].get()) - float_to_intx100(starting_value_row[index].get())):
                    print(f"{increment_value_row[index].get()} is greater than {final_value_row[index].get()} - {starting_value_row[index].get()}!")
                    increment_value_row[index].delete(0, tk.END)
                    increment_value_row[index].insert(0, intx100_to_float(float_to_intx100(final_value_row[index].get()) - float_to_intx100(starting_value_row[index].get())))

            return None
        



        # Remove all rows below the fixed ones
        self.clear_table()

        from_values = [self.temp_min, self.pressure_min]
        for i in range(self.number_of_components):
            from_values.append(self.z_min)

        to_values = [self.temp_max, self.pressure_max]
        for i in range(self.number_of_components):
            to_values.append(self.z_max)

        increment_values = [self.temp_increment, self.pressure_increment]
        for i in range(self.number_of_components):
            increment_values.append(self.z_increment)

        # Add a row with a button to auto-fill the table
        auto_fill_row = []
        auto_fill_button = ctk.CTkButton(   
            self.table_frame,
            text=self.save_text,
            cursor="hand2",
            command= lambda: auto_fill_values())
        auto_fill_button.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        auto_fill_row.append(auto_fill_button)
        self.table.append(auto_fill_row)

        # Add the label row:
        label_row = []

        labels = ["Settings", self.temperature_text, self.pressure_text]
        for i in range(self.number_of_components):
            labels.append(f"z{i+1}")
        for label in labels:
            label_label = ctk.CTkLabel(self.table_frame, text=label)
            label_label.grid(row=len(self.table) + 1, column=labels.index(label), padx=5, pady=5)
            label_row.append(label_label)

        self.table.append(label_row)

        # Add the row with starting values
        starting_value_row = []

        starting_label = ctk.CTkLabel(self.table_frame, text=self.starting_value_text)
        starting_label.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        starting_value_row.append(starting_label)
        
        for i, from_value in enumerate(from_values):
            initial_box = tk.Spinbox(
                self.table_frame,
                from_=intx100_to_float(from_value),
                to=intx100_to_float(to_values[i]),
                increment=intx100_to_float(increment_values[i]),
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
        
        final_label = ctk.CTkLabel(self.table_frame, text=self.final_value_text)
        final_label.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        final_value_row.append(final_label)
        
        for i, to_value in enumerate(to_values):
            final_box = tk.Spinbox(
                self.table_frame,
                from_=intx100_to_float(from_values[i]),
                to=intx100_to_float(to_value),
                increment=intx100_to_float(increment_values[i]),
                width=5)
 
            final_box.grid(
                row=len(self.table) + 1,
                column= i + 1,
                padx=5,
                pady=5)
            final_value_row.append(final_box)


        self.table.append(final_value_row)

        # Add the row with increment values
        increment_value_row = []
        increment_label = ctk.CTkLabel(self.table_frame, text=self.increment_text)
        increment_label.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        increment_value_row.append(increment_label)

        for i, increment_value in enumerate(increment_values):
            increment_box = tk.Spinbox(
                self.table_frame,
                from_=0,
                to=intx100_to_float(to_values[i]),
                increment=intx100_to_float(increment_value),
                width=5)
            increment_box.grid(
                row=len(self.table) + 1,
                column= i + 1,
                padx=5,
                pady=5)
            increment_value_row.append(increment_box)
        
        self.table.append(increment_value_row)

        # Add a separator row
        separator_row = []
        for col in range(self.max_columns):
            separator = ctk.CTkLabel(self.table_frame, text="·"*37)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0,)
            separator_row.append(separator)

        self.table.append(separator_row)

        # Fill the table with values
        auto_fill_values()

        

        
        
        