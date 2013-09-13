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

from peonordersystem import path
from peonordersystem.interface.UI import UI
from peonordersystem import ConfirmationSystem

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
        load_data = ConfirmationSystem.generate_files()
        super(PeonOrderSystem, self).__init__(title, load_data=load_data)
    
    def order_confirmed(self, *args):
        """Callback Method. Called when the order has been confirmed.
        This method calls the ConfirmationSystem functions to export
        the data to the parent directory.
        
        @param *args: wildcard argument to catch button that calls
        this method.
        """
        super(PeonOrderSystem, self).order_confirmed()
        order_name, order_list = self.get_order_info()
        ConfirmationSystem.order_confirmed(order_name, order_list)
    
    def checkout_confirm(self, *args):
        """Callback Method. Called when the order checkout has been
        confirmed. This method calls the ConfirmationSystem functions
        to export the checkout data to its parent directory.
        
        @param *args: wildcard argument to catch button that calls
        this method.
        """
        super(PeonOrderSystem, self).checkout_confirm()
        order_name, order_list = self.get_order_info()
        ConfirmationSystem.checkout_confirmed(order_name, order_list)
    
if __name__ == '__main__':
    
    USER = PeonOrderSystem()
    Gtk.main()
