"""This module provides support for accessing external files
for generating the UI and its components.
"""
import os

SYSTEM_DIRECTORY_PATH = os.getcwd() 

SYSTEM_UI_PATH = SYSTEM_DIRECTORY_PATH + '/data/ui/'
SYSTEM_FILE_PATH = SYSTEM_DIRECTORY_PATH + '/data/files/'
MAIN_UI_PATH = SYSTEM_UI_PATH + 'PeonOrderSystemWindow.ui'

MENU_DATA = SYSTEM_FILE_PATH + 'menu_document.json'
OPTIONS_DATA = SYSTEM_UI_PATH + 'option_choices.json'
