"""Editor module contains the Editor class that
relies on the Dialog windows to generate, display
and run the Dialog windows to edit MenuItems and
confirm Orders.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from gi.repository import Gtk
from peonordersystem.interface import Dialog
from peonordersystem import ErrorLogger
from peonordersystem.CustomExceptions import InvalidItemError, InvalidOrderError

PRINT_RESPONSE = Dialog.PRINT_DIALOG_RESPONSE
COMP_RESPONSE = Dialog.COMP_DIALOG_RESPONSE
DISCOUNT_RESPONSE = Dialog.DISCOUNT_DIALOG_RESPONSE
SPLIT_CHECK_RESPONSE = Dialog.SPLIT_CHECK_DIALOG_RESPONSE
GENERAL_OPTIONS_RESPONSE = Dialog.GENERAL_OPTIONS_DIALOG_RESPONSE

ACCEPT_RESPONSE = Gtk.ResponseType.ACCEPT
REJECT_RESPONSE = Gtk.ResponseType.REJECT

@ErrorLogger.error_logging
class Editor(object):
    """Editor performs the control functionality
    of the dialog windows. This object allows for
    confirmation of orders and editing of MenuItems.
    
    @var parent: Object that will be the parent of all
    generated Dialog windows.
    
    """
    
    def __init__(self, parent):
        """Initializes the Editor object and sets
        the given parent.
        
        @param parent: Object representing the parent
        that the created Dialogs will be displayed from.
        Expecting Gtk.Window
        """
        self.parent = parent

    #==========================================================================
    # This block is what I refer to as the editor/confirmer section. This block
    # contains highly generic methods that are utilized by other methods to
    # perform standard operations. Editing methods in this block may cause
    # errors.
    #==========================================================================

    def edit(self, menu_item, entry_dialog):
        """Generates and runs the given EntryDialog with the
        given MenuItem as a parameter.

        @param menu_item: Parameter passed into the dialog
        window. This parameter is expected to be a
        MenuItem instance.

        @param entry_dialog: function pointer representing
        the dialog to be called. this parameter is
        expected to be subclass instances of the EntryDialog

        @return: int representing the Gtk.ResponseType emitted
        by this dialog window.
        """
        if menu_item_check(menu_item):
            dialog_window = entry_dialog(self.parent, menu_item)
            value = dialog_window.run_dialog()
            del dialog_window

            return value

    def confirm(self, order_list, confirm_dialog, confirm_function):
        """Generates and runs the given ConfirmationDialog with
        the given parameters as arguments.

        @raise TypeError: If the given confirm_dialog is not a
        subclass instance of the ConfirmationDialog.

        @param order_list: list representing some information
        passed to the confirmation window.

        @param confirm_dialog: ConfirmationDialog subclass that
        is to be run.

        @param confirm_function: function pointer that is executed
        when confirmation of the dialog occurs.

        @return: int representing the Gtk.ResponseType emitted by
        the dialog window, or None if no dialog window was
        executed.
        """
        if order_check(order_list):
            dialog_window = confirm_dialog(self.parent, confirm_function,
                                           order_list)
            response = dialog_window.run_dialog()
            del dialog_window

            return response

        return None

    #=========================================================================
    # This block contains methods that are performed on MenuItem objects. All
    # methods expect to be given a menu item, and then make reference to the
    # respective editor/confirmer method in the editor/confirmer section. All
    # dialogs contained in this bock rely on the editor/confirmer to run and
    # instantiate their respective dialog windows.
    #=========================================================================
    
    def edit_stars(self, menu_item):
        """Calls a dialog window on the given MenuItem
        that edits its star content.
        
        @param menu_item: MenuItem object that is to
        have the dialog initiated on it.

        @return: bool representing if the dialog window was confirmed
        or cancelled. True for confirmed, False for cancelled.
        """
        value = self.edit(menu_item, Dialog.StarEntryDialog)
        return value == Gtk.ResponseType.ACCEPT
    
    def edit_note(self, menu_item):
        """Calls a dialog window on the given MenuItem
        that edits its note content.
        
        @param menu_item: MenuItem object that is to
        have the dialog initiated on it.

        @return: bool representing if the dialog window was confirmed
        or cancelled. True for confirmed, False for cancelled.
        """
        value = self.edit(menu_item, Dialog.NoteEntryDialog)
        return value == Gtk.ResponseType.ACCEPT
    
    def edit_options(self, menu_item):
        """Calls a dialog window on the given MenuItem
        that edits its chosen options from its options
        choices.
        
        @param menu_item: MenuItem object that is to
        have the dialog initiated on it.

        @return: int representing the response type emitted
        by the dialog window.
        """
        return self.edit(menu_item, Dialog.OptionEntryDialog)
    
    def confirm_order(self, order_list, confirm_function):
        """Calls the confirm order dialog on the given
        order list. If confirmed this dialog calls the given
        confirm function. Confirm order displays information
        that should be accessible to the kitchen.
        
        @param order_list: list of MenuItem objects that
        represents the current order to be confirmed
        
        @param confirm_func: function pointer that points
        to the function to be executed if the order is confirmed.

        @return: bool representing if the dialog window was confirmed
        or cancelled. True for confirmed, False for cancelled.
        """
        order_list = get_unconfirmed_order(order_list)

        response = self.confirm(order_list, Dialog.OrderConfirmationDialog,
                                confirm_function)

        return response == ACCEPT_RESPONSE
    
    def checkout_order(self, order_list, confirm_function):
        """Calls the checkout confirmation dialog on the given
        order list. If confirmed this dialog calls the given
        confirm function. Confirm checkout displays information
        that will be used in calculating the total for the 
        customers payment.
        
        @param order_list: list of MenuItem objects that represents
        the current order to be checked out.
        
        @param confirm_function: function pointer that points to the
        function to be executed if the checkout is confirmed.

        @return: bool representing if the dialog window was confirmed
        or cancelled. True for confirmed, False for cancelled.
        """
        response = self.confirm(order_list, Dialog.CheckoutConfirmationDialog,
                                confirm_function)
        return response

    def split_check_order(self, order_list, confirm_function):
        """Calls the split confirmation dialog on the given
        order list. If confirmed this dialog calls the given
        confirmation function.

        @param order_list: list of MenuItem objects that represents
        the MenuItems to be split.

        @param confirm_function: function that is to be called when
        the split check confirmation occurs.

        @return: bool representing of the dialog window was confirmed
        or cancelled. True for confirmed, False for cancelled.
        """
        response = self.confirm(order_list, Dialog.SplitCheckConfirmationDialog,
                                confirm_function)
        return response == ACCEPT_RESPONSE

    def comp_item_order(self, order_list, confirm_function):
        """Calls the comp item confirmation dialog on the
        given order list. Only the locked menu items contained
        in the given order list will be operated on. If confirmed
        this dialog calls the given confirm function with the first
        argument as a list of MenuItem objects that represents the
        edited order.

        @param order_list: list of MenuItem objects that represents
        the order to have the dialog performed on it.

        @param confirm_function: function pointer that points to
        the function to be called if the dialog is confirmed.

        @return: bool representing if the dialog window was confirmed
        or cancelled. True for confirmed, False for cancelled.
        """
        order_list = get_locked_item_order(order_list)

        response = self.confirm(order_list,
                                Dialog.CompItemsOrderConfirmationDialog,
                                confirm_function)

        return response == ACCEPT_RESPONSE

    #======================================================================
    # Methods in this block require special considerations when
    # instantiating their dialog windows and as such cannot be run with the
    # generic editor/confirmer archetype utilized by most other dialogs.
    #======================================================================
    
    def select_misc_order(self, name_list, confirm_function):
        """Calls the misc selection confirmation dialog on the
        given name list. Calls the confirmation function if the
        misc selection is confirmed.
        
        @param name_list: list of 3-tuples that represent the
        given misc orders.
        
        @param confirm_function: function pointer that is called
        when the a misc order has been confirmed or added
        """
        dialog = Dialog.OrderSelectionConfirmationDialog(self.parent, confirm_function,
                                                         name_list)
        return dialog.run_dialog() == ACCEPT_RESPONSE

    def discount_item_order(self, order_list, confirm_function, discount_templates):
        """Calls the discount item confirmation dialog on the
        given order list. This confirmation dialog allows the
        user to edit the given order by opening a new dialog
        window through which the user may add 'discount' MenuItems
        and apply them to the order via confirmation. If confirmed
        this dialog calls the given confirm function with the
        first argument as a list fo MenuItems that represents the
        newly adjusted order list.

        @param order_list: list of MenuItem objects that represents
        the order to be operated on.

        @param confirm_function: function that is to be called if
        the dialog window receives confirmation.

        @param discount_templates: list of tuple that represents
        the stored discount template information.

        @return: bool representing if the discount dialog window was
        confirmed. True if the dialog was confirmed, False otherwise.
        """
        if order_check(order_list):

            dialog = Dialog.DiscountCheckoutConfirmationDialog(self.parent,
                                                               confirm_function,
                                                               order_list,
                                                               discount_templates)
            response = dialog.run_dialog()
            return response == ACCEPT_RESPONSE

        return False
    
    def add_new_reservation(self, confirm_function):
        """Calls a dialog window to add a new reservation to
        the reservations list. Runs dialog via this method.

        @param confirm_function: function pointer to be
        called when the dialog window has been confirmed.
        
        @return: returns a 3-tuple representing the added
        reservation. Format will be (str, str, float) 
        representing the name, number, and secs since the epoch
        respectively.
        """
        dialog = Dialog.AddReservationsDialog(self.parent, confirm_function)
        return dialog.run_dialog() == ACCEPT_RESPONSE

    def update_menu_items_data(self, menu_data, options_data, confirm_func):
        """Calls a dialog window that allows the user to edit
        the stored menu item data file that the UI uses to
        generate the menu items from. Runs dialog via this
        method.

        @param menu_data: dict of str key to list of MenuItem
        object values. Each key represents a category in the
        dict, and each list represents the MenuItems associated
        with that category.

        @param confirm_func: function to be called if or when
        the dialog window has been confirmed.

        @return: bool value representing if the data was updated
        or not.
        """
        dialog = Dialog.UpdateMenuItemsDialog(self.parent, menu_data,
                                              options_data, confirm_func)
        return dialog.run_dialog() == ACCEPT_RESPONSE

    def update_discount_templates(self, confirm_function, discount_templates):
        """Calls a dialog window that allows the user to edit
        the stored discount templates data file that the UI
        uses to generate the discount templates available during
        the discount selection dialog. Runs dialog via this method.

        @param confirm_function: function that is to be called upon
        confirmation of the dialog window.

        @param discount_templates: list of tuple that represents the
        discount templates that is stored and to be updated.

        @return: bool value representing if the templates updating was
        confirmed or not.
        """
        dialog = Dialog.UpdateTemplateDiscountCheckoutConfirmationDialog(self.parent,
                                                                         confirm_function,
                                                                         discount_templates)
        response = dialog.run_dialog()
        del dialog
        return response == ACCEPT_RESPONSE

    def update_option_items_data(self, options_data, confirm_func):
        """Calls a dialog window that allows the user to edit
        the stored general OptionItems data file that the UI
        uses to generate the general OptionItems from. Runs dialog
        via this method. Upon confirmation the given confirm
        func is called with the new option data.

        @param options_data: dict of str keys representing the
        option categories mapped to list of OptionItem objects
        that represents the associated options.

        @param confirm_func: Function that is to be called
        with the given updated options data in the same format,
        upon confirmation.

        @return: bool value representing if the data updating
        was confirmed or not.
        """
        dialog = Dialog.UpdateGeneralOptionSelectionDialog(self.parent,
                                                           confirm_func,
                                                           options_data)
        response = dialog.run_dialog()
        del dialog
        return response == ACCEPT_RESPONSE

    def undo_checkout_order(self, checked_out_data, confirm_function):
        """Calls a dialog window that allows the user to retrieve
        previously checked out orders and return them to UI for editing
        or adjustment. Calls the confirm function upon confirmation.
        Runs the dialog window via this method.

        @param checked_out_data: dict of tuple keys, represented as
        (str, str) -> (name, date). Keys are mapped to values
        representing the associated order as a list of MenuItem
        objects.

        @param confirm_function: Function that is to be called upon
        confirmation. This function will be called with a dict of
        key tuple (str, str, str) -> (name, _, date) to lists of
        MenuItem objects.

        @return: bool value representing if the dialog window
        was confirmed or not. True representing if the dialog
        was confirmed. False if it was cancelled.
        """
        dialog = Dialog.UndoCheckoutDialog(self.parent, checked_out_data,
                                           confirm_function)
        response = dialog.run_dialog()

        return response == ACCEPT_RESPONSE

    def edit_general_options(self, option_data, menu_item):
        """Calls a dialog window that allows the user to
        edit/remove options from the given MenuItem object
        with reference to all possible options available for
        any MenuItem.

        @param option_data: dict of str keys representing the
        categories to values list of OptionItems that represent
        the options available under that specific category.

        @param menu_item: MenuItem object that is to be edited
        by this dialog window.

        @return: int representing the response type associated
        with the dialog window.
        """
        if menu_item_check(menu_item):
            dialog = Dialog.GeneralOptionSelectionDialog(self.parent,
                                                         option_data,
                                                         menu_item)
            response = dialog.run_dialog()
            return response


#===========================================================================
# This block contains functions that are called as conditionals to
# ensure that specific conditions are met with given items. These functions
# are module wide.
#===========================================================================


def menu_item_check(menu_item):
    """Checks whether the given MenuItem is a valid 
    MenuItem to have operations performed on it.

    @raise InvalidItemError: If the given item is
    None or it is not editable

    @return: bool representing True if the MenuItem
    is not None and the MenuItem is editable. False
    otherwise.
    """
    if not menu_item or not menu_item.is_editable():
        message = 'Expected a MenuItem type object that ' + \
                  'is also editable. Got instead:\n' + \
                  'Type -> {}\n'.format(type(menu_item))

        raise InvalidItemError(message)

    return True


def order_check(current_order):
    """Checks if the current order is a accessible, valid
    order.

    @raise InvalidOrderError: If order is None or its
    length is less than or equal to zero.
    
    @return: bool representing True if the given order is
    not None and is of length > 0. False otherwise.
    """
    if not current_order or not len(current_order) >= 0:
        message = 'Expected a list of MenuItem objects. ' + \
                  'That has a length greater than zero. ' + \
                  'Instead got type -> {}\n'.format(type(current_order))
        if current_order:
            message += 'length -> {}'.format(len(current_order))

        raise InvalidOrderError(message)

    return True


def get_unconfirmed_order(current_order):
    """Checks each MenuItem if it is confirmed. Returns
    the a new order with all confirmed items removed.

    @param current_order: list of MenuItem objects.

    @return: list of MenuItem objects that have not
    been confirmed yet.
    """
    def is_confirmed(menu_item):
        return not menu_item.confirmed

    order_list = filter(is_confirmed, current_order)

    if len(order_list) <= 0:
        message = 'Cannot confirm an empty order list'
        raise InvalidOrderError(message)

    return order_list


def get_locked_item_order(current_order):
    """Gets only the locked MenuItem objects
    that are stored within the given order.

    @param current_order: list of MenuItem
    objects.

    @raise InvalidOrderError: if the given
    list contains no locked menu items.

    @return: List of Locked MenuItem objects.
    """

    def is_locked(menu_item):
        return menu_item.is_locked()

    order_list = filter(is_locked, current_order)

    if len(order_list) <= 0:
        message = 'Expected to comp order with locked menu' + \
                  ' items. None found.'
        raise InvalidOrderError(message)

    return order_list
