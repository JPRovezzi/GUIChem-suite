'''This module contains the classes for the frames of the datachempy addon.'''
# For threading and progress bar info, read this:
#https://stackoverflow.com/questions/33768577/tkinter-gui-with-progress-bar

# Import the standard libraries
# OS module provides functions to interact with the operating system.
import os
# Tkinter is the standard Python interface to the Tk GUI toolkit.
import tkinter as tk
# Threading is a built-in Python module that allows you to run multiple
# threads (tasks, function calls) at once.
import threading
# TheadPoolExecutor is a high-level interface for asynchronously executing callables using threads.
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures._base import CancelledError
# Time is a built-in Python module that provides various time-related functions.
import time
# JSON is a built-in Python module that provides functions to work with 
# JSON data.
import json

# Import the third party libraries:
# NistChemPy is a Python library for accessing the NIST Chemistry WebBook and other NIST databases.
import nistchempy as nist
# Requests is a simple and elegant HTTP library for Python, built for human beings.
import requests
# BeautifulSoup is a library for parsing HTML and XML documents. 
# It creates parse trees from page source codes that can be used to extract data easily.
from bs4 import BeautifulSoup
# Tqdm is a fast, extensible progress bar for Python and CLI. 
# But we are using the tkinter version of tqdm for GUI.
from tqdm.tk import tqdm
# CustomTkinter is a custom GUI library for Python.
import customtkinter as ctk
# CTkXYFrame is a custom frame with XY scrollbars for Python.
from modules.ctk_xyframe import CTkXYFrame
# widget_classes is a module that provides classes for GUI widgets.
import modules.widget_classes as widget_classes

if os.name == 'nt':
    import pywinstyles


#------------------------------------------------------------------------------
class DataChemPyFrame(ctk.CTkFrame):
    '''Class to create the DataChemPy frame. It has the following methods: 
    save, open.'''
    master = None
    tool = None
    error_message = None
    #problem_name = None
    #model = None
    #parameter_table = None
    #comment = None

    def __init__(self, master, tool, **kwargs):
        '''This method initializes an instance of the DataChempyFrame class.'''
        if os.name == 'nt':
            super().__init__(master=master, corner_radius=50, bg_color="#000000")
        else:
            super().__init__(master=master, corner_radius=0, bg_color="#000000")
        self.master = master
        self.tool = tool
        kwargs
    
    def save(self):
        '''Save the data'''
        print("WiP: Save the data")
        # Here goes the code to save the data
        pass
        
    def open(self):
        '''Load the data from a file.'''
        print("WiP: Open the data")
        # Here goes the code to load the data
        pass

class WelcomeFrame(DataChemPyFrame):
    '''Class to create the welcome frame. It has the following methods: 
    load.'''

    master=None
    tool=None

    def __init__(self, master, tool,**kwargs):
        '''Initialize the class.'''

        super().__init__(master, tool,**kwargs)
        self.load(tool)

    def load(self, tool):
        '''Load the welcome frame with its widgets.'''
        def select_database(option):
            '''Select the database to use.'''
            if option == "NIST":
                return "NistFrame"
            pass

        self.tkraise()
        self.pack_propagate(False)
        widget_classes.TitleLabel(self, text="").pack(pady=0)
        widget_classes.TitleLabel(self, text=f"Welcome to {tool}!").pack(pady=0)
        
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, "res", "databases.json")
        with open(json_path, "r") as json_file:
            databases = json.load(json_file)
        database_menu = ctk.CTkOptionMenu(
            self,
            values=databases.get("databases", []))
        database_menu.pack(pady=10)
        
        ctk.CTkButton(
            self,
            text="New search",
            cursor="hand2",
            command=lambda: self.master.load_module(
                self.tool,
                select_database(database_menu.get()),
                location="frame_classes")
            ).pack(pady=10)
        
        ctk.CTkButton(
            self,
            text="Load previous search",
            cursor="hand2",
            command=lambda: self.open()
            ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="CLOSE",
            cursor="hand2",
            command=self.master.close_module
            ).pack(pady=10)

        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")
        self.pack(pady=100, expand=True, fill="y")
        return None

