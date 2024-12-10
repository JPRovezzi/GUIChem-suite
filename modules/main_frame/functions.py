"""This module provides functions to create and manage a graphical user
interface (GUI) for UGROpyGUI.
Functions:
    clear_widgets_except(currentFrame): Clear all widgets except those in the
    specified frame.
"""
# Import the required modules:

# import json module to read the configuration file
import json
#---------------------------------------------------------
def read_json(path = "res",filename = "app",section = None, key = None):
    '''Read the value from the configuration JSON file.'''
    with open(f'{path}/{filename}.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
    f.close()
    return config[section][key]


