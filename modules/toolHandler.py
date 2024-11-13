import modules.guiFrames.frameRoot as frameRoot
import modules.guiFrames.frameWelcome as frameWelcome
import modules.guiFrames.ugropygui as ugropygui
from modules.guiFrames.ugropygui import frameSelection

def destroy_all_frames():
    i = 0
    for widget in frameRoot.root.winfo_children():
        if i < 2:
            None
        else:
            widget.destroy()
        i += 1

def selectTool_event(tool: str):
    try :
        destroy_all_frames()
    except:
        None
    frameWelcome.load(tool)
    None
    
def startTool_event(tool: str):
    if tool == "UgropyGUI":
        try :
            destroy_all_frames()
        except:
            None
        ugropygui.frameSelection.load()
    elif tool == "Flash-Calc":
        None


