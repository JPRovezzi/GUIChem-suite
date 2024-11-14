'''This script is the main script for the GUIChem-suite application.'''

# Import the required libraries

# frameRoot is the main frame of the GUIChem-suite application
import modules.guiFrames.frame_root as frame_root
#------------------------------------------------------------

# Create the main window

if __name__ == "__main__":
    frame_root.create_gui()
