'''This module contains the FlashTableWindow class for the FlashCalc app.
This class creates a window with a table to input the temperature,pressure and
z values for each flash. It can be filled manually by adding or subtracting
rows, or automatically by setting the starting, final and increment values for
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
    nc = 5 # Number of components
    nf = 0 # Number of flashes
    flash_list = [] # List with T, P and z values for each flash
    show_TPZ = True # Show the temperature, pressure and z values in the table
    show_ZMatrix = False # Show the z matrix in the table

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

        self.load()

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
                self.toggle_buttons(),
                self.auto_fill() if self.auto_fill_checkbox.get()
                else self.clear_table())
            )
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

    def toggle_buttons(self):
        '''Toggle the add and subtract buttons.'''
        if self.auto_fill_checkbox.get():
            self.add_row_button.configure(state="disabled")
            self.subtract_row_button.configure(state="disabled")
        else:
            self.add_row_button.configure(state="normal")
            self.subtract_row_button.configure(state="normal")

    def clear_table(self):
        '''Clear the table.'''
        while len(self.table) > self.fixed_rows:
            row = self.table.pop()
            for entry in row:
                entry.destroy()
        self.nf_label.configure(
        text = self.set_nf())

    def load_table(self,table):
        '''Load a table from a file.'''
        self.table = table
        for row in table:
            for entry in row:
                entry.grid()
        self.nf_label.configure(
            text=self.set_nf())

    def set_nf(self, flash_number=None):
        '''Return the number of flashes in the table.'''
        if flash_number is None:
            self.nf = int(len(self.table)/3)
        else:
            self.nf = flash_number
        return f"{self.number_of_flashes_text}\n {self.nf}"

    def add_row(self):
        '''Add a pair of rows to the table if autofill is disabled.'''
        # First row with labels
        row1 = []

        # Flash label
        flash_label = ctk.CTkLabel(
            self.table_frame, text=f"Flash {int(len(self.table)/3)+1}:")
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
                              from_= self.temp_min,
                              to = self.temp_max,
                              increment = self.temp_increment,
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
                              from_= self.pressure_min,
                              to = self.pressure_max,
                              increment = self.pressure_increment,
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
                                    from_=self.z_min,
                                    to=self.z_max,
                                    increment=self.z_increment,
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
            for _ in range(rows_to_substract):
                if len(self.table) > self.fixed_rows:
                    row = self.table.pop()
                    for entry in row:
                        entry.destroy()
        self.nf_label.configure(
            text = self.set_nf())

    def auto_fill(self):
        '''Fill the table with values.'''
        # Define the functions used in the method:
        def float_to_intx100(value : float) -> int:
            '''Convert a value to an integer multiplied by 100.'''
            return int(float(value)*100)

        def intx100_to_float(value: int) -> float:
            '''Convert an integer multiplied by 100 to a float.'''
            return float(value)/100

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
                if self.show_TPZ:
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
            z_values = generate_combinations(
                input_list = auto_list[2:],
                n = self.nc,
                condition = ("==",1))

            print(z_values)
            # Add the z values to the table
            for index,z_value in enumerate(z_values):
                row = []
                z_values_text = ""
                for value in z_value:
                    z_values_text += f"{value:.2f}; "
                label = ctk.CTkLabel(self.table_frame, text=z_values_text)
                if self.show_ZMatrix:
                    label.grid(
                        row=len(self.table) + 1,
                        column=0,
                        padx=5,
                        pady=5,
                        columnspan=self.max_columns,
                        sticky="w")
                row.append(label)
                self.table.append(row)

            self.nf = len(z_values)*len(auto_list[0])*len(auto_list[1])
            # Set the number of flashes text
            self.nf_label.configure(
            text = self.set_nf(self.nf))

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
                if float_to_intx100(
                    ((starting_value_row[index].get()) < from_values[index-1])
                    or (float_to_intx100(starting_value_row[index].get()) >
                    to_values[index-1])):
                    print(f"{starting_value_row[index].get()} is out of range!")
                    starting_value_row[index].delete(0, tk.END)
                    starting_value_row[index].insert(
                        0, intx100_to_float(from_values[index-1]))

                if float_to_intx100(
                    (final_value_row[index].get() > to_values[index-1]) or
                    (float_to_intx100(final_value_row[index].get()) <
                    from_values[index-1])):
                    print(f"{final_value_row[index].get()} is out of range!")
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, intx100_to_float(to_values[index-1]))

                if float_to_intx100(increment_value_row[index].get()) < 0:
                    print(f"{increment_value_row[index].get()} is negative!")
                    increment_value_row[index].delete(0, tk.END)
                    increment_value_row[index].insert(
                        0, intx100_to_float(0))

                if float_to_intx100(increment_value_row[index].get()) < increment_values[index-1]:
                    print(f'''{increment_value_row[index].get()} is less than
                     {intx100_to_float(increment_values[index-1])}!''')
                    increment_value_row[index].delete(
                        0, tk.END)
                    increment_value_row[index].insert(
                        0, intx100_to_float(increment_values[index-1]))

                # Check if the final value is greater than the starting value:
                if (float_to_intx100(final_value_row[index].get()) <
                    float_to_intx100(starting_value_row[index].get())):
                    print(f'''{final_value_row[index].get()} is less than
                     {starting_value_row[index].get()}!''')
                    final_value_row[index].delete(0, tk.END)
                    final_value_row[index].insert(
                        0, starting_value_row[index].get())
                # Check if the increment value is greater than the difference
                # between the final and starting values:
                if (float_to_intx100(increment_value_row[index].get()) >
                    (float_to_intx100(final_value_row[index].get()) -
                    float_to_intx100(starting_value_row[index].get()))):
                    print(f'''{increment_value_row[index].get()} is greater
                          than {final_value_row[index].get()} - 
                          {starting_value_row[index].get()}!''')
                    increment_value_row[index].delete(
                        0, tk.END)
                    increment_value_row[index].insert(
                        0, (intx100_to_float(
                            float_to_intx100(final_value_row[index].get()) -
                            float_to_intx100(starting_value_row[index].get
                                             ()))))
            return None
        # ---------------------------------------------------------------------

        # Remove all rows below the fixed ones
        self.clear_table()

        from_values = [self.temp_min, self.pressure_min]
        for i in range(self.nc):
            from_values.append(self.z_min)

        to_values = [self.temp_max, self.pressure_max]
        for i in range(self.nc):
            to_values.append(self.z_max)

        increment_values = [self.temp_increment, self.pressure_increment]
        for i in range(self.nc):
            increment_values.append(self.z_increment)

        # Add a row with a button to auto-fill the table
        auto_fill_row = []
        auto_fill_button = ctk.CTkButton(
            self.table_frame,
            text=self.save_text,
            cursor="hand2",
            command= lambda: update_table())
        auto_fill_button.grid(row=len(self.table) + 1, column=0, padx=5, pady=5)
        auto_fill_row.append(auto_fill_button)
        self.table.append(auto_fill_row)

        # Add the label row:
        label_row = []

        labels = ["Settings", self.temperature_text, self.pressure_text]
        for i in range(self.nc):
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
        update_table()
