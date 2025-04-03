"""
This script creates a simple GUI application using Tkinter that demonstrates the use of a custom hover menu.
Classes:
    HoverInfo(Menu):
        A custom menu that appears when hovering over a widget and disappears when the mouse leaves the widget.
        It can also execute a command when the "Return" key is pressed while the menu is displayed.
        Methods:
            __init__(parent, text, command=None):
                Initializes the hover menu with the parent widget, text to display, and an optional command.
            __del__():
                Unbinds the hover events when the object is deleted.
            Display(event):
                Displays the hover menu at the mouse cursor's position.
            Remove(event):
                Hides the hover menu when the mouse leaves the widget.
            Click(event):
                Executes the command associated with the hover menu when the "Return" key is pressed.
    MyApp(Frame):
        A simple application that demonstrates the use of the HoverInfo class.
        Methods:
            __init__(parent=None):
                Initializes the application with two labels, one of which has a hover menu.
            HelloWorld():
                Prints "Hello World" to the console when called.
Usage:
    Run the script to launch the application. Hover over the second label to see the hover menu.
    Press the "Return" key while the hover menu is displayed to execute the associated command.
"""
from tkinter import *
from customtkinter import *
import re
# Class HoverInfo inherits from the Tkinter Menu class
class HoverInfo_old(Menu):
    # Constructor to initialize the HoverInfo object
    def __init__(self, parent, text, command=None):
        self._com = command  # Store the optional command to execute on "Return" key press
        Menu.__init__(self, parent, tearoff=0)  # Initialize the parent Menu class with no tear-off
        if not isinstance(text, str):  # Check if the provided text is a string
            raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__)
        toktext = re.split('\n', text)  # Split the text into lines using newline as a delimiter for hover menu.
        #self._displayed = False
        #self.master.bind("<Enter>", self.Display)
        #self.master.bind("<Leave>", self.Remove)
        if True:
            for t in toktext:  # Iterate over each line of text
                self.add_command(label=t)  # Adds each line of the text as a label in the menu
                #self._displayed = False  # Initialize the displayed state to False
                # Bind the "Enter" event to display the hover menu
                self.master.bind("<Enter>", self.Display)
                # Bind the "Leave" event to remove the hover menu
                self.master.bind("<Leave>", self.Remove)

    # Destructor to clean up event bindings when the object is deleted
    #def __del__(self):
        #self.master.unbind("<Enter>")  # Unbind the "Enter" event
        #self.master.unbind("<Leave>")  # Unbind the "Leave" event

    # Method to display the hover menu at the mouse cursor's position
    def Display(self, event):
        if True:
        #if not self._displayed:  # Check if the menu is not already displayed
            #self._displayed = True  # Set the displayed state to True
            self.post(event.x_root, event.y_root)  # Display the menu at the cursor's position
        #if self._com is not None:  # If a command is provided
            #self.master.unbind_all("<Return>")  # Unbind any existing "Return" key bindings
            #self.master.bind_all("<Return>", self.Click)  # Bind the "Return" key to the Click method

    # Method to hide the hover menu when the mouse leaves the widget
    def Remove(self, event):
        if True:
        #if self._displayed:  # Check if the menu is currently displayed
            #self._displayed = False  # Set the displayed state to False
            self.unpost()  # Hide the menu
        #if self._com is not None:  # If a command is provided
            #self.unbind_all("<Return>")  # Unbind the "Return" key

    # Method to execute the associated command when the "Return" key is pressed
    #def Click(self, event):
        #self._com()  # Call the command function
class HoverInfo(Menu):
    # Constructor to initialize the HoverInfo object
    def __init__(self, parent, text, command=None):
        self._com = command  # Store the optional command to execute on "Return" key press
        Menu.__init__(self, parent, tearoff=0)  # Initialize the parent Menu class with no tear-off
        if not isinstance(text, str):  # Check if the provided text is a string
            raise TypeError('Trying to initialise a Hover Menu with a non string type: ' + text.__class__.__name__)
        toktext = re.split('\n', text)  # Split the text into lines using newline as a delimiter for hover menu.
        for t in toktext:  # Iterate over each line of text
            self.add_command(label=t)  # Adds each line of the text as a label in the menu
            # Bind the "Enter" event to display the hover menu
            self.master.bind("<Enter>", self.Display)
            # Bind the "Leave" event to remove the hover menu
            self.master.bind("<Leave>", self.Remove)
    # Method to display the hover menu at the mouse cursor's position
    def Display(self, event):
        self.post(event.x_root, event.y_root)

    # Method to hide the hover menu when the mouse leaves the widget
    def Remove(self, event):
        self.unpost()  # Hide the menu

class MyApp(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.grid()
        self.lbl = Label(self, text='testing')
        self.lbl2 = Label(self, text='testing2')

        self.lbl.grid()
        Label(self, text='').grid()
        Label(self, text='').grid()
        self.lbl2.grid()

        self.hover = HoverInfo(
            self.lbl2,
            'while hovering press return \n for an exciting msg',
            #self.HelloWorld
            )
        self.hover = HoverInfo(
            self.lbl,
            'Label',
            #self.HelloWorld
            )

    def HelloWorld(self):
        None
 
app = MyApp()
app.master.title('test')
app.master.geometry('400x400')
app.mainloop()

# Fix the issue by explicitly binding the hover events to the specific widget (lbl2)
