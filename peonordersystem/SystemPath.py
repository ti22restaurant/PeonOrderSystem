"""This module provides support for accessing external files
for generating the UI and its components.
"""
from os.path import join, realpath, split, dirname

curr_dir = dirname(realpath(__file__))
SYSTEM_DIRECTORY_PATH = split(curr_dir)[0]

SYSTEM_DATA_PATH = join(SYSTEM_DIRECTORY_PATH, 'data')

SYSTEM_LOG_PATH = join(SYSTEM_DATA_PATH, 'log')
SYSTEM_UI_PATH = join(SYSTEM_DATA_PATH, 'ui')
SYSTEM_FILE_PATH = join(SYSTEM_DATA_PATH, 'files')
SYSTEM_ORDERS_PATH = join(SYSTEM_DATA_PATH, 'orders')
SYSTEM_AUDIT_PATH = join(SYSTEM_DATA_PATH, 'audit')

SYSTEM_TEMPLATE_PATH = join(SYSTEM_DATA_PATH, 'templates')
SYSTEM_MEDIA_PATH = join(SYSTEM_DATA_PATH, 'media')
SYSTEM_FONT_PATH = join(SYSTEM_MEDIA_PATH, 'fonts')

SYSTEM_AUDIT_REQUESTS_PATH = join(SYSTEM_AUDIT_PATH, 'requests')

SYSTEM_TEMPLATE_RECEIPT_PATH = join(SYSTEM_TEMPLATE_PATH, 'receipts')
SYSTEM_TEMPLATE_RECEIPT_HEADER_PATH = join(SYSTEM_TEMPLATE_RECEIPT_PATH, 'header')
SYSTEM_TEMPLATE_RECEIPT_FOOT_PATH = join(SYSTEM_TEMPLATE_RECEIPT_PATH, 'footer')
SYSTEM_TEMPLATE_RECEIPT_MAIN_PATH = join(SYSTEM_TEMPLATE_RECEIPT_PATH, 'main')

SYSTEM_ORDERS_CONFIRMED_DIRECTORY = join(SYSTEM_ORDERS_PATH, 'Confirmed')
SYSTEM_ORDERS_CHECKOUT_DIRECTORY = join(SYSTEM_ORDERS_PATH, 'Checkout')

SYSTEM_DATABASE_PATH = join(SYSTEM_DATA_PATH, 'databases')
SYSTEM_ORDERS_DATABASE = join(SYSTEM_DATABASE_PATH, 'Orders.db')
SYSTEM_RESERVATIONS_DATABASE = join(SYSTEM_DATABASE_PATH, 'Reservations.db')

MAIN_UI_PATH = join(SYSTEM_UI_PATH, 'PeonOrderSystemWindow.ui')
MENU_DATA = join(SYSTEM_FILE_PATH, 'menu_document.json')
OPTION_DATA = join(SYSTEM_FILE_PATH, 'options_document.json')
DISCOUNT_DATA = join(SYSTEM_FILE_PATH, 'discount_template_data.json')
CATEGORIES_DISPLAY_DATA = join(SYSTEM_UI_PATH, 'option_choices.json')
NON_FATAL_ERROR_MESSAGES_DATA = join(SYSTEM_LOG_PATH,
                                             'non_fatal_error_messages.json')
