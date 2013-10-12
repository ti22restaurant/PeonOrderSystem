"""This module provides support for accessing external files
for generating the UI and its components.
"""
import os

SYSTEM_DIRECTORY_PATH = os.getcwd() 

SYSTEM_DATA_PATH = SYSTEM_DIRECTORY_PATH + '/data/'

SYSTEM_LOG_PATH = SYSTEM_DATA_PATH + 'log/'
SYSTEM_UI_PATH = SYSTEM_DATA_PATH + 'ui/'
SYSTEM_FILE_PATH = SYSTEM_DATA_PATH + 'files/'
SYSTEM_ORDERS_PATH = SYSTEM_DATA_PATH + 'orders/'

MAIN_UI_PATH = SYSTEM_UI_PATH + 'PeonOrderSystemWindow.ui'
MENU_DATA = SYSTEM_FILE_PATH + 'menu_document.json'
OPTIONS_DATA = SYSTEM_UI_PATH + 'option_choices.json'
NON_FATAL_ERROR_MESSAGES_DATA = SYSTEM_LOG_PATH + 'non_fatal_error_messages.json'
