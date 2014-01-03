"""Settings module that defines constants
used in testing.

@author: Carl McGraw
@contact: cjmcgraw( at )u.washington.edu
"""
import os
import string

from src.peonordersystem.Settings import TOGO_SEPARATOR

#====================================================================================
# This block represents constants used in generators
#====================================================================================
POSSIBLE_CHARS = string.printable * 10 + TOGO_SEPARATOR * 2
GENERATOR_MAX = 10**10
NUM_OF_CHARS = 100

#====================================================================================
# Constants used in defining print statements across modules
#====================================================================================
TABS = '    '

#====================================================================================
#This block represents constants used for defining the number of tests to run
#====================================================================================
NUMBER_OF_ITEMS_TO_GENERATE = 500