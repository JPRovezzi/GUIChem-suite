import pytest
from modules.guiFrames.frame_root import create_gui
import main

def test_create_gui(mocker):
    # Mock the create_gui function
    mock_create_gui = mocker.patch('modules.guiFrames.frame_root.create_gui')
    
    # Import the main script to trigger the __main__ block
    
    # Assert that create_gui was called once
    mock_create_gui.assert_called_once()