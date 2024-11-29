import pytest
import importlib

import modules.guiFrames.frame_root as frame_root

def test_create_gui(mocker):
    mock_create_gui = mocker.patch('modules.guiFrames.frame_root.create_gui')
    frame_root.create_gui()
    mock_create_gui.assert_called_once()




