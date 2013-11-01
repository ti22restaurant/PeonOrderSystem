#! /usr/bin/env python
# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
# ## BEGIN LICENSE
# This file is in the public domain
# ## END LICENSE

"""This module contains the PeonOrderSystem class which 
is the top level object that generates and controls
the PeonOrderSystem GUI.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from gi.repository import Gtk  # IGNORE:E0611 @UnresolvedImport

# Path import unused. Imported to set working directory
# as the one that PeonOrderSystem object is placed in.

from peonordersystem import path  # IGNORE:W0611
from peonordersystem.interface import Editor
from peonordersystem.interface.UI import UI
from peonordersystem import ConfirmationSystem
from peonordersystem import ErrorLogger

@ErrorLogger.error_logging
class PeonOrderSystem(UI):
    """Generates and controls the PeonOrderSystem GUI and
    establishes its functionality.
    """
    def __init__(self, title='Fish Cake Factory'):
        """Initializes and displays PeonOrderSystem GUI
        
        @keyword load_data: Keyword argument that accepts a
        2 tuple representing a dict of lists for the table orders
        and togo orders respectively. This Keyword argument is
        only to be used in cases of failure.
        
        @keyword title: Keyword argument that sets the title
        of the main GUI window. Default value is 'Fish Cake
        Factory'
        """
        ErrorLogger.initializing_fencepost_begin()
        load_data = ConfirmationSystem.generate_files()
        super(PeonOrderSystem, self).__init__(title, load_data=load_data)
        ErrorLogger.initializing_fencepost_finish()
    
    def order_confirmed(self, priority_order, non_priority_order):
        """Callback Method. Called when the order has been confirmed.
        This method calls the ConfirmationSystem functions to export
        the data to the parent directory.

        @param priority_order: list of MenuItems that represents the
        current priority order associated with the order.

        @param non_priority_order: list of MenuItems that represents
        the non-priority order associated with the order.

        @param *args: wildcard argument to catch button that calls
        this method.
        """
        order_name, current_order = super(PeonOrderSystem,
                                          self).order_confirmed(priority_order)
        ConfirmationSystem.order_confirmed(order_name, priority_order,
                                           non_priority_order, current_order)
    
    def checkout_confirm(self, order):
        """Callback Method. Called when the order checkout has been
        confirmed. This method calls the ConfirmationSystem functions
        to export the checkout data to its parent directory.
        
        @param order: n-tuple of subdivded checks. This is to ensure
        that checks that have had the split operation performed on
        them are acceptable as well.
        """
        order_name, order_list = super(PeonOrderSystem, self).checkout_confirm()
        ConfirmationSystem.checkout_confirmed(order_name, order, order_list)

    def initiate_response_dialog(self, response_type):
        """Override Method

        @param response_type:
        @return:
        """
        if response_type == Editor.PRINT_RESPONSE:
            self.print_check_info()
        else:
            super(PeonOrderSystem, self).initiate_response_dialog(response_type)

    def print_check_info(self):
        """Calls the ConfirmationSystem function that
        prints the check information associated with
        the given order.

        This performs the same operation as checking
        out the check, except it doesn't clear the checks
        data. This is so that it can be accessed again.

        @return: None
        """
        order_name, order_list = self.get_order_info()
        ConfirmationSystem.print_check(order_name, order_list)
    
if __name__ == '__main__':
    
    USER = PeonOrderSystem()
    Gtk.main()
