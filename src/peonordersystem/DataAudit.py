"""DataAudit module holds the necessary functions and
information for auditing previous orders and compiling
them into an xls document that is more human readable.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""
import os
import xlsxwriter
from datetime import time, date, datetime, timedelta

from src.peonordersystem import path
from src.peonordersystem import ConfirmationSystem

#====================================================================================
# This block in the module generates and checks the necessary directories,
# as well as creates the module wide constants.
#====================================================================================

ORDERS_DIRECTORY = path.SYSTEM_ORDERS_PATH
AUDIT_DIRECTORY = path.SYSTEM_AUDIT_PATH

TODAY = datetime.now()
TODAY_DIRECTORY = AUDIT_DIRECTORY + TODAY.strftime('%Y/%m/%d')

if not os.path.exists(TODAY_DIRECTORY):
    os.mkdir(TODAY_DIRECTORY)

REQUEST_DIRECTORY = AUDIT_DIRECTORY + "/requests"

if not os.path.exists(REQUEST_DIRECTORY):
    os.mkdir(REQUEST_DIRECTORY)
#====================================================================================
# This block defines formating constants utilized to write the audit file.
#====================================================================================

AREA_COL_WIDTH = 3

BOLD_BORDER_FORMAT = {'border', 2}



#====================================================================================
#
#====================================================================================



