"""UI module stores the UI object which instantiates
and controls the main underlying GUI with user
interactions being compatible. All functionality of
the main GUI is utilized as components in UI object.

@author: Carl McGraw
@contact: cjmcgraw.u.washington.edu
@version: 1.0
"""
from peonordersystem.path import MAIN_UI_PATH

import copy

from peonordersystem.interface.Builder import Builder
from peonordersystem.interface.Orders import Orders
from peonordersystem.interface.Reservations import Reservations
from peonordersystem.interface.Editor import Editor


class UI(object):
    """UI Object operates on higher level functions of the
    PeonOrderSystem GUI. Functionally it instantiates all
    user side interactions of the GUI and ties them together.
    
    @var builder: Builder object that holds all information
    about generated base GUI from xml file
    
    @var orders: Orders object that stores and operates the
    table orders, also displays them.
    
    @var reservations: Reservations object that stores and
    operates the current reservations. 
    """
    
    def __init__(self, title):
        """Initializes a new object. Generates the base GUI
        from XML file obtained from Path. Instantiates the
        component objects.
        
        @param title: str representing the current title to
        be displayed on the GUI
        """
        self.builder = Builder()
        
        self.builder.add_from_file(MAIN_UI_PATH, title)
        self.builder.connect_signals(self)
        self.orders = Orders(self.builder.order_window)
        self.reservations = Reservations(self.builder.reservation_window)
        self.editor = Editor(self.builder.window)
        
    def table_button_clicked(self, table_button, table):
        """Callback method called when a table button is clicked.
        This method sets the current order to be displayed as
        the same as the table button clicked.
        
        @param table_button: Gtk.Button widget representing
        the current table button clicked.
        
        @param table: str representing the stored text on the
        table button. Represented as 'Table N', where N is the
        table number.
        """
        num = int(table.split(' ')[1])
        
        self.builder.set_table(table)
        self.orders.set_current_table(num - 1)
        
    def menu_button_clicked(self, menu_button):
        """Callback method called when a MenuButton has been
        clicked. MenuButton stores an instance of the MenuItem
        that it corresponds to as MenuItem. This method obtains
        that MenuItem and adds it to the current Order object.
        
        @param menu_button: Gtk.Button object that stores a MenuItem
        as MenuItem.
        """
        menu_item = menu_button.MenuItem
        self.orders.add(copy.copy(menu_item))
        
    def remove_menu_item(self, *args):  # @IGNORE:W0613
        """Removes currently selected MenuItem
        from the order.
        
        @param *args: wildcard representing the 
        selected menu button "remove". This parameter
        is added as a catch all.
        """
        self.orders.remove()
        
    def remove_selected_reservation(self, *args):  # @IGNORE:W0613
        """Callback method called when remove reservation
        has been clicked. Removes the selected reservation
        from the reservations list.
        
        @param *args: wildcard that represents a catch
        for selected widget 
        """
        self.reservations.remove_selected_reservation()
        
    def add_new_reservation(self, *args):  # @IGNORE:W0613
        """Callback method when reservation has been added.
        Calls dialog window to get new reservation information
        and adds it to the reservations displayed.
        
        @param *args: wildcard representing the widget of
        the selected item 
        """
        name, number, arrival_time = self.editor.add_new_reservation()
        self.reservations.add_reservation(name, number, arrival_time)
    
    def edit_note(self, *args):  # @IGNORE:W0613
        """Callback method when edit note button has been
        clicked. This method instantiates a new dialog window
        which the user performs the desired actions on. Upon
        closing the window is the deleted.
        
        @param *args: wildcard representing the button clicked.
        """
        menu_item = self.orders.get_selected()
        self.editor.edit_note(menu_item)
        self.orders.update()
        
    def edit_stars(self, *args):  # @IGNORE:W0613
        """Callback method when edit stars button has been
        clicked. This method instantiates a new dialog window
        which the desired actions may be performed by the user.
        Upon closing the window is deleted.
        
        @param *args: wildcard representing the button clicked
        """
        menu_item = self.orders.get_selected()
        self.editor.edit_stars(menu_item)
        self.orders.update()
        
    def edit_options(self, *args):  # @IGNORE:W0613
        """Callback method when edit options button has been
        clicked. This methods instantiates a new dialog window
        in which the user may perform the desired actions. Upon
        closing the dialog window is deleted.
        
        @param *args: wildcard representing the button clicked
        """
        menu_item = self.orders.get_selected()
        self.editor.edit_options(menu_item)
        self.orders.update()
        
    def order_confirmed(self, *args):
        """Method called when the order has been
        confirmed as is to be sent to the kitchen.
        
        @param args: wildcard parameter as catch all  
        """
        pass
        
    def confirm_order(self, *args):  # @IGNORE:W0613
        """Callback method when confirm order button has been
        clicked. This method instantiates a new dialog window
        that the user interacts with to confirm the order and
        send it to the kitchen. Upon closing the window
        is deleted.
        
        @param *args: wildcard representing the button clicked.
        """
        current_order = self.orders.get_current_order()
        self.editor.confirm_order(current_order, self.order_confirmed)
        
    def set_accessible_buttons(self, *args):  # @IGNORE:W0613
        """Callback method that is preformed any time an item
        is selected from orders. This method checks to see
        which valid buttons should be accessible to the user,
        and sets those buttons as accessible.
        
        @param *args: wildcard representing the item selected.
        """
        pass
    
    def confirm_checkout(self, *args):  # @IGNORE:W0613
        """Callback method when check order button has been
        clicked. This method instantiates a new dialog window
        that prompts the user to confirm or cancel the checkout.
        
        @param *args: wildcard that represents the button pressed
        """
        current_order = self.orders.get_current_order()
        self.editor.checkout_order(current_order, self.checkout_confirm)
    
    def checkout_confirm(self, *args):
        """Callback method when the checkout window has been confirmed.
        
        @param *args: wildcard as a catch all
        """
        pass
    
    def confirm_togo(self, *args):
        """Callback method when the togo button has been pressed.
        This instantiates a Dialog for the user to interact with.
        
        @param *args: wild card that represents a catch all.
        """
        current_names = self.orders.get_togo_orders()
        self.editor.select_togo_order(current_names,
                                      self.togo_confirm_function)
        
    def togo_confirm_function(self, curr_order):
        """Callback method that is called when a given TOGO confirmation
        dialog has been confirmed. Sets the GUI for menu items to be
        added to the order created or selected.
        
        @param curr_order: 3-tuple, representing the name, number
        and time which is used for storing information about the
        togo order.
        """
        # order is 3-tuple (name, number, time)
        self.orders.select_togo_order(curr_order)
        self.builder.set_table(curr_order[0] + 
                               ' (' + curr_order[1] + ')')

