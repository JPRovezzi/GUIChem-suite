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

    # The following variables are used to store the search results
    # The search result is a dictionary with the following structure:
    search_result = {}
    # The search_refs are the references to search for in the NIST 
    # database.
    search_refs = []


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

    def data_extract(self,url):
        '''Gets the cTP value for the given list of substances.'''
        if not isinstance(url, str):
            print('The url is a non string type: ' + url.__class__.__name__)
            return None
        if len(url) == 0:
            print('The url is empty')
            return None
        # Fetch the webpage
        try:
            response = requests.get(url,timeout = 20)
        except:
            print(f"Error: Unable to connect to {url}.")
            return None
        html_content = response.text
        # Check if the request was successful
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage: {response.status_code}")
            return None
        # Print the URL to verify
        #print(f"URL: {url}")
        # Print the response content (optional)
        # print(response.text)
        # Check if the response contains HTML content
        if 'text/html' not in response.headers.get('Content-Type', ''):
            print("The response does not contain HTML content.")
            return None
        # Print the response content (optional)
        # print(response.text)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Locate the table (adjust based on your needs, e.g., by class or id)
        # If you want to find a specific table, you can use more specific selectors
        # For example, if the table has a class name 'data-table':
        # table = soup.find('table', class_='data-table')
        # To find a table by id:
        # table = soup.find('table', id='my-table-id')
        # to finde more than one table
        # table = soup.find_all('table', class_='data-table')
        # If you want to find a table by id:
        # table = soup.find_all('table', id='my-table-id')
        # If you want to find a table by class:
        # table = soup.find_all('table', class_='data-table')
        # If you want to find a table by attribute:
        # table = soup.find_all('table', attrs={'data-type': 'my-table'})
        tables = soup.find_all('table')  # This finds the first table in the HTML

        

        # Extract table data
        table_data = {}
        
        for index, table in enumerate(tables):  # Iterate through each table found
            # Get the aria-label of the table
            table_name = table.get('aria-label', f"Table {index+1}")
            headers = []
            table_data[table_name] = []
            for row in table.find_all('tr'):  # Iterate through each row
                cells = []
                # Get the header
                if len(headers) == 0:
                    headers = row.find_all('th')
                    table_data[table_name].append(
                        [
                            header.text.strip()
                            for header in headers
                            ])                          
                cells = row.find_all('td')  # Get data cells
                if len(cells) != 0:
                    table_data[table_name].append(
                        [
                            cell.text.strip() for cell in cells
                            ])
        return table_data

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
        self.console = widget_classes.CopyTextBox(self.text_frame, width=500, height=300)
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
            for parameter, checkbox in checkboxes.items():
                if parameters_dict[parameter]["state"] != "disabled":
                    checkbox.select()
            select_all.select()
            return None

        def deselect_all_parameters():
            '''Deselects all the parameters to search for.'''
            for parameter, checkbox in checkboxes.items():
                if parameters_dict[parameter]["state"] != "disabled":
                    checkbox.deselect()
            select_all.deselect()
            return None

        def get_selected_parameters():
            '''Returns a list of the selected parameters.'''
            selected_parameters = []
            for parameter, checkbox in checkboxes.items():
                if checkbox.get() == 1:
                    selected_parameters.append(parameter)
            self.search_refs = selected_parameters
            return selected_parameters

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
        # It will be a top level window,
        # so it will be on top of the main window.
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
            parameters_dict = data.get("search_parameters", {})
            # Get the list of parameters from the JSON file
            parameters_list = list(parameters_dict.keys())


        checkboxes = {}

        # Create a frame to hold the checkboxes
        checkbox_frame = CTkXYFrame(param_window, width=640, height=300)
        checkbox_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        number_of_columns = 5
        # Create a list of checkboxes
        for index, parameter in enumerate(parameters_list):
            if index % number_of_columns == 0:
                row = (index // number_of_columns)
                column = 0
            else:
                row = (index // number_of_columns)
                column = index % number_of_columns

            # Create a checkbox for each parameter
            checkboxes[parameter] = ctk.CTkCheckBox(
                checkbox_frame,
                text=parameter,
                state=parameters_dict[parameter]["state"])
            widget_classes.HoverInfo(
                checkboxes[parameter],
                text=parameters_dict[parameter]["description"])
            if parameters_dict[parameter]["selected"] == "True":
                checkboxes[parameter].select()
            
            
            checkboxes[parameter].grid(row=row, column=column, padx=10, pady=10)
        
        # Create a checkbox to select all parameters
        select_all = ctk.CTkCheckBox(
            checkbox_frame,
            text="Select All",
            command=lambda: (
                (select_all_parameters() if select_all.get() else deselect_all_parameters())
            ))
        select_all.grid(row=(len(parameters_list)//number_of_columns)+1, column=0, padx=10, pady=10)
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
            command=lambda: [
                get_selected_parameters(),
                close_window(run=True)
                ]
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
        self.run_search_task(substances)




#--------------------------------------------------------------------------

    def run_search_task(self,substances):
        '''Runs the search for the parameters in a separate thread.'''
        #-------------------------------
        # Here goes everything before the main loop
        self.search_result = {
        }
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
                    self.search_result[identifier] = data
                    # Search for each id of a compuound:
                    for key,_ in data.items():
                        # Get the ref value from the data
                        for ref in self.search_refs:
                            if ref in data[key]["data_refs"]:
                                # Get the URL from the data
                                url = data[key]["data_refs"][ref]
                                # Check if "data_table" is in the search result
                                # If not, create it
                                if "data_table" not in self.search_result[identifier][key]:
                                    self.search_result[identifier][key]["data_table"] = {}
                                # Check if the ref is in the data_table
                                # If not, create it
                                if ref not in self.search_result[identifier][key]["data_table"]:
                                    self.search_result[identifier][key]["data_table"][ref] = {}
                                # Save the data in the data_table
                                self.search_result[identifier][key]["data_table"][ref] = self.data_extract(url)
                return None

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
                return None

        # Here comes everything after the main loop
        def on_thread_complete():
            print("Job done")

            print("-" * 50)
            print(f"Results: {len(self.search_result)}")
            for key, value in self.search_result.items():
                print(key)
            # Save the result dictionary into a JSON file
            
            with open("result.json", "w") as json_file:
                json.dump(self.search_result, json_file, indent=4)
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
            print("-" * 50)
            return None
            
            
            #start_button['state'] = 'normal'
        #threading.Thread(target=threaded_task, kwargs={'iterable': substances}).start()
        threading.Thread(target=lambda: [
            threaded_task(substances),
            on_thread_complete()
            ]).start()
        print("Thread started")
        return None
    #--------------------------------------------------------------------------






