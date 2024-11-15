'''
    This module provides functions to handle the file menu. Such as opening, 
    saving, and closing files.
'''
# Import the required libraries:
import modules.guiFrames.frame_root as frame_root
import modules.tool_handler as tool_handler
#------------------------------------------------------------

def file_menu_event(file_option:str):
    '''Handle the file menu events.'''
    match file_option:
        case "New":
            tool_handler.select_tool_event(frame_root.tools_menu.get())
            frame_root.file_menu.set("File")
        case "Open":
            print("Open file")
            frame_root.file_menu.set("File")
        case "Save":
            print("Save file")
            frame_root.file_menu.set("File")
        case "Close":
            tool_handler.destroy_all_frames()
            frame_root.file_menu.set("File")
        case "Exit":
            frame_root.root.destroy()
        case _:
            print("Invalid option")
