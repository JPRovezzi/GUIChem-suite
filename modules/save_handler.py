'''This module is used to handle the save functionality of the GUIChem-suite application.'''
import modules.guiFrames.ugropygui.frame_save as ugropygui_frame_save

def load(tool):
    match tool:
        case "UgropyGUI": 
            ugropygui_frame_save.load()
        case "Flash-Calc":
            None