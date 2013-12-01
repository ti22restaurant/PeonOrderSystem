"""
Settings module holds constants that are used
throughout the PeonOrderSystem project.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
# in milliseconds, 10 minutes default
RESERVATION_UPDATE_TIME_FRAME = 1000 * 60 * 10
# in seconds, 12000 sec(20 minutes) default
RESERVATION_NOTIFICATION_TIME_MAX = RESERVATION_UPDATE_TIME_FRAME / 1000 * \
                                      2.0 - 1.0
# in seconds, 0 seconds
RESERVATION_NOTIFICATION_TIME_MIN = 0.0

# notification time frame as str
RESERVATION_NOTIFICATION_TIME_FRAME_STR = \
    str(round(RESERVATION_NOTIFICATION_TIME_MAX / 60)) + ' minutes'

STANDARD_TEXT = 500
STANDARD_TEXT_BOLD = STANDARD_TEXT + 300
STANDARD_TEXT_LIGHT = STANDARD_TEXT - 300

MENU_ITEM_NON_CONFIRMED_COLOR_HEXADECIMAL = '#000000'
MENU_ITEM_CONFIRMED_COLOR_HEXADECIMAL = '#999999'

SALES_TAX = .10
