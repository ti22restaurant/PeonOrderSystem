"""This module provides support for accessing external files
for generating the UI and its components.
"""
import os

curr_dir = os.path.dirname(os.path.realpath(__file__))
SYSTEM_DIRECTORY_PATH = os.path.split(curr_dir)[0]

SYSTEM_DATA_PATH = os.path.join(SYSTEM_DIRECTORY_PATH,'data')

SYSTEM_LOG_PATH = os.path.join(SYSTEM_DATA_PATH, 'log')
SYSTEM_UI_PATH = os.path.join(SYSTEM_DATA_PATH, 'ui')
SYSTEM_FILE_PATH = os.path.join(SYSTEM_DATA_PATH, 'files')
SYSTEM_ORDERS_PATH = os.path.join(SYSTEM_DATA_PATH, 'orders')
SYSTEM_AUDIT_PATH = os.path.join(SYSTEM_DATA_PATH, 'audit')

SYSTEM_AUDIT_REQUESTS_PATH = os.path.join(SYSTEM_AUDIT_PATH, 'requests')

SYSTEM_ORDERS_CONFIRMED_DIRECTORY = os.path.join(SYSTEM_ORDERS_PATH, 'Confirmed')
SYSTEM_ORDERS_CHECKOUT_DIRECTORY = os.path.join(SYSTEM_ORDERS_PATH, 'Checkout')

SYSTEM_DATABASE_PATH = os.path.join(SYSTEM_DATA_PATH, 'databases')
SYSTEM_ORDERS_DATABASE = os.path.join(SYSTEM_DATABASE_PATH, 'Orders.db')
SYSTEM_RESERVATIONS_DATABASE = os.path.join(SYSTEM_DATABASE_PATH, 'Reservations.db')

MAIN_UI_PATH = os.path.join(SYSTEM_UI_PATH, 'PeonOrderSystemWindow.ui')
MENU_DATA = os.path.join(SYSTEM_FILE_PATH, 'menu_document.json')
OPTION_DATA = os.path.join(SYSTEM_FILE_PATH, 'options_document.json')
DISCOUNT_DATA = os.path.join(SYSTEM_FILE_PATH, 'discount_template_data.json')
CATEGORIES_DISPLAY_DATA = os.path.join(SYSTEM_UI_PATH, 'option_choices.json')
NON_FATAL_ERROR_MESSAGES_DATA = os.path.join(SYSTEM_LOG_PATH,
                                             'non_fatal_error_messages.json')
