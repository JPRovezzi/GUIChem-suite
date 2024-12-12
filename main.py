'''This script is the main script for the GUIChem-suite application.'''

# Import the required libraries

# frameRoot is the main frame of the GUIChem-suite application
from modules.main_frame.frame_root import Root
#------------------------------------------------------------

# Create the main window

if __name__ == "__main__":
    #create_gui()
    root=Root()
    root.create_gui()
