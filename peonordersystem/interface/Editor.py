"""Editor module contains the Editor class that
relies on the Dialog windows to generate, display
and run the Dialog windows to edit MenuItems and
confirm Orders.

@author: Carl McGraw
@contact: cjmcgraw@u.washington.edu
@version: 1.0
"""

from peonordersystem.interface import Dialog

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
    
    def edit(self, menu_item, entry_dialog):
        """Generates and runs the given EntryDialog with the
        given MenuItem as a parameter.
        
        @param menu_item: Parameter passed into the dialog
        window. This parameter is expected to be a 
        MenuItem instance.
        
        @param entry_dialog: function pointer representing
        the dialog to be called. this parameter is
        expected to be subclass instances of the EntryDialog
        
        @return: value returned by the dialog windows run_dialog
        method.
        """
        dialog_window = entry_dialog(self.parent, menu_item)
        return dialog_window.run_dialog()
    
    def edit_stars(self, menu_item):
        """Calls a dialog window on the given MenuItem
        that edits its star content.
        
        @param menu_item: MenuItem object that is to
        have the dialog initiated on it.
        """
        self.edit(menu_item, Dialog.StarEntryDialog)
    
    def edit_note(self, menu_item):
        """Calls a dialog window on the given MenuItem
        that edits its note content.
        
        @param menu_item: MenuItem object that is to
        have the dialog initiated on it.
        """
        self.edit(menu_item, Dialog.NoteEntryDialog)
    
    def edit_options(self, menu_item):
        """Calls a dialog window on the given MenuItem
        that edits its chosen options from its options
        choices.
        
        @param menu_item: MenuItem object that is to
        have the dialog initiated on it.
        """
        self.edit(menu_item, Dialog.OptionEntryDialog)
    
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
        """
        is_confirm_dialog = issubclass(confirm_dialog,
                                       Dialog.ConfirmationDialog)
        if not is_confirm_dialog:
            raise TypeError('Editor object expected subclass ' + 
                            'instance of ConfirmationDialog. ' + 
                            'subclass of ConfirmationDialog ' + 
                            ' ---> ' + str(is_confirm_dialog))
        
        dialog_window = confirm_dialog(self.parent, confirm_function,
                                            order_list)
        dialog_window.run_dialog()
        del dialog_window
    
    def confirm_order(self, order_list, confirm_function):
        """Calls the confirm order dialog on the given
        order list. If confirmed this dialog calls the given
        confirm function. Confirm order displays information
        that should be accessible to the kitchen.
        
        @param order_list: list of MenuItem objects that
        represents the current order to be confirmed
        
        @param confirm_func: function pointer that points
        to the function to be executed if the order is confirmed.
        """
        self.confirm(order_list, Dialog.OrderConfirmationDialog,
                     confirm_function)
    
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
        """
        self.confirm(order_list, Dialog.CheckoutConfirmationDialog,
                     confirm_function)
    
    def select_misc_order(self, name_list, confirm_function):
        """Calls the misc selection confirmation dialog on the
        given name list. Calls the confirmation function if the
        misc selection is confirmed.
        
        @param name_list: list of 3-tuples that represent the
        given misc orders.
        
        @param confirm_function: function pointer that is called
        when the a misc order has been confirmed or added
        """
        self.confirm(name_list,
                    Dialog.OrderSelectionConfirmationDialog, confirm_function)
    
    def add_new_reservation(self):
        """Calls a dialog window to add a new reservation to
        the reservations list. Calls the edit function.
        
        @return: returns a 3-tuple representing the added
        reservation. Format will be (str, str, float) 
        representing the name, number, and secs since the epoch
        respectively.
        """
        return self.edit(None, Dialog.AddReservationsDialog)