class NistFrame(DataChemPyFrame):
    '''Class to create the NIST frame. It has the following methods: 
    load, save, open.'''
    master=None
    tool=None
    def __init__(self, master, tool,**kwargs):
        '''Initialize the class.'''
        super().__init__(master, tool,**kwargs)
        self.master = master
        self.tool = tool
        self.load(tool)
        self.pack_propagate(False)
        self.pack(pady=0, expand=True)
        if os.name == 'nt':
            pywinstyles.set_opacity(self, color="#000000")  
    def load(self, tool):
        '''Load the NIST frame with its widgets.'''
        self.tkraise()
        #Create the title and
        widget_classes.TitleLabel(self, text=f"NIST Search").grid(row=0, column=1, padx=10, pady=10)
        
        #Create the input label
        self.input_label = ctk.CTkLabel(self, text="Enter the names of the compounds separated by semicolon (;) or load a JSON file")
        self.input_label.grid(row=1, column=0, columnspan = 3, padx=10, pady=10)
        #Create a checkbox to select the type of search
        self.search_type = ctk.CTkCheckBox(
            self,
            text="Import from JSON",
            command=
            lambda: (
                (self.input_text.delete(0, "end"),
                self.input_text.insert(0, "-"*50),
                self.input_text.configure(state="disabled")
                ) if self.search_type.get() else (
                    self.input_text.configure(state=("normal")),
                    self.input_text.delete(0, "end"),
                    self.input_text.insert(0, "methane; ethane;...")
                )
            )
        )
        self.search_type.grid(row=2, column=0, padx=10, pady=10)
        self.search_type.select()  # Select the checkbox by default

        #Create a input box for the user to enter the name of the compound
        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        self.input_text = widget_classes.TextEntry(
            self.input_frame,
            width=200)
        self.input_text.pack(side="left", padx=10, pady=10)
        self.input_text.insert(0, "-"*50)
        self.input_text.configure(state="disabled")  # Disable the text box to prevent editing

        
        # Create the buttons
        self.search_button = ctk.CTkButton(
            self,
            text="Search",
            cursor="hand2",
            command= lambda: self.search_param_window()
            )
        self.search_button.configure(state="normal")
        self.search_button.grid(row=3, column=0, padx=10, pady=10)

        ctk.CTkButton(
            self,
            text="Save",
            cursor="hand2",
            command=self.save
            ).grid(row=3, column=1, padx=10, pady=10)
        
        ctk.CTkButton(
            self,
            text="Go Back",
            cursor="hand2",
            command=lambda: self.master.load_module(self.tool,"WelcomeFrame",location="frame_classes")
            ).grid(row=3, column=2, padx=10, pady=10)
        
        # Create the text box
        self.text_frame = CTkXYFrame(self, width=500, height=50)
        self.text_frame.grid(row=4, column=0, columnspan=3, padx=10, pady=10)
        self.console = ctk.CTkTextbox(self.text_frame, width=500, height=300)
        self.console.pack(fill="both", expand=True)
        self.console.insert("0.0", "This is the NIST frame. You can search for compounds here.")
        self.console.configure(state="disabled")  # Disable the text box to prevent editing

    # Define the functions:
    def search_id(self,identifier, search_type):
        '''Searches the NIST Chemistry WebBook for the compound with the given identifier.'''
        search = nist.run_search(
            identifier= identifier,
            search_type= search_type)

        if search.success:
            if search.num_compounds == 0:
                print(
                    "\n",
                    f"Error: No results found for '{identifier}'."
                    )
                return None
            identifier_dict = {}
            for compound_id in search.compound_ids:
                identifier_dict[compound_id] = nist.get_compound(compound_id).__dict__
                identifier_dict[compound_id].pop('nist_response') #To avoid an error when saving the data
            return identifier_dict
        else:
            print(
                "\n",
                f"Search for '{identifier}' failed.")
            return None

    def search_param_window(self):
        '''Creates a window to search for the parameters of the compound.'''
        def select_all_parameters():
            '''Selects all the parameters to search for.'''
            for parameter in checkboxes:
                checkboxes[parameter].select()
            select_all.select()
            return None

        def deselect_all_parameters():
            '''Deselects all the parameters to search for.'''
            for parameter in checkboxes:
                checkboxes[parameter].deselect()
            select_all.deselect()
            return None

        def close_window(run =False):
            '''Closes the window.'''
            self.search_button.configure(state="normal")
            param_window.destroy()
            if run:
                self.run_search()
            return None
 
        # Disable the search button in order to avoid multiple clicks
        self.search_button.configure(state="disabled")

        # Create a new window.
        # This window will be used to select the parameters to search for.
        # It will be a top level window, so it will be on top of the main window.        
        param_window = ctk.CTkToplevel(self)
        # Set the title and size of the window
        param_window.title("Search Parameters")
        param_window.geometry("640x480")
        # Set the window to be resizable
        param_window.resizable(True, True)
        # Set the window to be always on top
        param_window.attributes('-topmost', True)
        # Set the focus on the window
        param_window.focus_get()
        # Set the actions when the window is closed
        # This is to avoid the window to be closed and the search button to be left disabled.
        param_window.protocol("WM_DELETE_WINDOW", lambda: [
            param_window.destroy(),
            self.search_button.configure(state="normal"),
            ])
        
        # Create the widgets:

        # Create a label
        label = ctk.CTkLabel(param_window, text="Select the parameters to search for:")
        label.grid(row=0, column=0, columnspan = 3, padx=10, pady=10)

        # Create a checkbox for each parameter

        # Load the parameters from the JSON file
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, "res", "nist.json")

        with open(json_path, "r") as json_file:
            data = json.load(json_file)
            parameters = data.get("search_parameters", [])
        checkboxes = {}

        # Create a frame to hold the checkboxes
        checkbox_frame = CTkXYFrame(param_window, width=640, height=300)
        checkbox_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        number_of_columns = 5
        for index, parameter in enumerate(parameters):
            if index % number_of_columns == 0:
                row = (index // number_of_columns)
                column = 0
            else:
                row = (index // number_of_columns)
                column = index % number_of_columns

            # Create a checkbox for each parameter
            checkboxes[parameter] = ctk.CTkCheckBox(
                checkbox_frame,
                text=parameter)
            checkboxes[parameter].grid(row=row, column=column, padx=10, pady=10)
        
        # Create a checkbox to select all parameters
        select_all = ctk.CTkCheckBox(
            checkbox_frame,
            text="Select All",
            command=lambda: (
                (select_all_parameters() if select_all.get() else deselect_all_parameters())
            ))
        select_all.grid(row=(len(parameters)//number_of_columns)+1, column=0, padx=10, pady=10)
        # Create a button to close the window
        close_button = ctk.CTkButton(
            param_window,
            text="Close",
            command=lambda:close_window()
            )
        close_button.grid(row=2, column=1, padx=10, pady=10)
        
        # Create a button to search for the parameters
        run_button = ctk.CTkButton(
            param_window,
            text="Run",
            command=lambda: close_window(run=True)
            )
        run_button.grid(row=2, column=0, padx=10, pady=10)

    def run_search(self):
        '''Runs the search for the parameters.'''
        if self.search_type.get():
            # Load the JSON file from a file dialog
            json_path = tk.filedialog.askopenfilename(
                title="Select a JSON file",
                filetypes=[("JSON files", "*.json")]
            )
            # Check if the file exists
            if not json_path:
                return None
            # Load the JSON file
            with open(json_path, "r") as json_file:
                data = json.load(json_file)
                # Get the list of keys from the JSON file
                keys = list(data.keys())
                # Get the substance for each category
                substances = []
                for key in keys:
                    # Get the list of substances for each category
                    substances += data[key]
                # Remove the empty strings from the list
                substances = [substance.strip() for substance in substances if substance.strip()]
        else:
            # Get the input from the text box
            input_text = self.input_text.get()
            # Split the input text by semicolon
            substances = input_text.split(";")
            # Remove the empty strings from the list
            substances = [substance.strip() for substance in substances if substance.strip()]
        # Remove the empty strings from the list
        substances = [substance.strip() for substance in substances if substance.strip()]
        print(f"Substances: {substances}")     
        # Run the task in a separate thread
        #threading.Thread(target=lambda: (self.run_task(), self.search_button.configure(state="normal"))).start()




#--------------------------------------------------------------------------

def run_task(self):
    #start_button['state'] = 'disabled'
    #-------------------------------
    # Here goes everything before the main loop
    substances = [
        # Acidos
        "Formic Acid", "Acetic Acid", "Trichloroacetic Acid", "Acrylic Acid", "Caprylic Acid",
        "Capric Acid", "Lauric Acid", "Oleic Acid", "Stearic Acid", "Benzoic Acid", "Nicotinic Acid",
        
        # Alcoholes
        "Methanol", "Ethanol", "1-Propanol", "Isopropanol", "1-Butanol", "Isopentanol", 
        "Phenol", "Cyclohexanol", "Cetyl Alcohol",
        
        # Formiatos
        "Methyl Formate", "Ethyl Formate", "n-Propyl Formate", "Isopropyl Formate", "Butyl Formate",
        "Isopentyl Formate", "Phenyl Formate", "Cyclohexyl Formate", "Cetyl Formate",
        
        # Acetatos
        "Methyl Acetate", "Ethyl Acetate", "n-propyl Acetate", "Isopropyl Acetate", "Butyl Acetate",
        "Isopentyl Acetate", "Phenyl Acetate", "Cyclohexyl Acetate", "Cetyl Acetate",
        
        # Tricloroacetatos
        "Methyl Trichloroacetate", "Ethyl Trichloroacetate", "n-propyl Trichloroacetate",
        "Isopropyl Trichloroacetate", "Butyl Trichloroacetate", "Isopentyl Trichloroacetate", 
        "Phenyl Trichloroacetate", "Cyclohexyl Trichloroacetate", "Cetyl Trichloroacetate",
        
        # Acrilatos
        "Methyl Acrylate", "Ethyl Acrylate", "n-propyl Acrylate", "Isopropyl Acrylate", "Butyl Acrylate",
        "Isopentyl Acrylate", "Phenyl Acrylate", "Cyclohexyl Acrylate", "Cetyl Acrylate",
        
        # Caprilatos
        "Methyl Caprylate", "Ethyl Caprylate", "n-propyl Caprylate", "Isopropyl Caprylate", 
        "Butyl Caprylate", "Isopentyl Caprylate", "Phenyl Caprylate", "Cyclohexyl Caprylate", "Cetyl Caprylate",
        
        # Capratos
        "Methyl Caprate", "Ethyl Caprate", "n-propyl Caprate", "Isopropyl Caprate", 
        "Butyl Caprate", "Isopentyl Caprate", "Phenyl Caprate", "Cyclohexyl Caprate", "Cetyl Caprate",
        
        # Lauratos
        "Methyl Laurate", "Ethyl Laurate", "n-propyl Laurate", "Isopropyl Laurate", 
        "Butyl Laurate", "Isopentyl Laurate", "Phenyl Laurate", "Cyclohexyl Laurate", "Cetyl Laurate",
        
        # Oleatos
        "Methyl Oleate", "Ethyl Oleate", "n-propyl Oleate", "Isopropyl Oleate", "Butyl Oleate",
        "Isopentyl Oleate", "Phenyl Oleate", "Cyclohexyl Oleate", "Cetyl Oleate",
        
        # Estearatos
        "Methyl Stearate", "Ethyl Stearate", "n-propyl Stearate", "Isopropyl Stearate", "Butyl Stearate",
        "Isopentyl Stearate", "Phenyl Stearate", "Cyclohexyl Stearate", "Cetyl Stearate",
        
        # Benzoatos
        "Methyl Benzoate", "Ethyl Benzoate", "n-propyl Benzoate", "Isopropyl Benzoate", "Butyl Benzoate",
        "Isopentyl Benzoate", "Phenyl Benzoate", "Cyclohexyl Benzoate", "Cetyl Benzoate",
        
        # Nicotinatos
        "Methyl Nicotinate", "Ethyl Nicotinate", "n-propyl Nicotinate", "Isopropyl Nicotinate",
        "Butyl Nicotinate", "Isopentyl Nicotinate", "Phenyl Nicotinate", "Cyclohexyl Nicotinate", "Cetyl Nicotinate",

        # Solventes
        "Toluene", "n-heptane"
    ]
    result = {}
    substances_no_data = []
    substances_with_data = []
    substances_pending = []
    search_limit = lambda x: x if len(substances) > x else len(substances)
    search_limit = search_limit(200)
    search_offset = 0
    substances = substances[search_offset:search_limit]

    #substances =["acetic acid"]

    def threaded_task(iterable: []):
        def dummy_task(substance):
            if tpe._shutdown:
                return
            time.sleep(1)


        def inner_task(substance):
            # Check if the thread pool executor is shutdown.
            # If tpe.shutdown(cancel_futures=false) is called below,
            # all the inner tasks will continue to run until it the hole
            # process finishes. So to avoid that every full task is run,
            # we check if the thread pool executor is shutdown to end
            # each pending task.
            # Also, it tracks which substances are pending.
            if tpe._shutdown:
                substances_pending.append(substance)
                return
            identifier = substance
            search_type = 'name'
            # URL of the webpage containing the table
            data = self.search_id(identifier, search_type)
            if data is None:
                substances_no_data.append(substance)
            else:
                substances_with_data.append(substance)
                result[identifier] = data



        try:
            with ThreadPoolExecutor(max_workers=10) as tpe:
                pbar = tqdm(
                    tpe.map(inner_task, iterable),
                    total=len(iterable),
                    grab=True,
                    desc="Main progress bar",
                    tk_parent=self,
                    cancel_callback=lambda: (
                        #tpe.shutdown() is a way to stop the executor. 
                        # If wait is True, 
                        # it will wait for all the tasks to finish.
                        # If cancel_futures is True, 
                        # it will cancel all the tasks that are not finished
                        # but it will raise a CancelledError exception.
                        # So tpe._shudown inside the inner task is a way to check if the executor is shutdown.
                        tpe.shutdown(wait=False,cancel_futures=False),
                        pbar.close(),
                        pbar._tk_window.destroy()
                        )
                    )

                pbar._tk_window.attributes('-topmost', True)  # Keep the main progress bar on top, or it's hard to see
                pbar._tk_window.focus_get()
                list(pbar)
                pbar._tk_window.destroy()
        except CancelledError:
            # Handle the case when the progress bar is cancelled and tpe.shutdown(cancel_futures=True) is called.
            print("Cancelled!")
            #start_button['state'] = 'normal'
            return

    

    # Here comes everything after the main loop
    def on_thread_complete():
        print("Job done")
        # 
        print("-" * 50)
        print(f"Results: {len(result)}")
        for key, value in result.items():
            print(key)
        # Save the result dictionary into a JSON file
        
        with open("result.json", "w") as json_file:
            json.dump(result, json_file, indent=4)
        print("Results saved to result.json")
        
        
        
        # Print the list of substances with data
        print("-" * 50)
        print(f"Substances with data:{len(substances_with_data)}")
        for substance in substances_with_data:
            print(substance)
        # Print the list of substances without data
        print("-" * 50)
        print(f"Substances without data:{len(substances_no_data)}")
        for substance in substances_no_data:
            print(substance)
        # Print the list of substances pending
        print("-" * 50)
        print(f"Substances pending:{len(substances_pending)}")
        for substance in substances_pending:
            print(substance)
        
        #start_button['state'] = 'normal'
    #threading.Thread(target=threaded_task, kwargs={'iterable': substances}).start()
    threading.Thread(target=lambda: (threaded_task(substances), on_thread_complete())).start()
#------------------------------------------------------------------------------

class ChemicalCompound(nist.compound.NistCompound):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cTP = None
        self.cTP_url = None
        self.cTP_data = None

    def set_cTP(self, cTP):
        self.cTP = cTP

    def set_cTP_url(self, url):
        self.cTP_url = url

    def set_cTP_data(self, data):
        self.cTP_data = data

if __name__ == "__main__":
    n_thread = 10

    window = tk.Tk()

    start_button = tk.Button(window, text="Start", command=run_task)
    start_button.pack()

    window.mainloop()









