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
from peonordersystem.interface.UpcomingOrders import UpcomingOrders


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
    
    def __init__(self, title, load_data=None):
        """Initializes a new object. Generates the base GUI
        from XML file obtained from Path. Instantiates the
        component objects.
        
        @param title: str representing the current title to
        be displayed on the GUI
        """
        
        print load_data
        
        self.builder = Builder()
        
        self.builder.add_from_file(MAIN_UI_PATH, title)
        self.builder.connect_signals(self)
        
        # These objects control the main orders and their displays
        self.orders = Orders(self.builder.order_window,
                             load_data=load_data)
        
        # These objects control secondary displays
        self.reservations = Reservations(self.builder.reservation_window)
        self.upcoming_orders = UpcomingOrders(self.builder.upcoming_orders_window,
                                              load_data=load_data)
        
        # These objects control dialog windows.
        self.editor = Editor(self.builder.window)
        
    
    #===========================================================================
    # This block contains methods that add, remove, or otherwise alter
    # an entire order. Such as adding, removing menu items or selecting
    # an order
    #===========================================================================
    
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
        if menu_item != None:
            self.orders.add(copy.copy(menu_item))
        
    def remove_menu_item(self, *args):  # @IGNORE:W0613
        """Removes currently selected MenuItem
        from the order.
        
        @param *args: wildcard representing the 
        selected menu button "remove". This parameter
        is added as a catch all.
        """
        self.orders.remove()
        
    #===========================================================================
    # This block contains methods that pertain directly to the reservations
    # and upcoming orders tabbed pane of the XML generated by self.builder
    #===========================================================================
    
    def add_new_reservation(self, *args):  # @IGNORE:W0613
        """Callback method when reservation has been added.
        Calls dialog window to get new reservation information
        and adds it to the reservations displayed.
        
        @param *args: wildcard representing the widget of
        the selected item 
        """
        name, number, arrival_time = self.editor.add_new_reservation()
        if not None in (name, number, arrival_time):
            self.reservations.add_reservation(name, number, arrival_time)
    
    def remove_selected_reservation(self, *args):  # @IGNORE:W0613
        """Callback method called when remove reservation
        has been clicked. Removes the selected reservation
        from the reservations list.
        
        @param *args: wildcard that represents a catch
        for selected widget 
        """
        self.reservations.remove_selected_reservation()
    
    def remove_selected_upcoming_order(self, *args):
        """Callback method called when the remove order
        button for the upcoming orders tab is pressed.
        
        @param *args: wildcard that represents a catch
        for the selected widget
        """
        self.upcoming_orders.remove_selected_order()
    
    #===========================================================================
    # This block contains methods that are utilized to edit/adjust selected
    # MenuItem objects. This functions are all Callback methods invoked by
    # the user when their subsequent buttons are clicked. These buttons are
    # generated in the self.builder object
    #===========================================================================
    
    def edit_note(self, *args):  # @IGNORE:W0613
        """Callback method when edit note button has been
        clicked. This method instantiates a new dialog window
        which the user performs the desired actions on. Upon
        closing the window is the deleted.
        
        @param *args: wildcard representing the button clicked.
        """
        menu_item = self.orders.get_selected()
        if menu_item_check(menu_item):
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
        if menu_item_check(menu_item):
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
        if menu_item_check(menu_item):
            self.editor.edit_options(menu_item)
            self.orders.update()
    
    #===========================================================================
    # This block contains methods pertaining to dialog windows that
    # are initiated by the user. These are all called via callback from
    # buttons generated in builder
    #===========================================================================
    
    def confirm_order(self, *args):  # @IGNORE:W0613
        """Callback method when confirm order button has been
        clicked. This method instantiates a new dialog window
        that the user interacts with to confirm the order and
        send it to the kitchen. Upon closing the window
        is deleted.
        
        @param *args: wildcard representing the button clicked.
        """
        current_order = self.orders.get_current_order()
        if order_check(current_order):
            self.editor.confirm_order(current_order, self.order_confirmed)
    
    def confirm_checkout(self, *args):  # @IGNORE:W0613
        """Callback method when check order button has been
        clicked. This method instantiates a new dialog window
        that prompts the user to confirm or cancel the checkout.
        
        @param *args: wildcard that represents the button pressed
        """
        current_order = self.orders.get_current_order()
        if order_check(current_order):
            self.editor.checkout_order(current_order, self.checkout_confirm)
    
    def select_misc_order(self, *args):
        """Callback method when the misc order button has been pressed.
        This instantiates a Dialog for the user to interact with.
        
        @param *args: wild card that represents a catch all.
        """
        current_names = self.orders.get_togo_orders()
        self.editor.select_misc_order(current_names,
                                      self.togo_confirm_function)
    
    #===========================================================================
    # This block contains methods that are called via callback only when a
    # dialog window has been confirmed.
    #===========================================================================
    
    def order_confirmed(self, *args):
        """Method called when the order has been
        confirmed as is to be sent to the kitchen.
        
        @param args: wildcard parameter as catch all  
        """
        self.orders.confirm_order()
        curr_name, curr_order = self.get_order_info()
        self.upcoming_orders.add_order(curr_name, curr_order)
        return curr_name, curr_order
    
    def checkout_confirm(self, *args):
        """Callback method when the checkout window has been confirmed.
        
        @param *args: wildcard as a catch all
        """
        curr_name, curr_order = self.get_order_info()
        self.upcoming_orders.remove_by_name(curr_name)
        self.orders.clear_order()
        return curr_name, curr_order
    
    def togo_confirm_function(self, curr_order):
        """Callback method that is called when a given TOGO confirmation
        dialog has been confirmed. Sets the GUI for menu items to be
        added to the order created or selected.
        
        @param curr_order: 3-tuple, representing the name, number
        and time which is used for storing information about the
        togo order.
        """
        # order is 3-tuple (name, number, time)
        if curr_order is not None:
            self.orders.select_togo_order(curr_order)
            self.builder.set_table(curr_order[0] + 
                                   ' (' + curr_order[1] + ')')
    
    #===========================================================================
    # This block contains methods that are used for obtaining information
    # about the current order, menu item, or other things the components
    # of this class are operating on, and would be necessary to know external
    # to the this class
    #===========================================================================
    
    def get_order_info(self):
        """Gets the current information associated
        with the current order.
        
        @return: 2-tuple representing the information
        of the table. The first entry represents the
        table number or order information, and the
        second entry represents the MenuItem list associated
        with that entry.
        """
        current_order = self.orders.get_current_order()
        current_table_info = self.orders.get_order_info()
        return current_table_info, current_order


#===========================================================================
# This block contains functions that are called as conditionals to
# ensure that specific conditions are met with given items. These functions
# are module wide.
#===========================================================================

def menu_item_check(menu_item):
    """Checks whether the given MenuItem is a valid 
    MenuItem to have operations performed on it.
    
    @return: bool representing True if the MenuItem
    is not None and the MenuItem is editable. False
    otherwise.
    """
    return menu_item != None and menu_item.is_editable()

def order_check(current_order):
    """Checks if the current order is a accessible, valid
    order.
    
    @return: bool representing True if the given order is
    not None and is of length > 0. False otherwise.
    """
    return current_order != None and len(current_order) > 0
    

