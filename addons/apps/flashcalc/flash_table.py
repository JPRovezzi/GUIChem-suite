'''This module contains the FlashTableWindow class for the FlashCalc app.
This class creates a window with a table to input the temperature,pressure and
z values for each flash. It can be filled manually by adding or subtracting
rows, or automatically by setting the starting, final and step values for
the temperature, pressure and z values.'''

# Import the required libraries:
# tkinter is Python's standard GUI (Graphical User Interface) package.
import tkinter as tk
# os is a module that provides a portable way of using operating system
# dependent functionality.
import os

# Import the required third-party libraries:
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# CTkXYFrame is a custom frame with XY scrollbars for Python.
from modules.ctk_xyframe import CTkXYFrame

# widget_classes is a module that provides classes for GUI widgets.
#import modules.widget_classes as widget_classes
#from . import frame_classes

if os.name == 'nt':
    import pywinstyles

class FlashTableWindow(ctk.CTkToplevel):
    '''Class to create the composition table window.'''
    # Class variables:
    table = []
    parameter_table = None
    groups = []
    nc = 3 # Number of components
    nf = 0 # Number of flashes
    flash_list = [] # List of flashes with T,P, and z values
    auto_list = [] # List of autofilled values
    z_values = [] # List of z values that sum to 1
    show_TPZ = True # Show the temperature, pressure and z values in the table
    show_ZMatrix = False # Show the z matrix in the table

    #Constants for the table
    # The values are intergers
    t_min = 27300 # 273 K
    t_max = 47300 # 473 K
    t_step = 100 # 1 K
    p_min = 100 # 1 bar
    p_max = 1000 # 1000 bar
    p_step = 10 # 0.1 bar
    z_min = 0 # 0
    z_max = 100 # 1
    z_step = 5 # 0.05

    fixed_rows = 2 # Minimum number of rows in the table
    max_columns = nc+3 if ((nc+3)>8) else 8 # Max. n of columns in table

    #Text for the table
    add_flash_text = "Add\nFlash"
    auto_fill_text = "Auto Fill"
    close_text = "Close"
    final_value_text = "Final Value"
    flash_text = "Flash"
    number_of_flashes_text = "Number of flashes:"
    pressure_text = "Pressure (bar):"
    save_text = "Save"
    setting_text = "Settings"
    starting_value_text = "Starting Value"
    step_text = "Step"
    subtract_flash_text = "Subtract\nFlash"
    temperature_text = "Temperature (K):"
    title_text = "Flash Config Table"
    update_text = "Update"


    def __init__(self, master,partable=None, **kwargs):
        '''Initialize the class.'''
        super().__init__(master, **kwargs)
        self.title(self.title_text)
        self.geometry("600x400")
        self.parameter_table = partable

        self.table = []
        self.table_frame = CTkXYFrame(self)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.load()

    def add_row(self):
        '''Add a pair of rows to the table if autofill is disabled.'''
        # First row with labels
        row1 = []

        # Flash label
        flash_label = ctk.CTkLabel(
            self.table_frame, text=f"Flash {self.nf+1}:")
        
        flash_label.grid(
            row=len(self.table) + 1, column=0, padx=0, pady=5)
        row1.append(flash_label)

        # Temperature label
        t_label = ctk.CTkLabel(
            self.table_frame, text=self.temperature_text)
        t_label.grid(
            row=len(self.table) + 1, column=1, padx=0, pady=5)
        row1.append(t_label)

        # Pressure label
        pressure_label = ctk.CTkLabel(
            self.table_frame, text=self.pressure_text)
        pressure_label.grid(
            row=len(self.table) + 1, column=2, padx=0, pady=5)
        row1.append(pressure_label)

        # Z labels
        z_colmin = 3 # The first column with z values after the temperature
        # and pressure columns
        z_colmax = z_colmin + self.nc
        for col in range(z_colmin,z_colmax):
            comp_label = ctk.CTkLabel(self.table_frame, text=f"z{col-z_colmin+1}", width=10)
            comp_label.grid(row=len(self.table) + 1, column=col, padx=5, pady=5)
            row1.append(comp_label)

        self.table.append(row1)

        # Second row with spinboxes
        row2 = []

        # temperature spinbox
        t_spinbox = tk.Spinbox(self.table_frame,
                              from_= self.intx100_to_float(self.t_min),
                              to = self.intx100_to_float(self.t_max),
                              increment = self.intx100_to_float(
                                  self.t_step),
                              width = 5)

        # If the table has more than 3 rows,
        # copy the value from the previous row
        if len(self.table) > (self.fixed_rows + 3) :
            prev_box = self.table[-3][0]
            t_spinbox.delete(0,tk.END)
            t_spinbox.insert(0,prev_box.get())

        t_spinbox.grid(row = len(self.table) + 1,
                      column = 1,
                      padx = 5,
                      pady = 5)
        row2.append(t_spinbox)

        # pressure spinbox
        pressure_box = tk.Spinbox(self.table_frame,
                              from_= self.intx100_to_float(self.p_min),
                              to = self.intx100_to_float(self.p_max),
                              increment = self.intx100_to_float(
                                  self.p_step),
                              width = 5)
        # If the table has more than 3 rows,
        # copy the value from the previous row
        if len(self.table) > (self.fixed_rows + 3) :
            prev_box = self.table[-3][1]
            pressure_box.delete(0,tk.END)
            pressure_box.insert(0,prev_box.get())

        pressure_box.grid(row = len(self.table) + 1,
                      column = 2,
                      padx = 5,
                      pady = 5)
        row2.append(pressure_box)

        # z spinboxes
        for col in range(z_colmin,z_colmax):
            z_box = tk.Spinbox(self.table_frame,
                                    from_=self.intx100_to_float(self.z_min),
                                    to=self.intx100_to_float(self.z_max),
                                    increment=self.intx100_to_float(
                                        self.z_step),
                                    width=5)
            # If the table has more than 3 rows,
            # copy the value from the previous row
            if len(self.table) > (self.fixed_rows + 3) :
                prev_box = self.table[-3][col-1]
                z_box.delete(0,tk.END)
                z_box.insert(0,prev_box.get())
            z_box.grid(row=len(self.table) + 1, column=col, padx=5, pady=5)
            row2.append(z_box)

        self.table.append(row2)

        # update the number of flashes
        self.nf_label.configure(
            text=self.set_nf())

        # Add a separator row
        separator_row1 = []
        for col in range(self.max_columns):
            separator = ctk.CTkLabel(self.table_frame, text="·"*37)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0,)
            separator_row1.append(separator)

        self.table.append(separator_row1)

    def auto_fill(self):
        '''Fill the table with values.'''
        # Define the functions used in the method:

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
                        0, self.intx100_to_float(from_values[index-1]))
                try:
                    float(final_value_row[index].get())
                except ValueError:
                    print(f"{final_value_row[index].get()} is not a number!")
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, self.intx100_to_float(from_values[index-1]))
                try:
                    float(step_value_row[index].get())
                except ValueError:
                    print(f"{step_value_row[index].get()} is not a number!")
                    step_value_row[index].delete(0, tk.END)
                    step_value_row[index].insert(
                        0, self.intx100_to_float(0))

                # Check if the values are within the limits:
                if ((self.float_to_intx100(starting_value_row[index].get()) <
                    from_values[index-1]) or
                    (self.float_to_intx100(starting_value_row[index].get()) >
                    to_values[index-1])):
                    print(f"{starting_value_row[index].get()} is out of range!")
                    starting_value_row[index].delete(0, tk.END)
                    starting_value_row[index].insert(
                        0, self.intx100_to_float(from_values[index-1]))

                if ((self.float_to_intx100(
                    final_value_row[index].get()) > to_values[index-1]) or
                    (self.float_to_intx100(final_value_row[index].get()) <
                    from_values[index-1])):
                    print(f"{final_value_row[index].get()} is out of range!")
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, self.intx100_to_float(to_values[index-1]))

                if self.float_to_intx100(step_value_row[index].get()) < 0:
                    print(f"{step_value_row[index].get()} is negative!")
                    step_value_row[index].delete(0, tk.END)
                    step_value_row[index].insert(
                        0, self.intx100_to_float(0))

                if self.float_to_intx100(step_value_row[index].get()) < step_values[index-1]:
                    print(f'''{step_value_row[index].get()} is less than
                     {self.intx100_to_float(step_values[index-1])}!''')
                    step_value_row[index].delete(
                        0, tk.END)
                    step_value_row[index].insert(
                        0, self.intx100_to_float(step_values[index-1]))

                # Check if the final value is greater than the starting value:
                if (self.float_to_intx100(final_value_row[index].get()) <
                    self.float_to_intx100(starting_value_row[index].get())):
                    print(f'''{final_value_row[index].get()} is less than
                     {starting_value_row[index].get()}!''')
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, starting_value_row[index].get())
                # Check if the step value is greater than the difference
                # between the final and starting values:
                if (self.float_to_intx100(step_value_row[index].get()) >
                    (self.float_to_intx100(final_value_row[index].get()) -
                    self.float_to_intx100(starting_value_row[index].get()))):
                    print(f'''{step_value_row[index].get()} is greater
                          than {final_value_row[index].get()} - 
                          {starting_value_row[index].get()}!''')
                    step_value_row[index].delete(
                        0, tk.END)
                    step_value_row[index].insert(
                        0, (self.intx100_to_float(
                            self.float_to_intx100(
                                final_value_row[index].get()) -
                            self.float_to_intx100(
                                starting_value_row[index].get()))))
            return None

        def generate_combinations(
                input_list, n, condition, current_level=0,current_combination=None, values=None):
            '''Generate all possible combinations of values from a list
            following a certain condition.'''
            if current_combination is None:
                current_combination = []
            if values is None:
                values = []
            # Base case: If we've reached the desired level of nesting
            if current_level == n:
                match condition[0]:
                    case ">":
                        if sum(current_combination) > int(condition[1]):
                            values.append(current_combination[:])
                    case "<":
                        if sum(current_combination) < int(condition[1]):
                            values.append(current_combination[:])
                    case ">=":
                        if sum(current_combination) >= int(condition[1]):
                            values.append(current_combination[:])
                    case "<=":
                        if sum(current_combination) <= int(condition[1]):
                            values.append(current_combination[:])
                    case "==":
                        if sum(current_combination) == int(condition[1]):
                            values.append(current_combination[:])
                    case "!=":
                        if sum(current_combination) != int(condition[1]):
                            values.append(current_combination[:])
                    case _:
                        values.append(current_combination[:])

                return values

            # Iterate over the elements of input_list at the current level
            for item in input_list[current_level]:
                current_combination.append(item)
                generate_combinations(
                    input_list, n, condition, current_level + 1,
                    current_combination, values)
                current_combination.pop()  # Backtrack to explore other combinations

            return values

        def update_table():
            '''Fill the table with values.'''
            # Check if input values are correct:
            check_values()
            self.clear_table(leave_rows=6)
            self.auto_list = []
            print(self.auto_list)
            # Add the auto-filled values into rows
            for index,label in enumerate(labels):
                print(f"index={index}, label={label}")
                if index == 0:
                    continue
                self.auto_list.append([])
                auto_values=label

                # If the step value is not zero,
                # fill the list with the values
                if int(float(step_value_row[index].get())*100) != 0:
                    for value in range(
                        self.float_to_intx100(
                            starting_value_row[index].get()),
                        self.float_to_intx100(
                            final_value_row[index].get())+1,
                        self.float_to_intx100(
                            step_value_row[index].get())):
                        self.auto_list[index-1].append(float(value)/100)

                else:
                    self.auto_list[index-1] = [float(starting_value_row[index].get())]

                if self.show_TPZ:
                    print(self.auto_list)
                    print_flag = False
                    print(len(self.auto_list[index-1])-3)
                    for i,value in enumerate(list(self.auto_list[index-1])):
                        #show only the first 3 and last 3 values
                        if (i < 3) or (
                            (i - len(self.auto_list[index-1])+4) > 0):
                            print_flag = True
                            auto_values += f" {value};"
                        elif print_flag:
                            print_flag = False
                            auto_values += f" ...;"
                        
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

            # Add a matrix with the z values that sum to 1
            self.z_values = generate_combinations(
                input_list = self.auto_list[2:],
                n = self.nc,
                condition = ("==",1))

            #print(z_values)
            if self.show_ZMatrix:
                # Add the z values to the table
                for index,z_value in enumerate(self.z_values):
                    row = []
                    z_values_text = ""
                    for value in z_value:
                        z_values_text += f"{value:.2f}; "
                    label = ctk.CTkLabel(self.table_frame, text=z_values_text)
                    label.grid(
                    row=len(self.table) + 1, column=0, padx=5, pady=5,
                    columnspan=self.max_columns, sticky="w")
                    row.append(label)
                    self.table.append(row)

            self.nf = (len(self.z_values)*
                       len(self.auto_list[0])*
                       len(self.auto_list[1]))
            # Set the number of flashes text
            self.nf_label.configure(
            text = self.set_nf(self.nf))
            return None

        # ---------------------------------------------------------------------

        # Remove all rows below the fixed ones
        self.clear_table()

        from_values = [self.t_min, self.p_min]
        for i in range(self.nc):
            from_values.append(self.z_min)

        to_values = [self.t_max, self.p_max]
        for i in range(self.nc):
            to_values.append(self.z_max)

        step_values = [self.t_step, self.p_step]
        for i in range(self.nc):
            step_values.append(self.z_step)

        # Add the label row:
        label_row = []

        labels = ["Settings", self.temperature_text, self.pressure_text]
        for i in range(self.nc):
            labels.append(f"z{i+1}:")
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
                from_ = self.intx100_to_float(from_value),
                to = self.intx100_to_float(to_values[i]),
                increment = self.intx100_to_float(step_values[i]),
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
                from_ = self.intx100_to_float(from_values[i]),
                to = self.intx100_to_float(to_value),
                increment = self.intx100_to_float(step_values[i]),
                width=5)

            final_box.grid(
                row=len(self.table) + 1,
                column= i + 1,
                padx=5,
                pady=5)
            final_value_row.append(final_box)

        self.table.append(final_value_row)

        # Add the row with step values
        step_value_row = []
        step_label = ctk.CTkLabel(self.table_frame, text=self.step_text)
        step_label.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        step_value_row.append(step_label)

        for i, step_value in enumerate(step_values):
            step_box = tk.Spinbox(
                self.table_frame,
                from_= 0,
                to = self.intx100_to_float(to_values[i]),
                increment = self.intx100_to_float(step_value),
                width=5)
            step_box.grid(
                row=len(self.table) + 1,
                column= i + 1,
                padx=5,
                pady=5)
            step_value_row.append(step_box)

        self.table.append(step_value_row)

        # Add a row with a button to auto-fill the table
        auto_fill_row = []
        update_button = ctk.CTkButton(
            self.table_frame,
            text=self.update_text,
            cursor="hand2",
            command= lambda: update_table())
        update_button.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        auto_fill_row.append(update_button)
        self.table.append(auto_fill_row)

        # Add a separator row
        separator_row2 = []
        for col in range(self.max_columns):
            separator = ctk.CTkLabel(self.table_frame, text="·"*37)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0)
            separator_row2.append(separator)

        self.table.append(separator_row2)

        # Fill the table with values
        update_table()
        return None

    def clear_table(self,leave_rows=0):
        '''Clear the table.'''
        if self.auto_fill_checkbox.get():
            while len(self.table) > self.fixed_rows + leave_rows:
                row = self.table.pop()
                for entry in row:
                    entry.destroy()
            self.nf_label.configure(text = self.set_nf())   
        else:
            while len(self.table) > self.fixed_rows + 0:
                row = self.table.pop()
                for entry in row:
                    entry.destroy()
            self.nf_label.configure(text = self.set_nf())

    def float_to_intx100(self, value : float) -> int:
        '''Convert a value to an integer multiplied by 100.'''
        return int(float(value)*100)

    def intx100_to_float(self, value: int) -> float:
        '''Convert an integer multiplied by 100 to a float.'''
        return float(value)/100

    def load(self):
        '''Load the table.'''
        # First row of the table:
        # Number of flashes,
        # autofill, add and subtract buttons, save button and close button
        buttons_row = []

        # Number of flashes label:
        self.nf_label = ctk.CTkLabel(
            self.table_frame,
            text=self.set_nf())
        self.nf_label.grid(row=0, column=0, padx=5, pady=5)
        buttons_row.append(self.nf_label)

        # Autofill checkbox:
        self.auto_fill_checkbox = ctk.CTkCheckBox(
            self.table_frame,
            text=self.auto_fill_text,
            variable=tk.BooleanVar(),
            command=lambda: (
                print("Autofill: ",self.auto_fill_checkbox.get()),
                self.toggle_buttons(),
                self.clear_table(),
                self.auto_fill() if self.auto_fill_checkbox.get()
                else None
            ))
        self.auto_fill_checkbox.grid(row=0, column=1, padx=5, pady=5)
        buttons_row.append(self.auto_fill_checkbox)

        # Add and subtract buttons:
        self.add_row_button = ctk.CTkButton(
            self.table_frame,
            text=self.add_flash_text,
            cursor="hand2",
            command=lambda: self.add_row())
        self.add_row_button.grid(row=0, column=2, padx=5, pady=5)
        buttons_row.append(self.add_row_button)

        self.subtract_row_button = ctk.CTkButton(
            self.table_frame,
            text=self.subtract_flash_text,
            cursor="hand2",
            command=lambda: self.subtract_row())
        self.subtract_row_button.grid(row=0, column=3, padx=5, pady=5)
        buttons_row.append(self.subtract_row_button)

        # Save and close buttons:
        self.save_button = ctk.CTkButton(
            self.table_frame,
            text=self.save_text,
            cursor="hand2",
            command=lambda: self.save_table())
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

        # Second row of the table:
        line_row = []

        # Separation line
        for col in range(self.max_columns):
            separator = ctk.CTkLabel(self.table_frame, text="_"*25)
            separator.grid(
                row=len(self.table) + 1, column=col, padx=0, pady=0,
                ipadx=0, ipady=0,sticky="n")
            line_row.append(separator)
        self.table.append(line_row)

    def load_table(self,table):
        '''Load a table from a file.'''
        self.table = table
        for row in table:
            for entry in row:
                entry.grid()
        self.nf_label.configure(
            text=self.set_nf())

    def save_table(self):
        '''Save the table to be used in the FlashCalc app.'''
        self.update_flash_list()
        return
    
    def set_nf(self, flash_number=None):
        '''Return the number of flashes in the table.'''
        if flash_number is None:
            self.nf = int(len(self.table)/3)
        else:
            self.nf = flash_number
        return f"{self.number_of_flashes_text}\n {self.nf}"

    def subtract_row(self):
        '''Subtract rows from the table.'''
        rows_to_substract = 3 # Number of rows to subtract

        if self.table:
            for _ in range(rows_to_substract):
                if len(self.table) > self.fixed_rows:
                    row = self.table.pop()
                    for entry in row:
                        entry.destroy()
        self.nf_label.configure(
            text = self.set_nf())

    def toggle_buttons(self):
        '''Toggle the add and subtract buttons.'''
        if self.auto_fill_checkbox.get():
            self.add_row_button.configure(state="disabled")
            self.subtract_row_button.configure(state="disabled")
        else:
            self.add_row_button.configure(state="normal")
            self.subtract_row_button.configure(state="normal")
        return None
    
    def update_flash_list(self):
        '''Update the list of flashes.'''
        self.flash_list = []
        if self.auto_fill_checkbox.get():
                tp_values = self.auto_list[:2]
                flash_queue = 0
                for t in tp_values[0]:
                    for p in tp_values[1]:
                        for z in self.z_values:
                            self.flash_list.append([t,p]+z)
                print("Flash list:")
        else:
            flash_queue = 0
            for index,row in enumerate(self.table):
                if (index) == (flash_queue + 1) * 3:
                    self.flash_list.append([])
                    for entry in row:
                        self.flash_list[flash_queue].append(float(entry.get()))
                    flash_queue += 1
        for i,flash in enumerate(self.flash_list):
                    print(i+1,": ",flash)
        return None
        