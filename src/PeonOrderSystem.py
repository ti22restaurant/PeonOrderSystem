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

from src.peonordersystem.interface import Editor
from src.peonordersystem.interface.UI import UI
from src.peonordersystem import ConfirmationSystem
from src.peonordersystem import ErrorLogger
from src.peonordersystem import DataAudit
from src.peonordersystem.Settings import SYSTEM_TITLE

@ErrorLogger.error_logging
class PeonOrderSystem(UI):
    """Generates and controls the PeonOrderSystem GUI and
    establishes its functionality.
    """
    def __init__(self, title=SYSTEM_TITLE):
        """Initializes and displays PeonOrderSystem GUI
        
        @keyword title: Keyword argument that sets the title
        of the main GUI window. Default value is title constant
        given by Settings module.
        """
        ErrorLogger.initializing_fencepost_begin()

        load_data = ConfirmationSystem.unpack_order_data()
        reservation_data = ConfirmationSystem.unpack_reservations_data()

        super(PeonOrderSystem, self).__init__(title, load_data=load_data,
                                              reservation_data=reservation_data)
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

    def add_reservation_confirmed(self, new_reservation):
        """Override Method

        Updates the reservation data by passing it to the
        confirmation system so that it may be serialized and
        persist.

        @param new_reservation: data representing the
        reservation.

        @warning: This data is not used. Instead it is
        expected that the call to the super class will
        return an instance of the reservation that may
        be used instead.

        @return: Reservation object that was yielded
        from the call on super.
        """
        reserver = super(PeonOrderSystem, self).add_reservation_confirmed(
            new_reservation)
        ConfirmationSystem.add_reservation_to_database(reserver)
        return reserver

    def undo_checkout_order(self, *args):
        """Override Method

        This method is called whenever the
        associated widget is clicked. This method
        obtains the stored checked out order data
        and initiates the requisite dialog window
        that allows the user to interact with, and
        retrieve stored orders that were previously
        checked out.

        @param args: wildcard catchall that is used
        to catch the Gtk.Widget that called this
        method.

        @return: None
        """
        load_data = ConfirmationSystem.unpack_checkout_data()
        super(PeonOrderSystem, self).undo_checkout_order(load_data)

    def initiate_response_dialog(self, response_type):
        """Override Method

        initiates the appropriate response
        to the dialog response_type emitted.

        @param response_type: int constants
        that are defined in the Editor module.

        @return: None
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

    def perform_audit(self, start_date, end_date, **kwargs):
        """Override Method.

        Performs an audit over the specified period from start date
        until end date. The audited file is stored in a spread sheet
        and saved at the location given, with the given name.

        @param start_date: datetime.date object that represents the
        beginning date to start the audit.

        @param end_date: datetime.date object that represents the
        ending date to end the audit.

        @param location: str representing the directory to which
        the generated audit spreadsheet should be saved to.

        @param name: str representing the file name to which
        the generated audit spreadsheet should be saved as.

        @return: None
        """
        DataAudit.request_audit(start_date, end_date, **kwargs)

    def run(self):
        """Runs the thread to execute the UI
        built by this object.

        @return: int value representing the
        response associated with the closure of
        running this object.
        """
        Gtk.main()

        message_title = "Do you want to perform a closing audit?"

        message = 'You are about to close the POS UI.\n\n Do you want to '
        message += 'perform a closing audit?\n\n'
        message += 'This audit will compile all the data for the today ' + \
                   'and store it in an easy to read excel file in the ' + \
                   'standard audit area. \n\n' \
                   ' This make take a minute though, are you sure you ' + \
                   'want to perform the audit?'

        if self.run_warning_dialog(message_title, message):
            ConfirmationSystem.update_database()
            DataAudit.closing_audit()

    
if __name__ == '__main__':
    
    USER = PeonOrderSystem()
    USER.run()
