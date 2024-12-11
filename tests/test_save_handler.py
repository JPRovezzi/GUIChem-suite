'''This module contains tests for the tool_handler module'''

from modules.tool_handler import save

def test_load_ugropygui(mocker):
    '''Test that the load function calls the load function from the frame_save
    module when the input is "UgropyGUI"'''
    mock_load = mocker.patch('addons.ugropygui.frame_save.load')
    save("UgropyGUI")
    mock_load.assert_called_once()

def test_load_flash_calc():
    '''Test that the load function returns None when the input is "Flash-Calc"'''
    assert save("Flash-Calc") is None
