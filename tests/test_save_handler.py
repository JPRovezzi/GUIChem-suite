'''This module contains tests for the save_handler module'''

from modules.save_handler import load

def test_load_ugropygui(mocker):
    '''Test that the load function calls the load function from the frame_save
    module when the input is "UgropyGUI"'''
    mock_load = mocker.patch('modules.tool_frame.ugropygui.frame_save.load')
    load("UgropyGUI")
    mock_load.assert_called_once()

def test_load_flash_calc():
    '''Test that the load function returns None when the input is "Flash-Calc"'''
    assert load("Flash-Calc") is None
